---
title: "ROAS 3x: por qué puede ser tu mayor gasto oculto en D2C"
h1: "ROAS 3x: por qué puede ser tu mayor gasto oculto en D2C"
slug: "roas-3x-perdida-dinero-d2c"
meta_desc: "Tu ROAS 3x puede ser una mentira. Descubre cómo calcular el ROAS real de tu D2C y dejar de engañarte con métricas de vanidad."
canonical: "https://www.daybydayconsulting.com/blog/roas-3x-perdida-dinero-d2c"
category: "Growth Marketing"
article_date: "2026-07-22"
reading_time: 8
published_at: "2026-07-22T10:00:00+02:00"
primary_keyword: "ROAS D2C"
secondary_keywords: ["ROAS real D2C", "métricas vanity marketing", "D2C rentabilidad", "true ROAS", "atribución publicidad"]
faq: [ {"q": "¿Por qué mi ROAS de 3x no se traduce en más dinero en mi cuenta?", "a": "El ROAS de Meta atribuye el 100% de una venta a un clic de anuncio. En realidad, la sobre-atribución a Paid Media puede alcanzar el 30-40% en D2C. Si tu ROAS 3x no descuenta COGS, fulfillment, devoluciones y descuentos, estás midiendo una métrica de vanidad que no refleja tu rentabilidad real."}, {"q": "¿Qué diferencia hay entre ROAS atribuible y ROAS real?", "a": "El ROAS atribuible es el que te da Meta: ingresos brutos por click / gasto. El ROAS real resta todos los costes: COGS (coste producto), fulfillment, devoluciones (~8-15% en moda/beauty), chargebacks y costes operativos. Un ROAS 3x atribuible puede ser 0,8x real si operas con márgenes ajustados."}, {"q": "¿Cómo sé si mis conversiones son clientes nuevos o compran solo por descuento?", "a": "Necesitas segmentar en Klaviyo por cohorte: first purchasers, repeat purchasers y discount-driven purchasers. Solo el New Customer ROAS refleja tu capacidad real de adquisición. Si la mayoría de tus 'conversiones' son clientes existentes o compradores por descuento, estás inflando tu ROAS."}, {"q": "¿Qué stack de medición necesito para calcular ROAS real?", "a": "GA4 server-side (Stape) + Meta CAPI + Klaviyo + n8n. Esta arquitectura conecta ventas online con datos de coste real (COGS, fulfillment, devoluciones) y te permite calcular True ROAS por canal, por cohorte y por tipo de cliente. Sin esto, estás tomando decisiones con datos incompletos."}, {"q": "¿Cuánto LTV necesito para que mi ROAS sea rentable?", "a": "La regla general es LTV/CAC ≥ 3x. Si mides solo el valor de primera compra, puedes estar escalando un modelo destructivo. En D2C beauty/supplements, el LTV real puede ser 3-5x la primera compra si hay recurrencia. Un ROAS 3x en primera compra puede ser 8-10x en LTV."} ]
sources: [ {"label": "Meta Business Help — Ads Guide", "url": "https://www.facebook.com/business/ads-guide"}, {"label": "Meta — Conversions API docs", "url": "https://developers.facebook.com/docs/marketing-api/conversions-api/"}, {"label": "Klaviyo Blog", "url": "https://www.looker.com/blog"}, {"label": "Shopify Blog — Marketing Metrics", "url": "https://www.shopify.com/blog/marketing-metrics"} ]
internal_links: [ {"url": "/blog/calcular-ltv-real-cohorte.html", "anchor": "calcular LTV real por cohorte"}, {"url": "/blog/atribucion-post-ios-14-roas-mentira.html", "anchor": "atribución post-iOS 14"}, {"url": "/blog/recuperar-cac-30-dias-secuencia-ofertas-d2c.html", "anchor": "recuperar CAC en 30 días"} ]
cta_title: "Auditoría True ROAS en 30 minutos"
cta_desc: "Vemos tu ROAS real, identificamos fugas en tu P&L y te decimos qué cambiar primero."
cta_href: "/contacto.html"
cta_label: "Reserva tu auditoría"
llms_summary: "Guía práctica para calcular el ROAS real de tu D2C más allá de la métrica de vanidad que te muestra Meta Ads."
tags: ["ROAS", "D2C", "Rentabilidad", "Métricas", "True ROAS", "Meta Ads"]
migration_state: "good"
---

