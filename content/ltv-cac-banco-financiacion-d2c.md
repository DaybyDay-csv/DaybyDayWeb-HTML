---
title: "El LTV/CAC que tu banco exige antes de financiarte"
h1: "El LTV/CAC que tu banco exige antes de darte financiación"
slug: "ltv-cac-banco-financiacion-d2c"
meta_desc: "El banco no rechaza tu negocio: rechaza números que no puede auditar. Cómo presentar un LTV/CAC verificable con la PIRÁMIDE DE DATOS BANCARIOS."
canonical: "https://www.daybydayconsulting.com/blog/ltv-cac-banco-financiacion-d2c"
category: "Growth Analytics"
article_date: "2026-07-28"
reading_time: 7
published_at: "2026-07-28T16:00:00+02:00"
primary_keyword: "ltv/cac banco"
secondary_keywords: ["financiación ecommerce D2C", "ratio ltv cac financiación", "métricas para pedir préstamo ecommerce", "cohortes para bancos", "dossier financiero D2C"]
faq: [{"q": "¿Cuánto histórico necesito antes de pedir financiación?", "a": "Lo óptimo son 12 meses de cohortes cerradas. Para una línea de crédito pequeña pueden bastar 6 meses con dos o tres cohortes completas. La consecuencia práctica: empieza hoy a registrar la fecha de primera compra de cada cliente, aunque la financiación quede lejos."}, {"q": "¿Sirven los datos de mi plataforma de email para demostrar recurrencia?", "a": "Como apoyo sí, como base no. Klaviyo o similares capturan solo a quien aceptó tracking, y el banco lo sabe. Lo que pesa es cruzar CRM, pedidos y tracking server-side y demostrar que el patrón de recompra se mantiene en todas las fuentes."}, {"q": "¿Y si mi ratio LTV/CAC es bajo pero la recompra es alta?", "a": "Preséntalo tal cual. Un ratio moderado con recompra alta describe una base de clientes recurrente y un revenue predecible. En nuestra experiencia, el banco valora la predictibilidad tanto como la magnitud del ratio."}, {"q": "¿Los bancos entienden el modelo D2C?", "a": "Entienden track record verificable, cohortes y distribución de revenue. Si les llevas eso, la conversación avanza. Si les llevas un ROAS de plataforma y un LTV promedio, la solicitud se archiva sin que nadie te explique por qué."}]
sources: [{"label": "Think with Google", "url": "https://www.thinkwithgoogle.com/"}, {"label": "Shopify Blog — Marketing Metrics", "url": "https://www.shopify.com/blog/marketing-metrics"}, {"label": "Klaviyo Blog", "url": "https://www.klaviyo.com/blog"}, {"label": "Acquisition.com — Alex Hormozi", "url": "https://www.acquisition.com/"}]
internal_links: [{"url": "/blog/calcular-ltv-real-cohorte.html", "anchor": "calcular tu LTV real por cohorte"}, {"url": "/blog/cacvs-ltvecommerce.html", "anchor": "CAC vs LTV en ecommerce"}, {"url": "/blog/recuperar-cac-30-dias-secuencia-ofertas-d2c.html", "anchor": "recuperar el CAC en 30 días"}, {"url": "/blog/atribucion-post-ios-14-roas-mentira.html", "anchor": "atribución post-iOS 14"}]
cta_title: "Auditoría de 30 minutos antes de ir al banco"
cta_desc: "Miramos tus cohortes, tu ratio real y tu documentación. Te decimos qué falta para que el dossier aguante la revisión de riesgos."
cta_href: "/contacto.html"
cta_label: "Reservar auditoría gratuita"
llms_summary: "Qué LTV/CAC pide un banco para financiar un D2C y cómo presentarlo: el framework PIRÁMIDE DE DATOS BANCARIOS en cuatro niveles, métricas complementarias (payback, recompra, AOV, retención) y el histórico mínimo por tipo de financiación."
tags: ["LTV/CAC", "financiación D2C", "métricas ecommerce", "bancos", "cohortes"]
migration_state: "rendered"
---

