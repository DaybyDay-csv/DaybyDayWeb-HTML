---
title: "CAC blended vs CAC por canal: qué métrica usar para escalar un D2C"
h1: "CAC blended vs CAC por canal: qué métrica usar para escalar un D2C"
slug: cac-blended-vs-cac-canal-ecommerce
meta_desc: "Diferencias entre CAC blended y CAC por canal en eCommerce D2C: cuándo usar cada uno, cómo calcularlos sin inflar resultados, ratios LTV:CAC saludables, por qué la suma de CAC por canal no cuadra con el blended y cuándo merece la pena saltar a Marketing Mix Modeling."
canonical: "https://www.daybydayconsulting.com/blog/cac-blended-vs-cac-canal-ecommerce"
category: "Métricas"
article_date: "2026-05-04"
reading_time: 9
published_at: "2026-05-04T00:00:00+02:00"
primary_keyword: "cac blended vs"
secondary_keywords: []
faq: [{"q":"¿Qué diferencia hay entre CAC blended y CAC por canal?","a":"CAC blended (o blended CAC) divide todo el gasto de marketing del periodo entre todos los clientes nuevos del mismo periodo, sin distinguir canal. CAC por canal, en cambio, intenta atribuir cada cliente al canal que lo trajo (Meta, Google, email, orgánico) usando el modelo de atribución de la plataforma o el del CRM. El blended es resistente al ruido de atribución y refleja la realidad financiera del negocio; el CAC por canal es útil para decisiones de asignación de presupuesto pero depende totalmente del modelo de atribución elegido y suele inflar al canal con más cookies (last-click)."},{"q":"¿Cuál de los dos CAC se usa para escalar un D2C?","a":"Para decisiones de escalado a nivel negocio (cuánto puedo invertir en marketing manteniendo márgenes) se usa el CAC blended comparado contra el LTV blended. Para decisiones tácticas dentro de cada canal (subir/bajar presupuesto en un ad set, pausar una campaña Google) se usa el CAC del canal con la métrica que ofrece la plataforma. La regla práctica que aplicamos: la dirección del negocio mira blended; el media buyer mira por canal. Mezclarlos genera decisiones contradictorias — el media buyer sube presupuesto porque su CAC en plataforma es bueno, mientras el blended se dispara porque el incremental real es bajo."},{"q":"¿Por qué mi CAC por canal es mucho mejor que el CAC blended?","a":"Casi siempre por dos motivos: (1) atribución last-click duplica conversiones — Meta y Google se apuntan la misma venta porque ambos tocaron al usuario; (2) hay tráfico orgánico, recurrente o de marca que las plataformas se atribuyen pero que habría convertido igual sin pagar. El gap típico que vemos en cuentas D2C españolas es 30-60%: si la suma de CAC por canal da 25€ pero el blended da 38€, sobra atribución en algún sitio. El blended no miente; las plataformas sí."},{"q":"¿Cómo calculo el CAC blended correctamente?","a":"Fórmula: (gasto total marketing del periodo + costes herramientas + fees agencia) / clientes nuevos del periodo. Cliente nuevo = primera compra histórica, no primera compra del mes. Periodo mínimo recomendado 30 días para amortiguar ciclo de conversión; en tickets altos (\\u003e200€) usar 60-90 días. Excluye del numerador costes que no generan adquisición (retención, CRM puro). Excluye del denominador a clientes recurrentes — si los cuentas, infla el resultado y rompe la comparación con LTV de primer pedido."},{"q":"¿Qué relación CAC blended / LTV es saludable en eCommerce D2C?","a":"Depende del horizonte de LTV considerado. Con LTV a 12 meses, el ratio LTV:CAC blended sano para escalar D2C en España está en 3:1 mínimo — por debajo cuesta crecer sin comerse el margen. En productos de recompra alta (suplementos, café, cosmética) puede aceptarse 2:1 a 12 meses si LTV a 24 meses sube a 4-5:1. En productos de un solo uso (regalo, electrónica) el ratio debe medirse contra margen de la primera venta, no LTV proyectado, y conviene exigir CAC blended ≤60% del margen bruto del primer pedido."},{"q":"¿Vale la pena montar Marketing Mix Modeling para resolver el CAC por canal?","a":"Sí cuando el negocio supera ~50K€/mes de spend total y hay \\u003e2 canales relevantes. Por debajo, MMM es un cañonazo para matar mosca: el coste de implementarlo y mantenerlo no se recupera en eficiencia. Antes que MMM, en cuentas medianas funciona muy bien combinar tres lecturas paralelas: CAC blended (verdad financiera), CAC plataforma (decisión táctica) y geo lift o holdout tests trimestrales para medir incrementalidad real de un canal concreto. Esa triangulación cubre el 80% de las decisiones que tomaría un MMM sin la complejidad."},{"q":"¿Cómo afecta iOS y la pérdida de cookies al CAC por canal?","a":"Mucho, y desigual. Meta sufrió más que Google porque dependía más de la cookie cross-site, pero ambos han recuperado parte vía modeled conversions y CAPI/Enhanced Conversions. El efecto neto: el CAC por canal que reportan las plataformas hoy mezcla conversiones reales con conversiones modeladas estadísticamente — fiabilidad menor que pre-2021. Por eso el blended ha ganado peso: no depende de cookies, mide outputs (clientes nuevos) contra inputs (gasto total) sin atribución. En cuentas D2C medianas, mirar solo CAC plataforma en 2026 es ir ciego."}]
internal_links: [{"url":"/tech/meta-ads.html","anchor":"Meta Ads"},{"url":"/tech/google-ads-tech.html","anchor":"Google Ads"}]
cta_title: "¿Quieres aplicar esto en tu negocio?"
cta_desc: "En 30 minutos analizamos tu situación y te decimos exactamente qué acciones tendrían más impacto."
cta_href: "/contacto.html"
cta_label: "Solicitar diagnóstico gratuito"
llms_summary: "Diferencias entre CAC blended y CAC por canal en eCommerce D2C: cuándo usar cada uno, cómo calcularlos sin inflar resultados, ratios LTV:CAC saludables, por qué la suma de CAC por canal no cuadra con "
migration_state: "rendered"
---

