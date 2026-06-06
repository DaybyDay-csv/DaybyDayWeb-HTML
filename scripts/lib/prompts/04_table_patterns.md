# 04_table_patterns.md — table templates and visual patterns
# Used in step 5 of generate_post.py. ~2KB.

Cuando generes HTML, usa SOLO estas etiquetas. NO imágenes, NO SVG inline, NO Tailwind, NO <div> decorativos.

## Tabla de benchmarks (la más común)
```html
<table>
  <thead>
    <tr>
      <th>Sector</th>
      <th>ROAS medio</th>
      <th>CPA medio (€)</th>
      <th>CTR</th>
      <th>CPM (€)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Moda D2C</td>
      <td>3,8x</td>
      <td>22</td>
      <td>1,4%</td>
      <td>8,50</td>
    </tr>
    <!-- más filas -->
  </tbody>
</table>
```

## Tabla comparativa (planes, opciones, herramientas)
```html
<table>
  <thead>
    <tr>
      <th>Criterio</th>
      <th>Opción A</th>
      <th>Opción B</th>
      <th>Opción C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Coste mensual</strong></td>
      <td>1.500€</td>
      <td>3.000€</td>
      <td>5.000€+</td>
    </tr>
    <tr>
      <td><strong>Tiempo de setup</strong></td>
      <td>2 semanas</td>
      <td>4 semanas</td>
      <td>6-8 semanas</td>
    </tr>
    <tr>
      <td><strong>Account manager dedicado</strong></td>
      <td>Junior</td>
      <td>Senior</td>
      <td>Socio</td>
    </tr>
  </tbody>
</table>
```

## Tabla "antes/después" (auditoría de cuenta)
```html
<table>
  <thead>
    <tr>
      <th>Métrica</th>
      <th>Antes</th>
      <th>30 días</th>
      <th>60 días</th>
      <th>90 días</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ROAS</td>
      <td>1,9x</td>
      <td>2,4x</td>
      <td>3,1x</td>
      <td>3,6x</td>
    </tr>
    <tr>
      <td>CPA (€)</td>
      <td>38</td>
      <td>31</td>
      <td>26</td>
      <td>22</td>
    </tr>
  </tbody>
</table>
```

## Lista numerada con ranking
```html
<ol>
  <li><strong>Hook en los primeros 3 segundos.</strong> El 80% del drop-off ocurre aquí. Si no enganchas, el resto no importa.</li>
  <li><strong>Oferta clara en el frame 1.</strong> "30% de descuento", "Envío gratis", "3x2". Una sola oferta, no tres.</li>
  <!-- más items -->
</ol>
```

## Lista de bullets con dato
```html
<ul>
  <li><strong>Volumen mínimo:</strong> 50 conversiones por variante para que el test sea concluyente.</li>
  <li><strong>Duración:</strong> 7-14 días. Menos de 7 días, el learning phase distorsiona el CPA.</li>
  <li><strong>Presupuesto:</strong> 1.500-3.000€ por test si tu CPA está en 30€.</li>
</ul>
```

## Blockquote con tesis contraintuitiva
```html
<blockquote>
  <p><strong>La mayoría cree que más presupuesto = más ventas.</strong> En la práctica, escalar presupuesto sin EMQ &gt; 7 lo que consigues es inflar CPM sin mover CPA. La palanca no es el dinero, es la calidad del evento.</p>
</blockquote>
```

## Lista de "cuándo NO" (sección obligatoria, AEO-friendly)
```html
<h3>Cuándo NO usar esta estrategia</h3>
<ul>
  <li>Si tu cuenta tiene menos de 30 días de histórico: los datos no son estables.</li>
  <li>Si tu ticket medio es &lt; 15€: el CPA mínimo viable está por encima del margen.</li>
  <li>Si no tienes CAPI bien configurada: los datos del test son ruido.</li>
</ul>
```

## Resumen clave al final de un H2
```html
<p><strong>Idea clave:</strong> gasta 1.500€ en lugar de 5.000€ hasta que la variante gane con 50+ conversiones. Escalar antes de tiempo convierte un test en un descalabro de ROAS.</p>
```

## Reglas duras
- Mínimo 1 tabla por artículo.
- Mínimo 1 lista numerada (ol) o bullet (ul) por artículo.
- Mínimo 1 blockquote con tesis contraintuitiva.
- Mínimo 1 sección "cuándo NO" (puede ir al final o como H3 dentro de un H2).
- Tablas: mínimo 4 filas en tbody.
- Listas: mínimo 3 items, máximo 9.
