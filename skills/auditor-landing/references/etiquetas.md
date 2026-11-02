# Catálogo de etiquetas de defectos

Rótulos cortos (2–4 palabras, MAYÚSCULAS) para dibujar sobre la captura con `anotar.py`. Cada uno trae el criterio de la rúbrica al que pertenece, cómo detectarlo y el arreglo. Si ningún rótulo encaja, crear uno nuevo con el mismo estilo: nombra **el problema**, no la solución.

Para el "después" (`--modo despues`), rotular la mejora: `TITULAR CON RESULTADO`, `CTA A WHATSAPP`, `RESEÑAS REALES`, `1 SOLO OBJETIVO`, `FOTO REAL`, etc.

## Primer pantallazo y titular (criterios 1–2)

| Etiqueta | Qué es | Cómo detectarlo | Arreglo |
|---|---|---|---|
| NO SE ENTIENDE QUÉ VENDE | Tras 5 s en el celular no se sabe qué ofrecen | Prueba de 5 segundos | Titular con servicio + resultado; subtítulo que diga cómo |
| TITULAR VAGO | "Transforma tu negocio", "Lleva tu X al siguiente nivel" | `frases_genericas`, falla los 3 filtros de Dry | Quién + resultado + plazo o diferencia |
| HABLA DE SÍ MISMO | "Somos líderes en…", "Bienvenidos a…" | H1 empieza con "Somos" o "Bienvenido" | Reescribir desde el resultado del cliente |
| COPY INTERCAMBIABLE | Cualquier competidor podría firmarlo ("calidad garantizada") | Filtro "¿solo ellos pueden decirlo?" | Datos propios: años, zona, nº de clientes, método |
| SIN H1 | No hay titular principal, o es una imagen con texto | `h1` vacío en `datos.json` | Titular en texto real, el más grande de la página |
| SUBTÍTULO LADRILLO | Párrafo de 4+ líneas bajo el titular | Captura móvil | 1–2 frases: cómo se cumple la promesa |
| SIN MESSAGE MATCH | La promesa no coincide con el anuncio o reel que trajo al visitante | Comparar con el anuncio | Repetir la promesa y el visual del anuncio |
| HERO SIN PRODUCTO | Blob, gradiente, 3D o ilustración en vez del servicio real | Captura | Foto del servicio, del resultado o del equipo trabajando |
| CARRUSEL AUTOMÁTICO | Slider que rota en el hero | Captura/código | Una sola imagen y un solo mensaje |

## CTA y foco (criterios 3–4)

| Etiqueta | Qué es | Cómo detectarlo | Arreglo |
|---|---|---|---|
| CTA GENÉRICO | "Saber más", "Enviar", "Empezar", "Contáctanos" | `ctas[].texto` | Verbo + lo que recibe: "Agendar mi valoración gratis" |
| CTA SIN DESTINO | El botón baja a un ancla o no lleva a ninguna acción | `ctas[].tipo` = `ancla`/`boton` sin destino | Enlazar a WhatsApp, agenda o checkout |
| CTA INVISIBLE | El botón se pierde (poco contraste, pequeño, debajo del pliegue) | `sobre_pliegue: false` en móvil, captura | Color de mayor contraste, ≥ 44 px de alto, ancho completo en móvil |
| CTAS QUE COMPITEN | Comprar + demo + Instagram + llamar, con el mismo peso | Varios `tipo` distintos sobre el pliegue | Una acción principal; el resto en texto pequeño o fuera |
| MENÚ CON N FUGAS | Menú completo que saca al visitante de la página | `enlaces_menu` ≥ 3 | Quitar el menú; dejar logo y, como mucho, el teléfono |
| REDES EN EL HERO | Íconos de Instagram/Facebook arriba | Captura | Llevarlos al pie o quitarlos |
| SIN MICROCOPY | Nada debajo del botón que quite el miedo | Captura | "Te respondemos hoy", "Sin compromiso", garantía |

## Prueba y confianza (criterio 5)

| Etiqueta | Qué es | Cómo detectarlo | Arreglo |
|---|---|---|---|
| SIN PRUEBA SOCIAL | Ningún testimonio, reseña ni cifra | `prueba_social` vacío | Reseñas de Google con nota y cantidad, testimonios con nombre |
| TESTIMONIO ANÓNIMO | "María G.", sin foto, sin contexto | Captura | Nombre completo, foto, ciudad o negocio, resultado concreto |
| TESTIMONIO GENÉRICO | "¡Excelente servicio, lo recomiendo!" | Captura | Pedir resultado concreto: qué cambió, en cuánto tiempo |
| TESTIMONIO FALSO | Nombres o avatares inventados (típico de IA: "Sarah Chen") | Fotos de stock, nombres que no cuadran con el mercado | **Borrar.** Usar reseñas reales o dejar la sección fuera (riesgo legal: FTC, Directiva UE 2019/2161) |
| MÉTRICAS INVENTADAS | "10.000+ clientes", "99 % de satisfacción" sin fuente | Cifras redondas sin origen | Cifra real y exacta con fuente, o quitarla |
| LOGOS FANTASMA | Nube de logos que no son clientes | Preguntar | Solo clientes o medios reales, con permiso |
| SIN PERSONA DETRÁS | Ni nombre, ni cara, ni dirección, ni contacto | Captura | Foto y nombre del dueño o el equipo, dirección, WhatsApp |
| PRUEBA LEJOS DEL CTA | Los testimonios están al final, lejos de la decisión | Orden de secciones | Una prueba junto al titular y otra junto al precio o CTA |

