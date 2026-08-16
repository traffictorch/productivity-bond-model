// sw.js – Caching completely disabled

self.addEventListener('install', event => {
  // Skip waiting to activate immediately
  self.skipWaiting();
  event.waitUntil(
    // Delete any existing caches
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => caches.delete(cacheName))
      );
    })
  );
});

self.addEventListener('activate', event => {
  // Take control of all pages without reload
  event.waitUntil(
    clients.claim()
  );
});

// No 'fetch' listener = no caching, all requests go direct to network.