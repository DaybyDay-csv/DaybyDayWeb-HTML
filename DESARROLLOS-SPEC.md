# DESARROLLOS-SPEC — página de desarrollos web + 5 casos de proyecto

Patrón visual: igual que /casos/ (filas gigante McCann en el índice, narrativa 01-04 en cada proyecto, parte de caja con lo verificable). Diferencia clave: cada proyecto ENLAZA a la web viva del cliente (botón/badge "Ver la web →" con URL externa + target=_blank rel=noopener). Honestidad ante todo: donde el build no fue de DaybyDay, se dice.

## Índice /desarrollos/index.html
- H1: "Desarrollos web." (serif) + sub mono: "Cinco webs en producción, construidas o puestas en marcha por DaybyDay. Cada proyecto enlaza a la web viva."
- Filas gigante (estilo casos/index): logo/wordmark + NOMBRE DE PROYECTO en serif + cliente/sector en mono + badge externo "douf.es →" en mono azul.
- Orden: Douf, Cartri, Garett, Evolut Fitkid, Kueba.
- Al final: línea cruzada: "¿Buscas los casos de growth? → /casos/"

## Los 5 proyectos (copy listo)

### 1. desarrollos/douf.html · "13,5 GB a 28 megas." — DOUF (douf.es)
- Eyebrow: MARCA PROPIA · STREETWEAR · EN PRODUCCIÓN
- 01 La situación: "Douf es mi marca de streetwear. Antes de la web: 3.328 archivos y 13,5 GB de assets en iCloud — 2.947 imágenes sin organizar, 70 vídeos, 506 placeholders ilegibles. Y cero tienda."
- 02 El objetivo: "Auditar todo, decidir con benchmarks en vivo (Balenciaga, Moncler, Rhude, EME Studios…) y publicar una tienda que costara cero euros al mes en mantener."
- 03 Qué construimos: "Inventario foto a foto (inventory.jsonl) → tabla maestra de 30 productos con precio cerrado → tienda HTML/CSS/JS vanilla: cero frameworks, cero dependencias. 41 fichas de producto estáticas generadas desde un único products.js. Hero con vídeo dual recortado con ffmpeg. Lookbook de 88 fotos. Pipeline de imágenes WebP (ninguna pasa de 350 KB). El checkout, estilo Moncler: formulario precargado con producto y talla — la venta se cierra hablando."
- 04 El resultado (parte de caja + GO): "Web completa · 28 MB (de 13,5 GB de assets) · 41 fichas · CSS 24 KB · JS 40 KB · infra 0 €/mes" + "En producción en Cloudflare Pages: douf.es"
- Botón externo: "Ver la web → https://douf.es"

### 2. desarrollos/cartri.html · "Una campaña, 23 commits." — CARTRI (cartri.com)
- Eyebrow: CLIENTE · FABRICANTE DE PÁDEL · TEMA SHOPIFY EN PRODUCCIÓN
- 01: "Fabricante de pádel con 20 años y venta en 22 países, lanzando su campaña de renovación de almacén sobre Shopify Basic. El tema por defecto no sostenía la campaña: faltaba configurador, regalo por umbral y un carrito que vendiera."
- 02: "Montar la mecánica completa de la campaña sobre el tema, con deploy automático por Git — sin tocar el admin a mano jamás."
- 03: "Tema Shopify conectado a GitHub: cada push, deploy. Configurador de packs multi-paso con filtro por disciplina (pádel / beach tennis / pickleball). Regalo por umbral de 140 € que se añade solo al carrito y es reversible. Cart drawer con quick-add, trust bar y carril 'podría gustarte'. Motor de recomendaciones 'completa tu equipo'. Iconografía SVG propia — cero emojis. SEO de portada y colección reescritos. 23 commits en 10 días."
- 04 (honesto): "El tema está en producción vía deploys automáticos. Hoy el dominio presenta la nueva etapa de Cartri ('próximamente') mientras la tienda espera en Shopify — el siguiente paso es del cliente." + parte de caja con las mecánicas: "Configurador multi-paso · Regalo 140 € auto · Cart drawer + quick-add · 23 commits · 10 días"

