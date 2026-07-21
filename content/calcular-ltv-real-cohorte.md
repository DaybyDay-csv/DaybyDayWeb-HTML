---
title: "Cómo calcular LTV real por cohorte (sin spreadsheet)"
h1: "Cómo calcular LTV real por cohorte: el método que revela qué canales destruyen valor"
slug: "calcular-ltv-real-cohorte"
meta_desc: "Calcula tu LTV real por cohorte en 2 horas sin spreadsheets. Descubre qué canales destruyen valor y cuáles escala de verdad."
canonical: "https://www.daybydayconsulting.com/blog/calcular-ltv-real-cohorte"
category: "Growth Analytics"
article_date: "2026-07-21"
reading_time: 8
published_at: "2026-07-21T10:00:00+02:00"
primary_keyword: "calcular LTV real"
secondary_keywords: ["LTV cohorte D2C", "margen real ecommerce", "atribución multi-plataforma", "LTV vs ROAS", "cohorte adquisición ecommerce"]
faq: [{"q": "¿Cuál es la diferencia entre LTV bruto y LTV real?", "a": "LTV bruto es la suma de ingresos por cliente sin descontar nada. LTV real resta COGS, fulfillment, devoluciones, chargebacks, CAC atribuido y atención al cliente. Un cliente con LTV bruto puede tener LTV real negativo si sus costes superan los ingresos."}, {"q": "¿Cuántos meses necesito para tener datos fiables de una cohorte?", "a": "Mínimo 12 meses de datos por cohorte mensual, pero necesitas comparar cohortes del mismo período del año anterior para eliminar estacionalidad. Una cohorte de Navidad se comporta diferente a una de enero. Sin esa validación, estás tomando decisiones con ruido."}, {"q": "¿Cómo calculo LTV si vendo en D2C, Amazon y retail?", "a": "Unificas el perfil del cliente por email en Klaviyo y cruzas datos de todas las plataformas. Un cliente que te descubre en Meta, compra en D2C y recompra en Amazon tiene un LTV total. Si calculas LTV por canal por separado, fragmentas el dato y tomas decisiones erróneas."}, {"q": "¿Debo usar cohorte de adquisición o de primer pedido?", "a": "Usa ambas. La cohorte de adquisición (fecha del primer touchpoint) te muestra el coste real de adquisición. La cohorte de primer pedido te muestra rentabilidad del producto. Si usas descuentos agresivos para capturar primeros pedidos, la diferencia entre ambas cohortes te revela cuánto estás subsidiando tu crecimiento."}, {"q": "¿Qué costes debo incluir en el margen real del LTV?", "a": "Incluye: COGS (coste de producto), fulfillment (preparación + envío), devoluciones y chargebacks, CAC atribuido al cliente, y costes de atención al cliente asignables. No incluyas costes fijos de estructura (oficina, salarios) porque esos existen con o sin ese cliente."}]
sources: [{"label": "Think with Google", "url": "https://www.thinkwithgoogle.com/"}, {"label": "Shopify Blog — Marketing Metrics", "url": "https://www.shopify.com/blog/marketing-metrics"}, {"label": "Klaviyo Blog", "url": "https://www.klaviyo.com/blog"}, {"label": "Acquisition.com — Alex Hormozi", "url": "https://www.acquisition.com/"}]
internal_links: [{"url": "/blog/atribucion-post-ios-14-roas-mentira.html", "anchor": "atribución post-iOS 14"}, {"url": "/blog/recuperar-cac-30-dias-secuencia-ofertas-d2c.html", "anchor": "recuperar el CAC en 30 días"}]
cta_title: "Auditoría de 30 minutos sobre tu LTV real"
cta_desc: "Vemos tu LTV por cohorte, qué canales destruyen valor y qué cambiar primero."
cta_href: "/contacto.html"
cta_label: "Reservar auditoría"
llms_summary: "Guía práctica para calcular LTV real por cohorte sin spreadsheets, conectando Klaviyo, GA4 server-side y datos de fulfillment. Incluye framework de 5 pasos y validación de estacionalidad."
tags: ["LTV", "cohortes", "D2C", "margen real", "atribución", "ecommerce"]
migration_state: "good"
---

> "Mi ROAS es alto pero mi accountant me dice que no gano dinero. No entiendo qué está pasando."

Esto lo dijo el fundador de una marca de supplements D2C en nuestra primera llamada. Tenía un ROAS declarado de 3.5x y estaba escalando el canal. Cuando le pedimos los datos de fulfillment y devoluciones, encontramos que su LTV real por cliente era negativo: cada pedido le costaba más de lo que ingresaba.

