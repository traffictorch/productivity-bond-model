// ============================================================
// SHARE – Native Web Share API + fallback
// ============================================================
(function() {
  'use strict';

  function sharePage() {
    const url = window.location.href;
    const title = document.title;
    const text = 'Check out the ' + title + ' model:';

    if (navigator.share) {
      navigator.share({
        title: title,
        text: text,
        url: url
      }).catch((err) => {
        if (err.name !== 'AbortError') console.error('Share failed:', err);
      });
    } else if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(() => {
        alert('Link copied to clipboard!');
      }).catch(() => {
        prompt("Copy this link manually:", url);
      });
    } else {
      prompt("Copy this link manually:", url);
    }
  }

  // Attach to all .share-btn elements
  document.querySelectorAll('.share-btn').forEach(btn => {
    btn.addEventListener('click', sharePage);
  });

  // Also expose globally in case of dynamic content
  window.sharePage = sharePage;
})();