# Plan: Story Scroll, Glass Buttons, Testimonials

## Goal
Implementar animaciones de storytelling, glass buttons y sección de testimonials en la web.

## Contexto Actual
- Repo: `/root/projects/DaybyDay-HTML/`
- Live: https://daybydayweb-html.pages.dev
- Tech stack pages creadas: 12 páginas en `/tech/`
- Navegación actual: básica sin acceso a tech pages

## Propuesta de Implementación

### Step 1: Añadir Tech Pages a Navegación Principal
Actualizar nav en index.html:
```html
<li><a href="/tech/meta-ads.html">Meta Ads</a></li>
<li><a href="/tech/shopify.html">Shopify</a></li>
<li><a href="/tech/ga4.html">GA4</a></li>
...
```

### Step 2: Story Scroll Animations
CSS scroll-driven animations entre secciones de index.html:
- Hero → Servicios: fade + slide up
- Servicios → Founders: fade + scale
- Founders → Tech Stack → Resultados: staggered entrance

### Step 3: Apple Tahoe Glass Button
CSS-only liquid glass effect:
```css
.glass-button {
  backdrop-filter: blur(12px);
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
}
.glass-button:hover {
  /* liquid ripple effect */
}
```

### Step 4: Testimonials Carousel
Nueva sección en index.html:
- 3 testimonios
- Formato carousel simple (CSS-only o vanilla JS)
-Diseño参考 21st.dev/eldora-ui/testimonials

## Archivos a Modificar

| Archivo | Acción |
|---------|--------|
| `index.html` | Añadir nav links, animate sections, testimonios |
| `css/modern.css` | Añadir .glass-button, story animations |
| `js/main.js` | Scroll trigger + testimonials |

## Tests / Validación

```
- [ ] Navigation conecta a 12 tech pages
- [ ] Animaciones trigger al hacer scroll
- [ ] Glass button hover effect visible
- [ ] Testimonials muestran correctamente
- [ ] Mobile responsive
```

## Riesgos
- Demasiadas animaciones afectan performance
- Testimonials necesitan fotos reales

## Pendiente de Input
 Ninguno - continuar implementación directa.