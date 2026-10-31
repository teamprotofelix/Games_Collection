/* Remember games opened from their guide page. No tracking server. */
(() => {
  'use strict';
  const id = document.body?.dataset.gameId;
  if (!id) return;
  document.querySelectorAll('a[data-play-link]').forEach(link => {
    link.addEventListener('click', () => {
      try {
        const key = 'eon-games-recent-v1';
        let entries = JSON.parse(localStorage.getItem(key) || '[]');
        if (!Array.isArray(entries)) entries = [];
        entries = entries.filter(item => item && item.id !== id && Number.isFinite(item.time));
        entries.unshift({ id, time: Date.now() });
        localStorage.setItem(key, JSON.stringify(entries.slice(0, 20)));
      } catch (_error) { /* Storage is optional. */ }
    });
  });
})();
