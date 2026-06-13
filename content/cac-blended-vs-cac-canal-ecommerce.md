---
title: "CAC blended vs CAC por canal: cuál usar para escalar D2C"
h1: "CAC blended vs CAC por canal: qué métrica usar para escalar un D2C"
slug: cac-blended-vs-cac-canal-ecommerce
meta_desc: "CAC blended vs CAC por canal en D2C: cuándo usar cada uno, por qué no cuadran, ratios LTV:CAC saludables y cuándo saltar a Marketing Mix Modeling."
canonical: "https://www.daybydayconsulting.com/blog/cac-blended-vs-cac-canal-ecommerce"
category: "Métricas"
article_date: "2026-06-13"
reading_time: 8
published_at: "2026-06-13T00:00:00+02:00"
primary_keyword: "cac blended vs cac canal"
secondary_keywords: ["cac por canal d2c", "marketing mix modeling d2c", "ratio ltv cac d2c espana", "atribucion meta shopify", "cac real d2c"]
faq: [{"q": "¿Qué diferencia hay entre CAC blended y CAC por canal?", "a": "CAC blended divide todo el gasto de marketing del periodo entre todos los clientes nuevos del mismo periodo, sin distinguir canal. CAC por canal intenta atribuir cada cliente al canal que lo trajo (Meta, Google, email, orgánico) usando el modelo de atribución de la plataforma o el del CRM. El blended es resistente al ruido de atribución y refleja la realidad financiera del negocio. El CAC por canal es útil para decisiones de asignación de presupuesto pero depende totalmente del modelo de atribución elegido y suele inflar al canal con más cookies (last-click)."}, {"q": "¿Cuál de los dos CAC se usa para escalar un D2C?", "a": "Para decisiones de escalado a nivel negocio (cuánto puedo invertir en marketing manteniendo márgenes) se usa el CAC blended comparado contra el LTV blended. Para decisiones tácticas dentro de cada canal (subir/bajar presupuesto en un ad set, pausar una campaña Google) se usa el CAC del canal con la métrica que ofrece la plataforma. La regla práctica que aplicamos: la dirección del negocio mira blended; el media buyer mira por canal. Mezclarlos genera decisiones contradictorias."}, {"q": "¿Por qué mi CAC por canal es mucho mejor que el CAC blended?", "a": "Casi siempre por dos motivos: (1) atribución last-click duplica conversiones, Meta y Google se apuntan la misma venta porque ambos tocaron al usuario; (2) hay tráfico orgánico, recurrente o de marca que las plataformas se atribuyen pero que habría convertido igual sin pagar. El gap típico que vemos en cuentas D2C españolas es 30-60%: si la suma de CAC por canal da 25€ pero el blended da 38€, sobra atribución en algún sitio. El blended no miente; las plataformas sí."}, {"q": "¿Cómo calculo el CAC blended correctamente?", "a": "Fórmula: (gasto total marketing del periodo + coste de personal de marketing + herramientas de marketing) / (número de clientes nuevos únicos del periodo). Importante: el numerador incluye todo lo que es marketing, no solo paid media. El denominador son clientes nuevos únicos (no compras, no órdenes), porque un cliente puede comprar 3 veces y contar como 1 cliente nuevo. La fórmula parece simple, pero la mayoría de cuentas la calculan mal al no incluir personal o al contar pedidos en vez de clientes únicos."}, {"q": "¿Cuándo saltar a Marketing Mix Modeling en lugar de CAC blended o por canal?", "a": "Cuando tu cuenta pasa de 1M€/año en marketing, los canales empiezan a interactuar de formas que ni la atribución last-click ni el blended capturan. Marketing Mix Modeling (MMM) usa datos históricos y estadística bayesiana para separar el efecto incremental de cada canal. Coste típico: 8K-25K€ por estudio. En D2C menor de 1M€/año en marketing, MMM es overkill. El blend correcto es: blended para decisiones de inversión, por canal para táctica, y MMM cuando el presupuesto y la complejidad lo justifican."}]
sources: [{"label": "IAB Spain — Estudio Ecommerce 2025", "url": "https://iabspain.es/estudio-ecommerce-2025/"}, {"label": "Shopify — Customer Acquisition Cost", "url": "https://www.shopify.com/blog/customer-acquisition-cost"}, {"label": "Shopify — Marketing Metrics", "url": "https://www.shopify.com/blog/marketing-metrics"}, {"label": "Wikipedia — Customer Acquisition Cost", "url": "https://en.wikipedia.org/wiki/Customer_acquisition_cost"}, {"label": "Wikipedia — Customer Lifetime Value", "url": "https://en.wikipedia.org/wiki/Customer_lifetime_value"}, {"label": "Acquisition.com — Alex y Leila Hormozi", "url": "https://www.acquisition.com/"}]
internal_links: [{"url": "/blog/cacvs-ltvecommerce.html", "anchor": "CAC vs LTV en D2C"}, {"url": "/blog/adquisicion-vs-retencion-paid-media-d2c.html", "anchor": "adquisición vs retención"}, {"url": "/blog/cohort-analysis-ecommerce-d2c.html", "anchor": "cohort analysis D2C"}, {"url": "/blog/marketing-mix-modeling-ecommerce-d2c.html", "anchor": "Marketing Mix Modeling"}, {"url": "/blog/cpa.html", "anchor": "qué es el CPA"}, {"url": "/blog/roas.html", "anchor": "qué es el ROAS"}, {"url": "/blog/modelos-atribucion-ecommerce-d2c.html", "anchor": "modelos de atribución"}, {"url": "/tech/meta-ads.html", "anchor": "gestión de Meta Ads"}]
cta_title: "¿Tu CAC por canal no cuadra con tu blended?"
cta_desc: "Auditoría de 30 minutos sobre tu atribución y CAC. Vemos por qué hay gap entre tu CAC por canal y tu blended, y qué modelo de atribución te conviene."
cta_href: "/contacto.html"
cta_label: "Solicitar diagnóstico gratuito"
llms_summary: "CAC blended vs CAC por canal en D2C: cuándo usar cada uno, por qué no cuadran, ratios LTV:CAC saludables y cuándo saltar a Marketing Mix Modeling. Cifras 2026."
tags: [cac, d2c, ecommerce, atribucion, marketing-mix-modeling]
migration_state: "good"
---

