// Service Worker for BCA Exam Prep
// Strategy:
//   - HTML / navigation requests → network-first (so the live exam ticker
//     and auto-hide JS always run against the latest file). Falls back to
//     cache when offline.
//   - Static assets (icons, manifest) → cache-first.
// Bump CACHE_VERSION whenever PRECACHE_URLS changes so old caches are purged.

const CACHE_VERSION = 'bca-prep-v36';
const PRECACHE_URLS = [
  './',
  './index.html',
  './ctrc-exam-guide.html',
  './probstats-exam-guide.html',
  './r-datascience-exam-guide.html',
  './loc-exam-guide.html',
  './loc-crash-60.html',
  './wc-exam-guide.html',
  './dbms-exam-guide.html',
  './iks-exam-guide.html',
  './cn-exam-guide.html',
  './de-exam-guide.html',
  './manifest.json',
  './icon-192.svg',
  './icon-512.svg'
];

// Install: pre-cache all guides. Use individual put() so a single 404 does
// not abort the entire install.
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then(cache =>
      Promise.all(
        PRECACHE_URLS.map(url =>
          fetch(url, { cache: 'no-cache' })
            .then(res => res.ok ? cache.put(url, res) : null)
            .catch(() => null)
        )
      )
    ).then(() => self.skipWaiting())
  );
});

// Activate: clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch handler
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const isNavigation =
    req.mode === 'navigate' ||
    (req.destination === 'document') ||
    req.headers.get('accept')?.includes('text/html');

  if (isNavigation) {
    // Network-first: always try to get the freshest HTML so the live
    // exam ticker reflects the current time. Fall back to cache offline.
    event.respondWith(
      fetch(req)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE_VERSION).then(cache => cache.put(req, clone));
          return res;
        })
        .catch(() =>
          caches.match(req).then(cached => cached || caches.match('./index.html'))
        )
    );
    return;
  }

  // Cache-first for everything else (icons, manifest, future static assets)
  event.respondWith(
    caches.match(req).then(cached => {
      if (cached) return cached;
      return fetch(req).then(res => {
        if (!res || res.status !== 200 || res.type !== 'basic') return res;
        const clone = res.clone();
        caches.open(CACHE_VERSION).then(cache => cache.put(req, clone));
        return res;
      });
    })
  );
});
