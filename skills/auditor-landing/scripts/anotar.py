#!/usr/bin/env python3
"""Dibuja etiquetas de defecto (o de mejora) sobre una captura, estilo antes/después.

Uso:
    python anotar.py captura.png defectos.json --out antes-anotado.png [--modo antes|despues]
                     [--recorte x,y,ancho,alto] [--ancho 1080]

defectos.json es una lista:
    [
      {"etiqueta": "TITULAR VAGO", "bbox": [120, 210, 900, 140]},
      {"etiqueta": "CTA GENÉRICO", "bbox": [8, 40, 30, 6], "unidad": "pct"}
    ]
- bbox = [x, y, ancho, alto] en píxeles de la imagen (unidad "px", por defecto)
  o en porcentaje del ancho/alto de la imagen (unidad "pct", útil con capturas que manda el usuario).
- Las coordenadas de datos.json (capturar.py) están en px CSS: úsalas tal cual y pasa
  --escala 2 si anotas una captura movil-*.png.

--modo antes   → cajas y etiquetas magenta + insignia "ANTES" (defectos)
--modo despues → cajas y etiquetas verdes + insignia "DESPUÉS" (mejoras aplicadas)
--recorte      → recorta la imagen final a esa región (mismas unidades que bbox), p. ej. el pliegue
--escala       → 2 para las capturas movil-*.png de capturar.py (salen a doble resolución)
--tam          → tamaño de las etiquetas; 0.8 si tapan texto en layouts apretados
--ancho        → reescala el resultado a ese ancho (1080 para reels)

Requisito: pip install pillow
"""
import argparse
import json
import pathlib
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Falta Pillow: pip install pillow")

ESTILOS = {
    "antes": {"color": (194, 24, 110), "insignia": "ANTES", "insignia_fondo": (90, 90, 90)},
    "despues": {"color": (21, 128, 61), "insignia": "DESPUÉS", "insignia_fondo": (21, 128, 61)},
}
FUENTES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def fuente(tam):
    for f in FUENTES:
        if pathlib.Path(f).exists():
            return ImageFont.truetype(f, tam)
    return ImageFont.load_default()


def medir(draw, texto, f):
    x0, y0, x1, y1 = draw.textbbox((0, 0), texto, font=f)
    return x1 - x0, y1 - y0, y0


