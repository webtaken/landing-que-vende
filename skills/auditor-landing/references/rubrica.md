# Rúbrica de conversión — 10 criterios × 0–10

Principio que la ordena todo (Demand Curve / Julian Shapiro):

> **Tasa de compra = (Deseo + Confianza) / (Esfuerzo + Confusión)**

Cada elemento de la página sube el numerador o baja el denominador. Si no hace ninguna de las dos, sobra. Prueba final (Harry Dry): *¿esto te ayudaría a vender si estuvieras frente al cliente en persona? Si no, quítalo.*

## Escala (igual para los 10)

| Nota | Significa |
|---|---|
| 0–3 | Ausente o dañino |
| 4–6 | Está, pero genérico o mal resuelto |
| 7–8 | Correcto |
| 9–10 | Específico, con prueba y difícil de copiar por la competencia |

Escribir una línea de justificación por criterio, citando lo que se ve (elemento + texto real).

---

## 1. Claridad en 5 segundos
Mirando solo el primer pantallazo del **celular**: ¿se entiende qué venden, para quién, qué gano y qué hago?
- NN/g: la mayor probabilidad de abandono está en los primeros 10 s; la propuesta de valor tiene que comunicarse antes.
- 57 % del tiempo de visualización ocurre en el primer pantallazo y 74 % en los dos primeros (NN/g, 2018).
- El visual del hero muestra el servicio o el resultado real, no una ilustración abstracta.
- **Mirar en `datos.json`:** `h1` existe y `sobre_pliegue: true` en `movil`; al menos un CTA con `sobre_pliegue: true` en `movil`.

## 2. Titular y propuesta de valor
- Dice qué consigue el cliente, no cómo se describe el negocio.
- Pasa los 3 filtros de Harry Dry: **¿se puede visualizar? ¿se puede comprobar si es falso? ¿solo este negocio puede decirlo?** Tres "no" = relleno.
- Un solo cliente y una sola objeción por titular (Shapiro).
- **Message match:** repite la promesa del anuncio, post o reel que trajo al visitante (Unbounce).
- Subtítulo: una o dos frases que dicen cómo se cumple la promesa. Párrafos largos aquí matan el impulso.

## 3. Llamado a la acción (CTA)
- Texto = verbo + lo que recibe ("Agendar mi valoración gratis"), no "Enviar", "Saber más", "Empezar".
- Es el elemento con más peso visual del primer pantallazo y lleva a un destino real (WhatsApp, agenda, checkout, formulario), no a `#`.
- Debajo, un microcopy que quita la objeción principal ("Te respondemos hoy por WhatsApp", "Sin compromiso").
- Se repite con el mismo estilo y destino al final de la página.
- **Mirar:** `ctas[].tipo` (`ancla`/`boton` sin destino = sospechoso), `ctas[].texto`.

## 4. Foco: un objetivo, sin fugas
- **Attention ratio** (Unbounce/Oli Gardner) = cosas que *se pueden* hacer ÷ cosas que *se deberían* hacer. Ideal 1:1. Varios botones valen si van al mismo destino.
- Sin menú completo, redes sociales ni blog en una landing de campaña. Caso Yuppiechef (VWO, 2011): quitar la navegación pasó de 3 % a 6 % de conversión (no publicaron significancia).
- Sin carruseles automáticos: la oferta queda visible una fracción del tiempo y la gente asume que lo que se mueve es publicidad (NN/g).
- **Mirar:** `enlaces_menu`, `destinos_unicos`, CTAs con `tipo` distinto entre sí.

## 5. Prueba y confianza
- Testimonios con **nombre real, foto, contexto (rol, ciudad o negocio) y resultado concreto** (cifra o plazo). Los usuarios miran el cargo y la afiliación del autor (NN/g).
- Prueba cerca de las decisiones: una cifra verificable junto al titular, testimonios cerca del precio o del CTA.
- Reseñas externas (Google, Trustpilot) pesan más que citas sueltas en el propio sitio, que generan escepticismo (NN/g).
- Con 5 reseñas la probabilidad de compra es 270 % mayor que con 0; la compra alcanza su máximo con notas de 4,0–4,7, porque un 5,0 parece demasiado bueno (Spiegel Research Center).
- Hay una persona detrás: nombre, cara, ubicación física, contacto (NN/g).
- **Bloqueante:** testimonio, reseña, logo o métrica inventados. Además de mentir, la FTC (EE. UU., 2024) y la Directiva UE 2019/2161 prohíben las reseñas falsas, incluidas las generadas con IA.

