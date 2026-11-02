---
name: landing-pyme
description: Escribe la estructura y el copy completo de una landing page que vende para un negocio de servicios (consultorio, clínica, despacho, agencia, taller, academia, inmobiliaria, servicio local o B2B) cuyo objetivo es que el visitante escriba por WhatsApp, agende una cita o pida una cotización. Entrega el copy por sección, el enlace de WhatsApp con mensaje prellenado y un prompt para construirla en Lovable, v0, Framer o Claude, o un index.html si se pide. Usar cuando digan "hazme una landing para mi negocio", "escribe el copy de mi landing", "qué debe llevar mi landing", "landing para mi consultorio/clínica/agencia", "landing que lleve a WhatsApp", "estructura de landing que vende", "reescribe mi landing para que venda". NO usar para auditar una landing existente (→ auditor-landing), para tripwires o infoproductos con checkout, countdown y bonos (→ landing-alta-conversion-f100k si está instalada), ni para landings SaaS con Stripe (→ landing-producto-formula100k).
---

# Landing para pymes de servicios — estructura y copy que venden

Una landing de servicios no vende el servicio: vende **la siguiente conversación**. Su único trabajo es que la persona correcta escriba por WhatsApp o agende, ya convencida de que vale la pena. Todo lo que no empuja a eso se quita.

`<skill-dir>` = la carpeta donde está este SKILL.md.

## Reglas que no se rompen

1. **Un objetivo, una acción.** Toda la página empuja al mismo botón (WhatsApp, agenda o formulario corto). Sin menú de 5 enlaces ni redes sociales en el hero.
2. **Específico o nada.** Cada afirmación lleva número, plazo, lugar o nombre. "Atención de calidad" no dice nada; "Te atendemos el mismo día en Miraflores, sin cita previa" sí.
3. **Las palabras del cliente, no las del dueño.** El titular sale de cómo el cliente describe su problema (reseñas, mensajes de WhatsApp, preguntas frecuentes), no de cómo el negocio se describe a sí mismo.
4. **Nada inventado.** Testimonios, cifras, reseñas, logos y garantías solo si la persona los da. Si faltan, dejar el hueco marcado `[FALTA: …]` y decir cómo conseguirlo. Nunca rellenar con ejemplos que parezcan reales.
5. **Escribir como habla un humano.** Pasar el copy por [references/copy-humano.md](references/copy-humano.md) antes de entregar.

## Flujo

```
- [ ] Paso 1: Brief (lo que hace falta saber)
- [ ] Paso 2: Elegir el largo según qué tan consciente está el cliente
- [ ] Paso 3: Escribir el copy sección por sección
- [ ] Paso 4: Armar el CTA de WhatsApp / agenda
- [ ] Paso 5: Autoauditoría con la rúbrica
- [ ] Paso 6: Entregar (copy + prompt de constructor, o HTML)
```

### Paso 1 — Brief

Usar [assets/brief.md](assets/brief.md). Si la persona pasó un documento, su web actual, su Instagram o capturas de WhatsApp, sacar de ahí todo lo posible y **preguntar solo lo que falte, una pregunta a la vez** (máximo 6). Lo mínimo indispensable para escribir:
- Qué servicio, para quién y dónde (ciudad/zona o remoto).
- El resultado que el cliente compra (no el servicio: "dejar de perder citas", no "software de agenda").
- La acción: número de WhatsApp, link de agenda o formulario.
- Al menos una prueba real (reseñas, nº de clientes, años, caso con nombre).
- Las 3 dudas que más le hacen antes de comprar (precio, tiempo, confianza, "¿sirve para mí?").

### Paso 2 — Largo según el nivel de conciencia

Ver [references/anatomia.md](references/anatomia.md) § "Largo". Regla corta:
- **El cliente ya sabe que necesita el servicio y está comparando** (dentista, fontanero, contador): landing corta. Hero fuerte + prueba + cómo funciona + FAQ + CTA.
- **El cliente tiene el problema pero no sabe que esto lo resuelve** (automatización, consultoría, servicio nuevo): landing larga. Agregar problema, costo de no hacer nada, cómo funciona y caso real antes de pedir la acción.
- Más caro o más riesgoso el servicio → más prueba y más objeciones resueltas antes del CTA final.

### Paso 3 — Copy sección por sección

Seguir el orden y los requisitos de [references/anatomia.md](references/anatomia.md) y las fórmulas de [references/formulas-copy.md](references/formulas-copy.md). Para el titular, escribir **5 opciones** con fórmulas distintas, elegir una y decir por qué en una línea. Cada sección del entregable lleva:
- **Objetivo** de la sección en una línea.
- **Copy final** (lo que va en la página, tal cual).
- **Visual** sugerido (foto real del equipo/local/resultado; nunca ilustraciones genéricas de stock).

### Paso 4 — CTA de WhatsApp o agenda

- WhatsApp: `https://wa.me/<código-país><número>?text=<mensaje-url-encoded>`, sin `+`, espacios ni guiones. El mensaje prellenado dice de dónde viene y qué quiere: "Hola, vengo de la web y quiero agendar una valoración". Si hay varias campañas, una variante de mensaje por campaña para saber cuál trajo el contacto.
- Texto del botón: verbo + lo que recibe ("Agendar mi valoración gratis", "Cotizar por WhatsApp"). Nunca "Enviar", "Saber más" ni "Contáctanos".
- Debajo del botón, un reductor de riesgo concreto: tiempo de respuesta, "sin compromiso", garantía real.
- En móvil: botón visible en el primer pantallazo y repetido al final; si el constructor lo permite, botón flotante de WhatsApp.

### Paso 5 — Autoauditoría

Puntuar el borrador con la rúbrica de `auditor-landing` (si está instalada: `../auditor-landing/references/rubrica.md`; si no, con la lista de [references/anatomia.md](references/anatomia.md) § "Lista final"). Todo criterio por debajo de 7 se corrige antes de entregar. Hacer la prueba de 5 segundos sobre el hero: qué venden, para quién, qué gano, qué hago, por qué creerles.

### Paso 6 — Entregar

Guardar en `landing-<slug>/`:
- `copy.md` — todo el copy por sección, las 5 opciones de titular, el enlace de WhatsApp y la lista de `[FALTA: …]`.
- `prompt-constructor.md` — a partir de [assets/prompt-constructor.md](assets/prompt-constructor.md), con el copy final pegado, listo para Lovable, v0, Framer AI, Claude, etc.
- `index.html` — **solo si lo piden**: partir de [assets/plantilla.html](assets/plantilla.html), reemplazar tokens, borrar bloques sin dato real y probar a 390 px. Si `auditor-landing` está instalada, capturarla con su `capturar.py` y revisar el primer pantallazo en móvil.

Responder con: titular elegido, estructura en una línea, lo que falta conseguir y las rutas.

## Errores comunes

- **El titular habla del negocio** ("Somos líderes en…"): reescribir desde el resultado del cliente.
- **Testimonios sin nombre ni contexto:** pedir nombre, contexto (barrio, profesión, tipo de negocio) y foto o captura. Sin eso se leen inventados.
- **Tres CTAs distintos** (WhatsApp, llamar, formulario, Instagram): elegir uno principal; el resto, como mucho, en texto pequeño.
- **Copy con olor a IA** ("lleva tu negocio al siguiente nivel", "soluciones integrales"): aplicar [references/copy-humano.md](references/copy-humano.md).
- **Precio escondido cuando todos lo preguntan:** si la objeción nº 1 es el precio, poner un "desde" o rango, o decir claramente por qué depende y cuánto tarda la cotización.
