---
title: "Atribución post-iOS 14: por qué tu ROAS miente"
h1: "Atribución post-iOS 14: por qué tu ROAS dice 3x pero tu negocio no es rentable"
slug: "atribucion-post-ios-14-roas-mentira"
meta_desc: "Tu ROAS de 3.2x puede ser una mentira. Descubre cómo iOS 14 destruyó el tracking y qué hacer para medir rentabilidad real."
canonical: "https://www.daybydayconsulting.com/blog/atribucion-post-ios-14-roas-mentira"
category: "Meta Ads"
article_date: "2026-07-06"
reading_time: 8
published_at: "2026-07-06T10:00:00+02:00"
primary_keyword: "atribución post-iOS 14"
secondary_keywords: ["ROAS real D2C", "Meta CAPI tracking", "atribución multi-touch", "cash flow ROAS", "medición rentabilidad ads"]
faq: [ { "q": "¿Por qué Meta reporta ROAS 3.2x pero mi cuenta de resultados muestra pérdidas?", "a": "Meta atribuye a paid media el 100% de la venta cuando el usuario clickó en un anuncio, aunque otros canales influyeron antes. Si tu margen bruto es 35% y tienes un 20% de devoluciones, tu ROAS real baja de 3.2x a 0.89x. Estás escalando destruyendo caja." }, { "q": "¿Cómo recupero visibilidad de mis conversiones tras iOS 14.5?", "a": "Implementando Meta Conversion API via server-side (Stape) junto al pixel client-side. Esto restaura entre 60-80% de los eventos perdidos en dispositivos Apple. Sin CAPI, solo ves ~40% de tus conversiones reales." }, { "q": "¿Por qué Klaviyo y Meta atribuyen la misma venta a canales diferentes?", "a": "No mienten. Cada plataforma usa un modelo de atribución distinto: Meta usa last-click, Klaviyo usa first-touch o linear. La misma venta puede ser email para Klaviyo (porque abrió el email final) y paid para Meta (porque fue el último click). Necesitas un modelo unificado multi-touch." }, { "q": "¿Cuándo debería dejar de escalar campañas aunque el ROAS reportado sea bueno?", "a": "Cuando tu Cash-Flow ROAS cae por debajo de 1.5x. Esto significa que por cada euro invertido, te quedan menos euros de los que invertiste. Si tu ROAS de plataforma es 3x pero tu margen neto es bajo, estás quemando caja aunque las métricas de Meta digan lo contrario." }, { "q": "¿Qué es un holdout experiment y por qué lo necesito?", "a": "Es aislar un grupo de audiencia de toda publicidad durante 4-6 semanas. Comparando sus compras con el grupo expuesto, sabes qué ventas fueron incrementales (no habrían ocurrido sin ads) versus las que habrías conseguido igual. Sin esto, inviertes a ciegas." } ]
sources: [ {"label": "Meta Business Help — Ads Guide", "url": "https://www.facebook.com/business/ads-guide"}, {"label": "Meta — Conversions API docs", "url": "https://developers.facebook.com/docs/marketing-api/conversions-api/"}, {"label": "Shopify Blog — Marketing Metrics", "url": "https://www.shopify.com/blog/marketing-metrics"}, {"label": "Klaviyo Blog", "url": "https://www.klaviyo.com/blog"}, {"label": "Acquisition.com — Alex Hormozi", "url": "https://www.acquisition.com/"} ]
internal_links: [ {"url": "/blog/recuperar-cac-30-dias-secuencia-ofertas-d2c.html", "anchor": "recuperar el CAC en 30 días"} ]
cta_title: "Auditoría de 30 minutos de atribución y rentabilidad real"
cta_desc: "Vemos tu ROAS reportado vs ROAS real, qué canales destruyen caja y qué cambiar primero."
cta_href: "/contacto.html"
cta_label: "Reserva tu auditoría"
llms_summary: "Guía práctica para founders D2C que descubren que su ROAS reportado no refleja la rentabilidad real. Cubre atribución multi-touch, CAPI implementation, y Cash-Flow ROAS con cifras concretas."
tags: ["meta-ads", "ios-14", "atribucion", "roas", "d2c", "tracking", "klaviyo"]
migration_state: "good"
---

> "Llevo 6 meses escalando con ROAS alto en Meta. Cada mes tenía menos cash en el banco. Un día saqué los números bien: margen medio, devoluciones, shipping. El ROAS real era muy inferior al reportado. Estuve meses quemando caja porque confiaba en la métrica equivocada."