### 3. desarrollos/garett.html · "De Lovable a vender." — GARETT (garettespana.es)
- Eyebrow: CLIENTE · ECOMMERCE BEAUTY-TECH · EN PRODUCCIÓN Y VENDIENDO
- 01: "Una web nacida en un builder con 943 commits de historia encima. El Shopify anterior, muerto por un impago. Y la venta parada: sin checkout."
- 02: "Migrar, reconstruir y encender la venta — con el catálogo rescatado desde cero."
- 03: "Exportación a GitHub + Cloudflare Pages. Catálogo local reconstruido: 23 productos, 99 fotos renombradas a mano. Stripe Checkout en vivo con webhook que avisa de cada pedido por email. Rebrand de 24 tickets con benchmark (FOREO, Medicube, CurrentBody): tokens navy, home cuantitativa, PDP rebuild. Matriz de recomendaciones de 21 reglas. Búsqueda por intención. Pase apple-design: springs iOS y skeletons, sin añadir un KB de JS."
- 04 (parte de caja + GO): "23 productos con precio · Stripe live · 99 fotos · matriz de 21 reglas · entidad GARETT Sp. z o.o. desplegada" + "En producción y vendiendo: garettespaña.es"

### 4. desarrollos/evolutfitkid.html · "El proyecto que no podía esperar un presupuesto." — EVOLUT FITKID (evolutfitkid.com)
- Eyebrow: PRO BONO · ESCUELA DEPORTIVA INFANTIL · EN PRODUCCIÓN
- 01: "Una escuela de FitKid en Madrid que capta por boca-oreja y flyers. Sin web. Sin presupuesto de agencia — por eso fue pro bono."
- 02: "Discovery completo y una one-page que convierta visita en prueba: KPIs pactados de 40-60 leads al mes."
- 03: "Sesión de descubrimiento, arquitectura de la página (hero, método, entrenadora, horarios, packs, WhatsApp directo) y acompañamiento de la puesta en marcha hasta producción."
- 04 (honesto): "evolutfitkid.com en producción. La web vive en un builder moderno; la estructura, los textos y la puesta en marcha salieron de este discovery. Próximo paso técnico: el dominio raíz sin www aún no responde — hay que terminar de apuntarlo."
- Botón externo: "Ver la web → https://www.evolutfitkid.com"

### 5. desarrollos/kueba.html · "La cocina antes del código." — KUEBA (kuebakitchen.com)
- Eyebrow: FAVOR DE CASA · RESTAURACIÓN Y CATERING · EN PRODUCCIÓN
- 01: "Un chef amigo con catering, chef privado y clases — y cero presencia digital organizada. La sesión de descubrimiento duró lo que dura cenar bien: qué eres, qué no eres, a quién cocinas."
- 02: "Una arquitectura de contenidos que hiciera el negocio entendible en una página: servicios, precios como opciones, y la 'Firma Heredero' como ritual de marca."
- 03: "Transcripción del discovery, sitemap de 5 secciones, home en 6 bloques con precios transparentes (40/45/50 €), formularios por tipo de servicio y la separación entre lo profesional (protagonista) y lo académico (zona secundaria)."
- 04 (honesto): "kuebakitchen.com en producción. La estrategia y la estructura son de este discovery; el build final lo llevó el chef con su herramienta. Y así está bien: el caso demuestra que una sesión de discovery bien hecha ordena hasta lo que no construyes tú."
- Botón externo: "Ver la web → https://www.kuebakitchen.com"

## HOME (index.html)
1. En la sección "01 — 12 meses de operación": añadir un CUARTO anchor-stat igual que los existentes: valor "5" (con data-counter="5"), label "Desarrollos web en producción", envuelto en .voice-machine, link (envolver el anchor-stat en <a href="/desarrollos/">, mismo estilo).
2. Marquee: añadir 2 wordmarks nuevas antes de "y más…": <span class="cl lg-evolut">Evolut Fitkid</span> (serif itálica como lvp) y <span class="cl lg-kueba">Kueba Kitchen</span> (serif 600). En las DOS copias del track. Actualizar el aria-label del contenedor para incluirlas.

## Nav/cruces
- casos/index.html: al final, línea cruzada → /desarrollos/ ("¿Buscas los desarrollos web? Cinco webs en producción →").
- desarrollos/index.html: línea cruzada → /casos/.
- NO tocar el nav global (no cabe más; el índice se descubre desde home y desde casos).
