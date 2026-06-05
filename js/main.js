// Theme Toggle Logic - applies on first paint to avoid flicker
(function() {
  var saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  }
})();

document.addEventListener('DOMContentLoaded', function() {
  var toggles = document.querySelectorAll('.theme-toggle-btn');
  toggles.forEach(function(toggle) {
    toggle.addEventListener('click', function() {
      var current = document.documentElement.getAttribute('data-theme') || 'dark';
      var next = current === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    });
  });
});

// Sidebar Toggle
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.querySelector('.file-tree-overlay');
  sidebar.classList.toggle('open');
  overlay.classList.toggle('display');
}

// Close sidebar on escape key
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    const sidebar = document.getElementById('sidebar');
    if (sidebar && sidebar.classList.contains('open')) {
      toggleSidebar();
    }
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

  var animatedEls = document.querySelectorAll('.scroll-animate, .story-section, .fade-left, .fade-right, .scale-in');
  animatedEls.forEach(function(el) {
    observer.observe(el);
  });
})();

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    var target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
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