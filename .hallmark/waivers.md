# Hallmark — waives del site DaybyDay

Reglas del Floor que **no** se aplican en este proyecto, con su razón. Un waive sin razón es slop;
uno con razón es una decisión de diseño. Este fichero es la fuente de verdad para futuros barridos.

## 54 · Eyebrows (`01 — El trabajo`)

**Waived en todo el site.** El elemento `<div class="section-tag">01 — …</div>` no es un eyebrow
decorativo: es el **sistema de secciones numeradas de la marca**, fijado en `BRAND-SPEC.md` §4 y §6
("secciones numeradas donde tenga sentido: `01 — Qué hago` / `02 — Clientes` / `03 — Cómo opero`").
Hallmark lo lee como eyebrow porque sintácticamente lo parece; semánticamente es la estructura
editorial de la marca, no un adorno generado.

Cambiar el número por el heading (lo que pide la regla) rompería la navegación mental del site y
contradiría el contrato de marca, que en Hallmark tiene prioridad ("A locked design.md is the system
at every depth"; "The brand, when there is one, stays at every depth").

## 19 · Guion en copy

**Waived cuando el guion vive DENTRO de un `.section-tag`** (`01 — Paid media`). Es el separador
tipográfico del sistema de secciones. El resto de guiones del copy visible sí se eliminan (coma,
dos puntos o punto). Igual para el en-dash de rango de fechas (`2023–2026`), que en español es
tipográficamente correcto.

## R1 · Inter como display

**Waived.** `BRAND-SPEC.md` §2 fija Inter 800 para wordmark y H1 display. No es un default de
framework: es la cara de la marca, elegida y aprobada por Pablo (boards de 2026-09-15).

## 7b · Chips blancos de logos de terceros

**Waived.** El logo wall muestra marcas ajenas (Mirakl, El Corte Inglés, OneTime, ERPNext) que solo
funcionan sobre blanco neutro. Teñir el chip hacia el acento alteraría los logos de terceros, que es
peor que la regla que se salta.

## 64 · Mono en cifras

**Waived.** IBM Plex Mono es la "voz máquina" de la marca (BRAND-SPEC §2) y se usa **solo** en cifras,
métricas y labels técnicos. La regla apunta a mono usado como decoración en labels, que no es el caso.

## F54 parcial · `section-tag` en páginas nuevas

Las páginas nuevas (p. ej. `logistics.html`) pueden no usar `section-tag` si su propio diseño no lo
necesita. En ese caso el waive no aplica y la página pasa el linter limpia.