No era un problema de ROAS. Era un problema de qué métrica miraba.

:::direct-answer
Tu ROAS puede ser 3.5x y tu negocio puede estar destruyendo valor. ROAS mide ingresos brutos sobre inversión publicitaria. No resta COGS, fulfillment, devoluciones, chargebacks ni el coste de atención al cliente. LTV real es lo que queda después de todos esos costes. Sin ese número, estás escalando a ciegas.
:::

## La tesis que vas a aprender a usar

LTV real por cohorte te dice qué canales destruyen valor. ROAS no.

En nuestra experiencia auditando marcas D2C, el patrón se repite: las marcas miran ROAS, Meta les dice que van bien, el negocio no mejora. Esto pasa porque ROAS mide ingresos brutos sobre inversión publicitaria. No resta COGS, fulfillment, devoluciones, chargebacks ni atención al cliente. Escalas un canal que parece rentable pero destruye valor en cada nuevo cliente.

## LTV real vs. LTV de vanidad

LTV de vanidad = Ingresos brutos por cliente. Fácil de calcular. Inútil para tomar decisiones.

LTV real = Ingresos brutos − COGS − Fulfillment − Devoluciones/Chargebacks − CAC atribuido − Atención al cliente.

:::cifra
En nuestra experiencia auditando marcas D2C, hemos visto casos donde marcas con ROAS declarados altos descubrían que su LTV real por cliente era negativo. Escalaban destruyendo valor en cada nuevo cliente capturado a través de ese canal.
:::

## El framework COHORTE LIMPIA: 5 pasos

Es la herramienta que usamos en auditoría para pasar del ROAS de vanidad a un LTV que decide dónde inviertes.

## Paso 1: Abre tu panel y anota cuatro cifras

Sin estas cuatro cifras, cualquier cálculo de LTV es opinión:

1. Ingreso medio por pedido
2. Margen bruto sobre producto
3. Coste de fulfillment por pedido
4. Tasa de devolución

Con esas cuatro calculas tu LTV bruto por pedido. Falta saber qué canal trajo a cada cliente.

## Paso 2: No mires cohorte por fecha de pedido. Mira por fecha de adquisición

Necesitas separar clientes por fecha de primer touchpoint (cuando te descubrieron) y no por fecha de primera compra.

Si lanzas una campaña de Navidad con 30% de descuento, los clientes capturados en esa campaña pueden tener su primer pedido en enero (cuando se aplica el descuento deferred). Si mides solo por primer pedido, estás mezclando cohortes que pagaron precios distintos.

En GA4 server-side con Stape, configuramos cohortes por fuente/medium + fecha de adquisición. Esto te permite responder: ¿los clientes orgánicos tienen mayor LTV que los de Meta con descuento?

:::cifra
En nuestra experiencia auditando marcas, hemos visto casos donde los clientes de campañas con CPA bajo tenían un ratio de devolución mucho mayor. El canal parecía exitoso por volumen, pero destruía valor en cada pedido.
:::

## Paso 3: Necesitas 14 meses para validar estacionalidad

Una cohorte de 12 meses no es representativa sin comparar con el mismo período del año anterior. Los clientes capturados en noviembre tienen comportamiento diferente a los de enero.

El proceso que usamos en auditoría:

1. Cohorte mensual de los últimos 18-24 meses
2. Comparar cohorte enero 2025 vs. enero 2026
3. Si la cohorte más reciente es peor, hay un problema estructural (producto, precio, o segmentación)
4. Si es mejor, tus optimizaciones están funcionando

Nos pasó a nosotros: durante meses miré el LTV medio agregado y escalé el canal equivocado. La cohorte de un trimestre bueno tapaba la sangría del resto. Desde entonces, cohortes o nada.

:::pro-tip
La mayoría de marcas miran LTV medio de todos sus clientes juntos. Eso es inútil si tienes 3 años de datos mezclados con datos de este año. Mira LTV por cohorte de los últimos 14 meses. Si no tienes 14 meses, empieza a recoger datos ahora y no tomes decisiones de escala hasta que los tengas.
:::

## Paso 4: Unifica multi-plataforma (D2C + Amazon + Retail)

Si vendes en varias plataformas, el LTV del cliente es la suma de todas sus fuentes. Un cliente puede:

- Descubrirte en un anuncio de Meta
- Comprar en tu D2C
- Recomprar en Amazon

Si no unificas el perfil, estás calculando LTV fragmentado. Ves tres clientes donde hay uno. Tomas decisiones erróneas.

La unificación funciona así:

