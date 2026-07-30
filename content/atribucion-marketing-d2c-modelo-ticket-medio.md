---
title: "Atribución D2C: qué modelo usar según tu ticket medio"
h1: "Atribución marketing D2C: qué modelo usar según ticket medio y ciclo de venta"
slug: "atribucion-marketing-d2c-modelo-ticket-medio"
meta_desc: "Qué modelo de atribución necesita tu D2C según tu ticket medio y tu ciclo de venta. Framework práctico para dejar de decidir sobre datos falsos."
canonical: "https://www.daybydayconsulting.com/blog/atribucion-marketing-d2c-modelo-ticket-medio"
category: "Growth & Marketing"
article_date: "2026-07-30"
reading_time: 7
published_at: "2026-07-30T10:00:00+02:00"
primary_keyword: "atribución marketing D2C"
secondary_keywords: ["modelo atribución ecommerce", "last click vs data-driven", "ticket medio", "atribución cross-channel", "GA4 atribución"]
faq: [{"q": "¿Qué modelo de atribución necesito para mi tienda online?", "a": "Depende de tu ticket medio y ciclo de venta. Con ticket menor a 150€ y ciclo menor a 7 días, Linear o Data-Driven de GA4. Entre 150 y 500€, Position Based. Ticket mayor a 500€ o ciclo mayor a 30 días pide MMM o atribución desde CRM."}, {"q": "¿Por qué mi ROAS de Meta no coincide con mi crecimiento real?", "a": "Last-click infla la búsqueda de marca y canibaliza el presupuesto de descubrimiento. Sin server-side, GA4 reporta como tráfico directo una parte del tráfico que llegó desde campañas. El ROAS reportado mide crédito, no incremento real."}, {"q": "¿Necesito un data warehouse para mejorar mi atribución?", "a": "No. Server-side de GA4 más Conversions API de Meta, Google y TikTok cubre la mayor parte del problema de tracking en D2C. El data warehouse es opcional y tiene sentido si facturas más de 2M€ y tienes equipo de datos."}, {"q": "¿TikTok convierte de verdad o solo genera awareness?", "a": "Su contribución se pierde en modelos de último clic porque buena parte del efecto llega días después y sin clic. Activa la ventana view-through de 1 a 7 días y mide la conversión posterior antes de decidir que no funciona."}, {"q": "¿Cómo convenzo a mi CFO de cambiar el modelo de atribución?", "a": "Con el reporte dual: ROAS de atribución, que ya conoce, junto a contribución real por canal. Y con un geo-holdout de 4 a 6 semanas que compare lo reportado con el incremento medido."}]
sources: [{"label": "Meta Conversions API", "url": "https://developers.facebook.com/docs/marketing-api/conversions-api/"}, {"label": "TikTok Ads Help Center", "url": "https://ads.tiktok.com/help/"}, {"label": "Google Search Central", "url": "https://developers.google.com/search/docs"}]
internal_links: [{"url": "/blog/atribucion-post-ios-14-roas-mentira.html", "anchor": "atribución post-iOS 14"}, {"url": "/blog/roas-3x-perdida-dinero-d2c.html", "anchor": "ROAS de 3x puede ser una pérdida de dinero"}, {"url": "/blog/cuanto-gastar-meta-ads-visibilidad-caja.html", "anchor": "cuánto gastar en Meta según tu visibilidad de caja"}, {"url": "/blog/calcular-ltv-real-cohorte.html", "anchor": "calcular tu LTV real por cohorte"}]
cta_title: "Auditoría de atribución de 30 minutos"
cta_desc: "Vemos qué modelo usas, cuánto hueco hay entre tu ROAS reportado y tu realidad, y qué cambiar primero."
cta_href: "/contacto.html"
cta_label: "Reservar auditoría gratuita"
llms_summary: "Framework de atribución para D2C según ticket medio y ciclo de venta. Incluye la pirámide de 3 capas, el árbol de decisión por ticket y el stack server-side mínimo viable."
tags: ["atribución", "D2C", "GA4", "meta ads", "tiktok ads", "ecommerce"]
migration_state: "good"
---