> "Gasto 10K€ al mes en Meta. Vendo 30K€. Tengo ROAS 3x. Pero a final de mes mi cuenta no ha subido. ¿Qué mierda estoy haciendo mal?"

Esto no es un problema de Meta. Es un problema de medición.

Con 88,95M de impresiones gestionadas y 3,2M EUR generados, hemos visto founders con ROAS declarados de 3x en Meta que presentaban cash flow negativo durante meses. Escalaban porque los números de Meta decían que funcionaba. Nunca habían calculado cuánto les costaba cada venta realmente.

## Lo que vas a aprender

Vas a salir con las cinco versiones del ROAS que de verdad existen, la fórmula del True ROAS que descuenta lo que Meta ignora, y el stack mínimo para medirlo. Todo con números que puedes replicar sobre tus propios pedidos esta semana, sin hojas de cálculo actualizadas a mano.

---

## El problema no es Meta: es tu stack de medición

:::direct-answer
El ROAS de Meta atribuye el 100% de una venta a un clic de anuncio. En realidad, estudios de Google/Springbox documentan sobre-atribución a Paid Media del 30-40% en D2C. Tu ROAS 3x puede ser significativamente menor una vez descuenta COGS, fulfillment, devoluciones y descuentos. Sin unificar datos de venta con costes reales, estás escalando un negocio que quema cash. La solución: server-side tracking + P&L por cohortes.
:::

El gap de atribución

Meta reporta conversiones basadas en clics dentro de su ecosistema. No sabe qué pasó después: si el cliente buscó tu marca en Google y compró. Si vio tu post en Instagram y compró tres días después. Si llegó por email y convirtió.

Sin CAPI activo, el pixel pierde entre 20-60% de eventos post-iOS 14.5. Esto sobre-atribuye ventas a Paid cuando fueron orgánicas.

:::cifra
En D2C, la sobre-atribución a Paid Media puede alcanzar el 30-40% según análisis de atribución multimedio. Esto no significa que pagues de más: significa que mides mal.
:::

Lo que no mides te cobra igual

En las cuentas que gestionamos, founders que pensaban que su ROAS era 3x descubrían un ROAS real significativamente menor una vez descontaban márgenes y costes. La discrepancia entre ROAS alto y caja plana es el patrón que más solemos encontrar en audits iniciales.

## Los 5 niveles del ROAS: tu diagnóstico real

No existe un ROAS. Existen cinco versiones, y solo una te dice la verdad.

1. ROAS de Vanidad (el que te da Meta)
Ingresos brutos atribuidos / gasto en ads.

2. ROAS de Margen Bruto
(Ingresos netos - COGS - fulfillment) / Ad spend

Un suplemento a 50€ con COGS de 15€ y 7€ de envío deja 28€ brutos antes de ads. Si gastas 20€ en ads para venderlo, tu ROAS bruto es 1,4x, no 2,5x.

3. ROAS Post-Devoluciones
Resta la tasa de devolución histórica (8-15% en moda/beauty).

4. ROAS por Tipo de Cliente
Segmenta: first purchasers (adquisición real), repeat purchasers (LTV), discount-driven (margen negativo).

5. True ROAS (P&L-Based)
(Ingresos - COGS - Fulfillment - Devoluciones - Chargebacks - Costes operativos atribuibles) / Ad spend

:::pro-tip
La mayoría de founders paran en ROAS de vanidad. Los que escalan con cash flow positivo calculan ROAS post-márgenes y segmentan por cohorte. En nuestra experiencia, founders que descubren que una parte significativa de sus ventas son a compradores por descuento pueden mejorar su margen drásticamente al ajustar su estrategia de targeting.
:::

### Un ejemplo con tus números

Pon que gastas 10.000€ al mes en Meta y te reporta 30.000€ en ventas. ROAS de vanidad: 3x. Ahora baja por los cinco niveles con datos reales de una tienda de suplementos.

