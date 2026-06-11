---
title: "Margen de contribución vs ROAS: la métrica que media buyers olvidan"
h1: "Margen de contribución vs ROAS: la métrica que media buyers olvidan"
slug: margen-contribucion-vs-roas-ecommerce
meta_desc: "Por qué el ROAS de Meta/Google es insuficiente para decidir spend en eCommerce D2C España: definición de margen de contribución, fórmula operativa por pedido, rangos saludables por sector D2C 2026, relación con CAC objetivo y LTV, errores frecuentes de media buyers que solo miran ROAS de plataforma, dashboard mínimo viable y enfoque DayByDay (Pablo + Jorge)."
canonical: "https://www.daybydayconsulting.com/blog/margen-contribucion-vs-roas-ecommerce"
category: "Unit Economics"
article_date: "2026-05-09"
reading_time: 11
published_at: "2026-05-09T00:00:00+02:00"
primary_keyword: "margen de contribución"
secondary_keywords: []
faq: [{"q":"¿Qué es el margen de contribución en un eCommerce D2C y por qué importa más que el ROAS?","a":"El margen de contribución es lo que queda de cada pedido después de restar todos los costes variables: COGS (coste del producto), packaging, fulfilment, comisiones de pasarela de pago, devoluciones esperadas, gastos de envío subsidiados y, sobre todo, el coste de adquisición pagado en Meta/Google. El ROAS solo mira ingresos / inversión publicitaria — ignora todo lo demás. Un D2C de moda con ROAS 3x y margen bruto del 35% puede estar perdiendo dinero después de COGS, devoluciones (15-25%) y operaciones, mientras que un D2C de suplementos con ROAS 1,8x y margen bruto del 70% puede ser muy rentable. La métrica que decide si la cuenta gana o pierde dinero a fin de mes es el margen de contribución por pedido, no el ROAS de la plataforma."},{"q":"¿Cómo se calcula el margen de contribución por pedido en un eCommerce D2C español?","a":"Fórmula operativa: Margen de contribución = AOV − COGS − fulfilment − packaging − comisión pasarela − coste devoluciones esperado − coste adquisición. Ejemplo cuenta D2C moda España 2026: AOV 65€, COGS 22€ (34%), fulfilment 4,5€, packaging 1,2€, comisión Stripe/Bizum 1,8€, devoluciones 18% × coste medio devolución 4€ = 0,72€, coste adquisición Meta CAC 18€. Margen de contribución = 65 − 22 − 4,5 − 1,2 − 1,8 − 0,72 − 18 = 16,78€ por pedido (25,8% sobre AOV). Esta es la cifra real que entra en caja antes de costes fijos (equipo, software, alquiler). El error más frecuente en D2C es calcular ROAS objetivo sin haber calculado primero el margen de contribución mínimo aceptable — y por eso muchas cuentas escalan a pérdida sin saberlo."},{"q":"¿Cuál es el margen de contribución mínimo saludable para un eCommerce D2C en España?","a":"Los rangos que vemos en cuentas D2C españolas rentables a 12-24 meses: margen de contribución por pedido del 20-35% sobre AOV es saludable; del 35-50% es excelente y permite escalar agresivamente; por debajo del 15% el negocio depende de subir el AOV o el LTV (suscripción, repetición) para no perder dinero. Por sector: moda 18-28% (penalizada por devoluciones del 20-30%), belleza 30-45% (devoluciones bajas, COGS bajo), suplementos 40-55% (mejor unit economics del D2C), hogar/decoración 25-40% (logística cara), mascotas 25-35%, alimentación premium 20-30% (logística refrigerada), tecnología/gadgets 15-25%. Si tu margen de contribución está por debajo del rango de tu sector, el problema rara vez es el ROAS — es la estructura de costes (COGS demasiado alto, AOV demasiado bajo, devoluciones descontroladas) o el coste de adquisición (CAC) inflado por una agencia que solo mira ROAS de plataforma."},{"q":"¿Por qué el ROAS de Meta/Google puede ser engañoso al medir rentabilidad real?","a":"Tres razones principales: (1) ROAS in-platform reporta atribución last-click 7-day-click + 1-day-view, que sobreatribuye conversiones a la plataforma vs MER blended (Marketing Efficiency Ratio = revenue total / inversión paid total); en cuentas D2C el ROAS Meta suele ser 1,3-1,8x el MER real. (2) ROAS no descuenta devoluciones, que en moda llegan al 25-30% — un ROAS 3x pre-devoluciones es un MER 2,1-2,4x post-devoluciones. (3) ROAS no incluye descuentos automáticos aplicados en checkout (cupones, primer pedido) que sí aparecen en el revenue de plataforma; el AOV neto post-descuento suele ser 8-15% inferior. La conclusión: usar ROAS de plataforma como métrica única para decisiones de spend lleva a escalar campañas que parecen rentables pero queman caja. El indicador correcto combina margen de contribución, MER blended y CAC blended por canal."},{"q":"¿Cuál es la relación entre margen de contribución, CAC objetivo y LTV en D2C?","a":"La regla operativa: el CAC objetivo = margen de contribución del primer pedido × ratio LTV/CAC deseado. Para D2C español saludable, ratio LTV/CAC mínimo 3:1 a 12 meses, ideal 4-5:1. Ejemplo: marca de suplementos con margen de contribución primer pedido 22€, repetición 2,8 pedidos/cliente en 12 meses con margen 24€/pedido extra (mejor por economías de escala), LTV 12 meses = 22 + (1,8 × 24) = 65,2€. CAC objetivo a ratio 3:1 = 21,7€; a ratio 4:1 = 16,3€. Si la cuenta opera con CAC 30€ pero el equipo paid mira solo ROAS, no detectará que está sub-2:1 hasta que la caja se quede sin colchón. Por eso en DayByDay arrancamos cada cuenta calculando margen de contribución, LTV por cohorte y CAC objetivo antes de tocar una sola campaña — sin ese cálculo, optimizar el ROAS es optimizar la métrica equivocada."},{"q":"¿Qué dashboard o reporting hace falta para gestionar el margen de contribución de forma operativa?","a":"El stack mínimo que montamos para cuentas D2C: (1) Looker Studio o Power BI conectado a Shopify (revenue, AOV, devoluciones), Meta Ads (spend, ROAS in-platform), Google Ads (spend), GA4 (atribución cross-channel) y la pasarela (Stripe/Adyen) para comisiones reales. (2) Cálculo del margen de contribución por pedido automatizado con Google Sheets API o un script Node/Python que cruza COGS por SKU desde Shopify Inventory + costes operativos por categoría + spend paid blended por día. (3) Vista diaria de margen de contribución total (€), MER blended, CAC blended por canal, ratio LTV/CAC por cohorte mensual y % devoluciones. (4) Alerta automática cuando el margen de contribución diario cae bajo el umbral mínimo definido (típicamente -20% sobre baseline). En DayByDay el dashboard se entrega listo en la primera semana de onboarding — es la base para que las decisiones de spend dejen de mirar el ROAS y empiecen a mirar la métrica que realmente importa."},{"q":"¿Cuándo es aceptable operar con margen de contribución negativo o muy bajo en D2C?","a":"Solo en 3 escenarios concretos y siempre con cap de gasto definido: (1) lanzamiento de marca con runway de 6-12 meses y modelo basado en suscripción/recurrencia donde el LTV12-24 cubrirá el CAC inicial — exige modelo financiero con cohortes proyectadas y validación de retención real \\u003e30% mes 3. (2) Test de canal nuevo (TikTok, YouTube, programmatic) con presupuesto acotado del 10-15% del spend total y horizonte de 60-90 días para alcanzar margen positivo. (3) Pico estacional con producto loss-leader que activa cross-sell de catálogo con margen mejor (ej: descuento brutal en producto entrada para captar lead que luego compra bundle). Fuera de esos 3 escenarios, operar con margen de contribución negativo es quemar caja sin estrategia — y es el motivo nº1 por el que D2C aparentemente exitosos cierran a los 24-36 meses. La disciplina de margen de contribución es la diferencia entre escalar de verdad y escalar a pérdida."}]
internal_links: [{"url":"/tech/meta-ads.html","anchor":"Meta Ads"},{"url":"/tech/google-ads-tech.html","anchor":"Google Ads"}]
cta_title: "¿Quieres aplicar esto en tu negocio?"
cta_desc: "En 30 minutos analizamos tu situación y te decimos exactamente qué acciones tendrían más impacto."
cta_href: "/contacto.html"
cta_label: "Solicitar diagnóstico gratuito"
llms_summary: "Por qué el ROAS de Meta/Google es insuficiente para decidir spend en eCommerce D2C España: definición de margen de contribución, fórmula operativa por pedido, rangos saludables por sector D2C 2026, re"
migration_state: "rendered"
---

