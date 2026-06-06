# 05_visual_extras.md — optional inline visual patterns
# Used in step 5 of generate_post.py. ~1KB.

A veces una tabla no basta. Estos patrones visuales son HTML/CSS puro, sin imágenes, sin JS, sin SVG inline (lo que el usuario quiere es "tables, rankings, graphics" — todo en HTML).

## Gráfico de barras horizontal (CSS puro, sin imágenes)

Para mostrar benchmarks, progreso, distribución. Usa este patrón:

```html
<div class="bar-chart">
  <div class="bar-row">
    <span class="bar-label">Moda D2C</span>
    <span class="bar-track"><span class="bar-fill" style="width:76%"></span></span>
    <span class="bar-value">3,8x</span>
  </div>
  <div class="bar-row">
    <span class="bar-label">Belleza</span>
    <span class="bar-track"><span class="bar-fill" style="width:84%"></span></span>
    <span class="bar-value">4,2x</span>
  </div>
  <!-- más filas -->
</div>
```

CSS que necesitas añadir en el `<style>` inline del post:
```css
.bar-chart { display:flex; flex-direction:column; gap:0.5rem; margin:1.5rem 0; }
.bar-row { display:grid; grid-template-columns: 140px 1fr 80px; gap:0.75rem; align-items:center; }
.bar-label { color:var(--text-secondary); font-size:0.9rem; }
.bar-track { background:var(--bg-elevated); border-radius:4px; height:14px; overflow:hidden; }
.bar-fill { display:block; height:100%; background:linear-gradient(90deg, #6366f1, #8b5cf6); }
.bar-value { color:var(--text-primary); font-weight:600; font-size:0.9rem; text-align:right; }
```

## "Cuándo SÍ / Cuándo NO" (split visual)

```html
<div class="si-no-grid">
  <div class="si-card">
    <h3>✓ Cuándo SÍ</h3>
    <ul>
      <li>Cuenta con +30 días de histórico</li>
      <li>EMQ &gt; 7 en eventos de purchase</li>
      <li>Ticket medio &gt; 30€</li>
    </ul>
  </div>
  <div class="si-card">
    <h3>✗ Cuándo NO</h3>
    <ul>
      <li>Cuenta nueva, sin datos de cohorte</li>
      <li>EMQ &lt; 5</li>
      <li>Ticket medio &lt; 15€</li>
    </ul>
  </div>
</div>
```

CSS:
```css
.si-no-grid { display:grid; grid-template-columns: 1fr 1fr; gap:1rem; margin:1.5rem 0; }
.si-card { background:var(--bg-card); border:1px solid var(--border); border-radius:10px; padding:1.25rem; }
.si-card h3 { font-size:1rem; margin:0 0 0.75rem 0; }
.si-card ul { margin:0; padding-left:1.25rem; }
.si-card li { margin-bottom:0.4rem; line-height:1.5; color:var(--text-secondary); font-size:0.95rem; }
@media (max-width: 640px) { .si-no-grid { grid-template-columns: 1fr; } }
```

## Step diagram (proceso numerado)

```html
<ol class="steps">
  <li><strong>Audita</strong> el tracking server-side. Sin EMQ &gt; 7, todo lo demás es ruido.</li>
  <li><strong>Mide</strong> el CAC por cohorte mensual. No por canal, por cohorte.</li>
  <li><strong>Compara</strong> LTV a 90, 180 y 365 días por origen de tráfico.</li>
  <li><strong>Decide</strong> el ratio LTV/CAC mínimo. Por debajo de 3x, no escalas.</li>
</ol>
```

CSS:
```css
ol.steps { counter-reset: step; list-style:none; padding:0; margin:1.5rem 0; }
ol.steps li { counter-increment: step; position:relative; padding:0.75rem 0 0.75rem 3rem; border-bottom:1px solid var(--border); }
ol.steps li::before { content: counter(step); position:absolute; left:0; top:0.5rem; width:2rem; height:2rem; background:var(--accent-color,#6366f1); color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.9rem; }
ol.steps li:last-child { border-bottom:none; }
ol.steps li strong { color:var(--text-primary); }
```

## Reglas
- Usa bar-chart cuando compares 3+ valores numéricos con un máximo claro.
- Usa si-no-grid cuando expliques "haz X" vs "no hagas X".
- Usa ol.steps cuando el proceso tenga 3-6 pasos secuenciales.
- Máximo 1 visual_no_tabla por H2 — no satures.
