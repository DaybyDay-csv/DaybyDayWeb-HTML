---
title: "Checklist de cohortes antes de escalar ads: cash real vs ROAS inflado"
h1: "Checklist de cohortes antes de escalar ads: cash real vs ROAS inflado"
slug: "checklist-cohortes-antes-escalar-ads"
meta_desc: "Antes de escalar ads necesitas ver cash real, no ROAS inflado. Checklist de visibilidad financiera para founders D2C que venden pero no ganan."
canonical: "https://www.daybydayconsulting.com/blog/checklist-cohortes-antes-escalar-ads"
category: "Growth"
article_date: "2026-07-14"
reading_time: 8
published_at: "2026-07-14T10:00:00+02:00"
primary_keyword: "checklist cohortes ads"
secondary_keywords: ["ROAS inflado D2C", "cashflow publicidad ecommerce", "cohort analysis ecommerce", "atribución real google ads", "unit economics D2C"]
faq: [{"q": "¿Por qué mi ROAS miente?", "a": "ROAS se calcula sobre revenue nominal, no sobre cash recibido. Descuentos, devoluciones y chargebacks reducen drásticamente el margen real. Necesitas reconstruir tu Revenue Real descontando para ver si realmente ganas dinero."}, {"q": "¿Cuántos datos de cohorte necesito antes de escalar ads?", "a": "Sin un mínimo de visibilidad de cohorte, estás tomando decisiones con datos incompletos: las devoluciones suelen llegar en las primeras semanas, y el LTV real no se ve hasta pasado el primer mes. Necesitas paciencia con los datos."}, {"q": "¿Qué es el Cash ROAS y cómo se calcula?", "a": "Es efectivo cobrado dividido por coste de adquisición real, con LTV proyectado descontado por retención histórica. La fórmula: Cash ROAS = LTV 90 días / CAC. Solo escala cuando supere el umbral de rentabilidad para tu modelo de márgen."}, {"q": "¿Cómo sé si mi agencia me está dando datos falsos?", "a": "Si solo te muestra ROAS sobre revenue nominal, sin descontar devoluciones ni chargebacks, estás viendo la mitad de la foto. Pide un dashboard con Effective ROAS: net revenue entre ad spend real. Si no lo tienen, tienes un problema de visibilidad, no solo de rendimiento."}, {"q": "¿Cuándo debo parar de escalar hasta tener claridad?", "a": "Cuando tu Effective ROAS esté por debajo del umbral durante dos cohortes consecutivas (60+ días cada una). Esto indica que la campaña no está generando la rentabilidad esperada y necesitas investigar antes de incrementar inversión."}]
sources: [{"label": "TikTok Ads Help Center", "url": "https://ads.tiktok.com/help/"}, {"label": "Shopify Blog — Marketing Metrics", "url": "https://www.shopify.com/blog/marketing-metrics"}, {"label": "Klaviyo Blog", "url": "https://www.klaviyo.com/blog"}, {"label": "Acquisition.com — Alex Hormozi", "url": "https://acquisition.com/"}]
internal_links: [{"url": "/blog/atribucion-post-ios-14-roas-mentira.html", "anchor": "atribución post-iOS 14"}, {"url": "/blog/recuperar-cac-30-dias-secuencia-ofertas-d2c.html", "anchor": "secuencia de ofertas D2C para recuperar CAC"}]
cta_title: "¿Ves ROAS alto pero cashflow negativo?"
cta_desc: "Auditoría de 30 minutos sobre tu visibilidad de cohortes. Vemos tu ROAS real, el gap con revenue nominal y qué cambiar primero."
cta_href: "/contacto.html"
cta_label: "Reservar auditoría gratuita"
llms_summary: "Framework práctico para founders D2C que quieren dejar de escalar ads a ciegas y empezar a tomar decisiones con cash real, no con ROAS inflado por devoluciones y descuentos."
tags: ["ROAS", "cohortes", "cashflow", "D2C", "ecommerce", "meta ads", "google ads"]
migration_state: "rendered"
---

> "Llevo 3 meses subiendo presupuesto en Meta. Mi agencia celebra: ROAS de 4.2x. El banco me llama porque el cashflow no mejora. Yo no sé si estoy ganando dinero o quemando ahorros para aparentar crecimiento."