> Epígrafe pendiente. Una frase pegadiza + fecha, opcional pero recomendado.

## Qué es el margen de contribución en un eCommerce D2C

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Fórmula operativa: cómo calcular el margen de contribución por pedido

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Margen de contribución saludable por sector D2C en España 2026

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Por qué el ROAS de Meta/Google es engañoso (y qué métricas usar en su lugar)

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## CAC objetivo: cómo derivarlo desde el margen de contribución

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Dashboard mínimo viable para gestionar margen de contribución

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

### ¿Qué es el margen de contribución en un eCommerce D2C y por qué importa más que el ROAS?

El margen de contribución es lo que queda de cada pedido después de restar todos los costes variables: COGS (coste del producto), packaging, fulfilment, comisiones de pasarela de pago, devoluciones esperadas, gastos de envío subsidiados y, sobre todo, el coste de adquisición pagado en Meta/Google. El ROAS solo mira ingresos / inversión publicitaria — ignora todo lo demás. Un D2C de moda con ROAS 3x y margen bruto del 35% puede estar perdiendo dinero después de COGS, devoluciones (15-25%) y operaciones, mientras que un D2C de suplementos con ROAS 1,8x y margen bruto del 70% puede ser muy rentable. La métrica que decide si la cuenta gana o pierde dinero a fin de mes es el margen de contribución por pedido, no el ROAS de la plataforma.