> «El trimestre pasado movimos el 40% del presupuesto a Google Shopping porque marcaba 6x. Después de migrar a server-side, Shopping tenía 2,1x. Habíamos vaciado los canales que traían clientes nuevos.»

Nos pasó a nosotros, gestionando una cuenta propia. Y explica por qué existe este framework.

El patrón se repite en casi todas las cuentas que auditamos. El panel dice Meta 2,5x, Shopping 6x, TikTok 0,8x. La decisión parece obvia: subir Shopping, bajar Meta, apagar TikTok. Al trimestre siguiente las ventas caen. No porque Meta sea mejor ni TikTok peor, sino porque el modelo de atribución roba crédito a los canales que traen clientes nuevos y se lo entrega a los que cierran la venta.

El arreglo no es cambiar de modelo mañana. Es entender qué mide cada uno y elegir según tu ticket medio y tu ciclo de venta.

## Lo que vas a aprender

1. Por qué el último clic infla la búsqueda de marca y te vacía el presupuesto de descubrimiento
2. El framework PIRÁMIDE D2C y sus tres capas
3. Qué modelo te toca según ticket medio y duración del ciclo
4. El stack server-side que puedes montar esta semana sin tocar el modelo
5. El reporte dual para que tu director financiero entre en la conversación

## Tu ROAS miente y el culpable no es el modelo

Buena parte del problema de atribución no está en el modelo. Está en el tracking.

Sin server-side, GA4 registra como directo un volumen alto de tráfico que no lo es. Alguien llega desde un post de Instagram, un email de Klaviyo o un anuncio de TikTok, su navegador bloquea el pixel y GA4 lo apunta como visita directa. O ve el anuncio en el móvil y compra por la tarde en el ordenador, donde ya tenía tu web abierta. Venta directa, según el panel.

Estuvimos seis meses en una cuenta de moda con el pixel sin CAPI activo. Cada compra desde Safari móvil aparecía como directa, Meta marcaba 1,8x y recortamos presupuesto por eso. Las ventas cayeron después. Es el patrón post-iOS 14 que seguimos viendo hoy en casi todas las auditorías, y lo desmenuzamos en [atribución post-iOS 14](/blog/atribucion-post-ios-14-roas-mentira.html).

Antes de discutir modelos, asegúrate de que tus eventos llegan limpios. Si no, cualquier modelo que elijas trabajará sobre datos inventados.

## El framework PIRÁMIDE D2C

Tres capas. Si falla una, las de arriba dejan de importar.

**1. Capa de tracking.**

GA4 server-side vía Stape con alojamiento en la UE. Eventos de ecommerce (purchase, addToCart, viewItem) enviados desde servidor. Conversions API de Meta, Google y TikTok activas. Sin esto, el resto es decoración.

**2. Capa de modelo.**

Elegir entre lineal, basado en posición, data-driven o MMM según ticket medio y ciclo de venta. El árbol de decisión está justo debajo.

**3. Capa de lectura.**

El ROAS reportado no es incremento. Un canal puede marcar mal en atribución y ser imprescindible para tus ventas. Saber leer esa diferencia es lo que evita decisiones destructivas.

:::cifra
Con 31.555 conversiones gestionadas, el modelo data-driven de GA4 empieza a ser fiable a partir de unas 500 conversiones mensuales por canal. Por debajo de ahí no hay señal suficiente y el modelo inventa.
:::

## Qué modelo te toca según tu ticket medio

La pregunta útil no es cuál es el mejor modelo, sino cuál tiene sentido para tu negocio.