## 6. Copy: beneficio, especificidad y voz del cliente
- Cada característica se traduce a "lo que significa para ti" y trae prueba.
- Números, nombres, plazos y lugares en vez de adjetivos ("1.247 clientes" > "miles de clientes").
- Lectura fácil: el copy a nivel escolar de 5.º–7.º grado tuvo una conversión mediana del 11,1 %, frente al 5,3 % del lenguaje profesional (Unbounce 2024, medido en inglés). En español: frases cortas, palabras de todos los días.
- Lenguaje objetivo y conciso: quitar el tono promocional mejoró la usabilidad un 27 %, y combinado con concisión y facilidad de escaneo, un 124 % (NN/g, 1997).
- Las frases salen de cómo habla el cliente (reseñas, WhatsApp, comentarios), no del folleto de la empresa (Copyhackers).
- Sin vocabulario ni estructuras de IA (ver `etiquetas.md` → VOCABULARIO DE IA).
- **Mirar:** `frases_genericas` en `datos.json`.

## 7. Objeciones, precio y riesgo
- Precio o "desde" visible antes de pedir datos. Esconderlo hace pensar que "esconden algo" (NN/g).
- FAQ con preguntas que de verdad hicieron los clientes, no "¿Por qué elegirnos?".
- Garantía o reversión de riesgo junto al CTA, con plazo y condiciones claras. **Ojo:** probarla, no darla por buena. A KitchenAid destacar su garantía le bajó los pedidos (Conversion.com).
- Las objeciones típicas son precio, tiempo, "¿sirve para mí?", confianza y esfuerzo. Cada una se responde en algún lugar de la página.

## 8. Estructura según el nivel de conciencia
- El largo depende de cuánto hay que argumentar (Copyhackers, sobre los niveles de Eugene Schwartz):
  - Cliente que ya conoce y busca el servicio → página corta: oferta, CTA y prueba.
  - Cliente que compara → diferenciación, comparación y prueba.
  - Cliente que tiene el problema pero no conoce la solución → abrir con el dolor y explicar el mecanismo; página larga.
- Orden lógico: promesa → prueba → cómo funciona → beneficios → prueba → oferta/riesgo → FAQ → CTA final.
- Queda claro contra qué alternativa compite, incluidas "hacerlo yo mismo" y "no hacer nada" (April Dunford).

## 9. Móvil y fricción
- En un análisis de Unbounce, el 83 % de las visitas fueron móviles. Auditar primero a 390 px.
- Nada se desborda de lado; el titular no queda partido en una palabra por línea; el CTA mide 44 px o más de alto (el mínimo absoluto de WCAG 2.2 es 24 × 24 px).
- Formularios: pedir solo lo que se usa en el siguiente paso. Caso Imaginary Landscape: de 11 a 4 campos, +160 % de envíos (antes/después, no fue un A/B). HubSpot: los textarea y los desplegables son los campos que más bajan la conversión. Matiz: más campos pueden convenir si hace falta calificar al lead.
- Contraste de texto ≥ 4,5:1 (≥ 3:1 en texto grande). El bajo contraste es el error más común: aparece en el 79,1 % de las home pages (WebAIM 2025).
- **Mirar:** `formularios[].campos`, captura `movil-pliegue.png`.

## 10. Velocidad
- Objetivo, medido en el percentil 75 de las visitas: **LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1** (web.dev).
- Vodafone: un LCP 31 % más rápido trajo 8 % más ventas en un A/B test (web.dev).
- Deloitte/Google: 0,1 s más rápido subió la conversión un 8,4 % en retail y un 10,1 % en viajes (37 marcas).
- **Mirar:** `movil.rendimiento.lcp_ms`, `carga_ms`, `peso_kb`. Es una sola carga desde la máquina local, no datos de campo: tomarla como señal y recomendar PageSpeed Insights para confirmar.
- Guía de nota: LCP ≤ 2,5 s → 8–10 · 2,5–4 s → 4–7 · > 4 s → 0–3 (bloqueante).

---

## Bloqueantes (el total no puede pasar de 49)

- Testimonio, reseña, logo o métrica inventados.
- Ningún CTA visible sin hacer scroll en móvil.
- El titular no dice qué se vende.
- LCP > 4 s en móvil.

## Veredicto

| Total | Veredicto |
|---|---|
| 80–100 | **Lista para publicar o pautar.** Afinar con pruebas A/B. |
| 60–79 | **Corregir antes de pautar.** Hay fugas que cuestan dinero. |
| 0–59 | **Rehacer el primer pantallazo** (y lo que marquen los críticos). |

Estos umbrales son un criterio de diseño de esta skill, no un hallazgo de un estudio. Decirlo si preguntan.

## Severidad de cada defecto

- **Crítico:** la página no puede hacer su trabajo (no se entiende qué vende, no hay forma visible de actuar, se rompe en el celular, tarda tanto que la gente se va, hay prueba inventada).
- **Mayor:** se ve mal hecho y quita confianza (CTAs que compiten, sin prueba cerca de la decisión, titular genérico, precio escondido, formulario largo).
- **Menor:** pulido (microcopy, orden de secciones, detalles visuales).

Si salen más de 2 críticos, revisar y bajar alguno.