> Epígrafe pendiente. Una frase pegadiza + fecha, opcional pero recomendado.

## CAC blended vs CAC por canal: en qué se diferencian

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Por qué la suma de CAC por canal nunca cuadra con el blended

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Cómo calcular el CAC blended sin inflarlo ni desinflarlo

[BODY-TO-REWRITE] Escribir 150-250 palabras bajo este H2 con la voz Hormozi-DayByDay: 4-12 palabras por frase, al menos 1 cifra concreta, al menos 1 retórico del repertorio (cadena lógica / negación encadenada / cifra que abofetea / regla de tres). Mencionar DayByDay / Pablo / Jorge si encaja sin forzar. Verificar que la cifra de referencia se sostiene en growth-partner.html o en el caso real documentado.

## Ratios LTV:CAC blended saludables en D2C español 2026

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

### ¿Qué diferencia hay entre CAC blended y CAC por canal?

CAC blended (o blended CAC) divide todo el gasto de marketing del periodo entre todos los clientes nuevos del mismo periodo, sin distinguir canal. CAC por canal, en cambio, intenta atribuir cada cliente al canal que lo trajo (Meta, Google, email, orgánico) usando el modelo de atribución de la plataforma o el del CRM. El blended es resistente al ruido de atribución y refleja la realidad financiera del negocio; el CAC por canal es útil para decisiones de asignación de presupuesto pero depende totalmente del modelo de atribución elegido y suele inflar al canal con más cookies (last-click).

### ¿Cuál de los dos CAC se usa para escalar un D2C?

