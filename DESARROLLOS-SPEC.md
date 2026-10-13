# DESARROLLOS-SPEC — página de desarrollos web + 7 casos de proyecto

Patrón visual: igual que /casos/ (filas gigante McCann en el índice, narrativa 01-04 en cada proyecto, parte de caja con lo verificable). Diferencia clave: cada proyecto ENLAZA a la web viva del cliente (botón/badge "Ver la web →" con URL externa + target=_blank rel=noopener). Honestidad ante todo: donde el build no fue de DayByDay, se dice.

## Índice /desarrollos/index.html
- H1: "Desarrollos web." (serif) + sub mono: "Siete webs en producción, construidas o puestas en marcha por DaybyDay. Cada proyecto enlaza a la web viva."
- Filas gigante (estilo casos/index): logo/wordmark + NOMBRE DE PROYECTO en serif + cliente/sector en mono + badge externo "douf.es →" en mono azul.
- Orden: Douf, Cartri, Garett, Evolut Fitkid, Kueba, content.fuel, Intermex Group.
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

### 6. desarrollos/contentfuel.html · "De la ficha a la mesa." — CONTENT.FUEL (content-fuel.com) [AÑADIDO 13-OCT-2026]
- Eyebrow: PRODUCTO PROPIO · CONTENIDO PARA MARCAS PERSONALES · EN PRODUCCIÓN
- 01: "content.fuel es el servicio de dirección de contenido para marcas personales: análisis, guiones palabra por palabra, edición, calendario y posteo. El cliente pone la cara y graba; el resto lo hace el sistema. Con varios clientes dentro, eso no cabe en carpetas: necesita producto."
- 02: "Que cada cliente vea su producción y apruebe desde su panel, y que la operación avance etapa a etapa — con gates humanos donde de verdad importan: la mesa de guiones, los análisis, las propuestas."
- 03: "Portal Cloudflare Worker + D1 + R2 (panel de cliente + panel interno) + pipeline de 12 etapas (ficha → referentes → recolección → informe → forense del cliente → perfil → playbook → estrategia → redacción → plan → forense post-publicación). Runner en servidor propio: cada 5 min, una etapa (cola → LLM → hooks con clave). Publicación IG automática (n8n, 15 min), insights cada 6 h. Identidad propia: Bodoni Moda + Inter sobre esmeralda y oro viejo."
- 04 (parte de caja + GO): "Portal Worker+D1+R2 · paneles cliente+interno · 12 etapas con gates · runner 1 etapa/5 min · IG automática · en producción con clientes dentro"
- Botón externo: "Ver la web → https://content-fuel.com"

### 7. desarrollos/intermex.html · "Cifras con fuente." — INTERMEX GROUP (intermexgroup.es) [AÑADIDO 13-OCT-2026]
- Eyebrow: CLIENTE · HOLDING DE DISTRIBUCIÓN · EN PRODUCCIÓN
- 01: "Intermex Group mete marcas internacionales en España — importación, stock, tienda y logística, con ERP propio — y su web tenía que hacer lo mismo hacia fuera: convencer a marcas de fuera de que aquí hay mercado. En inglés, con datos, y sin parecer una plantilla más."
- 02: "Convertir la web en el pitch: qué hace el grupo, por qué España — con cifras reales y su fuente a la vista — y prueba que se puede clicar: las webs vivas de sus marcas."
- 03: "Identidad desde su logo oficial (azul profundo + oro, grotesca auto-hospedada). Sección 'Why Spain' con 4 gráficos SVG hechos a mano sobre series oficiales (CNMC, INE, Stanpa), cada dato con enlace a su fuente. Casos con 'ventanas' de navegador y las webs vivas dentro (Cartri, Garett, Cyramiko). 4 páginas legales en inglés, 0 dependencias, 0 trackers. Publicada en Cloudflare Pages y servida en su dominio — el registro raíz seguía aparcado y se resolvió con un Worker reverse-proxy, sin tocar el DNS."
- 04 (parte de caja + GO): "4 gráficos con fuente · CNMC/INE/Stanpa · 3 casos con web viva · 4 legales EN · 0 dependencias · en producción"
- Botón externo: "Ver la web → https://intermexgroup.es"

## HOME (index.html)
1. Anchor-stat "Desarrollos web en producción": valor ligado al número de proyectos — hoy **"7"** (data-counter="7"), envuelto en .voice-machine y en <a href="/desarrollos/">. Si se añade un proyecto nuevo, subir el número aquí Y el "Siete webs" de desarrollos/index.html y casos/index.html.
2. Marquee de clientes: imágenes monocromas (filtro brightness(0) / invert en dark) + el span "y más…". Últimas adiciones (13-oct-2026): `contentfuel.svg` (wordmark dibujado de content.fuel, asset de su branding) e `intermex.svg` (lockup autorado en serif Georgia: "Intermex / GROUP"). En las DOS copias del track + aria-label actualizado.
3. Notas de logos por contexto: en el ÍNDICE /desarrollos/ cada fila lleva su logo en la caja de 110px — content.fuel usa su marca `contentfuel-mark.svg` (monograma, color #9AA3B2 para verse en ambos temas) e Intermex la placa `intermex.png` (PNG transparente). Los SVG sueltos SIEMPRE con `xmlns` (los inline del header de content-fuel.com no lo llevan: al copiarlos hay que añadirlo o no cargan como <img>).

## Nav/cruces
- casos/index.html: al final, línea cruzada → /desarrollos/ ("¿Buscas los desarrollos web? Cinco webs en producción →").
- desarrollos/index.html: línea cruzada → /casos/.
- NO tocar el nav global (no cabe más; el índice se descubre desde home y desde casos).
