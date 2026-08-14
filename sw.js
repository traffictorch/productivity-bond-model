// sw.js
const CACHE_NAME = 'prod-bond-model-v1';
const urlsToCache = [
  '/productivity-bond-model/index.html',
  '/productivity-bond-model/manifest.json',
  '/productivity-bond-model/icon-512.png',
  '/productivity-bond-model/favicon.ico'
];

// Install
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Activate
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit
        if (response) {
          return response;
        }

        // Clone the request (streams can only be consumed once)
        const fetchRequest = event.request.clone();

        return fetch(fetchRequest).then(response => {
          // Only cache valid basic responses
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clone the response (streams can only be consumed once)
          const responseToCache = response.clone();

          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache);
            });

          return response;
        });
      })
  );
});