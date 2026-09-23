// Theme Toggle Logic - applies on first paint to avoid flicker
(function() {
  var saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  }
})();

var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

document.addEventListener('DOMContentLoaded', function() {
  var toggles = document.querySelectorAll('.theme-toggle-btn');
  var themeAnimTimer = null;
  toggles.forEach(function(toggle) {
    toggle.addEventListener('click', function() {
      var root = document.documentElement;
      var current = root.getAttribute('data-theme') || 'dark';
      var next = current === 'light' ? 'dark' : 'light';
      // Cross-fade del cambio de tema: sin salto de brillo abrupto
      root.classList.add('theme-anim');
      root.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      clearTimeout(themeAnimTimer);
      themeAnimTimer = setTimeout(function() {
        root.classList.remove('theme-anim');
      }, 350);
    });
  });

  // Scroll-edge: la línea fina del nav solo aparece cuando hay contenido
  // pasando por debajo (no un divisor duro permanente)
  var nav = document.querySelector('.main-nav');
  if (nav) {
    var onNavScroll = function() {
      nav.classList.toggle('is-scrolled', window.scrollY > 4);
    };
    onNavScroll();
    window.addEventListener('scroll', onNavScroll, { passive: true });
  }

  // Megamenu: hover is CSS-driven (.nav-dropdown:hover .nav-dropdown-content),
  // but touch devices need a click handler. We add an .is-open class on tap
  // and a document-level click to close when tapping outside.
  var dropdowns = document.querySelectorAll('.nav-dropdown');
  dropdowns.forEach(function(dd) {
    var btn = dd.querySelector('.nav-dropdown-btn');
    if (!btn) return;
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      var wasOpen = dd.classList.contains('is-open');
      // Close all other open dropdowns first
      document.querySelectorAll('.nav-dropdown.is-open').forEach(function(o) {
        o.classList.remove('is-open');
      });
      if (!wasOpen) dd.classList.add('is-open');
    });
  });
  // Close on click outside
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.nav-dropdown')) {
      document.querySelectorAll('.nav-dropdown.is-open').forEach(function(o) {
        o.classList.remove('is-open');
      });
    }
  });
  // Close on Escape
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.nav-dropdown.is-open').forEach(function(o) {
        o.classList.remove('is-open');
      });
    }
  });

  // Mobile menu toggle (replaces inline onclick="..." on the hamburger)
  var menuBtn = document.querySelector('.mobile-menu-btn');
  var mobileNav = document.getElementById('mobile-nav');
  if (menuBtn && mobileNav) {
    menuBtn.addEventListener('click', function() {
      var isOpen = mobileNav.classList.toggle('active');
      menuBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }
});

// Scroll Animations - Intersection Observer
(function() {
  var observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, observerOptions);

  var animatedEls = document.querySelectorAll('.scroll-animate, .story-section, .fade-left, .fade-right, .scale-in, .reveal, .loop-station');
  animatedEls.forEach(function(el) {
    observer.observe(el);
  });
})();

// Smooth scroll for anchor links (respeta prefers-reduced-motion)
document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    var target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: prefersReducedMotion.matches ? 'auto' : 'smooth',
        block: 'start'
      });
    }
  });
});

// Live counter animation for stats (e.g. "Lo que hemos hecho")
(function() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var containers = document.querySelectorAll('.anchor-stats');
  if (!containers.length) return;

  var DURATION = 1800;

  function format(value, decimals) {
    return new Intl.NumberFormat('es-ES', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(value);
  }

  function animate(el) {
    var target = parseFloat(el.dataset.counter);
    var decimals = parseInt(el.dataset.decimals || '0', 10);
    var suffix = el.dataset.suffix || '';
    var start = performance.now();

    function step(now) {
      var progress = Math.min((now - start) / DURATION, 1);
      var eased = 1 - Math.pow(1 - progress, 4); // easeOutQuart
      var current = target * eased;
      el.textContent = format(current, decimals) + suffix;
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = format(target, decimals) + suffix;
      }
    }
    requestAnimationFrame(step);
  }

  containers.forEach(function(container) {
    var counters = container.querySelectorAll('[data-counter]');
    counters.forEach(function(counter) {
      var decimals = parseInt(counter.dataset.decimals || '0', 10);
      var suffix = counter.dataset.suffix || '';
      counter.textContent = format(0, decimals) + suffix;
    });

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (!entry.isIntersecting) return;
        var stats = entry.target.querySelectorAll('[data-counter]');
        stats.forEach(function(stat, i) {
          setTimeout(function() { animate(stat); }, i * 120);
        });
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.3 });

    observer.observe(container);
  });
})();

