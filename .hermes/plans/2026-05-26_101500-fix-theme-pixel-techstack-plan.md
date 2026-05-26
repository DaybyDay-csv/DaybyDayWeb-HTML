# Plan: Fix Theme, Founders Pixel Grid, Tech Stack Pages

## Goal
Corregir theme toggle, añadir pixel grid en founders, y crear páginas separadas para cada herramienta del stack tecnológico.

## Contexto Actual
- Repo: `/root/projects/DaybyDay-HTML/`
- Live: https://daybydayweb-html.pages.dev
- 6 service pages creadas: meta-ads, google-ads, automatizacion, analytics, growth-strategy, agentic-ai
- Stack actual en homepage: grid básico sin descripciones

## Issues a Resolver

### 1. Theme Toggle no funciona correctamente
- Estado actual: click toggles pero CSS variables no cambian
- Problema: CSS externo (/css/theme.css) puede no cargarse, o JS no actualiza variables

### 2. Pixel Grid en Founders
- Estado actual: skills-grid existe pero posición incorrecta
- Necesita: mover a sección founders, con descripción de cada tool

### 3. Tech Stack sin páginas dedicadas
- Estado actual: solo grid con nombres
- Necesita: 12 páginas individuales explicando cada tool

## Propuesta de Implementación

### Step 1: Fix Theme Toggle
```javascript
// Verificar que main.js ejecuta correctamente
// Verificar que theme.css carga
// Posible fix: inline critical CSS o verificar CDN paths
```

### Step 2: Pixel Grid en Founders
Localizar sección founders en index.html:
- Añadir `.skills-grid` con 12 habilidades de cada founder
- Descripción de cada tool en tooltip/hover

### Step 3: Tech Stack Pages (12 páginas)
Lista de herramientas a documentar:

| Tool | Página | Descripción |
|------|--------|-------------|
| Meta Ads | `/tech/meta-ads.html` | Advertising platform |
| Google Ads | `/tech/google-ads.html` | Search + Display |
| GA4 | `/tech/ga4.html` | Analytics |
| GTM | `/tech/gtm.html` | Tag Manager |
| Shopify | `/tech/shopify.html` | eCommerce platform |
| n8n | `/tech/n8n.html` | Automation |
| Azure | `/tech/azure.html` | Cloud + AI |
| CAPI | `/tech/capi.html` | Conversions API |
| GSC | `/tech/gsc.html` | Search Console |
| TikTok Ads | `/tech/tiktok-ads.html` | Video ads |
| LinkedIn Ads | `/tech/linkedin-ads.html` | B2B ads |
| DSP | `/tech/dsp.html` | Programmatic |

## Archivos a Modificar

| Archivo | Acción |
|---------|--------|
| `index.html` | Mover skills-grid a founders + fix navigation |
| `css/theme.css` | Verificar/corregir CSS |
| `js/main.js` | Verificar theme toggle logic |
| `/tech/*.html` | Crear 12 páginas nuevas |

## Tests / Validación

```
- [ ] Theme toggle cambia correctamente background
- [ ] Pixel grid visible en founders
- [ ] 12 páginas de tech stack accesibles
- [ ] each page tiene descripción + use cases
```

## Riesgos
- Tema claro puede afectar altri components
- Demasiadas páginas = maintenance cost

## Preguntas Abiertas
1. Preferred depth para cada tech page? (500-1000 palabras)
2. Incluir pricing estimates per tool?