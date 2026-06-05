// js/dots.js — Subtle animated dot grid background
// Reads --accent from CSS so it adapts to the page mood + theme.
// Honors prefers-reduced-motion, reduces density on mobile, re-randomizes
// the wave pattern on every page load for a different visual each visit.
(function () {
  'use strict';

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var canvas = document.getElementById('bg-dots');
  if (!canvas) return;
  var ctx = canvas.getContext('2d', { alpha: true });
  if (!ctx) return;

  var DOT_RADIUS = 1.4;
  var OPACITY = 0.3;
  var SPEED = 0.012;
  var SEPARATION_DESKTOP = 48;
  var SEPARATION_MOBILE = 80;
  var MOBILE_BREAKPOINT = 768;

  var sep, w, h, amountX, amountY;
  var dots = [];
  var color = '#3B82F6';
  var time = 0;
  var raf = null;
  var resizeTimer = null;

  // Tiny seeded PRNG (mulberry32) for reproducible per-visit randomness.
  function mulberry32(seed) {
    return function () {
      seed = (seed + 0x6D2B79F5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function setup() {
    var isMobile = window.innerWidth < MOBILE_BREAKPOINT;
    sep = isMobile ? SEPARATION_MOBILE : SEPARATION_DESKTOP;
    w = window.innerWidth;
    h = window.innerHeight;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.scale(dpr, dpr);
    amountX = Math.ceil(w / sep) + 2;
    amountY = Math.ceil(h / sep) + 2;

    // Unique seed per visit → different wave pattern each load.
    var seed = (Date.now() ^ Math.floor(Math.random() * 0x7fffffff)) >>> 0;
    var rng = mulberry32(seed);

    var ox = (amountX * sep) / 2;
    var oy = (amountY * sep) / 2;
    dots = new Array(amountX * amountY);
    for (var ix = 0; ix < amountX; ix++) {
      for (var iy = 0; iy < amountY; iy++) {
        dots[iy * amountX + ix] = {
          x: ix * sep - ox,
          y: iy * sep - oy,
          phase: rng() * Math.PI * 2,
          freq: 0.18 + rng() * 0.15,   // ~35–50s period at 60fps
          amp: 6 + rng() * 8
        };
      }
    }
    readAccentColor();
  }

  function readAccentColor() {
    var v = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();
    if (v) color = v;
  }

  function draw() {
    raf = requestAnimationFrame(draw);
    ctx.clearRect(0, 0, w, h);

    var ox = (amountX * sep) / 2;
    var oy = (amountY * sep) / 2;

    ctx.fillStyle = color;
    ctx.globalAlpha = OPACITY;

    // Batch as single path for fewer state changes.
    ctx.beginPath();
    for (var i = 0; i < dots.length; i++) {
      var d = dots[i];
      var wave = Math.sin(time * d.freq + d.phase) * d.amp;
      ctx.moveTo(d.x + ox + DOT_RADIUS, d.y + oy + wave);
      ctx.arc(d.x + ox, d.y + oy + wave, DOT_RADIUS, 0, Math.PI * 2);
    }
    ctx.fill();

    time += SPEED;
  }

  function handleResize() {
    if (resizeTimer) clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      if (raf) cancelAnimationFrame(raf);
      setup();
      draw();
    }, 120);
  }

  // Re-read color when theme or mood changes.
  var observer = new MutationObserver(readAccentColor);
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme', 'data-mood']
  });

  // Defer init to idle so first paint isn't blocked.
  function init() {
    setup();
    draw();
    window.addEventListener('resize', handleResize);
  }
  if ('requestIdleCallback' in window) {
    requestIdleCallback(init, { timeout: 200 });
  } else {
    setTimeout(init, 0);
  }
})();