Lo cuento porque lo he vivido en una auditoría reciente. Su dashboard de Meta decía 4.2x. Su cuenta bancaria decía otra cosa. El problema no es tu campaña. El problema es que mides con los ojos de tu agencia, no con los ojos de tu banco.

Antes de que nadie te diga que escales, necesitas visibilidad real de cohortes.

---

:::direct-answer
Un ROAS alto puede ser ficticio porque se calcula sobre revenue nominal, no sobre cash recibido. Descuentos, devoluciones y chargebacks reducen drásticamente el margen real. Antes de escalar, necesitas un dashboard que conecte ad spend con net revenue real por cohorte, con mínimo 60 días de historial. Sin eso, estás escalando con los ojos vendados.
:::

## Lo que vas a aprender

1. Por qué tu ROAS reporting es una mentira que te cuesta dinero cada mes
2. Cómo calcular Revenue Real descontando devoluciones, chargebacks y descuentos
3. El framework Stop/Go que usamos con clientes antes de aprobar escalada
4. Qué infraestructura necesitas (GA4 server-side, Klaviyo, n8n) para ver la verdad

---

## 1. Por qué tu ROAS reporting miente

ROAS = Revenue / Ad Spend. Revenue es lo que entra antes de restar lo que sale.

Imagina este escenario: gastas X en Meta, vendes 5X en nominal. ROAS: 5x. Bien, ¿no?

Ahora mira lo que pasa después: un porcentaje de esas ventas se devuelve (normalmente en las primeras semanas post-compra), algunos pagos se disputan como chargebacks, y muchos clientes compraron solo porque aplicaste un descuento. Tu net revenue real es significativamente menor.

:::cifra
En las marcas D2C que auditamos, una porción significativa del revenue reportado se desvanece en devoluciones antes de llegar a tu cuenta. Tu dashboard probablemente no lo muestra porque está conectado a revenue nominal, no a efectivo real cobrado.
:::

Lo que ocurre cuando auditas una cuenta D2C: lo primero que verifico es si GA4 y Klaviyo están segmentados por cohorte. La mayoría no lo están. Lo segundo: si existe conexión entre eventos de reembolso y atribución. Casi nunca existe. Sin esto, el ROAS reported es ficción.

Recuerdo una vez que yo mismo tomé una decisión de escalar sin tener los datos de cohorte completos. Confié en el ROAS que me mostraban. Tres meses después, cuando finalmente pude reconstruir los números reales, descubrí que había estado quemando presupuesto en campañas que nunca fueron rentables. Esa experiencia me enseñó que la paciencia con los datos no es opcional.

---

## 2. Revenue Real vs Nominal: el cálculo que cambia todo

Revenue Real = Revenue Nominal - Devoluciones - Chargebacks - Descuentos netos - Coste de financing implícito (pagos fraccionados, BNPL).

El orden importa.

:::pro-tip
La mayoría calcula descuentos al final. Error. Calcula descuentos PRIMERO porque en nuestra experiencia, algunos clientes compran SOLO por el descuento, lo que significa que su LTV real puede ser cero sin el código aplicado. Si el descuento genera la compra, el cliente pertenece al descuento, no a tu producto.
:::

Cómo lo hacemos con clientes:

1. Conecta Klaviyo con Shopify. Trae devoluciones históricas por cohorte de primera compra.
2. Calcula net revenue: (Pedidos - Reembolsos - Chargebacks) del mismo período.
3. Segmenta por cohorte de adquisición, no por mes. Julio no es mejor que marzo porque vendiste más. Es mejor si la cohorte de marzo ha recomprado el doble a día 90.

En las cuentas que gestionamos, cuando calculamos Revenue Real descontando devoluciones, chargebacks y descuentos, solemos ver gaps significativos respecto al revenue nominal. Cuando lo ves por primera vez, cambia cómo lees cada informe de tu agencia.

---

## 3. Cash ROAS: la métrica que tu agencia no te va a dar

Revenue ROAS te dice cuánto vendes por euro invertido. Cash ROAS te dice cuánto cash recibes por euro invertido.

Cash ROAS = LTV 90 días / CAC

Donde:

- Cash received = pedidos cobrados menos reembolsos procesados menos chargebacks
- LTV 90 días = suma de ingresos netos por cliente desde el día 0 hasta el día 90, descontados por tasa de abandono histórica