La escena: un fundador de una marca de suplementación celebraba sus campañas en Meta. Invertía capital en ads. Meta le decía que generaba ventas con buen ROAS. Su accountant le dijo un jueves que llevaba meses con flujo de caja negativo.

:::direct-answer
iOS 14.5 rompió el tracking del lado del cliente. En las cuentas que gestionamos, el pixel capta en torno al 40% de las compras. Meta sobrevalora el último click e ignora márgenes, devoluciones y el trabajo previo de tu email, tu contenido y tu marca. El ROAS de plataforma no mide rentabilidad: mide ingresos brutos atribuidos a un canal. Para saber si tu negocio es viable necesitas el Cash-Flow ROAS, que incorpora margen real, costes de fulfillment y datos reconstruidos via CAPI.
:::

## Lo que vas a aprender

1. Por qué iOS 14 destruyó tu visibilidad de conversiones y cómo recuperarla con CAPI
2. Qué es el Cash-Flow ROAS y por qué es la métrica que decide si escalas
3. Por qué Klaviyo y Meta pueden tener razón los dos a la vez
4. El framework PIRÁMIDE DE ATRIBUCIÓN para diagnosis en 5 pasos

---

## El problema: tu pixel solo ve el 40% de lo que pasa

Cuando Apple lanzó iOS 14.5, el seguimiento del lado del cliente se desplomó. En las cuentas que gestionamos, el pixel capta en torno al 40% de los eventos de compra. El resto se evapora sin atribuir.

Meta te dice que tienes un ROAS de 3.2x. Pero calcula sobre una muestra incompleta. Imagina que generaste 100 ventas y tu pixel solo registró 40. Divídelas entre el spend y te sale una cifra inflada.

El ROAS reportado post-iOS 14.5 es como pesar a tu hijo en la báscula de la esquina: la báscula solo funciona la mitad de las veces.

**1. Instala Meta Conversion API via Stape.**

La CAPI envía eventos desde tu servidor, saltándose el navegador. En las cuentas donde la hemos implementado —264.712€ de inversión y 31.555 conversiones registradas con CAPI del lado del servidor—, esto restaura entre un 60% y un 80% de los eventos perdidos. Necesitas un servidor Stape, un contenedor GA4 del lado del servidor y la conexión CAPI activa en tu Events Manager.

**2. Valida el match quality score.**

En Meta Events Manager, busca el match quality score. En nuestra experiencia debe pasar de 7; por debajo, ajusta los parámetros de usuario (email y teléfono hasheados, nombre, apellido, ciudad) o la CAPI pierde efectividad.

**3. Compara eventos emitidos vs eventos recibidos.**

Tras activar CAPI, exporta desde tu backend los eventos de compra enviados y compáralos con los recibidos en Meta. Una discrepancia alta indica un problema de configuración.

La primera auditoría que hacemos con clientes nuevos casi siempre revela un pixel medio ciego. Sin visibilidad no hay optimización real: estás disparando a oscuras.

---

## Cash-Flow ROAS: la métrica que destruye el ego

Aquí viene lo que nadie te cuenta. El ROAS que ves en Meta es ingresos brutos atribuidos divididos entre ad spend. Ignora tu margen bruto por producto, el fulfillment y el shipping, la tasa de devoluciones, los chargebacks y el lifetime value del cliente.

Un ejemplo con números que vemos a menudo en las cuentas que gestionamos: un ROAS de 3.2x en un producto con margen bruto 35% y 20% de devoluciones se queda en un Cash-Flow ROAS de 0.90x. Estás perdiendo 10 céntimos por cada euro invertido.

La fórmula, con el fulfillment ya incorporado en el coste de producto:

Cash-Flow ROAS = ROAS de plataforma × margen bruto × (1 − tasa de devoluciones)

Con los números del ejemplo: 3.2 × 0.35 × 0.80 = 0.90x. Con devoluciones del 20%, puedes estar bajo el agua sin saberlo.

:::cifra
Un ROAS de 3.2x con margen bruto del 35% y un 20% de devoluciones equivale a un Cash-Flow ROAS real de 0.90x. Estás destruyendo caja aunque Meta te diga que vas bien. Son márgenes y devoluciones típicos en D2C de suplementación y cosmética; ajústalo a tus números.
:::

La primera vez que calculé el Cash-Flow ROAS de un cliente, me llevé un susto. Tenían buen ROAS reportado en campaña y un Cash-Flow ROAS bastante inferior. Habían invertido en ads y generado ventas brutas aparentemente buenas. Después de márgenes, devoluciones y shipping, el retorno real era mucho menor de lo que parecía.

No estaba mal. Pero tampoco era el retorno que parecía.