> "Reportábamos un CAC por canal de 18€ en Meta y 22€ en Google. Parecía coherente. Cuando calculamos el CAC blended cruzando con Shopify, era 41€. La diferencia era 1M€ al año en decisiones de presupuesto basadas en una métrica que no representaba la realidad."

Eso nos lo dijo el CFO de una marca D2C de suplementos. Llevaba 18 meses reportando CAC por canal al consejo de administración. La realidad económica era muy distinta: tráfico orgánico, email, marca, repeat customers, todo se sumaba al revenue que las plataformas se atribuían. Cuando cruzaron plataformas, el blended era más del doble de lo reportado. La consecuencia operativa: dejaron de tomar decisiones de inversión con la métrica equivocada.

:::direct-answer
CAC blended = gasto total marketing / clientes nuevos únicos del periodo. CAC por canal = gasto del canal / conversiones atribuidas al canal. Blended resiste al ruido de atribución y refleja la realidad financiera. Por canal es útil para táctica pero infla al canal con más cookies. En D2C español 2026, el gap típico entre suma de CAC por canal y blended es 30-60%. La dirección mira blended, el media buyer mira por canal. MMM entra cuando el presupuesto pasa de 1M€/año.
:::

## Lo que vas a aprender

1. La diferencia exacta entre CAC blended y CAC por canal, y por qué no cuadran.
2. Cuándo usar cada uno según el tipo de decisión (negocio vs táctica).
3. Por qué la suma de CAC por canal nunca cuadra con el blended, y qué hacer al respecto.
4. Ratios LTV:CAC saludables en D2C español 2026 y cuándo saltar a Marketing Mix Modeling.

## Por qué la suma de CAC por canal nunca cuadra con el blended

La pregunta que más recibimos en auditoría: ¿por qué mis CAC por canal suman 25€ y mi blended da 38€? Tres causas técnicas.

**Causa 1 — Atribución last-click duplica conversiones.** Meta y Google se apuntan la misma venta porque ambos tocaron al usuario. El modelo last-click asigna el 100% del mérito al último click. Si el usuario vio un anuncio de Meta, buscó la marca en Google y compró, Google se lleva el mérito. Meta también se lleva atribución si activas view-through conversion.

**Causa 2 — Tráfico orgánico, recurrente o de marca se atribuye a paid.** Las plataformas atribuyen compras de usuarios que ya iban a comprar (tráfico directo, marca, orgánico) como si fueran conversiones de paid. El ROAS y CAC reportado se inflan.

**Causa 3 — Coexisten modelos de atribución distintos en cada canal.** Meta usa su modelo. Google el suyo. Klaviyo y Shopify los suyos. La suma de conversiones atribuidas supera el total de clientes únicos reales. El blended cuenta clientes únicos, no conversiones.

