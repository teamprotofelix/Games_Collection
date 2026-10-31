/* Same-origin portal shell only; external games are NEVER cached or intercepted. */
const CACHE = 'eon-games-portal-33fb677a6358';
const SHELL = [
  "./",
  "./index.html",
  "./styles.css",
  "./app.js",
  "./detail.js",
  "./data/games.js",
  "./manifest.webmanifest",
  "./favicon.svg",
  "./assets/portal-hero.webp",
  "./assets/icon-192.png",
  "./assets/icon-512.png",
  "./games/witch.html",
  "./games/chrono.html",
  "./games/spider.html",
  "./games/skill.html",
  "./games/starlight.html",
  "./games/dutchman.html",
  "./games/battles.html",
  "./games/striker.html",
  "./assets/covers/witch.webp",
  "./assets/covers/chrono.webp",
  "./assets/covers/spider.webp",
  "./assets/covers/skill.webp",
  "./assets/covers/starlight.webp",
  "./assets/covers/dutchman.webp",
  "./assets/covers/battles.webp",
  "./assets/covers/striker.webp"
];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', event => {
  event.waitUntil(Promise.all([
    caches.keys().then(keys => Promise.all(keys.filter(key => (key.startsWith('moip-games-portal-') || key.startsWith('eon-games-portal-')) && key !== CACHE).map(key => caches.delete(key)))),
    self.clients.claim()
  ]));
});
self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== self.location.origin) return;
  // Network-first HTML keeps deployed updates visible. Cached shell remains readable offline.
  if (req.mode === 'navigate') {
    event.respondWith(fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(cache => cache.put(req, copy)); }
      return res;
    }).catch(() => caches.match(req).then(hit => hit || caches.match('./index.html'))));
    return;
  }
  event.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => {
    if (res.ok && (url.pathname.endsWith('.webp') || url.pathname.endsWith('.css') || url.pathname.endsWith('.js'))) {
      const copy = res.clone(); caches.open(CACHE).then(cache => cache.put(req,copy));
    }
    return res;
  })));
});
