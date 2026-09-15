# CASOS-SPEC — páginas de caso DaybyDay (patrón McCann × Ogilvy, estética libreta)

Referencias navegadas 2026-09-15: mccann.com (intro tipográfica full-viewport; casos como filas gigante CLIENTE+IDEA) y ogilvy.com/work (caso = página propia, título "IDEA — CLIENTE", Info con Challenge/Approach/Results). Adaptación DaybyDay: narrativa visible estilo editorial (sin overlay), sello GO, parte de caja, cifras en voice-machine, días como unidad (Día 1→90). REGLA DE ORO: solo los hechos verificados abajo; nada inventado; lo "en curso" se marca como tal.

## Estructura de página de caso (todos)
1. Barra superior: `← Todos los casos` (link a /casos/) · título centrado `IDEA — CLIENTE`
2. Hero del caso: eyebrow `.section-tag` con sector + estado (ACTIVO / EN CURSO / HISTÓRICO), H1 serif = el nombre de la IDEA, sub en mono = cliente + sector
3. Bloques narrativos numerados estilo board: `01 — La situación` · `02 — El objetivo` · `03 — Qué hicimos` · `04 — Los resultados` (cada uno .section-tag + h2 .h2-serif + prosa corta). Cifras SIEMPRE .voice-machine. El bloque 04 lleva `.parte-caja` con las métricas + `.stamp.stamp-go` (si hay resultados) o nota honesta de "en curso"
4. Cierre: CTA-box estándar (piloto cero)
5. Footer estándar

## Índice /casos/ (casos/index.html)
- H1: "Los casos." (serif) + sub mono: "Seis historias con nombre propio. Las cifras salen del CRM de cada cliente o de sus plataformas — lo en curso se marca como en curso."
- Filas gigantes estilo McCann (una por caso): [logo cliente pequeño] + IDEA en serif grande + cliente/sector en mono + estado. Hover: se subraya el trazo (sketch). Cada fila = link a su página.

---

## CASO 1 — casos/garett.html · "Seis semanas." — GARETT ESPAÑA
- Estado: ACTIVO · Sector: ecommerce D2C beauty-tech
- 01 La situación: "Una web exportada de un constructor sin checkout. El Shopify anterior, muerto por un impago. En la cuenta de ads: presupuesto fragmentado en demasiadas campañas, creatividades con frecuencia alta — quemadas — y un pixel sin Conversion API. El ROAS que decía la plataforma y la caja del banco no contaban la misma historia."
- 02 El objetivo: "Reconstruir la operación completa — cuenta de ads y ecommerce — y que la caja confirme. Sin baseline bonito: desde el ruido."
- 03 Qué hicimos: "Auditoría de cuenta y tracking primero (Conversion API server-side antes que tocar una campaña). Reestructuración del presupuesto. Rebuild del ecommerce: catálogo reconstruido desde cero, web propia en Cloudflare con Stripe en vivo. Rebrand completo. [Cifra de honestidad:] 14 de los 23 precios se estimaron por benchmark y quedaron marcados a la espera de validación."
- 04 Los resultados (parte de caja + GO): "6 semanas → CPA 4,8 € · 14.936 clicks · 661 inicios de pago" + presente: "Hoy: web propia con Stripe en vivo, catálogo completo y 78 relojes contados uno a uno."
- Fecha: ago 2026.

## CASO 2 — casos/universidad.html · "El caso que no puedo contar." — UNIVERSIDAD PRIVADA (NDA)
- Estado: CLIENTE MENSUAL 2023–2026 · Sector: educación superior high-ticket
- 01: "Una universidad privada grande — el NDA no me deja decir cuál ni quién operaba. Más de 30 programas de postgrado compitiendo por los mismos alumnos. El lead valía mucho; el gasto también."
- 02: "Captación multicanal con atribución real en su CRM — no en el dashboard de la plataforma."
- 03: "Meta + Google operados contra el CRM del cliente. 711 creatividades. Landings por programa. Reporting de cierre anual con presupuestos y leads por facultad — la cultura del dato antes de cualquier optimización."
- 04 (parte de caja + GO): "193.829 € gestionados · 711 creatividades · 1.980 leads en el último año completo reportado (77.386 € de inversión, CPL ~39 €). Por programa: de 583 a 2.987 leads por máster y temporada."
- Cierre honesto: "Por el acuerdo, esta es la única página donde el cliente no tiene nombre. Las cifras son las de los informes de cierre."

## CASO 3 — casos/tres-negocios.html · "Tres negocios, un decisor." — ARAS LIFE PLUS → CARTRI → GARETT
- Estado: HISTÓRICO → ACTIVO (la cadena sigue) · Sector: ecommerce + automation
- 01: "Todo empezó con una tienda de accesorios tecnológicos que necesitaba vender sin depender del dueño. Shopify como base, WhatsApp como canal, campañas automáticas encima. Funcionó."
- 02: "Que el dueño no fuera el cuello de botella de su propia venta."
- 03: "Setup completo en 4 semanas: tienda, canal de venta por WhatsApp Business, campañas automáticas. Y algo que no sale en ninguna captura: hacer que el resultado fuese obvio para el que decide."
- 04: "El resultado medible no está en esta página — está en las otras dos. El mismo decisor nos confió después Cartri y hoy Garett. Su texto, publicado en esta web desde el primer día: «Contraté a DayByDay para la web de Aras Life Plus… Por eso confié en ellos para Cartri, y ahora para el desarrollo y la expansión de Garett en España.»"
- Stamp: GO + línea: "El mejor indicador de un caso no es su ROAS: es la repetición."