---

## Atribución multi-touch: por qué Klaviyo y Meta pueden tener razón los dos

Klaviyo te dice que email generó ventas. Meta te dice que paid generó la misma venta. Los dos tienen razón parcial y los dos te dan una fotografía incompleta.

Klaviyo suele atribuir por first-touch o linear. Meta usa last-click: la venta entera para el último canal donde hubo click. La misma compra puede ser de email para uno y de paid para el otro sin que ninguno mienta.

El customer journey real tiene 5-7 touchpoints: una impresión de awareness en Instagram, un primer click desde un post del blog, un anuncio de retargeting, un reel guardado, el alta en la newsletter, la secuencia de bienvenida y, al final, la compra tras un email con descuento. Cada touchpoint influye. Pero last-click le da el 100% del crédito al último.

**1. Elige un modelo de atribución.**

First-touch da todo el crédito al canal que trajo al cliente: útil para entender adquisición. Linear reparte a partes iguales: útil para visibilidad. Time-decay pesa más los touchpoints cercanos a la conversión. U-shaped da 40% al primero, 40% al último y reparte el resto. Para D2C recomendamos time-decay como punto de partida porque refleja la realidad del nurturing.

**2. Implementa seguimiento unificado.**

Necesitas una fuente de verdad: GA4 del lado del servidor + CAPI de Meta + Klaviyo como hub de datos, con eventos unificados fluyendo entre plataformas. Sin esto, cada herramienta cuenta su propia historia.

**3. Reconcilia los números a mano al principio.**

Exporta ventas de Shopify y crúzalas con Meta, Google Ads y Klaviyo. Verás overlaps, ventas que nadie reclama y otras que todos reclaman. El objetivo es entender la fotografía real, no tener la herramienta perfecta.

:::pro-tip
Optimiza por ROAS de canal después de corregir por atribución. Si tu canal paid muestra 3x pero la atribución multi-touch revela que solo fue responsable de una fracción de la venta, tu ROAS real de paid es bastante menor. Deja de escalar lo que parece rentable y empieza a escalar lo que genera euros netos.
:::

---

## El framework PIRÁMIDE DE ATRIBUCIÓN: diagnosis en 5 pasos

Esta es la herramienta que usamos con clientes para dejar de decidir con datos rotos.

**1. Reconstruye.** Implementa CAPI + GA4 del lado del servidor. Recupera los eventos que iOS te robó. Sin datos completos, todo lo demás es aproximación.

**2. Calcula.** Computa tu Cash-Flow ROAS real, no el de plataforma. Usa márgenes netos e incluye devoluciones. Si es menor a 1.5x, para de escalar.

**3. Atribuye.** Aplica un modelo multi-touch e identifica qué porcentaje de cada venta movió de verdad el paid. Si solo influyó en una parte, tu contribución real es menor.

**4. Experimenta.** Ejecuta un test de control: aísla un segmento de audiencia de toda publicidad durante 4-6 semanas y mide la diferencia contra el grupo expuesto. Eso es tu lift real. Una parte de tus ventas hubieran ocurrido sin ads.

**5. Unifica.** Construye un panel con datos de Shopify, Meta, Google Ads y Klaviyo. Una fuente de verdad. Sin esto, cada reunión es un debate sobre quién tiene razón.

---

## Acción: tus próximos 30 minutos

Abre una hoja de cálculo y crea tres columnas: ingresos brutos de los últimos 30 días (Shopify), ad spend total (Meta + Google) y margen bruto medio (ingresos menos coste de producto y shipping).

Multiplica la columna 1 por la 3, réstale la columna 2 y divide entre la columna 2. Ese es tu Cash-Flow ROAS.

Si es menor a 1.5x, tienes un problema de rentabilidad. No de ROAS. No de ads. De rentabilidad.

Si no tienes claro tu margen bruto, pregúntale a tu accountant. No a Meta.

---

## En este post cubrimos

Por qué el pixel solo ve una fracción de las compras tras iOS 14.5 y cómo CAPI lo resuelve, la diferencia entre ROAS de plataforma y Cash-Flow ROAS con un ejemplo calculado, por qué Klaviyo y Meta cuentan la misma venta distinto, la PIRÁMIDE DE ATRIBUCIÓN en 5 pasos y el test de control previo a escalar.

---

Tu próximo paso es calcular tu Cash-Flow ROAS real. En el próximo post te explico cómo montar el panel unificado con n8n, GA4 del lado del servidor y Klaviyo para tener una fuente de verdad funcionando en 48 horas. Sin Excel manual. Sin debates en reuniones.