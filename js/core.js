// ============================================================
// CORE.JS – Site‑wide JavaScript
// ============================================================

(function() {
  'use strict';

  function getEl(id) { return document.getElementById(id); }
  function qs(sel) { return document.querySelector(sel); }
  function qsa(sel) { return document.querySelectorAll(sel); }

  function initTheme() {
    const html = document.documentElement;

    function setTheme(theme) {
      html.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme);
      const icon = document.getElementById('themeIcon');
      const toggle = document.getElementById('themeToggle');
      if (icon) icon.textContent = theme === 'dark' ? '🌙' : '☀️';
      if (toggle) toggle.setAttribute('aria-pressed', theme === 'dark' ? 'false' : 'true');
    }

    function getPreferredTheme() {
      const stored = localStorage.getItem('theme');
      if (stored) return stored;
      return window.matchMedia?.('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    }

    setTheme(getPreferredTheme());

    document.addEventListener('click', function(e) {
      const toggle = e.target.closest('#themeToggle');
      if (!toggle) return;
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      setTheme(next);
      if (typeof Plotly !== 'undefined') {
        setTimeout(() => {
          if (window.renderAllCharts) window.renderAllCharts();
        }, 200);
      }
    });

    const systemMedia = window.matchMedia('(prefers-color-scheme: light)');
    systemMedia.addEventListener('change', function(e) {
      if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'light' : 'dark');
      }
    });
  }

  function initHamburger() {
    document.removeEventListener('click', handleHamburgerClick);
    document.removeEventListener('click', handleNavLinkClick);
    document.removeEventListener('click', handleOutsideClick);

    function handleHamburgerClick(e) {
      const hamburger = e.target.closest('.hamburger');
      if (!hamburger) return;
      e.stopPropagation();
      const navLinks = getEl('navLinks');
      if (navLinks) {
        navLinks.classList.toggle('open');
        hamburger.classList.toggle('open');
      }
    }

    function handleNavLinkClick(e) {
      const link = e.target.closest('a');
      if (!link) return;
      if (link.closest('.dropdown-toggle')) return;
      const navLinks = getEl('navLinks');
      if (navLinks && navLinks.contains(link)) {
        navLinks.classList.remove('open');
        const hamburger = document.querySelector('.hamburger');
        if (hamburger) hamburger.classList.remove('open');
      }
    }

    function handleOutsideClick(e) {
      const nav = document.querySelector('.sticky-nav');
      if (!nav) return;
      if (!nav.contains(e.target)) {
        const navLinks = getEl('navLinks');
        if (navLinks) {
          navLinks.classList.remove('open');
          const hamburger = document.querySelector('.hamburger');
          if (hamburger) hamburger.classList.remove('open');
        }
      }
    }

    document.addEventListener('click', handleHamburgerClick);
    document.addEventListener('click', handleNavLinkClick);
    document.addEventListener('click', handleOutsideClick);
  }

  function initDropdowns() {
    qsa('.dropdown-toggle').forEach(toggle => {
      toggle.removeEventListener('click', toggleDropdown);
      toggle.addEventListener('click', toggleDropdown);
    });
  }

  // FIX: Auto-collapse other dropdowns on mobile
  function toggleDropdown(e) {
    e.preventDefault();
    const current = this.closest('.dropdown');
    if (!current) return;

    const allDropdowns = document.querySelectorAll('.nav-links .dropdown');
    const isOpen = current.classList.contains('open');

    // Close all dropdowns first
    allDropdowns.forEach(d => d.classList.remove('open'));

    // If the clicked one wasn't open, open it
    if (!isOpen) {
      current.classList.add('open');
    }
  }

  function initAccordion() {
    qsa('.accordion-toggle').forEach(el => {
      el.removeEventListener('click', accordionClick);
      el.addEventListener('click', accordionClick);
    });
  }

  function accordionClick(e) {
    const el = e.currentTarget;
    const content = el.nextElementSibling;
    const arrow = el.querySelector('.arrow');
    if (content) {
      content.classList.toggle('open');
      el.classList.toggle('open');
      if (arrow) arrow.classList.toggle('open');
    }
  }

  window.toggleAccordion = function(el) {
    const content = el.nextElementSibling;
    const arrow = el.querySelector('.arrow');
    if (content) {
      content.classList.toggle('open');
      el.classList.toggle('open');
      if (arrow) arrow.classList.toggle('open');
    }
  };

  function initShare() {
    qsa('.share-btn').forEach(btn => {
      btn.removeEventListener('click', sharePage);
      btn.addEventListener('click', sharePage);
    });
  }

  function sharePage() {
    const url = window.location.href;
    const title = document.title;
    const text = 'Check out the ' + title + ' model:';
    if (navigator.share) {
      navigator.share({ title, text, url }).catch(() => {});
    } else if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(() => alert('Link copied!')).catch(() => prompt('Copy this link manually:', url));
    } else {
      prompt('Copy this link manually:', url);
    }
  }

  function initFloatingReturn() {
    const btn = getEl('floatingReturnTop');
    if (btn) {
      btn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }
  }

  function initPWA() {
    const installBtn = getEl('pwaInstallBtn');
    const iosOverlay = getEl('pwaIosOverlay');
    const closeIosBtn = getEl('pwaCloseIosModal');
    let deferredPrompt = null;

    const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
    if (isStandalone) {
      if (installBtn) {
        installBtn.style.display = 'none';
        installBtn.dataset.installed = 'true';
      }
      return;
    }

    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
      if (installBtn && installBtn.style.display !== 'flex' && !installBtn.dataset.installed) {
        installBtn.style.display = 'flex';
      }
    });

    window.addEventListener('appinstalled', () => {
      if (installBtn) {
        installBtn.style.display = 'none';
        installBtn.dataset.installed = 'true';
      }
      console.log('PWA installed.');
      deferredPrompt = null;
    });

    setTimeout(() => {
      if (installBtn && !installBtn.dataset.installed && !window.matchMedia('(display-mode: standalone)').matches && !window.navigator.standalone) {
        installBtn.style.display = 'flex';
      }
    }, 12000);

    if (installBtn) {
      installBtn.addEventListener('click', async () => {
        if (deferredPrompt) {
          deferredPrompt.prompt();
          const { outcome } = await deferredPrompt.userChoice;
          console.log('PWA install:', outcome);
          deferredPrompt = null;
          if (outcome === 'accepted') {
            installBtn.style.display = 'none';
            installBtn.dataset.installed = 'true';
          }
        } else if (/iphone|ipad|ipod/.test(window.navigator.userAgent.toLowerCase())) {
          if (iosOverlay) iosOverlay.style.display = 'flex';
        } else {
          alert("To install this app, look for 'Install' or 'Add to Home Screen' in your browser's menu.");
        }
      });
    }

    if (closeIosBtn) {
      closeIosBtn.addEventListener('click', () => {
        if (iosOverlay) iosOverlay.style.display = 'none';
      });
    }

    if (iosOverlay) {
      iosOverlay.addEventListener('click', (e) => {
        if (e.target === e.currentTarget) iosOverlay.style.display = 'none';
      });
    }
  }

  function setLastUpdated() {
    const el = getEl('last-updated');
    if (el) {
      el.textContent = 'Last updated: ' + new Date().toLocaleString();
    }
  }

  function initCore() {
    initTheme();
    initHamburger();
    initDropdowns();
    initAccordion();
    initShare();
    initFloatingReturn();
    initPWA();
    setLastUpdated();
  }

  window.initCore = initCore;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCore);
  } else {
    initCore();
  }

})();