def choca(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("imagen")
    ap.add_argument("defectos", help="JSON con la lista de etiquetas")
    ap.add_argument("--out", required=True)
    ap.add_argument("--modo", choices=ESTILOS, default="antes")
    ap.add_argument("--recorte", help="x,y,ancho,alto en px de la imagen original")
    ap.add_argument("--ancho", type=int, help="ancho final (reescala)")
    ap.add_argument("--sin-insignia", action="store_true")
    ap.add_argument("--tam", type=float, default=1, help="tamaño de las etiquetas (0.8 = 20%% más chicas, útil en móvil)")
    ap.add_argument("--escala", type=float, default=1,
                    help="factor de la captura (2 para movil-*.png de capturar.py); multiplica bbox y --recorte en px")
    a = ap.parse_args()

    im = Image.open(a.imagen).convert("RGB")
    W, H = im.size
    items = json.loads(pathlib.Path(a.defectos).read_text())
    est = ESTILOS[a.modo]
    color = est["color"]

    # Escala de trazo y texto proporcional al ancho CSS de la captura (× escala de píxeles).
    e = a.escala
    base = max(W / e / 1440, 0.7) * e
    grosor = max(2, round(4 * base))
    f = fuente(max(12, round(22 * base * a.tam)))
    pad = max(4, round(9 * base * a.tam))

    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)

    # Zona útil: si hay recorte, las etiquetas y la insignia se colocan dentro de él.
    if a.recorte:
        rx, ry, rw, rh = [round(float(v) * e) for v in a.recorte.split(",")]
        LX0, LY0, LX1, LY1 = max(0, rx), max(0, ry), min(W, rx + rw), min(H, ry + rh)
    else:
        LX0, LY0, LX1, LY1 = 0, 0, W, H

    # 1) Elementos señalados y sus cajas (con margen); se calculan antes de colocar etiquetas.
    elementos, cajas = [], []
    for it in items:
        x, y, w, h = it["bbox"]
        if it.get("unidad") == "pct":
            x, y, w, h = x * W / 100, y * H / 100, w * W / 100, h * H / 100
        else:
            x, y, w, h = x * e, y * e, w * e, h * e
        elementos.append((x, y, x + w, y + h))
        x0, y0 = max(0, x - pad), max(0, y - pad)
        x1, y1 = min(W - 1, x + w + pad), min(H - 1, y + h + pad)
        cajas.append((x0, y0, x1, y1))
        d.rounded_rectangle([x0, y0, x1, y1], radius=round(10 * base), outline=color + (255,), width=grosor)

    def solape(r, s):
        return max(0, min(r[2], s[2]) - max(r[0], s[0])) * max(0, min(r[3], s[3]) - max(r[1], s[1]))

    gris = im.convert("L")

    def ocupacion(r):
        """Fracción de píxeles con contenido (texto, bordes, fotos) dentro de r, leída de la captura."""
        x0, y0, x1, y1 = [int(v) for v in r]
        if x1 - x0 < 2 or y1 - y0 < 2:
            return 0.0
        zona = gris.crop((x0, y0, x1, y1))
        if zona.width * zona.height > 40000:  # muestrear para ir rápido
            zona = zona.resize((max(2, zona.width // 3), max(2, zona.height // 3)))
        hist = zona.histogram()
        total = sum(hist)
        acum, mediana = 0, 0
        for v, n in enumerate(hist):
            acum += n
            if acum >= total / 2:
                mediana = v
                break
        distintos = sum(n for v, n in enumerate(hist) if abs(v - mediana) > 28)
        return distintos / total

    def costo(r, propia=None):
        # Tapar un elemento señalado pesa mucho; tapar otro contenido de la captura, bastante;
        # pisar solo el margen de otra caja, poco.
        area = (r[2] - r[0]) * (r[3] - r[1])
        c = ocupacion(r) * area * 8                      # lo que se ve debajo (texto, botones, fotos)
        c += sum(solape(r, el) * 2 for el in elementos)  # entrar en un elemento señalado, aunque esté vacío ahí
        c += sum(solape(r, cj) for j, cj in enumerate(cajas) if j != propia)
        return c

    ocupadas = []  # etiquetas ya colocadas (no se pueden pisar)

    # 2) Insignia ANTES/DESPUÉS en la esquina que menos tapa.
    if not a.sin_insignia:
        fi = fuente(max(14, round(20 * base)))
        tw, th, off = medir(d, est["insignia"], fi)
        bw, bh = tw + 2 * pad, th + 2 * pad
        m = round(16 * base)
        cx = (LX0 + LX1 - bw) // 2
        esquinas = [(LX0 + m, LY1 - bh - m), (LX1 - bw - m, LY1 - bh - m), (LX1 - bw - m, LY0 + m), (LX0 + m, LY0 + m),
                    (cx, LY1 - bh - m), (cx, LY0 + m)]
        ix, iy = min(esquinas, key=lambda q: costo((q[0], q[1], q[0] + bw, q[1] + bh)))
        caja_i = (ix, iy, ix + bw, iy + bh)
        ocupadas.append(caja_i)
        d.rounded_rectangle(caja_i, radius=round(6 * base), fill=est["insignia_fondo"] + (235,))
        d.text((ix + pad, iy + pad - off), est["insignia"], font=fi, fill=(255, 255, 255, 255))

    # 3) Etiquetas: se prueban posiciones alrededor de su caja y se elige la que menos tapa.
    for i, it in enumerate(items):
        x0, y0, x1, y1 = cajas[i]
        texto = it["etiqueta"].upper()
        tw, th, off = medir(d, texto, f)
        cw, ch = tw + 2 * pad, th + 2 * pad
        g = grosor + 2
        candidatas = [
            (x0, y0 - ch - g), (x0, y1 + g), (x1 - cw, y0 - ch - g), (x1 - cw, y1 + g),   # fuera, arriba/abajo
            (x0 + g, y0 - ch // 2), (x1 - cw - g, y0 - ch // 2),                        # montada en el borde superior
            (x0 + g, y1 - ch // 2), (x1 - cw - g, y1 - ch // 2),                        # montada en el borde inferior
            (x0 - cw - g, y0), (x1 + g, y0),                                            # a los lados
            (x1 - cw - g, y0 + g), (x1 - cw - g, y1 - ch - g), (x0 + g, y1 - ch - g),     # dentro, en esquinas
            (x0 + g, y0 + g),
        ]
        mejor, mejor_costo = None, None
        for cx, cy in candidatas:
            cx = min(max(LX0, cx), LX1 - cw)
            cy = min(max(LY0, cy), LY1 - ch)
            r = (cx, cy, cx + cw, cy + ch)
            if any(choca(r, o) for o in ocupadas):
                continue
            c = costo(r, propia=i)
            if mejor_costo is None or c < mejor_costo:
                mejor, mejor_costo = r, c
            if c < cw * ch * 0.02:
                break
        if mejor is None:  # todo ocupado: apilar hacia abajo desde arriba de la caja
            r = (min(max(LX0, x0), LX1 - cw), max(LY0, y0 - ch), 0, 0)
            r = (r[0], r[1], r[0] + cw, r[1] + ch)
            while any(choca(r, o) for o in ocupadas) and r[3] + ch < LY1:
                r = (r[0], r[1] + ch + 2, r[2], r[3] + ch + 2)
            mejor = r
        ocupadas.append(mejor)
        d.rounded_rectangle(mejor, radius=round(6 * base), fill=(255, 255, 255, 245),
                            outline=color + (255,), width=max(2, grosor - 1))
        d.text((mejor[0] + pad, mejor[1] + pad - off), texto, font=f, fill=color + (255,))

    im = Image.alpha_composite(im.convert("RGBA"), capa).convert("RGB")
    if a.recorte:
        im = im.crop((LX0, LY0, LX1, LY1))
    if a.ancho:
        im = im.resize((a.ancho, round(im.height * a.ancho / im.width)), Image.LANCZOS)
    im.save(a.out)
    print(f"✓ {a.out} ({im.width}x{im.height}, {len(items)} etiquetas)")


if __name__ == "__main__":
    main()
