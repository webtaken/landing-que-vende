#!/usr/bin/env python3
"""Captura una landing (URL o archivo .html) y extrae los datos que necesita la auditoría.

Uso:
    python capturar.py <url-o-ruta.html> --out <carpeta>

Requisitos:
    pip install playwright && python -m playwright install chromium

Salida en <carpeta>:
    desktop-pliegue.png   primera pantalla en escritorio (1440x900)
    desktop-completa.png  página completa en escritorio (recortada a --max-alto)
    movil-pliegue.png     primera pantalla en móvil (390x844)
    movil-completa.png    página completa en móvil (recortada a --max-alto)
    datos.json            hechos medibles: titulares, CTAs con coordenadas, formularios,
                          tiempos de carga, frases genéricas detectadas, etc.

Las coordenadas (bbox = [x, y, ancho, alto]) son en píxeles CSS de la página completa
de cada vista. La captura móvil sale a escala 2 (780 px de ancho, nítida para reels):
pasa --escala 2 a anotar.py en las imágenes movil-*.png (datos.json → escala_captura).
"""
import argparse
import json
import pathlib
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Falta Playwright: pip install playwright && python -m playwright install chromium")

VISTAS = {
    "desktop": {"viewport": {"width": 1440, "height": 900}, "is_mobile": False},
    "movil": {
        "viewport": {"width": 390, "height": 844},
        "is_mobile": True,
        "has_touch": True,
        "device_scale_factor": 2,  # nítido para reels; las coordenadas siguen en px CSS
        "user_agent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        ),
    },
}

# Frases que delatan copy genérico (muchas salen tal cual de generadores de IA).
FRASES_GENERICAS = [
    "lleva tu negocio al siguiente nivel", "siguiente nivel", "soluciones innovadoras",
    "solución integral", "soluciones integrales", "potencia tu", "impulsa tu", "transforma tu",
    "revoluciona", "en un mundo", "descubre el poder", "desbloquea", "bienvenido a",
    "bienvenidos a", "somos una empresa", "líderes en", "calidad y compromiso",
    "tu aliado", "a otro nivel", "experiencia única", "de vanguardia", "innovación",
    "lorem ipsum", "get started", "learn more", "welcome to", "the best solution",
    "unlock", "supercharge", "elevate your", "next level", "seamless", "cutting-edge",
    "empieza ahora", "saber más", "más información", "leer más",
]