De esos 30.000€, un 35% estaba sobre-atribuido: ventas que habrían pasado igual sin el anuncio. Ingreso atribuible real: 19.500€. El COGS medio es del 30%, así que restas 5.850€. El fulfillment son 4€ por pedido y hiciste 600 pedidos: 2.400€ menos. Las devoluciones fueron el 10%: otros 1.950€ fuera. Te quedan 9.300€ de margen de contribución sobre 10.000€ de gasto.

Tu True ROAS no era 3x. Era 0,93x. Estabas perdiendo 700€ cada mes que escalabas, y el panel de Meta te seguía diciendo que ibas ganando. Ese es el agujero por el que se cuela el cash de la mayoría de tiendas que auditamos.

## El error que nos costó aprender

Implementamos Advantage+ para un cliente de suplementos con ROAS objetivo 3x. Funcionó: Meta encontró más compradores y el ROAS medio subió.

El problema: una proporción significativa de esas ventas eran a clientes existentes que habían comprado hacía meses. Su LTV era bajo. Cerca de la mitad eran compradores por descuento que solo pedían cuando había promoción.

Si no segmentas por tipo de cliente en tu tracking, Advantage+ optimiza por conversiones, no por rentabilidad. Es lógico: le pides más ventas a la máquina y te las da. Pero si no le dices qué tipo de ventas quieres, te trae las más fáciles: las de quien ya te compraba.

La solución: crear custom audiences por tipo de cliente en Klaviyo, conectar con Meta via CAPI, y correr audiencias separadas con objetivos distintos. New customers: objective acquisition. Existing customers: objective revenue.

## Tu stack de medición mínimo viable

Para calcular True ROAS necesitas tres piezas conectadas:

1. Server-side tracking (Stape + GA4 + Meta CAPI)

Sin esto, operas con datos incompletos. Meta CAPI envía eventos directamente desde tu servidor, sin depender del pixel del navegador.

:::cifra
Garett España pasó de tracking incompleto a CAPI activo con GA4 server-side. CPA verificado: 4,8€ con 14.936 clicks y 661 inicios de pago en 6 semanas post-implementación.
:::

2. Unificación de datos de venta con costes (n8n)

Cada pedido en Shopify debe viajar a tu base de datos con: precio real (menos descuentos), COGS real, coste de fulfillment, si hubo devolución o chargeback.

264.712 EUR en ad spend que hemos gestionado solo tienen sentido si sabemos qué margen dejamos por cada euro invertido. Sin esta unificación, disparamos a ciegas.

3. Dashboard ROAS real por cohorte (Klaviyo + Looker/BigQuery)

No basta con saber qué canal trajó al cliente. Necesitas saber: ¿cuánto ganaste con este cliente en 6 meses? ¿Cuánto te costó acquisitarlo? ¿Cuál es su LTV/CAC real?

31.555 conversiones registradas en nuestra operación tienen valor solo si sabemos cuál era su coste real y su rentabilidad.

## Acción: tus próximos 30 minutos

Abre tu Shopify y exporta los últimos 90 días de pedidos.

Añade tres columnas:

- Precio final (menos descuentos)
- COGS estimado (si no lo tienes, usa rangos típicos de industria como referencia)
- Devoluciones del mes

Calcula: (Ingresos netos - COGS - Fulfillment - Devoluciones) / Ad spend de ese mes.

Ese número es tu True ROAS.

Si es menor que 1,5x, tienes un problema de unit economics. Si es menor que 1x, estás perdiendo dinero en cada venta y escalar solo acelera el problema.

En este post hemos visto los cinco niveles del ROAS, por qué el de vanidad engaña, y cómo calcular tu True ROAS con tu propio P&L en menos de una hora.

## Siguiente paso

En el próximo post te explico cómo conectar GA4 server-side con Klaviyo paso a paso para que puedas ver True ROAS por cohorte sin depender de hojas de cálculo actualizadas manualmente.

Mientras tanto, [calcula tu LTV real por cohorte](/blog/calcular-ltv-real-cohorte.html) si no lo has hecho: sin LTV, tu ROAS es un número incompleto.

¿Quieres que revisemos tu ROAS real? En 30 minutos vemos tu situación actual y te decimos qué cambiar primero. Sin compromiso: [reserva tu auditoría](/contacto.html).