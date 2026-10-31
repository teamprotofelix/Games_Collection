/* EON Games: lightweight static catalog. Local browser data never leaves this page. */
(() => {
  'use strict';
  const games = Array.isArray(window.EON_GAMES) ? window.EON_GAMES : [];
  const $ = selector => document.querySelector(selector);
  const grid = $('#gameGrid');
  const search = $('#searchInput');
  const results = $('#resultsText');
  const empty = $('#emptyState');
  const sort = $('#sortSelect');
  if (!grid || !search || !results || !empty || !sort) return;
  const byId = new Map(games.map(game => [game.id, game]));
  const cards = [...grid.querySelectorAll('[data-game]')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const favoriteButtons = [...document.querySelectorAll('[data-favorite]')];
  const FAV_KEY = 'eon-games-favorites-v1';
  const OLD_FAV_KEY = 'moip-games-favorites-v1';
  const RECENT_KEY = 'eon-games-recent-v1';
  const safeRead = key => {
    try {
      const value = JSON.parse(localStorage.getItem(key) || 'null');
      return Array.isArray(value) ? value : null;
    } catch (_error) { return null; }
  };
  const safeWrite = (key, value) => {
    try { localStorage.setItem(key, JSON.stringify(value)); return true; }
    catch (_error) { return false; }
  };
  // Existing favorites survive the MOIP -> EON name change on the same origin.
  const oldFavorites = safeRead(OLD_FAV_KEY) || [];
  const currentFavorites = safeRead(FAV_KEY);
  const favorites = new Set((currentFavorites ?? oldFavorites).filter(id => byId.has(id)));
  if (currentFavorites === null && oldFavorites.length) safeWrite(FAV_KEY, [...favorites]);
  const recent = new Map((safeRead(RECENT_KEY) || []).filter(item => item && byId.has(item.id) && Number.isFinite(item.time)).map(item => [item.id, item.time]));
  let currentGenre = '전체';
  let toastTimer;
  const normalize = value => String(value || '').normalize('NFKC').toLocaleLowerCase('ko-KR').replace(/\s+/g, ' ').trim();
  const showToast = message => {
    const el = $('#toast');
    if (!el) return;
    el.textContent = message;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2600);
  };
  const render = () => {
    const q = normalize(search.value);
    const visible = cards.filter(card => {
      const game = byId.get(card.dataset.game);
      const matchesGenre = currentGenre === '전체' ||
        (currentGenre === '즐겨찾기' ? favorites.has(card.dataset.game) :
        currentGenre === '최근 실행' ? recent.has(card.dataset.game) : game?.genres?.includes(currentGenre));
      const matchesQuery = !q || normalize(card.dataset.name).includes(q);
      const isVisible = matchesGenre && matchesQuery;
      card.hidden = !isVisible;
      return isVisible;
    });
    const compareDefault = (a, b) => (byId.get(a.dataset.game)?.order ?? 0) - (byId.get(b.dataset.game)?.order ?? 0);
    visible.sort((a, b) => {
      if (sort.value === 'name') return a.querySelector('h3').textContent.localeCompare(b.querySelector('h3').textContent, 'ko');
      if (sort.value === 'recent' || currentGenre === '최근 실행') return (recent.get(b.dataset.game) || 0) - (recent.get(a.dataset.game) || 0) || compareDefault(a, b);
      return compareDefault(a, b);
    });
    // Static, prerendered cards are reordered; all cards still work with JavaScript disabled.
    visible.forEach(card => grid.appendChild(card));
    empty.hidden = visible.length !== 0;
    results.textContent = `${currentGenre} ${visible.length}개 게임`;
  };
  const setGenre = genre => {
    currentGenre = genre;
    filters.forEach(button => {
      const active = button.dataset.filter === genre;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    render();
  };
  const updateFavorites = () => favoriteButtons.forEach(button => {
    const selected = favorites.has(button.dataset.favorite);
    button.setAttribute('aria-pressed', String(selected));
    button.setAttribute('aria-label', `${byId.get(button.dataset.favorite)?.name || '게임'} 즐겨찾기 ${selected ? '해제' : '추가'}`);
    button.textContent = selected ? '♥' : '♡';
    button.title = selected ? '즐겨찾기 해제' : '즐겨찾기 추가';
  });
  filters.forEach(button => button.addEventListener('click', () => setGenre(button.dataset.filter)));
  search.addEventListener('input', render);
  sort.addEventListener('change', render);
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName || '') && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault(); search.focus();
    }
    if (event.key === 'Escape' && document.activeElement === search) {
      search.value = ''; search.blur(); render();
    }
  });
  favoriteButtons.forEach(button => button.addEventListener('click', () => {
    const id = button.dataset.favorite;
    if (favorites.has(id)) favorites.delete(id); else favorites.add(id);
    if (!safeWrite(FAV_KEY, [...favorites])) showToast('브라우저 저장이 제한되어 현재 화면에서만 즐겨찾기가 유지됩니다.');
    updateFavorites(); render();
  }));
  const addRecent = id => {
    if (!byId.has(id)) return;
    recent.delete(id);
    recent.set(id, Date.now());
    if (!safeWrite(RECENT_KEY, [...recent.entries()].map(([gameId, time]) => ({ id: gameId, time })).sort((a, b) => b.time - a.time).slice(0, 20))) {
      showToast('브라우저 저장이 제한되어 최근 실행 목록은 현재 화면에서만 유지됩니다.');
    }
    render();
  };
  cards.forEach(card => card.querySelector('.btn-play')?.addEventListener('click', () => addRecent(card.dataset.game)));
  $('#resetBtn')?.addEventListener('click', () => {
    search.value = ''; sort.value = 'default'; setGenre('전체'); search.focus();
  });
  $('#randomBtn')?.addEventListener('click', () => {
    // Prefer games matching search/genre; if nothing matches, use the entire library.
    const available = cards.filter(card => !card.hidden);
    const pool = available.length ? available : cards;
    if (!pool.length) return;
    const card = pool[Math.floor(Math.random() * pool.length)];
    window.location.assign(byId.get(card.dataset.game).guide);
  });
  updateFavorites(); render();
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    window.addEventListener('load', () => navigator.serviceWorker.register('./sw.js').catch(() => {}));
  }
})();
