# DayByDay Blog Pipeline

Pipeline de generación de posts SEO/GEO/AEO para [daybydayconsulting.com](https://www.daybydayconsulting.com).

- **3 posts/semana** en español
- **HTML estático limpio** (sin SPA, sin JSX, sin Tailwind)
- **Cloudflare Pages** para hosting, **Cloudflare Worker** para IndexNow + Telegram
- **MiniMax M3** como LLM (mismo modelo que este chat)
- **Topic research semanal** desde Google News (surfacing Reddit/Quora) + blogs ES
- **Internal backlinking** automático entre posts del mismo cluster
- **External authority linking** verificado por HEAD + Wayback fallback

## Quickstart

```bash
# 1. Configurar API key
export MINIMAX_API_KEY="sk-..."

# 2. Generar el siguiente post de la cola
python3 scripts/generate_post.py

# 3. Revisar el archivo en blog/<slug>.html
# 4. Si está OK:
git add blog/<slug>.html data/ && git commit -m "post: <slug>" && git push
# Cloudflare Pages auto-deploya → Worker dispara IndexNow + Telegram.
```

## Estructura

```
DaybyDayWeb-HTML/
├── blog/                          # 124+ posts (HTML estático)
│   └── capi-server-side-emq-2026-shopify.html
├── data/                          # Estado del pipeline (regenerable)
│   ├── posts.json                 # Índice maestro: 124 posts
│   ├── clusters.json              # 5 clusters temáticos
│   ├── internal-links.json        # Grafo de enlaces internos
│   ├── topic-queue.json           # Cola de topics pendientes + completados
│   ├── backlink-proposals.json    # Propuestas de reverse-links
│   └── link_check_cache.json      # Caché HEAD checks (24h TTL)
├── scripts/
│   ├── generate_post.py           # Pipeline principal 9-step
│   ├── regenerate_index.py        # Regenera blog.html, sitemap, feed, llms-full
│   ├── topic_research.py          # Scraping Google News + ES blogs (semanal)
│   ├── inject_backlinks.py        # Reverse-links entre posts del mismo cluster
│   ├── build_posts_index.py       # Reconstruye data/posts.json desde /blog/
│   ├── build_clusters.py          # Re-calcula clusters + edges
│   ├── build_topic_queue.py       # Seed manual de topics iniciales
│   ├── test_build_one_post.py     # Smoke test del template (sin API key)
│   └── lib/
│       ├── llm_client.py          # Cliente MiniMax M3 con retry + JSON parsing
│       ├── authority_link_checker.py  # HEAD verify + Wayback fallback
│       ├── post_builder.py        # Ensambla el HTML final desde el JSON del LLM
│       ├── post_template.html.j2  # Template HTML5 (clean, sin JSX, sin Tailwind)
│       └── prompts/
│           ├── 00_voice.md        # Voz DayByDay (2.6KB)
│           ├── 01_research.md     # Contrato JSON research (1.9KB)
│           ├── 02_audit.md        # Checklist Hormozi adaptado (4.3KB)
│           ├── 03_write_es.md     # Contrato JSON del artículo (5.7KB)
│           ├── 04_table_patterns.md  # Plantillas HTML de tablas (3.7KB)
│           └── 05_visual_extras.md   # Bar chart, si-no grid, steps (3.8KB)
├── workers/
│   └── daybyday-post-deploy/      # Cloudflare Worker (TypeScript)
│       ├── src/index.ts
│       ├── wrangler.toml
│       ├── package.json
│       └── README.md
├── .well-known/
│   ├── security.txt               # RFC 9116
│   └── ai-plugin.json             # OpenAI plugin manifest (ChatGPT retrieval)
├── indexnow-<key>.txt             # IndexNow key file (en root)
├── blog.html                      # Índice del blog (regenerable)
├── sitemap.xml                    # Deduplicado, con lastmod (regenerable)
├── feed.xml                       # RSS 2.0 (regenerable)
├── llms.txt                       # Manifiesto LLM (estable, +Artículos top 30)
├── llms-full.txt                  # Contenido íntegro para AI ingestion (regenerable)
├── humans.txt                     # Créditos + AI assistance disclosure
├── robots.txt                     # Friendly a GPT/Claude/Perplexity bots
├── en/                            # Páginas en inglés (estáticas, sin pipeline EN)
└── tech/                          # Páginas de stack técnico
```

## Cadencia semanal

| Día | Acción | Script |
|-----|--------|--------|
| **Lun 09:00** | Topic research | `python3 scripts/topic_research.py` |
| **Lun 11:00** | Post 1 (BOFU) | `python3 scripts/generate_post.py` |
| **Mié 11:00** | Post 2 (MOFU) | `python3 scripts/generate_post.py` |
| **Vie 11:00** | Post 3 (BOFU) | `python3 scripts/generate_post.py` |
| **Dom 22:00** | Reverse-link injection | `python3 scripts/inject_backlinks.py` |

## El pipeline de un post (9 pasos)

1. **Pick topic** — Lee `data/topic-queue.json`, toma el top-scored pendiente.
2. **Research** — MiniMax M3 call (research-only prompt) → JSON brief con keyword, h2, FAQs, internal/external link targets.
3. **Verify externals** — HEAD request a cada link externo. 404 → Wayback fallback. Drop si ambos fallan.
4. **Plan visuals** — Incluido en el prompt de write (el LLM decide qué tabla, ranking, blockquote).
5. **Write** — MiniMax M3 call con prompt maestro → JSON del artículo.
6. **Audit** — MiniMax M3 call con checklist Hormozi adaptado. Score < 22 → loop con feedback, máx 2 retries.
7. **Schema** — JSON-LD local: `Article` + `FAQPage` + `BreadcrumbList` + `Person`.
8. **Assemble** — `post_builder.py` rellena el template y produce el HTML final.
9. **Persist** — Escribe `blog/<slug>.html`, actualiza `data/posts.json`, `data/topic-queue.json`. Regenera `blog.html`, `sitemap.xml`, `feed.xml`, `llms-full.txt`, `llms.txt`.

## SEO/GEO/AEO/AVO por post

Cada post nuevo incluye automáticamente:

- ✅ `<title>` y `<meta description>` con keyword
- ✅ `<link rel="canonical">` absoluto
- ✅ `<link rel="alternate" type="application/rss+xml" href="/feed.xml">`
- ✅ Open Graph + Twitter Card
- ✅ 4 JSON-LD blocks: Article, FAQPage, BreadcrumbList, Person
- ✅ `SpeakableSpecification` (data-speakable="true") en abstract, takeaways y FAQs
- ✅ 5-7 FAQs con respuestas 1-2 frases (PAA, featured snippets)
- ✅ 1+ tabla HTML con datos concretos
- ✅ 1+ lista numerada (`<ol class="steps">` o `<ol>` ranking)
- ✅ 1+ blockquote con tesis contraintuitiva
- ✅ 1+ sección "Cuándo NO" (sección obligatoria)
- ✅ 2-4 enlaces internos a posts del mismo cluster
- ✅ 2-4 enlaces externos a dominios de autoridad (Meta, Google, IAB, HBR, etc.)
- ✅ Schema Organization + Person en root index (existente)

## Backlinking interno

El grafo `data/internal-links.json` tiene **231 edges** seed entre los 123 posts originales,
agrupados por 5 clusters. Cada post nuevo hereda automáticamente:

- **2-4 outbound links** a posts del mismo cluster (research prompt los elige).
- **1 link** a una página de servicio (`/meta-ads.html`, etc.).
- **1 link** a una página de stack técnico (`/tech/capi.html`).
- **1 link** a la CTA (`/contacto.html`).

`scripts/inject_backlinks.py` corre semanalmente y propone **reverse-links**:
para cada post nuevo de los últimos 14 días, identifica los 3 posts más relevantes
del mismo cluster y pide al LLM una frase exacta donde inyectar `<a>Lee también: …</a>`.
Las propuestas quedan en `data/backlink-proposals.json` para revisión humana antes de aplicar.

## IndexNow + Cloudflare

`workers/daybyday-post-deploy/src/index.ts` se despliega como Cloudflare Worker:

1. **Webhook de Pages deploy** → diff sitemap, submit nuevos a IndexNow, notify Telegram.
2. **Cron Dom 06:00 UTC** → re-ping IndexNow con top 50 URLs recientes.
3. **Cron Dom 07:30 UTC** → check sitemap freshness, report por Telegram.

Setup detallado en `workers/daybyday-post-deploy/README.md`.

## Comandos útiles

```bash
# Reconstruir índices desde /blog/ (idempotente)
python3 scripts/build_posts_index.py
python3 scripts/build_clusters.py
python3 scripts/regenerate_index.py

# Refrescar cola de topics (semanal)
python3 scripts/topic_research.py            # ~30-60s, ~40 candidates

# Generar un post (requiere MINIMAX_API_KEY)
python3 scripts/generate_post.py             # siguiente de la cola
python3 scripts/generate_post.py --topic T100  # topic específico
python3 scripts/generate_post.py --dry-run  # escribe a .dry-run-post.html
python3 scripts/generate_post.py --skip-audit --auto-accept  # iterar prompts rápido

# Backlinks
python3 scripts/inject_backlinks.py         # propone reverse-links
python3 scripts/inject_backlinks.py --apply # los aplica

# Verificar enlaces externos (rápido)
python3 scripts/lib/authority_link_checker.py https://example.com https://...
```

## Variables de entorno

| Variable | Descripción | Dónde |
|----------|-------------|-------|
| `MINIMAX_API_KEY` | API key de MiniMax M3 | Local: `~/.zshrc` |
| `MINIMAX_MODEL` | Modelo a usar (default: `MiniMax-M3`) | opcional |
| `MINIMAX_API_BASE` | API base (default: `https://api.minimax.io/v1`) | opcional |
| `INDEXNOW_KEY` | 32-char hex de indexnow.org | CF Worker secret |
| `TELEGRAM_BOT_TOKEN` | Token del bot | CF Worker secret |
| `TELEGRAM_CHAT_ID` | Chat id numérico | CF Worker secret |

## Cómo añadir un topic manualmente

Edita `data/topic-queue.json` y añade a `pending_tasks`:

```json
{
  "id": "T999",
  "topic": "CAPI server-side y EMQ en 2026: ...",
  "cluster": "attribution-tracking",
  "search_intent": "transactional",
  "rationale": "Por qué este post (1 frase).",
  "source": "manual",
  "score": 90,
  "slug": "capi-server-side-emq-2026-shopify",
  "discovered_at": "2026-06-06T10:00:00Z",
  "status": "pending"
}
```

El slug se autogenera del topic si no lo pones. Score entre 70-100 (más alto = más prioritario).

## Troubleshooting

**"Empty response from model"** — el prompt pasó de 16KB. Cada call compone 2-4 prompts modulares; reduce el número si pasa. El `llm_client.py` reintenta 3 veces automáticamente.

**"JSON parse failed"** — el LLM devolvió markdown o texto extra. `parse_json_relaxed()` intenta arreglar trailing commas. Si sigue fallando, baja `temperature` a 0.2 o refuerza el prompt.

**"Topic already in posts"** — `is_duplicate()` bloquea. Para forzar, edita manualmente y borra el slug de `data/posts.json` antes de regenerar.

**"No JSON-LD" en el output** — verifica que el template no esté roto. `python3 scripts/test_build_one_post.py` valida 15 puntos.

**"403 desde Reddit"** — Reddit bloquea el scraper directo. Por eso `topic_research.py` usa Google News con `site:reddit.com`.

## Cosas que NO hace este pipeline (intencional)

- ❌ Posts en inglés (`en/blog/` queda congelado; decisión de scope).
- ❌ Imágenes raster / OG images / hero graphics (decisión de scope).
- ❌ Comments, likes, social embeds (cero surface de spam).
- ❌ Generative AI para creatividades publicitarias (otro vertical).
- ❌ RSS de comentarios (no hay comments).
- ❌ A/B testing automático del contenido (A/B se hace en prompt hatching, fuera de scope).
- ❌ Imágenes en `llms-full.txt` (texto plano por definición).

## Próximos pasos

1. **Set `MINIMAX_API_KEY`** en `~/.zshrc`.
2. **Probar el pipeline real** con el topic #1 de la cola:
   ```bash
   python3 scripts/generate_post.py --topic T100 --dry-run  # preview
   python3 scripts/generate_post.py --topic T100            # real
   ```
3. **Setup del Worker** siguiendo `workers/daybyday-post-deploy/README.md`.
4. **Crear bot de Telegram** con @BotFather.
5. **Generar los 3 primeros posts de la semana** y revisar.
6. **Programar el semanal** topic_research (lunes 09:00) y inject_backlinks (domingo 22:00).