Con ticket por debajo de 150€ y ciclo de menos de 7 días, ve a lineal o data-driven de GA4. Las decisiones son rápidas, el volumen alcanza para que el modelo aprenda y no necesitas complicarte con reparto por posición. Activa data-driven si superas las 500 conversiones mensuales en ese canal.

Entre 150 y 500€ de ticket, basado en posición. Reconoce que el descubrimiento importa y que el cierre también. Lo usamos con una marca de belleza que empezó a ver la contribución real de la parte alta del embudo y reasignó presupuesto hacia canales que antes parecían inútiles.

Por encima de 500€ de ticket, o con ciclos de más de 30 días, MMM o atribución desde el CRM con Klaviyo. GA4 pierde buena parte de las conversiones asistidas cuando el ciclo se alarga, y con producto de ticket alto infravalora de forma sistemática los canales de consideración.

Una señal de alarma sencilla: si tu búsqueda de marca concentra más del 30% de las conversiones, tienes un problema de distorsión. Esa marca ya estaba en la cabeza del cliente cuando buscó, y alguien la puso ahí antes.

## El stack server-side mínimo viable

No necesitas un data warehouse ni modelos probabilísticos. Necesitas server-side y Conversions API, y se monta en dos o tres semanas.

GTM server-side en Stape, eventos de ecommerce por servidor, CAPI de Meta activo, Enhanced Conversions de Google activo y Klaviyo conectado para el reparto de crédito.

Una marca de moda pasó de pixel sin CAPI a este stack completo en seis semanas. Su tráfico directo reportado bajó porque Meta empezó a recoger ventas que antes se perdían por el camino. Con 264.712€ de ad spend gestionado, es el resultado que esperamos cada vez que lo implementamos.

:::pro-tip
Activa la ventana view-through de TikTok (1 día de vista, 7 de clic) y crea en GA4 un segmento de gente que vio sin hacer clic. Mide su conversión a 7 y 14 días. Cuando recortes presupuesto en TikTok, vigila las ventas de las semanas 3 y 4: ahí aparece la correlación que el último clic no puede enseñarte.
:::

## El reporte dual para tu director financiero

Tu CFO entiende el ROAS de último clic. No se lo quites, añade una capa al lado.

El primer reporte es el de siempre, ROAS por atribución, útil para optimizar pujas dentro de cada canal. El segundo reparte el crédito según la contribución real al ciclo de venta, y es el que enseña que la búsqueda de marca es en parte asistencia y que TikTok trabaja aunque no cierre dentro de su ventana de clic.

Si necesitas prueba dura, corre un geo-holdout: aparta el 10-15% de tu mercado sin anuncios de Meta durante 4 a 6 semanas y compara lo reportado con el incremento real. La diferencia es exactamente el crédito que tu modelo se está inventando.

## Acción: tus próximos 30 minutos

Abre GA4 y ve a Adquisición, Adquisición de tráfico. Filtra por grupo de canales predeterminado y mira qué porcentaje cae en Direct. Si pasa del 30%, tu problema es de tracking, no de modelo.

Copia ese número y llévalo a tu próxima reunión con quien gestione tu marketing. Es la primera conversación honesta que vais a tener sobre atribución.

## En este post cubrimos

Por qué el tracking roto explica más que el modelo elegido, el framework PIRÁMIDE D2C con sus tres capas, qué modelo corresponde a cada ticket medio y ciclo, el stack server-side mínimo y el reporte dual para dirección financiera. Si lo que quieres saber es cuánto puedes invertir sin ahogar la caja, sigue por [cuánto gastar en Meta según tu visibilidad de caja](/blog/cuanto-gastar-meta-ads-visibilidad-caja.html); si el problema es que tu retorno no cuadra con el banco, mira por qué un [ROAS de 3x puede ser una pérdida de dinero](/blog/roas-3x-perdida-dinero-d2c.html).

En el próximo post de esta serie: cómo auditar tu propio setup de tracking en cinco pasos y sin herramientas de pago.