// Hero mini-explainer: "la plataforma dice" vs "tu caja dice" (home)
// One-shot al entrar en viewport, ≤1,6s en total. Reduced-motion o
// sin JS: el DOM ya contiene el estado final estático.
(function() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var wrap = document.querySelector('.hero-split');
  if (!wrap) return;

  var platformNum = wrap.querySelector('[data-split="platform"]');
  var crmNum = wrap.querySelector('[data-split="crm"]');
  if (!platformNum || !crmNum) return;

  var BASE = 214;   // el número real: ambos lados arrancan aquí
  var DRIFT = 298;  // ~+40%: la plataforma sigue inflando

  function tick(el, from, to, duration, done) {
    var start = performance.now();
    function step(now) {
      var progress = Math.min((now - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 4); // easeOutQuart, como el count-up
      el.textContent = Math.round(from + (to - from) * eased);
      if (progress < 1) {
        requestAnimationFrame(step);
      } else if (done) {
        done();
      }
    }
    requestAnimationFrame(step);
  }

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (!entry.isIntersecting) return;
      observer.disconnect();
      wrap.classList.add('play'); // t=0: barras (CSS) + números (JS)
      platformNum.textContent = '0';
      crmNum.textContent = '0';
      tick(platformNum, 0, BASE, 800);
      tick(crmNum, 0, BASE, 800, function() {
        setTimeout(function() { // t≈1,3s: la separación
          wrap.classList.add('is-split');
          tick(platformNum, BASE, DRIFT, 300);
        }, 500);
      });
    });
  }, { threshold: 0.35 });

  observer.observe(wrap);
})();
/* ==== HERO CRAFT: punto que recorre el bucle siguiendo al cursor + tilt del ticket ==== */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;
  if (reduce) return;
  var art = document.querySelector('.hero-art');
  if (!art) return;

  // Estaciones + punto sobre el path del bucle
  var path = document.querySelector('.craft-path');
  var dot = document.querySelector('.craft-dot');
  var stations = document.querySelector('.craft-stations');
  if (path && dot && stations) {
    var L = path.getTotalLength();
    [0, 0.25, 0.5, 0.75, 0.97].forEach(function (r) {
      var p = path.getPointAtLength(L * r);
      var c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      c.setAttribute('cx', p.x); c.setAttribute('cy', p.y); c.setAttribute('r', 8);
      stations.appendChild(c);
    });
    if (fine) {
      art.addEventListener('mousemove', function (e) {
        var b = art.getBoundingClientRect();
        var ratio = Math.min(1, Math.max(0, (e.clientX - b.left) / b.width));
        var p = path.getPointAtLength(L * ratio);
        dot.setAttribute('cx', p.x); dot.setAttribute('cy', p.y);
      });
      art.addEventListener('mouseleave', function () {
        var p = path.getPointAtLength(0);
        dot.setAttribute('cx', p.x); dot.setAttribute('cy', p.y);
      });
    }
    var p0 = path.getPointAtLength(0);
    dot.setAttribute('cx', p0.x); dot.setAttribute('cy', p0.y);
  }

  // Tilt 3D sutil del parte de caja
  var ticket = document.querySelector('[data-tilt]');
  if (ticket && fine) {
    ticket.style.transform = 'rotate(-3deg)';
    ticket.addEventListener('mousemove', function (e) {
      var b = ticket.getBoundingClientRect();
      var rx = ((e.clientY - b.top) / b.height - 0.5) * -6;
      var ry = ((e.clientX - b.left) / b.width - 0.5) * 7;
      ticket.style.transform = 'perspective(700px) rotateX(' + rx.toFixed(2) + 'deg) rotateY(' + ry.toFixed(2) + 'deg) rotate(-3deg)';
    });
    ticket.addEventListener('mouseleave', function () {
      ticket.style.transform = 'rotate(-3deg)';
    });
  }
})();

/* ==== Consentimiento de cookies: banner mínimo + bloqueo previo de terceros ==== */
// art. 22.2 LSSI + Guía AEPD/CNMC sobre el uso de cookies (2ª ed.): sin
// terceros cargados antes del consentimiento, rechazo tan visible como la
// aceptación y caducidad a los 12 meses. Las técnicas no piden permiso.
(function () {
  var KEY = 'ddb-consent';
  var TTL = 365 * 24 * 60 * 60 * 1000; // 12 meses

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; }
  }

  window.ddbGetConsent = read;

  window.ddbSetConsent = function (thirdParty) {
    var value = { thirdParty: !!thirdParty, ts: Date.now() };
    try { localStorage.setItem(KEY, JSON.stringify(value)); } catch (e) {}
    document.dispatchEvent(new CustomEvent('ddb-consent', { detail: value }));
    hideBanner();
  };

  function hideBanner() {
    var el = document.getElementById('consent-banner');
    if (el) el.remove();
  }

  // Reabrir el banner desde /cookies.html ("Revisar mi elección")
  window.ddbOpenConsent = function () { showBanner(); };

  function showBanner() {
    if (document.getElementById('consent-banner')) return;
    var el = document.createElement('div');
    el.id = 'consent-banner';
    el.className = 'consent-banner';
    el.setAttribute('role', 'region');
    el.setAttribute('aria-label', 'Consentimiento de cookies');
    el.innerHTML =
      '<p class="consent-text">Esta web usa por su cuenta solo cookies técnicas y guarda tu tema en tu navegador. ' +
      'Nada de analítica ni publicidad. La única pieza de terceros es Calendly, la agenda de reservas, y no la cargo sin tu permiso.</p>' +
      '<div class="consent-actions">' +
      '<button type="button" class="consent-btn consent-accept">De acuerdo</button>' +
      '<button type="button" class="consent-btn consent-reject">Solo lo necesario</button>' +
      '<a class="consent-more" href="/cookies.html">Qué uso exactamente</a>' +
      '</div>';
    document.body.appendChild(el);
    el.querySelector('.consent-accept').addEventListener('click', function () { window.ddbSetConsent(true); });
    el.querySelector('.consent-reject').addEventListener('click', function () { window.ddbSetConsent(false); });
  }

  function init() {
    var c = read();
    if (!c || Date.now() - c.ts > TTL) showBanner();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