## Copy (criterio 6)

| Etiqueta | Qué es | Cómo detectarlo | Arreglo |
|---|---|---|---|
| VOCABULARIO DE IA | "potencia", "impulsa", "desbloquea", "soluciones integrales", "de vanguardia", "experiencia única" | `frases_genericas` | Reescribir con frases del cliente (reseñas, WhatsApp) |
| PALABRAS DE RELLENO | Adjetivos sin dato ("innovador", "de calidad", "integral") | Lectura | Cambiar cada adjetivo por un número, plazo o ejemplo |
| CARACTERÍSTICAS SIN BENEFICIO | Lista de servicios sin "y eso qué me da" | Lectura | Servicio → resultado para el cliente → prueba |
| TRES TARJETAS ÍCONO | Tres columnas con ícono de línea y texto genérico | Captura | Beneficio + prueba + foto real; o una lista simple |
| "NO ES X, ES Y" | Estructura de contraste repetida, típica de IA | Lectura | Decirlo directo, una sola vez |
| TEXTO DIFÍCIL | Frases largas, jerga técnica | Lectura | Frases de < 20 palabras, palabras de todos los días |

## Objeciones, precio y riesgo (criterio 7)

| Etiqueta | Qué es | Cómo detectarlo | Arreglo |
|---|---|---|---|
| PRECIO ESCONDIDO | "Contáctanos para cotizar" cuando todos preguntan el precio | `precios_detectados` vacío | "Desde $X" o rango, o por qué depende y en cuánto llega la cotización |
| SIN FAQ | No se responden las dudas típicas | Captura | 4–8 preguntas reales de WhatsApp/DMs |
| FAQ DE RELLENO | "¿Por qué elegirnos?", "¿Qué es X?" | Lectura | Objeciones reales: precio, tiempo, "¿sirve para mí?" |
| SIN GARANTÍA | No hay nada que baje el riesgo | Lectura | Garantía real o primera consulta sin costo (probarla) |
| URGENCIA FALSA | "¡Últimos cupos!" sin límite real | Lectura | Fecha o cupo real, o quitarla |
| PRECIOS DE PLANTILLA | Planes Free/Pro/Enterprise que no corresponden | Captura | Precio real del servicio |

## Estructura (criterio 8)

| Etiqueta | Qué es | Arreglo |
|---|---|---|
| PIDE ANTES DE CONVENCER | El formulario o la venta aparece antes de cualquier prueba o explicación (en público que no conoce la solución) | Promesa → prueba → cómo funciona → CTA |
| SIN CÓMO FUNCIONA | No se sabe qué pasa después de escribir | 3 pasos: escribes → te respondemos/valoramos → resultado |
| PÁGINA INFINITA | Landing larga para un servicio que el cliente ya busca | Recortar: hero, prueba, cómo funciona, FAQ, CTA |

## Móvil, fricción y velocidad (criterios 9–10)

| Etiqueta | Qué es | Cómo detectarlo | Arreglo |
|---|---|---|---|
| N CAMPOS | Formulario con más campos de los que se usan | `formularios[].campos` ≥ 5 | Solo lo indispensable (nombre + WhatsApp suele bastar) |
| CAMPO DE TEXTO LIBRE | Textarea o desplegables obligatorios | `etiquetas` del formulario | Quitarlo o hacerlo opcional |
| SE DESBORDA EN MÓVIL | Scroll horizontal o elementos cortados | Captura móvil | Ajustar anchos; probar a 390 px |
| TITULAR PARTIDO | Una palabra por línea en el celular | Captura móvil | Bajar el tamaño solo en móvil |
| BOTÓN DIMINUTO | Objetivo táctil < 44 px | `ctas[].bbox` alto | ≥ 44 px, ancho completo |
| TEXTO GRIS ILEGIBLE | Gris claro sobre blanco o sobre color | Captura | Contraste ≥ 4,5:1 |
| LENTA EN MÓVIL | LCP > 2,5 s o página muy pesada | `rendimiento.lcp_ms`, `peso_kb` | Comprimir imágenes (WebP/AVIF), quitar video del hero, lazy-load |
| PLACEHOLDER OLVIDADO | Lorem ipsum, "Tu empresa", enlaces "#", © de otro año | `frases_genericas` (lorem), CTAs a `#` | Revisar todo antes de publicar |

## Diseño (solo señalar; el detalle va a `landing-page-audit` de Landingfolio)

| Etiqueta | Qué es | Arreglo |
|---|---|---|
| GRADIENTE MORADO | Morado/índigo sobre blanco por defecto (la "firma" de las landings hechas con IA según Anthropic) | Colores de la marca o del sector |
| INTER EN TODO | Tipografía por defecto sin decisión | 1–2 familias elegidas con intención |
| TARJETAS EN TARJETAS | Cajas dentro de cajas, mismo radio y sombra | Jerarquía con espacio y tamaño, no con cajas |
| FOTO DE STOCK | Gente genérica, apretón de manos | Fotos reales del dueño, equipo, local, clientes |
| ANIMACIÓN DECORATIVA | Aparecer/deslizar en cada sección | Quitar; animar solo lo que explica algo |
| ETIQUETA EN TODO | Mini-títulos en mayúsculas, 01/02/03, flechas "→" en cada botón | Quitar lo que no da información |
