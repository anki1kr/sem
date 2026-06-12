// Service Worker for BCA Exam Prep
// Strategy:
//   - HTML / navigation requests → network-first (so the live exam ticker
//     and auto-hide JS always run against the latest file). Falls back to
//     cache when offline.
//   - Static assets (icons, manifest) → cache-first.
// Bump CACHE_VERSION whenever PRECACHE_URLS changes so old caches are purged.

const CACHE_VERSION = 'bca-prep-v47';
const PRECACHE_URLS = [
  './',
  './index.html',
  './ctrc-exam-guide.html',
  './probstats-exam-guide.html',
  './r-datascience-exam-guide.html',
  './rds-crash-60.html',
  './loc-exam-guide.html',
  './loc-crash-60.html',
  './wc-exam-guide.html',
  './dbms-exam-guide.html',
  './iks-exam-guide.html',
  './cn-exam-guide.html',
  './de-exam-guide.html',
  './manifest.json',
  './icon-192.svg',
  './icon-512.svg',
  './wc-images/01-gsm-architecture.png',
  './wc-images/02-multiple-access.png',
  './wc-images/03-frequency-reuse.png',
  './wc-images/04-handoff.jpeg',
  './wc-images/05-spread-spectrum.png',
  './wc-images/06-cdma-spreading.png',
  './wc-images/07-cell-split-sector.png',
  './wc-images/08-gsm-call-flow.png',
  './wc-images/09-evolution-1g-5g.png',
  './wc-images/11-isdn-bri-pri.png',
  './wc-images/12-ccs-ss7.png',
  './wc-images/13-ain.png',
  './wc-images/3g-umts-architecture.png',
  './wc-images/4g-lte-architecture.png',
  './wc-images/basic-cellular-system.png',
  './wc-images/frequency-reuse-n12.png',
  './rds-images/supervised-vs-unsupervised.png',
  './rds-images/data-processing-chain.png',
  './rds-images/r-data-structures.png',
  './rds-images/db-vs-warehouse.png',
  './rds-images/ggplot2-layers.png',
  './rds-images/central-tendency-dispersion.png',
  './rds-images/oop-s3-s4-r5.png',
  './rds-images/debugging-tools.png',
  './rds-images/normal-curve-689599.png',
  './rds-images/csv-io-flow.png',
  './rds-images/dikw-pyramid.png',
  './rds-images/rstudio-4panes.png',
  './rds-images/ifelse-flowchart.png',
  './rds-images/loops-three-panel.png',
  './ps-images/correlation-gallery.png',
  './ps-images/data-classification.png',
  './ps-images/data-types.png',
  './ps-images/expectation-balance.png',
  './ps-images/exponential-density.png',
  './ps-images/geometric-pmf.png',
  './ps-images/kurtosis-shapes.png',
  './ps-images/least-squares-line.png',
  './ps-images/moments-ladder.png',
  './ps-images/normal-empirical-rule.png',
  './ps-images/pgf-pipeline.png',
  './ps-images/pmf-pdf-cdf.png',
  './ps-images/probability-rules.png',
  './ps-images/skewness-shapes.png',
  './ps-images/uniform-density.png',
  './ps-images/variance-spread.png'
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
