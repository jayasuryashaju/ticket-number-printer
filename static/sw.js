self.addEventListener('install', (e) => {
  console.log('[Service Worker] Install');
});

self.addEventListener('fetch', (e) => {
  // Basic fetch to keep the PWA active
  e.respondWith(fetch(e.request));
});