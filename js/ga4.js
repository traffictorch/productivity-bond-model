// ============================================================
// GA4 – Deferred Load
// Fires on user interaction or after 4.5s timeout
// ============================================================
(function() {
  const MEASUREMENT_ID = 'G-EY4X3BEXCX';
  const ENABLE_GA = true; // Set to false for local testing

  function loadGA() {
    if (window.gtag) return; // Already loaded

    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${MEASUREMENT_ID}`;
    document.head.appendChild(script);

    script.onload = function() {
      window.dataLayer = window.dataLayer || [];
      function gtag() { dataLayer.push(arguments); }
      window.gtag = gtag;

      gtag('js', new Date());
      gtag('config', MEASUREMENT_ID, {
        cookie_expires: 63072000,   // 2 years
        cookie_prefix: '_ga',
        send_page_view: true
      });
    };
  }

  let fired = false;

  function fireOnce() {
    if (fired || !ENABLE_GA) return;
    fired = true;
    loadGA();
    cleanup();
  }

  const events = ['scroll', 'pointerdown', 'keydown', 'touchstart'];
  function cleanup() {
    events.forEach(ev => window.removeEventListener(ev, fireOnce));
  }

  events.forEach(ev => {
    window.addEventListener(ev, fireOnce, { once: true, passive: true });
  });

  setTimeout(fireOnce, 4500);

  if (document.readyState === 'complete') {
    setTimeout(fireOnce, 100);
  } else {
    window.addEventListener('load', function() {
      setTimeout(fireOnce, 100);
    }, { once: true });
  }
})();