- Klaviyo usa el email como identificador principal
- Cruzas con datos de Amazon Seller Central y fulfillment
- n8n automatiza la consolidación semanal

Resultado: un cliente, un LTV total, compre donde compre.

La operación real tiene matices. La unificación completa pide el email del cliente en todas las plataformas. En D2C esto suele funcionar bien porque el checkout pide email. En Amazon la tasa de captura es baja si vendes FBA (Amazon cumple el pedido, no tú), pero puedes subir CSV con datos de compradores a Klaviyo usando el matching por nombre + dirección. No es perfecto, pero cubre buena parte de los recurrentes.

El timing también importa. Un cliente que compra en D2C en enero y en Amazon en marzo tiene un LTV que no ves si consultas las plataformas por separado. Si cruzas datos cada semana, ves el comportamiento completo del cliente. Si cruzas una vez al mes, pierdes la visibilidad de pedidos con poco intervalo entre plataformas.

Y los datos de fulfillment tienen que venir de tu 3PL o del panel de Amazon Seller Central. Si usas 3PL, pídeles un CSV semanal con pedido, cliente, plataforma y coste de envío real. Hay 3PL que te dan coste medio por kilo, no coste real por pedido. Exige el coste por pedido: un desvío de 2 euros en el envío cambia el LTV real de una cohorte entera.

## Paso 5: Calcula cuántos pedidos necesitas para recuperar el CAC

La última pregunta antes de escalar o cerrar un canal: ¿cuántos pedidos necesitas para recuperar el coste de adquirir ese cliente?

Si la cohorte de Meta con descuento tarda 200 días en recuperar el CAC y la cohorte orgánica tarda 45, ya tienes tu respuesta sobre dónde invertir. El canal que parece eficiente por volumen puede ser el que te está financiando el crecimiento con pérdidas.

La fórmula: CAC dividido entre margen neto por pedido. Y margen neto no es ingreso medio menos COGS: resta también el fulfillment y la tasa de devolución aplicada al ingreso, porque una devolución quita ingreso y además genera coste de retorno.

Con Klaviyo y datos de repetición de compra, puedes calcular esto por cohorte. El proceso:

Primero, saca tu cohorte mensual de los últimos 12 meses. Segundo, para cada cohorte, calcula cuántos pedidos ha hecho cada cliente y en qué fechas. Tercero, calcula el margen neto acumulado por cliente por mes. Cuarto, identifica el mes en que el margen acumulado cruza el CAC atribuido. Ese es tu payback period por cohorte.

Si tardas más de 90 días en recuperar el CAC en un canal, ese canal necesita optimización antes de escala. Si la cohorte de un canal nunca recupera el CAC atribuido a 12 meses, tienes que decidir si el volumen compensa las pérdidas o si cierras el canal.

Hay una variable que complica todo: la atribución. Si atribuyes el CAC completo al primer canal, puede que ese canal tenga payback largo aunque otros canales empujaran la conversión. Por eso importa la cohorte por fecha de adquisición: si la de primer touchpoint y la de primer pedido dan resultados distintos, ahí está la diferencia entre pagar por captar atención y pagar por cerrar la venta.

## Acción: tus próximos 30 minutos

Abre Klaviyo y exporta tus pedidos de los últimos 12 meses con fuente de adquisición. Anota tus cuatro cifras: ingreso medio, margen bruto, coste de fulfillment y tasa de devolución. Calcula LTV bruto por pedido restando COGS, fulfillment y tasa de devolución del ingreso medio. Divide tu CAC medio por canal entre ese número. El resultado es en cuántos pedidos recuperas el CAC.

Si no tienes los datos de fulfillment o devoluciones, ese es tu primer gap. Sin esos números, cualquier cálculo de LTV es opinión.

## En este post cubrimos

Por qué ROAS es una métrica de vanidad y LTV real es la que importa, la diferencia entre LTV bruto y LTV real, por qué necesitas 14 meses de datos para validar estacionalidad, cómo unificar LTV multi-plataforma (D2C + Amazon + Retail) y cuántos pedidos necesitas para recuperar el CAC por canal.

En el próximo post de esta serie hablamos de [atribución post-iOS 14](/blog/atribucion-post-ios-14-roas-mentira.html): por qué tu ROAS dice 3x pero tu negocio no es rentable, y cómo conectar GA4 server-side para recuperar la visibilidad que perdiste.

Si después de leer esto quieres calcular tu LTV real con tus datos, [reserva una auditoría de 30 minutos](/contacto.html). Vemos tu LTV por cohorte, qué canales destruyen valor y qué cambiar primero. Sin compromiso.