### ¿Cómo se calcula el margen de contribución por pedido en un eCommerce D2C español?

Fórmula operativa: Margen de contribución = AOV − COGS − fulfilment − packaging − comisión pasarela − coste devoluciones esperado − coste adquisición. Ejemplo cuenta D2C moda España 2026: AOV 65€, COGS 22€ (34%), fulfilment 4,5€, packaging 1,2€, comisión Stripe/Bizum 1,8€, devoluciones 18% × coste medio devolución 4€ = 0,72€, coste adquisición Meta CAC 18€. Margen de contribución = 65 − 22 − 4,5 − 1,2 − 1,8 − 0,72 − 18 = 16,78€ por pedido (25,8% sobre AOV). Esta es la cifra real que entra en caja antes de costes fijos (equipo, software, alquiler). El error más frecuente en D2C es calcular ROAS objetivo sin haber calculado primero el margen de contribución mínimo aceptable — y por eso muchas cuentas escalan a pérdida sin saberlo.

### ¿Cuál es el margen de contribución mínimo saludable para un eCommerce D2C en España?

Los rangos que vemos en cuentas D2C españolas rentables a 12-24 meses: margen de contribución por pedido del 20-35% sobre AOV es saludable; del 35-50% es excelente y permite escalar agresivamente; por debajo del 15% el negocio depende de subir el AOV o el LTV (suscripción, repetición) para no perder dinero. Por sector: moda 18-28% (penalizada por devoluciones del 20-30%), belleza 30-45% (devoluciones bajas, COGS bajo), suplementos 40-55% (mejor unit economics del D2C), hogar/decoración 25-40% (logística cara), mascotas 25-35%, alimentación premium 20-30% (logística refrigerada), tecnología/gadgets 15-25%. Si tu margen de contribución está por debajo del rango de tu sector, el problema rara vez es el ROAS — es la estructura de costes (COGS demasiado alto, AOV demasiado bajo, devoluciones descontroladas) o el coste de adquisición (CAC) inflado por una agencia que solo mira ROAS de plataforma.

### ¿Por qué el ROAS de Meta/Google puede ser engañoso al medir rentabilidad real?

