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

  var animatedEls = document.querySelectorAll('.scroll-animate, .story-section, .fade-left, .fade-right, .scale-in, .reveal');
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