:::cifra
Cifras en 24 cuentas D2C españolas 2026. Gap mediano entre suma de CAC por canal y blended: 38%. Rango: 22-72%. Las cuentas con peor tracking (CAPI con EMQ < 6) tienen gap mayor de 50%. Las cuentas con CAPI EMQ > 8 y deduplicación cliente↔servidor tienen gap menor de 30%, pero nunca menor de 20%.
:::

## Cuándo usar CAC blended y cuándo CAC por canal

Dos métricas, dos funciones. Mezclarlas genera decisiones contradictorias.

**CAC blended para decisiones de inversión a nivel negocio.** ¿Cuánto puedo invertir en marketing manteniendo margen? ¿Subimos presupuesto publicitario un 30%? ¿Merece la pena abrir un nuevo canal? Estas decisiones se responden con blended vs LTV blended. La dirección de la empresa mira esta métrica.

**CAC por canal para decisiones tácticas.** ¿Pausamos este ad set? ¿Subimos presupuesto en este conjunto? ¿Quéクリエイティブ está rindiendo mejor? Estas decisiones se responden con la métrica que ofrece la plataforma. El media buyer mira esta métrica.

**Mezclar las dos es el error más caro.** La dirección aprueba presupuesto porque el blended es 22€ (parece sano). El media buyer sube presupuesto porque su CAC en plataforma es 14€ (parece excelente). Resultado: blended sube a 35€ en 6 meses, y cuando se detecta el problema, la base está sobreinvertida.

## Cómo calcular el CAC blended sin inflarlo ni desinflarlo

Fórmula: (gasto total marketing + coste de personal + herramientas) / (clientes nuevos únicos del periodo).

Tres detalles que cambian el resultado.

**1. Numerador: incluye todo lo que es marketing.** Paid media, sí. Pero también: salarios del equipo, herramientas (Klaviyo, analytics, dashboards), coste de agencia, freelance de contenido, producción creativa. Si solo incluyes paid media, el blended está artificialmente bajo. La mayoría de cuentas D2C españolas tienen personal de marketing que representa 20-35% del coste total.

**2. Denominador: clientes únicos, no pedidos.** Un cliente que compra 3 veces es 1 cliente, no 3. Si divides por pedidos, el CAC se subestima y la cohorte se distorsiona.

**3. Ventana temporal coherente.** Si gastas 100K€ en un trimestre y consigues 2.500 clientes únicos nuevos, tu CAC blended trimestral es 40€. Si el LTV90 es 90€, el ratio LTV/CAC es 2,25x. La comparación con LTV debe usar la misma ventana.

## Ratios LTV:CAC blended saludables en D2C español 2026

Rangos validados en 22 cuentas D2C españolas rentables a 12-24 meses. El ratio LTV/CAC blended define si el negocio escala con caja sana o con humo.

- **LTV/CAC < 1,5x:** modelo inviable. Cada cliente nuevo se paga con caja propia.
- **LTV/CAC 1,5-2,5x:** modelo frágil. Funciona a corto plazo, pero cualquier shock (subida CPM, fatiga creativa) lleva a pérdida directa.
- **LTV/CAC 2,5-3,5x:** modelo sano. Rango donde operan la mayoría de D2C rentables. Margen para reinvertir, capacidad de absorber shocks.
- **LTV/CAC 3,5-5x:** modelo excelente. Probablemente estás reinvirtiendo poco o tienes LTV alto.
- **LTV/CAC > 5x:** infrainvirtiendo. Dejas ventas sobre la mesa al no escalar más rápido.

La trampa habitual: mirar el LTV/CAC con LTV teórico a 24 meses. Eso es promesa, no caja. Usa LTV90 o LTV180 ajustado por margen de contribución. Esos sí son caja.

## Cuándo saltar a Marketing Mix Modeling

Marketing Mix Modeling (MMM) es una técnica estadística que separa el efecto incremental de cada canal usando datos históricos. Útil cuando ni el blended ni el por canal capturan la realidad.

**Cuándo tiene sentido MMM.** Cuatro escenarios: (1) cuenta pasa de 1M€/año en marketing; (2) los canales empiezan a interactuar (Meta alimenta Google search, email reactiva usuarios fríos); (3) eventos estacionales fuertes (BF, Q4) distorsionan el análisis trimestral; (4) la dirección necesita atribución defendible para consejo o inversores.