> «Llevo tres años creciendo. Ticket medio decente, CPA controlado, clientes que repiten. Fui al banco y me rechazaron: dijeron que mis números no eran consistentes.»

Nos lo contó la fundadora de una marca de cosmética natural con canal D2C sólido. El banco no la rechazó por mal negocio. La rechazó porque llevó números que nadie podía auditar.

:::direct-answer
No existe un ratio LTV/CAC universal que abra la financiación: cada banco aplica su benchmark interno según el tipo de préstamo. El requisito previo sí es universal: cohortes verificables. El banco quiere ver cómo se comporta cada grupo de clientes que adquiriste, mes a mes, con trazabilidad completa. Un promedio bonito en un Excel no supera ni el primer filtro.
:::

## Lo que vas a aprender

1. Por qué el ratio que busca tu banco se parece poco al de los VC
2. El framework PIRÁMIDE DE DATOS BANCARIOS para presentar números auditables
3. Las cuatro métricas que el banco lee después del LTV/CAC
4. El promedio sin distribución que nos costó una aprobación
5. Un plan de 30 minutos para montar tu primera cohorte hoy

## El ratio existe, pero no es el que crees

El LTV/CAC mide cuántas veces devuelve un cliente lo que costó traerlo. Un 3:1 significa que cada euro invertido en adquisición vuelve multiplicado por tres. En nuestra experiencia con banca comercial en España, el benchmark de financiación se aleja del 10:1 que persiguen los fondos de Silicon Valley. El banco pide menos múltiplo y más trazabilidad. Prefiere un 3:1 auditable antes que un 6:1 contado de palabra.

## El error que frena tu solicitud

El founder medio presenta el LTV así: mi cliente gasta de media X€ al año. El analista pregunta cómo lo sabe. La respuesta suele señalar un informe de plataforma. Ahí muere la solicitud. Sin fecha de primera compra, sin cohorte y sin evolución temporal no hay nada que un departamento de riesgos pueda verificar.

:::cifra
De los 3,2M€ generados a clientes en los últimos doce meses, las operaciones que acompañamos ante banca presentaron siempre cohortes por mes de adquisición. En nuestra experiencia, una solicitud sin trazabilidad se filtra sola, da igual el ratio que muestre el Excel.
:::

## El framework PIRÁMIDE DE DATOS BANCARIOS

Cuatro niveles, de la base a la cima. Así ordenamos los números cuando acompañamos a un cliente a pedir financiación.

## Nivel 1: datos de base

Tracking server-side con CAPI activo. Sin esto, el resto del dossier es opinión. Con esto, el banco tiene el journey completo de cada cliente desde el click hasta la compra. Esta capa no se maquilla: se implementa una vez y sostiene todo lo demás. En las cuentas que gestionamos la montamos con GA4 server-side y un contenedor en Stape. El coste real está en horas de configuración, no en licencias. Y es la única capa del dossier que un analista no puede discutir.

## Nivel 2: cohortes por mes de adquisición

Agrupa a los clientes por el mes de su primera compra. Cada cohorte es una camada independiente. Calcula su revenue acumulado a 30, 60, 90 y 180 días. Con 12 meses de datos tienes 12 cohortes comparables entre sí.

## Nivel 3: ratio por cohorte

Nada de ratio global. La cohorte de enero tiene su LTV/CAC y la de junio el suyo. Presentados en serie, el banco ve tendencia y consistencia. Esas dos palabras deciden más aprobaciones que el múltiplo en sí.

## Nivel 4: proyección con contexto

Cierra con el benchmark de tu categoría, tu payback period medio y una proyección a 12 meses apoyada en las cohortes ya cerradas. Proyectar sobre cohortes reales es creíble. Proyectar sobre un promedio histórico es humo con formato.

