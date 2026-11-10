// ============================================
// Service Worker - حسابات ألمونتال
// ============================================
const CACHE_NAME = 'almontal-v2';
const urlsToCache = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  'https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
];

// ===== تثبيت =====
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return Promise.all(
        urlsToCache.map(url =>
          cache.add(url).catch(err => console.warn('⚠️ فشل تخزين:', url))
        )
      );
    })
  );
  self.skipWaiting();
});

// ===== تفعيل =====
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(names =>
      Promise.all(
        names.map(name => {
          if (name !== CACHE_NAME) {
            console.log('🗑️ حذف كاش قديم:', name);
            return caches.delete(name);
          }
        })
      )
    )
  );
  self.clients.claim();
});

// ===== جلب =====
self.addEventListener('fetch', event => {
  // تجاهل Firebase (لازم لايف دايماً)
  if (event.request.url.includes('firebaseio.com') ||
      event.request.url.includes('gstatic.com/firebasejs')) {
    return;
  }
  // تجاهل غير GET
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;

      return fetch(event.request).then(response => {
        if (!response || response.status !== 200) return response;
        const responseClone = response.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseClone);
        });
        return response;
      }).catch(() => {
        return caches.match('./index.html');
      });
    })
  );
});

// ===== رسائل =====
self.addEventListener('message', event => {
  if (event.data === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