Para decisiones de escalado a nivel negocio (cuánto puedo invertir en marketing manteniendo márgenes) se usa el CAC blended comparado contra el LTV blended. Para decisiones tácticas dentro de cada canal (subir/bajar presupuesto en un ad set, pausar una campaña Google) se usa el CAC del canal con la métrica que ofrece la plataforma. La regla práctica que aplicamos: la dirección del negocio mira blended; el media buyer mira por canal. Mezclarlos genera decisiones contradictorias — el media buyer sube presupuesto porque su CAC en plataforma es bueno, mientras el blended se dispara porque el incremental real es bajo.

### ¿Por qué mi CAC por canal es mucho mejor que el CAC blended?

Casi siempre por dos motivos: (1) atribución last-click duplica conversiones — Meta y Google se apuntan la misma venta porque ambos tocaron al usuario; (2) hay tráfico orgánico, recurrente o de marca que las plataformas se atribuyen pero que habría convertido igual sin pagar. El gap típico que vemos en cuentas D2C españolas es 30-60%: si la suma de CAC por canal da 25€ pero el blended da 38€, sobra atribución en algún sitio. El blended no miente; las plataformas sí.

### ¿Cómo calculo el CAC blended correctamente?

Fórmula: (gasto total marketing del periodo + costes herramientas + fees agencia) / clientes nuevos del periodo. Cliente nuevo = primera compra histórica, no primera compra del mes. Periodo mínimo recomendado 30 días para amortiguar ciclo de conversión; en tickets altos (\u003e200€) usar 60-90 días. Excluye del numerador costes que no generan adquisición (retención, CRM puro). Excluye del denominador a clientes recurrentes — si los cuentas, infla el resultado y rompe la comparación con LTV de primer pedido.

### ¿Qué relación CAC blended / LTV es saludable en eCommerce D2C?

Depende del horizonte de LTV considerado. Con LTV a 12 meses, el ratio LTV:CAC blended sano para escalar D2C en España está en 3:1 mínimo — por debajo cuesta crecer sin comerse el margen. En productos de recompra alta (suplementos, café, cosmética) puede aceptarse 2:1 a 12 meses si LTV a 24 meses sube a 4-5:1. En productos de un solo uso (regalo, electrónica) el ratio debe medirse contra margen de la primera venta, no LTV proyectado, y conviene exigir CAC blended ≤60% del margen bruto del primer pedido.

### ¿Vale la pena montar Marketing Mix Modeling para resolver el CAC por canal?

Sí cuando el negocio supera ~50K€/mes de spend total y hay \u003e2 canales relevantes. Por debajo, MMM es un cañonazo para matar mosca: el coste de implementarlo y mantenerlo no se recupera en eficiencia. Antes que MMM, en cuentas medianas funciona muy bien combinar tres lecturas paralelas: CAC blended (verdad financiera), CAC plataforma (decisión táctica) y geo lift o holdout tests trimestrales para medir incrementalidad real de un canal concreto. Esa triangulación cubre el 80% de las decisiones que tomaría un MMM sin la complejidad.

### ¿Cómo afecta iOS y la pérdida de cookies al CAC por canal?

Mucho, y desigual. Meta sufrió más que Google porque dependía más de la cookie cross-site, pero ambos han recuperado parte vía modeled conversions y CAPI/Enhanced Conversions. El efecto neto: el CAC por canal que reportan las plataformas hoy mezcla conversiones reales con conversiones modeladas estadísticamente — fiabilidad menor que pre-2021. Por eso el blended ha ganado peso: no depende de cookies, mide outputs (clientes nuevos) contra inputs (gasto total) sin atribución. En cuentas D2C medianas, mirar solo CAC plataforma en 2026 es ir ciego.


## Artículos relacionados (revisar, mantener 2 mejores)

- [Meta Ads](/tech/meta-ads.html)
- [Google Ads](/tech/google-ads-tech.html)
- [Shopify](/tech/shopify.html)
- [GA4](/tech/ga4.html)