JS_EXTRAER = r"""
(frases) => {
  const vh = window.innerHeight;
  const sx = window.scrollX, sy = window.scrollY;
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return r.width > 2 && r.height > 2 && cs.visibility !== 'hidden' && cs.display !== 'none' && parseFloat(cs.opacity) > 0.05;
  };
  const bbox = (el) => { const r = el.getBoundingClientRect(); return [Math.round(r.left + sx), Math.round(r.top + sy), Math.round(r.width), Math.round(r.height)]; };
  const txt = (el) => (el.innerText || el.value || el.getAttribute('aria-label') || '').replace(/\s+/g, ' ').trim();
  const sobrePliegue = (el) => el.getBoundingClientRect().top + sy < vh;

  const titulares = (sel) => [...document.querySelectorAll(sel)].filter(visible).map((el) => ({
    texto: txt(el).slice(0, 200), bbox: bbox(el), sobre_pliegue: sobrePliegue(el),
    fuente: getComputedStyle(el).fontFamily, tamano_px: parseFloat(getComputedStyle(el).fontSize),
  }));

  const tipoDestino = (href) => {
    if (!href) return 'boton';
    const h = href.toLowerCase();
    if (h.includes('wa.me') || h.includes('whatsapp')) return 'whatsapp';
    if (h.startsWith('tel:')) return 'telefono';
    if (h.startsWith('mailto:')) return 'email';
    if (/calendly|cal\.com|booking|reserva|agenda|acuityscheduling|tidycal|zcal/.test(h)) return 'agenda';
    if (/stripe|hotmart|checkout|paypal|mercadopago|gumroad|lemonsqueezy/.test(h)) return 'pago';
    if (h.startsWith('#')) return 'ancla';
    try { return new URL(h, location.href).host === location.host ? 'interno' : 'externo'; } catch (e) { return 'otro'; }
  };

  const enlaces = [...document.querySelectorAll('a[href]')].filter(visible);
  const botones = [...document.querySelectorAll('button, input[type=submit], [role=button]')].filter(visible);
  const pareceCTA = (el) => {
    const cs = getComputedStyle(el);
    const bg = cs.backgroundColor;
    const tieneFondo = bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent';
    return el.tagName !== 'A' || tieneFondo || /btn|button|cta/i.test(el.className || '');
  };
  let n = 0;
  const ctas = [...enlaces.filter(pareceCTA), ...botones].map((el) => ({
    id: 'cta-' + (++n), texto: txt(el).slice(0, 80), destino: el.getAttribute('href') || null,
    tipo: tipoDestino(el.getAttribute('href')), bbox: bbox(el), sobre_pliegue: sobrePliegue(el),
    color_fondo: getComputedStyle(el).backgroundColor, color_texto: getComputedStyle(el).color,
  })).filter((c) => c.texto);

  const nav = document.querySelector('header nav, nav');
  const formularios = [...document.querySelectorAll('form')].filter(visible).map((f, i) => {
    const campos = [...f.querySelectorAll('input, select, textarea')].filter((c) => !['hidden', 'submit', 'button'].includes(c.type) && visible(c));
    return { id: 'form-' + (i + 1), campos: campos.length, obligatorios: campos.filter((c) => c.required).length,
      etiquetas: campos.map((c) => c.name || c.placeholder || c.id || c.type).slice(0, 15), bbox: bbox(f), sobre_pliegue: sobrePliegue(f) };
  });

  const imgs = [...document.querySelectorAll('img')].filter(visible);
  const textoPagina = (document.body.innerText || '').replace(/\s+/g, ' ');
  const textoMin = textoPagina.toLowerCase();
  const frasesEncontradas = frases.filter((f) => textoMin.includes(f));

  const pruebaSocial = {
    palabras_clave: ['testimonio', 'opiniones', 'reseñas', 'clientes', 'casos de éxito', 'review', 'testimonial', '★', '⭐']
      .filter((k) => textoMin.includes(k)),
    blockquotes: document.querySelectorAll('blockquote').length,
    estrellas: (textoPagina.match(/[★⭐]/g) || []).length,
  };

  const gradientes = [...document.querySelectorAll('body *')].slice(0, 3000)
    .filter((el) => /gradient/.test(getComputedStyle(el).backgroundImage)).length;

  const fuentes = new Set();
  [...document.querySelectorAll('h1,h2,h3,p,a,button,li')].slice(0, 400).forEach((el) => fuentes.add(getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim()));

  const nav_t = performance.getEntriesByType('navigation')[0];
  const recursos = performance.getEntriesByType('resource');

  return {
    url: location.href, titulo: document.title, idioma: document.documentElement.lang || null,
    meta_descripcion: document.querySelector('meta[name=description]')?.content || null,
    meta_viewport: document.querySelector('meta[name=viewport]')?.content || null,
    alto_pagina: document.documentElement.scrollHeight, alto_pliegue: vh,
    h1: titulares('h1'), h2: titulares('h2').slice(0, 25),
    ctas, enlaces_totales: enlaces.length,
    destinos_unicos: [...new Set(enlaces.map((a) => a.href.split('#')[0]))].length,
    enlaces_menu: nav ? nav.querySelectorAll('a').length : 0,
    formularios, imagenes: imgs.length, imagenes_sin_alt: imgs.filter((i) => !i.alt).length,
    palabras: textoPagina.split(' ').filter(Boolean).length,
    frases_genericas: frasesEncontradas, prueba_social: pruebaSocial,
    precios_detectados: (textoPagina.match(/(\$|€|USD|MXN|COP|S\/)\s?\d[\d.,]*/g) || []).slice(0, 10),
    elementos_con_gradiente: gradientes, fuentes: [...fuentes].slice(0, 8),
    rendimiento: {
      dom_listo_ms: nav_t ? Math.round(nav_t.domContentLoadedEventEnd) : null,
      carga_ms: nav_t ? Math.round(nav_t.loadEventEnd) : null,
      lcp_ms: window.__lcp != null ? Math.round(window.__lcp) : null,
      peticiones: recursos.length,
      peso_kb: Math.round(recursos.reduce((s, r) => s + (r.transferSize || 0), (nav_t?.transferSize || 0)) / 1024),
    },
  };
}
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("objetivo", help="URL (https://...) o ruta a un .html local")
    ap.add_argument("--out", required=True, help="carpeta de salida")
    ap.add_argument("--max-alto", type=int, default=12000, help="alto máximo de la captura completa (px)")
    ap.add_argument("--timeout", type=int, default=45000, help="timeout de carga (ms)")
    a = ap.parse_args()

    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    objetivo = a.objetivo
    if not objetivo.startswith(("http://", "https://", "file://")):
        p = pathlib.Path(objetivo).resolve()
        if not p.exists():
            sys.exit(f"No existe: {p}")
        objetivo = p.as_uri()

    resultado = {"objetivo": a.objetivo, "vistas": {}}
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for nombre, cfg in VISTAS.items():
            ctx = nav.new_context(**cfg, locale="es-ES")
            # Registrar LCP antes de que cargue la página.
            ctx.add_init_script(
                "window.__lcp = null; try { new PerformanceObserver((l) => { const e = l.getEntries(); "
                "if (e.length) window.__lcp = e[e.length - 1].startTime; })"
                ".observe({type: 'largest-contentful-paint', buffered: true}); } catch (e) {}"
            )
            pg = ctx.new_page()
            try:
                pg.goto(objetivo, wait_until="load", timeout=a.timeout)
            except Exception as e:  # noqa: BLE001 — seguimos con lo que haya cargado
                print(f"[{nombre}] aviso al cargar: {e}", file=sys.stderr)
            try:
                pg.wait_for_load_state("networkidle", timeout=8000)
            except Exception:  # noqa: BLE001
                pass
            # Recorrer la página para disparar lazy-load y animaciones de entrada.
            pg.evaluate(
                """async () => { const h = document.documentElement.scrollHeight;
                for (let y = 0; y < h; y += innerHeight * 0.8) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
                scrollTo(0, 0); await new Promise(r => setTimeout(r, 400)); }"""
            )
            datos = pg.evaluate(JS_EXTRAER, FRASES_GENERICAS)
            pg.screenshot(path=str(out / f"{nombre}-pliegue.png"))
            alto = min(datos["alto_pagina"], a.max_alto)
            pg.screenshot(
                path=str(out / f"{nombre}-completa.png"), full_page=True,
                clip={"x": 0, "y": 0, "width": cfg["viewport"]["width"], "height": alto},
            )
            datos["captura_recortada"] = datos["alto_pagina"] > a.max_alto
            datos["escala_captura"] = cfg.get("device_scale_factor", 1)
            resultado["vistas"][nombre] = datos
            ctx.close()
        nav.close()

    (out / "datos.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2))
    d, m = resultado["vistas"]["desktop"], resultado["vistas"]["movil"]
    print(f"✓ capturas y datos en {out}")
    print(f"  H1: {d['h1'][0]['texto'] if d['h1'] else '— (no hay H1)'}")
    print(f"  CTAs sobre el pliegue: escritorio {sum(c['sobre_pliegue'] for c in d['ctas'])} · móvil {sum(c['sobre_pliegue'] for c in m['ctas'])}")
    print(f"  Destinos únicos de enlace: {d['destinos_unicos']} · formularios: {len(d['formularios'])}")
    print(f"  Frases genéricas: {', '.join(d['frases_genericas']) or 'ninguna'}")
    r = m["rendimiento"]
    print(f"  Móvil: LCP {r['lcp_ms']} ms · carga {r['carga_ms']} ms · {r['peso_kb']} KB · {r['peticiones']} peticiones")


if __name__ == "__main__":
    main()
