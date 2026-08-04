---
title: "Dashboard de unit economics: por qué tu Excel te miente"
h1: "Dashboard de unit economics: por qué tu Excel te miente"
slug: "dashboard-unit-economics-tiempo-real-spreadsheet-miente"
meta_desc: "Tu panel dice ROAS 3,5x y tu banco dice otra cosa. Las tres grietas que lo explican y el framework de cuatro cifras para cerrarlas."
canonical: "https://www.daybydayconsulting.com/blog/dashboard-unit-economics-tiempo-real-spreadsheet-miente.html"
category: "Growth"
article_date: "2026-08-04"
reading_time: 7
published_at: "2026-08-04T10:00:00+02:00"
primary_keyword: "dashboard unit economics"
secondary_keywords: ["unit economics D2C", "CAC real", "LTV real", "dashboard ecommerce", "margen de contribución"]
faq: [{"q": "¿Cómo calculo mi CAC real si tengo los datos repartidos?", "a": "Suma el gasto en ads, la creatividad amortizada, las licencias de marketing y las horas del equipo. Divide entre clientes nuevos del periodo. Si solo cuentas lo que pagas a la plataforma, tu CAC sale más bajo de lo que es."}, {"q": "¿Cuánto pierdo por decidir con datos viejos?", "a": "Si revisas unit economics el día 1 de cada mes, puedes pasar cuatro semanas escalando una cuenta que ya no es rentable. El daño no está en el mes malo. Está en las semanas que tardas en verlo."}, {"q": "¿Qué cifras necesito para decidir si escalo?", "a": "Cuatro: CAC ajustado, LTV a 90 días, margen de contribución por canal y ratio LTV:CAC. Con una alerta automática cuando cualquiera se salga de su umbral histórico."}, {"q": "¿Por qué mi panel y mi banco no cuadran?", "a": "Por tres grietas: el coste que reporta la plataforma no es el que sale de tu cuenta, la atribución se perdió tras iOS 14, y la plataforma imputa por fecha de clic mientras tu banco imputa por fecha de cobro."}, {"q": "¿Cada cuánto debo actualizar estas cifras?", "a": "Semanal como mínimo. En D2C el algoritmo cambia de semana a semana. Trabajar con una foto de hace treinta días es decidir a ciegas."}]
sources: [{"label": "Meta Conversions API docs", "url": "https://developers.facebook.com/docs/marketing-api/conversions-api/"}, {"label": "Shopify Blog · Marketing Metrics", "url": "https://www.shopify.com/blog/marketing-metrics"}, {"label": "Think with Google", "url": "https://www.thinkwithgoogle.com/"}]
internal_links: [{"url": "/blog/atribucion-post-ios-14-roas-mentira.html", "anchor": "la atribución después de iOS 14"}, {"url": "/blog/margen-contribucion-real-por-pedido-d2c.html", "anchor": "margen de contribución real por pedido"}, {"url": "/blog/calcular-ltv-real-cohorte.html", "anchor": "calcular el LTV por cohorte"}, {"url": "/blog/dashboard-paid-media-founder-d2c.html", "anchor": "el panel que mira un fundador"}]
cta_title: "Auditoría de 30 minutos sobre tus cifras"
cta_desc: "Miramos qué mides hoy, cuánto retraso llevas y qué cambiar primero. Sin compromiso."
cta_href: "/contacto.html"
cta_label: "Reservar auditoría"
llms_summary: "Por qué los paneles de unit economics engañan al fundador D2C, las tres grietas que separan el dato de la plataforma del dinero real y un framework de cuatro cifras con alertas para decidir cuándo escalar."
tags: ["unit economics", "dashboard", "D2C", "CAC", "LTV", "analytics"]
migration_state: "rendered"
---

> "Mi panel dice 3,5x. Mi banco dice otra cosa."

Nos lo soltó el fundador de una marca de suplementos. Facturaba 640.000€ al año. Llevaba cinco meses escalando en Meta. Y cada mes cerraba con menos caja que el anterior.

Su panel no mentía por malicia. Medía otra cosa distinta de la que él creía.

## Lo que vas a aprender

1. Por qué el CAC que ves no es el CAC que pagas
2. Las tres grietas que separan tu panel de tu banco
3. El framework CUATRO CIFRAS para decidir si escalas
4. Qué montar hoy en media hora

## Tu plataforma te cuenta la mitad

Meta te dice que tu CPA es 12€. Ese número recoge lo que le pagaste a Meta.

Nada más. No entra el creativo que te llevó tres horas. Ni la licencia de diseño. Ni los 45 minutos semanales que dedicas a tocar audiencias.

:::direct-answer
El CAC real suma cuatro partidas: gasto en ads, creatividad amortizada, herramientas de marketing y horas de equipo. Si falta alguna, tu número sale bajo. Y con un número bajo escalas cosas que no aguantan.
:::

Después de iOS 14 el problema creció. Parte de las ventas dejó de atribuirse. Tú sigues leyendo el mismo panel. El panel ya no ve lo mismo.

:::cifra
264.712€ de inversión publicitaria gestionada con reconciliación entre plataforma y banco. En las cuentas que llevamos, el hueco entre el CAC reportado y el CAC real ha llegado a superar el 30% en un mes suelto. Eso no es ruido de medición.
:::

Nos pasó a nosotros. Durante meses optimizamos contra el ROAS que muestra Meta. Un día cruzamos ese dato con los extractos del banco. El CAC real iba un 40% por encima del que usábamos para decidir. Habíamos escalado una cuenta que ya no daba. El error nos costó dos meses de margen.