## CASO 4 — casos/cartri.html · "233 captaciones y 5 pedidos." — CARTRI
- Estado: EN CURSO (campaña desde 15-09-2026) · Sector: fabricante de pádel, D2C
- 01: "Un fabricante con 20 años y 22 países vendiendo directo: 233 clientes nuevos al mes captados… y 5 pedidos, 0 repetidores. El problema no era el tráfico. Era lo que pasaba — y lo que no pasaba — después de captar."
- 02: "Activar la base sin comprar un euro más de tráfico. Email primero."
- 03: "Diagnóstico con datos de su Shopify. Sistema de email completo: 23 piezas escritas (welcome, checkout, post-purchase, browse, winback, replenishment). 4 códigos creados por API, 5 segmentos, campaña de reactivación sobre 200 mailables con línea de diseño propia. Theme de campaña con configurador de packs y gift por umbral. Y un fix que nadie veía: relojes de regalo vendiéndose con stock 0 porque el tracking de inventario estaba apagado."
- 04 (honesto): "La campaña arrancó el 15 de septiembre de 2026. Esta página se actualizará con los números cuando los haya — antes no. Así trabajamos."
- Stamp: no GO todavía → bloque "EN CURSO" con la promesa de actualización.

## CASO 5 — casos/globalthy.html · "0 € si no hay cita." — GLOBALTHY
- Estado: EN CURSO (test listo, lanzamiento pendiente del cliente) · Sector: salud privada, marketplace
- 01: "Un marketplace de salud con 150+ profesionales y una historia común: 730 € quemados en botones de boost de Instagram desde noviembre, 39 campañas sin estructura, ni un píxel instalado, dos anuncios activos — uno rechazado, otro roto. Y un trauma previo: otra agencia les firmó 5.000 € que no volvieron."
- 02: "Primera cita medible con el mínimo riesgo posible. Y recuperar la confianza."
- 03: "Auditoría gratis con acceso real a su Ads Manager (la factura de ese desastre, por escrito). Test de 30 días por 150 € con regla escrita: si no hay citas, no cobro fee. Click-to-WhatsApp — verificado en la librería de anuncios: 0 de 12 competidores lo usan. 15 creativos mapeados por funnel, criterios Go/No-Go firmados: ≥3 citas, CPA ≤ 18 €, CTR > 1,2 %."
- 04 (honesto): "El test está montado y las creatividades entregadas. El que falta para lanzar es el pago del test — está en manos del cliente. Esta es la página más honesta de la web: aquí se ve cómo trabajo incluso cuando el resultado aún no depende de mí."
- Sin stamp GO → bloque "TEST LISTO — PENDIENTE DE LANZAMIENTO".

## CASO 6 — casos/ferra.html · "11 cuentas antes de vender nada." — FERRA
- Estado: EN CURSO (lanzamiento 04-11-2026) · Sector: joyería D2C (JV DaybyDay + productora audiovisual)
- 01: "Una joyería nueva con un corto rodado en Mauritania dentro del producto. Cero audiencia el día uno. El lanzamiento: 500 unidades el 4 de noviembre de 2026."
- 02: "Construir audiencia orgánica antes de gastar el primer euro en anuncios — y que la máquina no dependiera de nadie publicando a mano."
- 03: "Sistema de distribución de contenido autoconstruido: n8n en VPS propio, 11 cuentas de Instagram (1 principal + 10 temáticas), ~386 conceptos creativos en 4 etapas. Workflow de publicación verificado en producción vía Graph API — publica solo. Editores externos con pricing cerrado para el volumen."
- 04 (honesto): "La máquina ya publica. Las ventas empiezan el 4 de noviembre. Los seguidores que hay ahora son el activo; el caso se cierra con el drop."
- Bloque "PRE-LANZAMIENTO · DÍA −50" con contador hacia el 4-nov (opcional visual).

---

## HOME — intro McCann (cambio en index.html)
- Sección NUEVA al inicio (antes del hero-craft actual), full-viewport (100svh), fondo tinta #14131A (color fijo, no var — es la "portada" tipo McCann, independiente del tema), texto color papel #FAF8F3:
  - "DaybyDay" — Inter 800, tamaño monumental full-width (font-size: clamp(4rem, 14.5vw, 15rem); line-height: .9; letter-spacing: -0.04em; text-align: center; padding-top para centrar verticalmente con flex column justify-center)
  - Debajo (margin-top ~2rem, centrado): "Growth is a daily craft." — Source Serif 4 itálica 600, clamp(1.6rem, 3.4vw, 3.2rem)
  - Debajo, mini en mono .55 opacity: "El crecimiento, día a día." + flecha ↓ (indicador de scroll, animación sutil de bajada 2s ease infinite — sin loop si reduced-motion)
  - h1 pasa a ser "DaybyDay" (la marca, como McCann); el eslogan queda como elemento tipográfico grande (p/h2). El hero-craft actual queda COMO SEGUNDA PANTALLA (sub, lead, explainer, arte interactivo — sin cambios).
- Comportamiento de scroll: normal (no hijack). La intro es static 100svh.
