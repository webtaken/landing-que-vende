---
name: auditor-landing
description: Audita si una landing page VENDE (no solo si se ve bonita) — desde una URL, un .html local o capturas — con una rúbrica de conversión de 10 criterios, etiqueta cada defecto sobre la captura con rótulos cortos ("TITULAR VAGO", "CTA SIN DESTINO", "SIN PRUEBA SOCIAL") y entrega informe con arreglos concretos, imagen "antes" anotada y, si se pide, "después" y comparación lista para reel o carrusel. Usar cuando digan "audita mi landing", "por qué mi landing no vende / no convierte", "revisa mi página de ventas", "qué le falta a mi landing", "mi landing sale mal", "califica esta landing", "tu landing sale mal por esto", "hazme el antes y después de esta landing" o pasen una URL de landing pidiendo opinión. NO usar para pulir solo diseño visual (tipografía, espaciado, color → landing-page-audit de Landingfolio o ux-elevacion), ni para construir una landing desde cero (→ landing-pyme), ni para SEO o accesibilidad completa.
---

# Auditor de landing — ¿esta página vende?

Revisa una landing como lo haría alguien que vive de que convierta: primero la mira como visitante (5 segundos, celular), después la recorre con una rúbrica de conversión, y entrega pocos defectos, bien señalados y con su arreglo escrito.

`<skill-dir>` = la carpeta donde está este SKILL.md.

## Reglas que no se rompen

1. **Mirar la página real antes de opinar.** Captura en escritorio y en móvil. Nunca auditar "de memoria" ni desde la idea de una landing típica.
2. **Cada defecto nombra el elemento** (sección › elemento, con su recuadro) **y trae el arreglo escrito.** ❌ "Mejora el titular." ✅ "Hero › H1: 'Lleva tu salud al siguiente nivel' → 'Ortodoncia invisible en Monterrey: sonrisa alineada en 12 meses, 0 brackets'."
3. **Cada defecto cita su criterio** de `references/rubrica.md` y, si usa un dato, la fuente de `references/fuentes.md`. Si no hay criterio que lo respalde, se borra. **Nunca inventar estadísticas.**
4. **Severidad calibrada.** Una landing real tiene 3–8 problemas que importan, no 25. Si hay más de 2 críticos, revisar y bajar.
5. **Conversión primero, estética después.** Si el problema es puro diseño (radios, sombras, escala tipográfica), mencionarlo en una línea y derivar a `landing-page-audit` (Landingfolio) si está instalada.
6. **Auditar, no rehacer.** No editar el código de la página salvo que lo pidan después del informe.

## Flujo

```
- [ ] Paso 1: Identificar entrada, negocio y objetivo de conversión
- [ ] Paso 2: Capturar (escritorio + móvil) y leer los datos
- [ ] Paso 3: Prueba de 5 segundos sobre el primer pantallazo
- [ ] Paso 4: Recorrer la rúbrica y puntuar
- [ ] Paso 5: Etiquetar defectos y dibujar el "antes"
- [ ] Paso 6: (opcional) Construir el "después" y la comparación
- [ ] Paso 7: Escribir el informe
```

### Paso 1 — Entrada, negocio y objetivo

| Entrada | Qué hacer |
|---|---|
| URL (pública o `localhost`) | Paso 2 con `capturar.py` |
| Archivo `.html` local | Paso 2 con `capturar.py <ruta.html>` |
| Capturas `.png/.jpg` | Abrirlas. Si solo hay escritorio, pedir una de celular o avisar que el móvil no se auditó. Sin `datos.json` no hay medición de velocidad: decirlo |
| Solo el texto de la landing | Auditar copy y estructura; avisar que no se evaluó diseño ni velocidad |
| Nada | Preguntar una vez: "¿Qué URL, archivo o captura audito?" |

Anotar en una línea: **tipo de negocio** (consultorio, agencia, curso, SaaS, tienda…), **acción que debe lograr la página** (WhatsApp, agendar cita, comprar, dejar datos) y **para quién**. Si no es obvio, inferirlo de la página y escribir la suposición en el informe en vez de preguntar.

### Paso 2 — Capturar y leer datos

```bash
python <skill-dir>/scripts/capturar.py "<url-o-ruta>" --out auditoria-<slug>
```

Genera `desktop-pliegue.png`, `desktop-completa.png`, `movil-pliegue.png`, `movil-completa.png` y `datos.json` (H1, CTAs con coordenadas y destino, formularios y nº de campos, enlaces del menú, frases genéricas detectadas, gradientes, fuentes, LCP/carga/peso en móvil). Abrir las 4 imágenes y leer `datos.json`.

Antes de auditar, describir en 2–3 líneas lo que se ve (secciones en orden, estilo) para que la persona confirme que es la página correcta.

Si falla (Playwright no instalado): `pip install playwright pillow && python -m playwright install chromium`. Si la página bloquea bots o carga vacía, pedir capturas a la persona.

### Paso 3 — Prueba de 5 segundos (solo el primer pantallazo del móvil)

Mirando **solo** `movil-pliegue.png`, responder en una línea cada una:
1. ¿Qué venden?
2. ¿Para quién es?
3. ¿Qué gano yo (resultado concreto)?
4. ¿Qué hago ahora (botón visible y claro)?
5. ¿Por qué creerles (alguna prueba visible)?

Cada respuesta que no se pueda contestar es un defecto **Crítico** o **Mayor** del hero. Esta prueba manda: la mayoría decide quedarse o irse en ese primer pantallazo.

### Paso 4 — Rúbrica