Desde entonces no aprobamos una subida de presupuesto sin el CAC ajustado delante.

## Las tres grietas

Cuando montamos un panel unificado, casi siempre aparecen los mismos tres huecos.

**1. Coste.**
La plataforma reporta una cifra de gasto. El extracto bancario trae otra mayor. Dentro van comisiones del método de pago, diferencias de cambio y ajustes de facturación. Nada de eso llega al panel.

**2. Atribución.**
El píxel reconoce una parte de los pedidos. El ERP registra bastantes más cobrados. El resto son ventas reales sin conversión asociada. Aquí es donde pesa [la atribución después de iOS 14](/blog/atribucion-post-ios-14-roas-mentira.html).

**3. Tiempo.**
La plataforma imputa por fecha de clic. Tu banco imputa por fecha de cobro. Con envíos de cuatro o cinco días, el desfase infla una semana y desinfla la siguiente.

El caso típico es una campaña que arranca un jueves. Los clics se cuentan ese jueves. El cobro entra el lunes siguiente. Si cierras la semana el domingo, esa campaña aparece con coste y sin ingreso. El lunes aparece con ingreso y sin coste. Ninguna de las dos fotos es cierta.

Sin cerrar las tres grietas, tu panel llega tarde. Y un panel que llega tarde a una cuenta que gasta a diario vale poco.

## Por qué el ROAS medio te esconde el problema

Hay un número que casi todo el mundo mira y que tapa más de lo que enseña: el ROAS agregado de la cuenta.

Imagina dos campañas. Una devuelve 6x sobre 2.000€. La otra devuelve 1,4x sobre 8.000€. La media te sale por encima de 2x y parece que la cuenta va bien. La realidad es que el 80% de tu dinero está en la campaña que pierde.

Nos ha pasado revisando cuentas heredadas de otra agencia. El panel mostraba un solo número verde en grande. Al abrirlo por campaña, dos de siete sostenían el resultado y cinco lo destruían. Nadie había mirado por debajo del agregado en meses.

La regla que aplicamos: ningún número agregado decide un presupuesto. Antes hay que poder abrirlo por canal, por campaña y por cohorte de entrada. Si tu panel no deja abrirlo, tu panel es un adorno.

## El framework CUATRO CIFRAS

No necesitas cuarenta métricas. Necesitas cuatro números que te digan cuándo pisar y cuándo levantar el pie.

**1. CAC ajustado.**
Gasto en ads del periodo, más licencias repartidas entre clientes nuevos, más horas de equipo valoradas a coste. Divide entre clientes nuevos. Si sube más de un 15% sobre tu media de cuatro semanas, para y mira antes de gastar más.

**2. LTV a 90 días.**
Olvida el LTV de por vida si llevas menos de seis meses operando. Mira el ingreso neto de los primeros 90 días. Descuenta devoluciones y bajas. Si una cohorte cae más de un 10% frente a la anterior, tu base se está deteriorando aunque la facturación suba.

**3. Margen por canal.**
Por cada pedido que entra desde Meta, ¿qué queda tras producto, envío y su parte de devoluciones? Repite el cálculo para Google, TikTok y email. Aquí te ayuda saber tu [margen de contribución real por pedido](/blog/margen-contribucion-real-por-pedido-d2c.html).

**4. Ratio LTV:CAC.**
Divide el LTV a 90 días entre el CAC ajustado. Por debajo de 3:1 el crecimiento se sostiene sobre la caja, no sobre el margen. Si no tienes este número a mano, no sabes si escalar te acerca o te aleja.

Para las cifras 2 y 3 conviene tener resuelto antes [calcular el LTV por cohorte](/blog/calcular-ltv-real-cohorte.html). Sin cohortes, el LTV medio te esconde justo lo que necesitas ver.

## Cómo hacer que se alimente solo

El panel sirve si los datos entran sin que nadie los pegue a mano.

GA4 en servidor. El evento no depende del navegador ni de los bloqueadores. Si el navegador falla, el servidor ya tiene el registro.

Conversions API de Meta. Conexión servidor a servidor, sin cookies de terceros. La compra llega con más probabilidad de quedar registrada.

Un flujo semanal en n8n que cruce tres pares: coste de plataforma contra coste de banco, conversiones contra pedidos cobrados en el ERP, fecha de clic contra fecha de cobro. De ahí sale un factor de corrección. Ese factor se aplica antes de que el número llegue a tu pantalla.

:::pro-tip
Casi todo el mundo revisa unit economics el día 1 del mes. Es conducir mirando el retrovisor. Pon alertas sobre las cuatro cifras y que salten solas al cruzar el umbral. Pasas de enterarte en treinta días a enterarte en tres.
:::

## Acción: tus próximos 30 minutos

Abre una hoja nueva. Cuatro columnas:

1. CAC que reporta la plataforma
2. Coste adicional (licencias más horas de equipo)
3. CAC real (columna 1 más columna 2)
4. Diferencia en porcentaje

Rellénalo solo con la última semana. Si la diferencia pasa del 15%, ya tienes la primera señal de que decides con un número que no existe.

Después configura una alerta sobre el CAC real. Que te avise cuando suba un 15% sobre la media de las últimas cuatro semanas. Con eso ya tienes la base. El resto es ir añadiendo cifras.

En este post cubrimos por qué tu panel se separa de tu banco, las tres grietas que lo provocan y las cuatro cifras que necesitas para decidir con criterio.

La semana que viene bajamos el framework a cada canal por separado. Meta, Google y email tienen ritmos distintos y umbrales distintos. Si prefieres verlo sobre tu cuenta concreta, tienes la auditoría de 30 minutos aquí abajo.