Tres razones principales: (1) ROAS in-platform reporta atribución last-click 7-day-click + 1-day-view, que sobreatribuye conversiones a la plataforma vs MER blended (Marketing Efficiency Ratio = revenue total / inversión paid total); en cuentas D2C el ROAS Meta suele ser 1,3-1,8x el MER real. (2) ROAS no descuenta devoluciones, que en moda llegan al 25-30% — un ROAS 3x pre-devoluciones es un MER 2,1-2,4x post-devoluciones. (3) ROAS no incluye descuentos automáticos aplicados en checkout (cupones, primer pedido) que sí aparecen en el revenue de plataforma; el AOV neto post-descuento suele ser 8-15% inferior. La conclusión: usar ROAS de plataforma como métrica única para decisiones de spend lleva a escalar campañas que parecen rentables pero queman caja. El indicador correcto combina margen de contribución, MER blended y CAC blended por canal.

### ¿Cuál es la relación entre margen de contribución, CAC objetivo y LTV en D2C?

La regla operativa: el CAC objetivo = margen de contribución del primer pedido × ratio LTV/CAC deseado. Para D2C español saludable, ratio LTV/CAC mínimo 3:1 a 12 meses, ideal 4-5:1. Ejemplo: marca de suplementos con margen de contribución primer pedido 22€, repetición 2,8 pedidos/cliente en 12 meses con margen 24€/pedido extra (mejor por economías de escala), LTV 12 meses = 22 + (1,8 × 24) = 65,2€. CAC objetivo a ratio 3:1 = 21,7€; a ratio 4:1 = 16,3€. Si la cuenta opera con CAC 30€ pero el equipo paid mira solo ROAS, no detectará que está sub-2:1 hasta que la caja se quede sin colchón. Por eso en DayByDay arrancamos cada cuenta calculando margen de contribución, LTV por cohorte y CAC objetivo antes de tocar una sola campaña — sin ese cálculo, optimizar el ROAS es optimizar la métrica equivocada.

### ¿Qué dashboard o reporting hace falta para gestionar el margen de contribución de forma operativa?

El stack mínimo que montamos para cuentas D2C: (1) Looker Studio o Power BI conectado a Shopify (revenue, AOV, devoluciones), Meta Ads (spend, ROAS in-platform), Google Ads (spend), GA4 (atribución cross-channel) y la pasarela (Stripe/Adyen) para comisiones reales. (2) Cálculo del margen de contribución por pedido automatizado con Google Sheets API o un script Node/Python que cruza COGS por SKU desde Shopify Inventory + costes operativos por categoría + spend paid blended por día. (3) Vista diaria de margen de contribución total (€), MER blended, CAC blended por canal, ratio LTV/CAC por cohorte mensual y % devoluciones. (4) Alerta automática cuando el margen de contribución diario cae bajo el umbral mínimo definido (típicamente -20% sobre baseline). En DayByDay el dashboard se entrega listo en la primera semana de onboarding — es la base para que las decisiones de spend dejen de mirar el ROAS y empiecen a mirar la métrica que realmente importa.

### ¿Cuándo es aceptable operar con margen de contribución negativo o muy bajo en D2C?

Solo en 3 escenarios concretos y siempre con cap de gasto definido: (1) lanzamiento de marca con runway de 6-12 meses y modelo basado en suscripción/recurrencia donde el LTV12-24 cubrirá el CAC inicial — exige modelo financiero con cohortes proyectadas y validación de retención real \u003e30% mes 3. (2) Test de canal nuevo (TikTok, YouTube, programmatic) con presupuesto acotado del 10-15% del spend total y horizonte de 60-90 días para alcanzar margen positivo. (3) Pico estacional con producto loss-leader que activa cross-sell de catálogo con margen mejor (ej: descuento brutal en producto entrada para captar lead que luego compra bundle). Fuera de esos 3 escenarios, operar con margen de contribución negativo es quemar caja sin estrategia — y es el motivo nº1 por el que D2C aparentemente exitosos cierran a los 24-36 meses. La disciplina de margen de contribución es la diferencia entre escalar de verdad y escalar a pérdida.


## Artículos relacionados (revisar, mantener 2 mejores)

- [Meta Ads](/tech/meta-ads.html)
- [Google Ads](/tech/google-ads-tech.html)
- [Shopify](/tech/shopify.html)
- [GA4](/tech/ga4.html)
