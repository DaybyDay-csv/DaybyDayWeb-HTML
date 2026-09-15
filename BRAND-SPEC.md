# DaybyDay — SPEC de implementación del rebranding (web)

Fuente de verdad: `negocio/identidad-marca/CONCEPTO-imagen-de-marca.md` (proyecto daybyday) + boards aprobados por Pablo 2026-09-15. Esta spec es el contrato para TODAS las páginas. Leyes: no se cambian claims ni cifras (las del copy vigente mandan), se respeta el modo oscuro (light = papel es el primario), español salvo el H1 del hero, cero dependencias externas nuevas (Google Fonts ya en uso está permitido).

## 1. Paleta (tokens en css/theme.css, light primario)
- `--paper: #FAF8F3` (fondo claro — ya existía, renombrar/asegurar) · `--ink: #14131A` (texto/negro tinta) · `--ink-blue: #3B82F6` (acento/acción) · `--flag-red: #EF4444` (SOLO red flags / alertas honestas) · `--go-green: #10B981` (SOLO sello Go/No-Go). Regla: rojo y verde nunca decoran.
- Dark mode: mismos roles con su fondo oscuro existente; post-its y papel se mantienen claros (es papel físico).

## 2. Tipografía — dos voces
- **Wordmark y H1 display**: Inter 800 (ya cargada) — "DaybyDay" como en el board.
- **Voz humana** (títulos de sección h2, frases de decisión, tagline): **Source Serif 4** (Google Fonts, 400/600) → clase `.voice-human`.
- **Voz máquina** (todos los NÚMEROS y datos: cifras, métricas, fechas, labels técnicos): **IBM Plex Mono** (Google Fonts, 400/500) → clase `.voice-machine` + `font-variant-numeric: tabular-nums`.
- **Notas a mano**: Caveat (ya cargada) → `.hand-note`.
- URL Google Fonts para todas las páginas: `family=Inter:wght@300;400;500;600;700;800;900&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=IBM+Plex+Mono:wght@400;500&family=Caveat:wght@400;600&display=swap`

## 3. Logo (assets nuevos — usar SIEMPRE estos)
- `/img/brand/loop-symbol.svg` (tinta, para light) · `/img/brand/loop-symbol-blue.svg` (azul, para dark nav) — `<img src="..." width="34" height="34" alt="">` junto al wordmark "DaybyDay" (Inter 800, lowercase D mayúscula solo la primera).
- En el nav: logo + "DaybyDay" + tagline mini opcional "El crecimiento, día a día." en `.voice-human` itálica pequeña (solo home, junto al wordmark).
- Footer: logo + "DaybyDay Consulting · Madrid" + la tagline.

## 4. Componentes del sistema (clases ya existentes + nuevas)
- `.section-tag` — eyebrow numerado estilo board: `01 — Qué hago` en mono uppercase con línea debajo (`border-bottom: 1px solid var(--ink)`, display inline-block, padding-bottom 4px). Sustituye a `.plain-eyebrow` donde se aplique.
- `.h2-serif` — h2 de sección en Source Serif 4 600, tamaño generoso.
- `.paper-grid` — fondo cuadriculado (líneas 1px rgba ink al 8%, celda 22px) SOLO bajo bloques con datos (métricas, casos, parte de caja). Implementación: background-image linear-gradients.
- `.parte-caja` — ticket: fondo #fff (dark: #1a1922), borde dashed 1px ink al 25%, padding generoso, header en mono uppercase letter-spacing, filas de datos mono con puntos de guía, esquinas dentadas simuladas con `background: repeating-linear-gradient` top/bottom o clip-path zigzag opcional.
- `.stamp` — sello: mono 700 uppercase, border 2.5px solid, padding 2px 10px, rotate(-4deg), color/border según variante: `.stamp-go` verde, `.stamp-nogo` rojo. Nunca animados.
- `.btn-sketch`, `.sketch-hover .sketch-circle`, `.post-it`, `.hand-note` — YA IMPLEMENTADOS en pages.css (capa papel): reutilizar, no duplicar.
- `.hero-display` — H1 del hero en Inter 800 tamaño display (clamp 2.6rem→4.2rem), tracking -0.02em.

## 5. Contenido (cambios de copy PERMITIDOS en este rebranding — nada más)
1. **Hero home**: H1 → `Growth is a daily craft.` (`.hero-display`, en inglés, decisión de Pablo). Debajo, en `.voice-human` itálica: `El crecimiento, día a día.` El sub y lead actuales se quedan (voz de siempre).
2. Tagline del footer: `El crecimiento, día a día.` (serif itálica).
3. Meta title de la home puede añadir la tagline: "DaybyDay Consulting — Growth is a daily craft".
4. PROHIBIDO: inventar claims, cifras, clientes o promesas nuevas. Los textos existentes solo se re-vesten tipográficamente y reestructuran en secciones numeradas.

## 6. Layout / actitud
- Mucho white space, líneas separadoras horizontales finas estilo board (`border-top: 1px solid color-mix(in srgb, var(--ink) 18%, transparent)`).
- Secciones numeradas donde tenga sentido (home, páginas core): `01 — Qué hago` / `02 — Clientes` / `03 — Cómo opero`…
- El nav mantiene su estructura y comportamiento (no tocar main.js ni la mecánica del menú): solo cambia el logo, el wordmark y las fuentes del propio nav.
- Reduced-motion y accesibilidad existentes: intactos.