:::pro-tip
El analista de riesgos sabe que el ROAS del píxel viene inflado desde iOS 14. Lleva las dos versiones: el ROAS de plataforma y el correlacionado con tu CRM. Explicar esa diferencia sin que te la pregunten te separa de las otras 50 solicitudes de la semana. La mecánica está en [atribución post-iOS 14](/blog/atribucion-post-ios-14-roas-mentira.html).
:::

## Las cuatro métricas que el banco lee después

Payback period. Cuántos días tardas en recuperar el CAC de cada cohorte. En nuestra experiencia, por debajo de 90 días se lee como sólido para financiación tradicional.

Tasa de recompra. Qué porcentaje de clientes vuelve a comprar. Le dice al banco que tu revenue no depende de captar sin parar.

AOV y su tendencia. Un ticket medio que sube trimestre a trimestre demuestra que sabes vender más al mismo cliente, sin gastar más en traerlo.

Retención por cohorte. Retener al 50% de una cohorte a 6 meses cuenta una historia. Retener al 30% cuenta otra. La retención decide si tu LTV proyectado es real o decorativo.

## Cuántos meses de histórico necesitas

Para una línea de crédito pequeña, 6 meses con dos o tres cohortes cerradas. Para un préstamo de crecimiento, 12 meses con trimestres consistentes. Por debajo de 6 meses, prepara proyecciones sobre el período disponible y asume que costará. En los casos que acompañamos pesa más la consistencia que el volumen: tres cohortes estables convencen más que seis erráticas. Y el histórico no se improvisa: la mejor fecha para empezar a registrarlo fue hace un año, la segunda mejor es hoy.

## El promedio que nos costó una aprobación

Presentamos una vez 18 meses de datos con un LTV medio que parecía sólido. El banco pidió la distribución y no la llevábamos montada. Al construirla apareció el problema: un segmento pequeño de clientes generaba la mayor parte del revenue y el resto quedaba lejos del promedio. El ratio efectivo no era el del Excel. Perdimos esa aprobación. Aprendimos que el banco quiere ver distribución y dispersión, y no una media que las esconda.

## Acción: tus próximos 30 minutos

Abre Shopify y exporta los pedidos de los últimos 6 meses. Añade una columna con el mes de primera compra de cada cliente. Agrupa por ese mes. Calcula el revenue acumulado de cada cohorte a 30, 60 y 90 días. Divide el LTV de cada cohorte entre el CAC medio de su mes. Mira la serie completa: ¿sube, baja o baila?

Si no puedes montarlo en 30 minutos porque los datos están dispersos, ese es el hallazgo. Antes de pedir financiación necesitas un sistema que genere este informe solo, cada mes.

:::cifra
Con 31.555 conversiones registradas con tracking server-side en las cuentas que gestionamos, el informe de cohortes se genera sin Excel manual: cada compra actualiza su cohorte y el dossier bancario sale de ahí.
:::

## En este post cubrimos

Por qué el benchmark bancario se aleja del de los VC, el framework PIRÁMIDE DE DATOS BANCARIOS con sus cuatro niveles, las métricas complementarias (payback, recompra, AOV y retención), el histórico mínimo por tipo de financiación y el promedio sin distribución que nos costó una aprobación. La mecánica de cohortes la tienes en [calcular tu LTV real por cohorte](/blog/calcular-ltv-real-cohorte.html) y la relación entre ambas métricas en [CAC vs LTV en ecommerce](/blog/cacvs-ltvecommerce.html).

En el próximo post de esta serie: cómo [recuperar el CAC en 30 días](/blog/recuperar-cac-30-dias-secuencia-ofertas-d2c.html) con una secuencia de ofertas que financia tu adquisición sin pasar por el banco.

Si tienes una petición de financiación cerca, [reserva una auditoría de 30 minutos](/contacto.html). Miramos tus números y te decimos qué documentación falta para que el banco pueda decir que sí.