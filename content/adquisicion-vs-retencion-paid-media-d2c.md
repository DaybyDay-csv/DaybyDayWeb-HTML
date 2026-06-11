---
title: "Adquisición vs retención: cómo separar presupuestos de paid media en D2C"
h1: "Adquisición vs retención: cómo separar presupuestos de paid media en D2C"
slug: adquisicion-vs-retencion-paid-media-d2c
meta_desc: "Guía operativa para separar presupuestos de adquisición y retención en paid media para eCommerce D2C España 2026: definición operativa de adquisición vs retención, splits recomendados por madurez de marca (joven 80-90/10-20, escala 65-75/25-35, maduro 45-60/40-55), estructura de cuenta Meta Ads con campañas ADQ/RET separadas y naming convention, por qué CAC blended esconde la economía real del negocio, fórmula CAC adquisición específico vs LTV90 ajustado por margen contribución, 4 señales para rebalancear hacia retención, encaje de Google Ads brand y email/SMS en el split, dashboard Looker Studio con 4 buckets de gasto/ingresos y enfoque DayByDay Pablo+Jorge con pipeline n8n + Shopify + Meta/Google Ads APIs para reporting blended automatizado."
canonical: "https://www.daybydayconsulting.com/blog/adquisicion-vs-retencion-paid-media-d2c"
category: "Estructura de cuenta"
article_date: "2026-05-15"
reading_time: 10
published_at: "2026-05-15T00:00:00+02:00"
primary_keyword: "adquisición vs retención:"
secondary_keywords: []
faq: [{"q":"¿Qué diferencia hay entre adquisición y retención en paid media D2C?","a":"Adquisición es el spend dirigido a conseguir clientes nuevos (first purchase): audiencias frías, lookalikes, Advantage+ Shopping con expansión, Google Search non-brand, Performance Max prospecting. Retención es el spend dirigido a generar segunda compra, upsell, cross-sell, reactivación de clientes inactivos y defensa de marca: audiencias warm (visitantes/AddToCart 7-30 días), audiencias de compradores con segunda compra pendiente, Google Search brand, email/SMS automatizado, WhatsApp retargeting. La distinción operativa es clave porque cada bucket tiene CPA distinto (retención 40-70% más barata), LTV distinto (compradores recurrentes 2,3-4,5x más rentables) y se mide con KPIs distintos (CAC blended vs ROAS por cohorte). Mezclar ambos en la misma cuenta sin separar presupuestos hace que el algoritmo concentre spend donde es más fácil convertir (warm) y deje sin alimentar el funnel superior, matando el crecimiento."},{"q":"¿Qué porcentaje del presupuesto debe ir a adquisición vs retención en un D2C?","a":"Depende del momento de la marca y del LTV real. Regla operativa que aplicamos en DayByDay: D2C joven (2M€) — 45-60% adquisición y 40-55% retención porque la rentabilidad marginal viene de LTV. Estos rangos asumen que email/SMS y comunidad propia no entran en paid media; si los metes, el split cambia. La trampa habitual es replicar el split de marcas grandes (50/50) cuando la marca todavía está en fase de crecimiento, lo que frena adquisición y aborta el escalado."},{"q":"¿Cómo separo presupuestos de adquisición y retención dentro de Meta Ads?","a":"Estructura recomendada para D2C \\u003e5K€/mes Meta: dos campañas top-level claramente etiquetadas. Campaña Adquisición: objetivo Sales, optimización Purchase, audiencias broad + lookalike high-value buyers + Advantage+ Shopping con expansión activa, exclusión de compradores últimos 60-90 días, ad sets DPA prospecting (DABA), ángulo creativo educativo/aspiracional. Campaña Retención: objetivo Sales, optimización Purchase o Add to Cart según volumen, audiencias warm (ViewContent/AddToCart 7-30d), compradores 90-180d sin segunda compra, ad sets DPA retargeting con product sets cross-sell/upsell, ángulo creativo prueba social/urgencia/recompra. Naming convention: [ADQ]_ o [RET]_ al inicio de cada campaña y ad set para que el reporting separe el spend automáticamente en Looker Studio. Sin esta separación, calcular CAC adquisición real es imposible."},{"q":"¿Por qué el CAC blended no basta para decidir entre adquisición y retención?","a":"El CAC blended mezcla el coste de adquirir clientes nuevos con el coste de generar repeticiones, y oculta la verdadera economía del negocio. Una marca puede tener CAC blended de 18€ que parece sano, pero si el desglose es CAC adquisición 42€ y CAC retención 7€, la realidad es que adquirir clientes nuevos es caro y el negocio está creciendo gracias a la base existente. Cuando esa base se queme (saturación retargeting, fatiga creativa, churn natural), el crecimiento se detiene de golpe. El número correcto a vigilar es CAC adquisición específico — solo cuenta first purchase de usuarios que NO eran clientes — y compararlo con LTV90 o LTV180 ajustado por margen contribución. Sin ese desglose, no se puede decidir cuánto subir/bajar presupuesto de adquisición sin romper margen."},{"q":"¿Cuándo recortar presupuesto de adquisición y meter más en retención?","a":"Cuatro señales operativas claras. (1) CPA adquisición sube \\u003e30% durante 3-4 semanas seguidas sin mejora en CTR ni Hook Rate: la audiencia objetivo está saturada, escalar más adquisición tira margen. (2) Tasa de segunda compra 5.000 últimos 12 meses: estás regalando LTV. (4) Margen contribución por pedido cae 4-6 puntos mes a mes pese a ROAS estable: el LTV implícito está bajando, hay que rebalancear hacia retención y subir AOV. Cuando se dan 2 de las 4 señales, recortamos adquisición un 15-25% durante 2-4 semanas, metemos ese spend en retención (cross-sell, reactivación, post-purchase flows) y reevaluamos. Si el negocio aguanta, el equilibrio nuevo se vuelve permanente."},{"q":"¿Cómo encajan Google Ads brand y email/SMS en el split adquisición vs retención?","a":"Google Ads brand (consultas con nombre de marca) es retención disfrazada de adquisición: el usuario ya te conoce, el clic es defensivo (que no te lo robe un competidor o un revendedor). Si no separas Google brand del resto en el reporting, infla artificialmente el ROAS de adquisición. Email y SMS no son paid media en el sentido estricto, pero compiten por el mismo objetivo: ingresos de base recurrente. La práctica DayByDay es construir un dashboard Looker Studio con 4 buckets de gasto/ingresos: (1) Adquisición pura (Meta cold + Google non-brand + TikTok prospecting), (2) Retención paid (Meta warm + DPA cross-sell + Google brand), (3) Owned (email + SMS + WhatsApp), (4) Orgánico (SEO + social orgánico + referrals). Esto permite ver el CAC marginal real y decidir dónde meter el siguiente euro."}]
internal_links: [{"url":"/tech/meta-ads.html","anchor":"Meta Ads"},{"url":"/tech/google-ads-tech.html","anchor":"Google Ads"}]
cta_title: "¿Quieres aplicar esto en tu negocio?"
cta_desc: "En 30 minutos analizamos tu situación y te decimos exactamente qué acciones tendrían más impacto."
cta_href: "/contacto.html"
cta_label: "Solicitar diagnóstico gratuito"
llms_summary: "Guía operativa para separar presupuestos de adquisición y retención en paid media para eCommerce D2C España 2026: definición operativa de adquisición vs retención, splits recomendados por madurez de m"
migration_state: "rendered"
---