Recorrer los 10 criterios de [references/rubrica.md](references/rubrica.md), puntuar cada uno 0–10 con su justificación de una línea y sumar el puntaje sobre 100. Usar los umbrales de ese archivo para el veredicto.

### Paso 5 — Etiquetar defectos y dibujar el "antes"

1. Para cada defecto, elegir su rótulo del catálogo [references/etiquetas.md](references/etiquetas.md) (o crear uno de 2–4 palabras con el mismo estilo si ninguno encaja).
2. Armar `auditoria-<slug>/defectos.json` con los del pliegue (máximo 6 en escritorio y 4–5 en móvil, para que se lea):
   ```json
   [{"etiqueta": "TITULAR VAGO", "bbox": [40, 179, 1360, 65]},
    {"etiqueta": "CTA SIN DESTINO", "bbox": [644, 320, 151, 47]}]
   ```
   Las coordenadas salen de `datos.json` (`h1[].bbox`, `ctas[].bbox`, `formularios[].bbox`). Para elementos que el script no mide o para capturas del usuario, estimar en porcentaje: `{"etiqueta": "...", "bbox": [x%, y%, ancho%, alto%], "unidad": "pct"}`.
3. Dibujar:
   ```bash
   python <skill-dir>/scripts/anotar.py auditoria-<slug>/desktop-completa.png auditoria-<slug>/defectos.json \
     --out auditoria-<slug>/antes-desktop.png --recorte 0,0,1440,900
   python <skill-dir>/scripts/anotar.py auditoria-<slug>/movil-completa.png auditoria-<slug>/defectos-movil.json \
     --out auditoria-<slug>/antes-movil.png --recorte 0,0,390,844 --escala 2
   ```
   Las capturas `movil-*` salen a doble resolución (780 px de ancho, nítidas para reels): con ellas siempre `--escala 2`, y `bbox` y `--recorte` siguen en px CSS, tal como vienen en `datos.json`.
4. **Abrir la imagen resultante y verificar** que cada recuadro cae sobre el elemento correcto y que ninguna etiqueta tapa lo que señala. El script coloca cada etiqueta donde menos contenido tapa; si aun así tapa texto, usar `--tam 0.8`, quitar una etiqueta o ajustar coordenadas, y repetir.

### Paso 6 — "Después" y comparación (solo si lo piden o si es para contenido)

1. Reescribir **solo el primer pantallazo** aplicando los arreglos, partiendo de [assets/hero-despues.html](assets/hero-despues.html): reemplazar cada marcador `{{…}}` con el copy corregido y los colores de marca de la página original (no inventar marca nueva). Borrar los bloques de reseñas o testimonio si no hay datos reales. Comprobar que no queden marcadores: `grep -o "{{[A-Z_]*}}" hero-despues.html` debe salir vacío.
2. Capturarlo y rotular las mejoras en verde (3–4 etiquetas):
   ```bash
   python <skill-dir>/scripts/capturar.py auditoria-<slug>/hero-despues.html --out auditoria-<slug>/despues
   python <skill-dir>/scripts/anotar.py auditoria-<slug>/despues/movil-completa.png auditoria-<slug>/mejoras.json \
     --modo despues --out auditoria-<slug>/despues-movil.png --recorte 0,0,390,844 --escala 2
   ```
3. Componer para redes:
   ```bash
   python <skill-dir>/scripts/componer.py auditoria-<slug>/antes-movil.png auditoria-<slug>/despues-movil.png \
     --out auditoria-<slug>/comparacion-reel.png --formato reel        # 1080x1920
   ```
   (`--formato carrusel` → 1080x1350, `--formato horizontal` → lado a lado.)

### Paso 7 — Informe

Escribir `auditoria-<slug>/informe.md` con la plantilla [assets/plantilla-informe.md](assets/plantilla-informe.md). En la respuesta: puntaje, veredicto, los críticos y las rutas de los archivos. Cerrar con una sola pregunta de siguiente paso ("¿Aplico los arreglos 1–3?" o "¿Te armo el guion del reel con estos defectos?").

## Modo contenido ("Tu landing sale mal por esto")

Si la auditoría es para un reel o carrusel, además del informe entregar `auditoria-<slug>/guion.md`: gancho con el defecto más visible, un beat por defecto (rótulo + frase de ≤12 palabras + imagen que lo prueba) y cierre con el "después". Reglas:
- **Landings de terceros:** usar páginas propias, de demo o con permiso. Si es de un tercero sin permiso, difuminar logo, nombre y datos de contacto antes de publicar, y criticar la página, nunca a la persona.
- Cada frase del guion debe tener su imagen de prueba; si no la tiene, se quita la frase.

## Errores comunes

- **El informe suena genérico, aplicaría a cualquier landing:** te saltaste el Paso 2 o rellenaste. Volver a abrir las capturas; cada defecto necesita su elemento con recuadro.
- **Todo es crítico:** inflación. Crítico = la página no puede cumplir su trabajo (no se entiende qué vende, no hay forma visible de actuar, se rompe en el celular, tarda tanto que se van).
- **Defecto de gusto disfrazado** ("prefiero fondo oscuro"): si no hay criterio en la rúbrica que lo respalde, borrarlo.
- **Cifras sin fuente:** solo se usan las de `references/fuentes.md`. Si no está ahí, no se dice.
- **`datos.json` sin CTAs** en páginas hechas con constructores (Wix, Framer, GHL): los botones pueden ser `div`. Ubicarlos visualmente y estimar el recuadro en `pct`.
- **LCP = null:** página local o sin imágenes grandes; usar `carga_ms` y el peso como referencia y decirlo.