:::cifra
En los 3,2M€ que gestionamos con visibilidad completa de cohortes, el ratio de eficiencia real solo es visible cuando conectas ad spend con cashflow, no solo con revenue atribuido.
:::

Aquí está lo que nadie te explica: la mayoría de dashboards dan ROAS sobre revenue nominal. Eso está inflado por descuentos y devoluciones no descontadas. Tu pregunta antes de escalar: ¿cuál es mi CPA real? ¿Cuál es mi tasa de devolución por cohorte? ¿Cuál es mi LTV 30/60/90 días? Si no puedes responder a las tres, estás escalando con datos incompletos.

---

## 4. El framework Stop/Go: 60 días antes de tocar presupuesto

Esto es lo que usamos internamente antes de aprobar cualquier escalada para clientes.

**Fase 1. Diagnostica**

Define "cohorte visible" = mínimo 60 días desde primera compra. Sin esto, no tienes datos de devoluciones ni de recompra temprana.

**Fase 2. Evalúa**

Con estos tres criterios:

- Cash ROAS supera tu umbral de rentabilidad
- LTV/CAC muestra múltiplo saludable
- Ratio de devolución dentro de rangos normales para tu categoría

**Fase 3. Decide**

STOP si cualquiera de los anteriores está fuera de rango durante 2 cohortes consecutivas. GO si todo está dentro de rango. Si es GO, escala con incremento moderado semana a semana. Si es STOP, freeze de escalada hasta tener visibilidad completa de la siguiente cohorte.

:::cifra
Una marca que auditamos necesitó semanas de auditoría antes de tocar presupuesto. Encontraron que su CPA real era muy superior al que les reportaban porque el pixel perdía eventos de pago. Escalar con datos incompletos quema spend en la dirección equivocada.
:::

La paciencia aquí no es virtud. Es matemática. Si escalas con datos incompletos y descubres a los 3 meses que tu cohorte era pésima, has quemado 3 meses de spend en la dirección equivocada.

---

## 5. Tu infraestructura mínima viable

No necesitas un data warehouse. Necesitas tres cosas conectadas:

GA4 server-side. El pixel de frontend pierde eventos cuando hay bloqueadores o latencia. El server-side mejora la captura de eventos de pago y reembolso.

Klaviyo con cohorts activo. Segmenta por fecha de primera compra. Mira LTV a 30, 60 y 90 días por cohorte, no por mes.

n8n para dashboard operativo. Conexión directa entre Meta Ads, Google Ads y Shopify. Spend diario vs. pedidos cobrados vs. devoluciones procesadas. El KPI principal: Effective ROAS = Net Revenue / Ad Spend.

Sin esto, cada vez que tu agencia te diga "el ROAS ha mejorado, escala", tú puedes preguntar: "¿Effective ROAS o revenue ROAS? ¿Net revenue de qué cohorte?"

Si no saben responder, tienes tu respuesta.

---

## Acción: tus próximos 30 minutos

Hoy, antes de cerrar el portátil:

1. Ve a tu Shopify. Filtra pedidos de los últimos 60 días. Exporta: pedidos, devoluciones, reembolsos.
2. Calcula: (Pedidos netos de devoluciones y chargebacks) / Ad Spend del mismo período.
3. Compara con el ROAS que tu agencia te reporta.

Si el gap es significativo, tienes un problema de visibilidad que necesita resolverse antes de escalar.

Si quieres que lo hagamos juntos, tenemos una auditoría de 30 minutos donde vemos tu situación real y te damos un plan concreto.

---

## Recap

En este post cubrimos:

- Por qué tu ROAS reporting miente (devoluciones, chargebacks, descuentos)
- Cómo calcular Revenue Real vs Nominal por cohorte
- Cash ROAS con LTV 90 días como métrica real
- Framework Stop/Go con 60 días de cohorte mínima
- Infraestructura mínima: GA4 server-side, Klaviyo, n8n

Tu próximo paso está claro. La pregunta es si tienes los datos para responderla.

---

## Siguiente paso

En el próximo post vamos a hablar de atribución post-iOS 14: por qué tu ROAS de Meta está especialmente inflado y qué hacer con tu setup de CAPI para recuperar la visibilidad que perdiste.

Si quieres profundizar ahora en cómo reconstruimos la atribución real con clientes, tenemos más casos documentados en nuestros resultados.