> Epígrafe pendiente. Una frase pegadiza + fecha, opcional pero recomendado.

## Qué es adquisición y qué es retención en paid media D2C

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Split recomendado por madurez de marca

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Cómo separar presupuestos dentro de Meta Ads

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Por qué el CAC blended esconde la economía real

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## 4 señales para rebalancear hacia retención

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Google brand, email y SMS: dónde encajan

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Dashboard Looker Studio con 4 buckets

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Cómo trabajamos en DayByDay

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.


:::pro-tip
Pro tip pendiente: un giro contraintuitivo que el lector no espera. Etiquetarlo como "Pro tip" para que el renderer lo destaque visualmente.
:::

## Acción de hoy

Acción concreta ejecutable en menos de 30 minutos. Con número concreto (minutos, pasos, herramienta). Que el lector pueda hacerla esta misma tarde.

## Recap + cliffhanger

Cubrimos [3 cosas concretas del post]. La semana que viene: [tema del siguiente post con gancho concreto].

## Preguntas frecuentes (mantener)

### ¿Qué diferencia hay entre adquisición y retención en paid media D2C?

Adquisición es el spend dirigido a conseguir clientes nuevos (first purchase): audiencias frías, lookalikes, Advantage+ Shopping con expansión, Google Search non-brand, Performance Max prospecting. Retención es el spend dirigido a generar segunda compra, upsell, cross-sell, reactivación de clientes inactivos y defensa de marca: audiencias warm (visitantes/AddToCart 7-30 días), audiencias de compradores con segunda compra pendiente, Google Search brand, email/SMS automatizado, WhatsApp retargeting. La distinción operativa es clave porque cada bucket tiene CPA distinto (retención 40-70% más barata), LTV distinto (compradores recurrentes 2,3-4,5x más rentables) y se mide con KPIs distintos (CAC blended vs ROAS por cohorte). Mezclar ambos en la misma cuenta sin separar presupuestos hace que el algoritmo concentre spend donde es más fácil convertir (warm) y deje sin alimentar el funnel superior, matando el crecimiento.