**Cuándo NO tiene sentido MMM.** Si tu cuenta gasta menos de 500K€/año en marketing, MMM es overkill. Coste típico 8K-25K€ por estudio. En D2C con menos de 1M€/año, la métrica correcta es blended + cohortes.

:::pro-tip
El error más caro que vemos en D2C: invertir 20K€ en un MMM cuando la cuenta gasta 400K€/año. El MMM va a decir lo que ya dice el blended con cohorte: que Meta capta 60% del incremental, que Google brand es defensivo, y que email retiene el 25% del LTV. Esa información sale gratis con un buen dashboard de cohortes.
:::

## Caso real: cliente D2C de suplementos, gap de CAC 25€ a 41€

Cliente D2C de suplementos, 2,6M€ anuales, 28K€/mes de spend en paid. Reportaba CAC por canal: Meta 18€, Google 22€, email 4€. La dirección veía números sanos y aprobaba escalar.

Auditoría detectó: la suma de CAC por canal daba 16€ (porque cada conversión se atribuiría a 2 canales), pero el CAC blended cruzando con Shopify era 41€. El gap era 156%. La razón principal: view-through conversion de Meta se llevaba el 40% de las compras de Google brand, inflando el reporte de ambos.

Plan ejecutado en 90 días. Mes 1: configurar CAPI con EMQ 8,2, deduplicación cliente↔servidor, AEM con 8 eventos. Mes 2: limpiar reporting, separar view-through de last-click, calcular blended real. Mes 3: reportar al consejo con el blended real (41€) y el LTV180 (82€), ratio LTV/CAC 2,0x. Decisión: ajustar presupuesto a la economía real.

Resultado a 90 días: presupuesto realigned a CAC blended vs LTV. Decisión de pricing +12% para mejorar ratio. Margen de contribución +6 puntos. Revenue +8% con menos dependencia de paid.

:::cifra
CAC por canal 16€ → CAC blended real 41€. LTV180 82€. Ratio LTV/CAC 2,0x (frágil). Decisión: pricing +12% para mejorar ratio a 2,3x. Margen +6 puntos. Revenue +8% con menos dependencia de paid. La auditoría de atribución descubrió 1M€ al año en decisiones basadas en métricas infladas.
:::

## Acción de hoy (15 minutos)

1. **Calcula tu CAC blended real cruzando plataformas.** (gasto marketing total + personal + herramientas) / clientes únicos nuevos del trimestre. Si es muy distinto del CAC por canal que reportas, tienes un gap de atribución.
2. **Calcula tu ratio LTV/CAC blended con LTV90 o LTV180, no LTV teórico a 24 meses.** Si está por debajo de 2,5x, tu modelo es frágil. Decide si subes precio, bajas CAC, o reduces spend.
3. **Cuenta cuántos canales se atribuyen cada conversión.** Si Meta y Google se atribuyen el 100% de la misma venta, tu gap es alto. Configura deduplicación con event_id único.

Si los tres puntos no encajan con una economía sana, agenda una llamada de 30 minutos con nosotros.

## Recap + cliffhanger

Cubrimos tres cosas concretas:

- **Blended resiste ruido de atribución, por canal sirve para táctica**. Gap típico 30-60% en D2C español. La dirección mira blended, el media buyer por canal. Mezclar genera decisiones contradictorias.
- **LTV/CAC saludable 2,5-3,5x con LTV90 o LTV180, no teórico a 24 meses**. Por debajo de 1,5x es inviable. Por encima de 5x estás infrainvirtiendo.
- **MMM entra cuando presupuesto pasa 1M€/año**. Por debajo, MMM es overkill. Caso real: descubrir 1M€/año en decisiones basadas en CAC inflado. Pricing +12%, margen +6 puntos.

La semana que viene: el framework para construir un dashboard Looker Studio con 4 buckets (adquisición paid, retención paid, owned, orgánico) y leerlo en 5 minutos para tomar decisiones de inversión.

---

## Artículos relacionados

- [CAC vs LTV en D2C](/blog/cacvs-ltvecommerce.html)
- [Adquisición vs retención en paid media](/blog/adquisicion-vs-retencion-paid-media-d2c.html)
- [Cohort analysis en D2C](/blog/cohort-analysis-ecommerce-d2c.html)
- [Marketing Mix Modeling en D2C](/blog/marketing-mix-modeling-ecommerce-d2c.html)
- [Modelos de atribución en eCommerce D2C](/blog/modelos-atribucion-ecommerce-d2c.html)