### ¿Qué porcentaje del presupuesto debe ir a adquisición vs retención en un D2C?

Depende del momento de la marca y del LTV real. Regla operativa que aplicamos en DayByDay: D2C joven (2M€) — 45-60% adquisición y 40-55% retención porque la rentabilidad marginal viene de LTV. Estos rangos asumen que email/SMS y comunidad propia no entran en paid media; si los metes, el split cambia. La trampa habitual es replicar el split de marcas grandes (50/50) cuando la marca todavía está en fase de crecimiento, lo que frena adquisición y aborta el escalado.

### ¿Cómo separo presupuestos de adquisición y retención dentro de Meta Ads?

Estructura recomendada para D2C \u003e5K€/mes Meta: dos campañas top-level claramente etiquetadas. Campaña Adquisición: objetivo Sales, optimización Purchase, audiencias broad + lookalike high-value buyers + Advantage+ Shopping con expansión activa, exclusión de compradores últimos 60-90 días, ad sets DPA prospecting (DABA), ángulo creativo educativo/aspiracional. Campaña Retención: objetivo Sales, optimización Purchase o Add to Cart según volumen, audiencias warm (ViewContent/AddToCart 7-30d), compradores 90-180d sin segunda compra, ad sets DPA retargeting con product sets cross-sell/upsell, ángulo creativo prueba social/urgencia/recompra. Naming convention: [ADQ]_ o [RET]_ al inicio de cada campaña y ad set para que el reporting separe el spend automáticamente en Looker Studio. Sin esta separación, calcular CAC adquisición real es imposible.

### ¿Por qué el CAC blended no basta para decidir entre adquisición y retención?

El CAC blended mezcla el coste de adquirir clientes nuevos con el coste de generar repeticiones, y oculta la verdadera economía del negocio. Una marca puede tener CAC blended de 18€ que parece sano, pero si el desglose es CAC adquisición 42€ y CAC retención 7€, la realidad es que adquirir clientes nuevos es caro y el negocio está creciendo gracias a la base existente. Cuando esa base se queme (saturación retargeting, fatiga creativa, churn natural), el crecimiento se detiene de golpe. El número correcto a vigilar es CAC adquisición específico — solo cuenta first purchase de usuarios que NO eran clientes — y compararlo con LTV90 o LTV180 ajustado por margen contribución. Sin ese desglose, no se puede decidir cuánto subir/bajar presupuesto de adquisición sin romper margen.

### ¿Cuándo recortar presupuesto de adquisición y meter más en retención?

Cuatro señales operativas claras. (1) CPA adquisición sube \u003e30% durante 3-4 semanas seguidas sin mejora en CTR ni Hook Rate: la audiencia objetivo está saturada, escalar más adquisición tira margen. (2) Tasa de segunda compra 5.000 últimos 12 meses: estás regalando LTV. (4) Margen contribución por pedido cae 4-6 puntos mes a mes pese a ROAS estable: el LTV implícito está bajando, hay que rebalancear hacia retención y subir AOV. Cuando se dan 2 de las 4 señales, recortamos adquisición un 15-25% durante 2-4 semanas, metemos ese spend en retención (cross-sell, reactivación, post-purchase flows) y reevaluamos. Si el negocio aguanta, el equilibrio nuevo se vuelve permanente.

### ¿Cómo encajan Google Ads brand y email/SMS en el split adquisición vs retención?

Google Ads brand (consultas con nombre de marca) es retención disfrazada de adquisición: el usuario ya te conoce, el clic es defensivo (que no te lo robe un competidor o un revendedor). Si no separas Google brand del resto en el reporting, infla artificialmente el ROAS de adquisición. Email y SMS no son paid media en el sentido estricto, pero compiten por el mismo objetivo: ingresos de base recurrente. La práctica DayByDay es construir un dashboard Looker Studio con 4 buckets de gasto/ingresos: (1) Adquisición pura (Meta cold + Google non-brand + TikTok prospecting), (2) Retención paid (Meta warm + DPA cross-sell + Google brand), (3) Owned (email + SMS + WhatsApp), (4) Orgánico (SEO + social orgánico + referrals). Esto permite ver el CAC marginal real y decidir dónde meter el siguiente euro.


## Artículos relacionados (revisar, mantener 2 mejores)

- [Meta Ads](/tech/meta-ads.html)
- [Google Ads](/tech/google-ads-tech.html)
- [Shopify](/tech/shopify.html)
- [GA4](/tech/ga4.html)
