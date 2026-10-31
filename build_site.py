from pathlib import Path
import html, json, textwrap
R=Path(__file__).parent
# 게임 추가/수정: data/games.json만 변경 후 이 스크립트를 다시 실행합니다.
DATA=json.loads((R/'data/games.json').read_text(encoding='utf-8'))
if not isinstance(DATA,list) or not DATA:
 raise ValueError('data/games.json은 하나 이상의 게임 목록이어야 합니다.')
ids=set()
for item in DATA:
 if not isinstance(item,dict) or not __import__('re').fullmatch(r'[a-z0-9-]+',item.get('id','')): raise ValueError('유효하지 않은 게임 ID')
 if item['id'] in ids: raise ValueError(f'중복 게임 ID: {item["id"]}')
 ids.add(item['id'])
 if not item['play'].startswith('https://') or not item['repo'].startswith('https://github.com/'): raise ValueError('게임 및 저장소 URL은 안전한 HTTPS 주소여야 합니다.')
 if not (R/'assets/covers'/f"{item['id']}.webp").exists(): raise FileNotFoundError(f'게임 표지 누락: {item["id"]}.webp')
for obj in DATA:
 obj['guide']='games/'+obj['id']+'.html'
 if obj.get('detail_art'):
  detail_art = obj['detail_art']
  if not __import__('re').fullmatch(r'assets/details/[a-z0-9-]+\.webp', detail_art): raise ValueError('허용되지 않은 상세 이미지 경로')
  if not (R/detail_art).is_file(): raise FileNotFoundError(detail_art)
(R/'data').mkdir(exist_ok=True)
# 입력 JSON은 재생성 시 수정하지 않습니다.
# Site JS loads data from bundled script, not network, to work even when opened as file://.
(R/'data/games.js').write_text('window.EON_GAMES = '+json.dumps([{k:v for k,v in row.items() if k not in ('steps','controls','world','features','tips')} for row in DATA],ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
GENRE_ORDER=['액션','전략','모험','힐링','교육']
ALL_GENRES=sorted(set(tag for g in DATA for tag in g['genres']),key=lambda g:(GENRE_ORDER.index(g) if g in GENRE_ORDER else 999,g))
GENRE_SYMBOLS={'액션':'⚡','전략':'♠','모험':'✦','힐링':'❀','교육':'◎'}
GENRE_BUTTONS=''.join(f'<button class="filter" type="button" data-filter="{html.escape(g,quote=True)}" aria-pressed="false">{GENRE_SYMBOLS.get(g,"✧")} {html.escape(g)}</button>' for g in ALL_GENRES)
H=lambda s:html.escape(str(s),quote=True)
header='''<header class="site-header"><div class="container header-row"><a class="brand" href="./index.html" aria-label="EON Games 홈"><span class="brand-mark" aria-hidden="true">E</span><span class="brand-copy"><b>EON<span>GAMES</span></b><small>INDEPENDENT GAME COLLECTION</small></span></a><nav class="site-nav" aria-label="주요 메뉴"><a class="nav-link active" href="#games">게임 둘러보기</a><a class="nav-link" href="#how">이용 안내</a><a class="nav-link nav-outline" href="https://github.com/teamprotofelix" target="_blank" rel="noopener noreferrer">GitHub <span aria-hidden="true">↗</span></a></nav><div class="mobile-nav-list"><a class="mobile-nav-link" href="#games">게임 목록</a><a class="mobile-nav-link" href="#how">이용 안내</a></div></div></header>'''
foot='''<footer class="footer"><div class="container footer-main"><div><div class="footer-brand">✦ EON <span>GAMES</span></div><p>서로 다른 세계를 잇는 작은 게임 우주.<br>게임은 각각의 독립 사이트에서 실행됩니다.</p></div><div class="footer-links"><a href="#games">모든 게임</a><a href="#how">이용 안내</a><a href="https://github.com/teamprotofelix" target="_blank" rel="noopener noreferrer">TeamProtoFelix ↗</a></div></div><div class="container footer-bottom"><small>© 2026 EON Games Portal · Built as a static website</small><small>포털 표지는 안내용 콘셉트 일러스트입니다. 실제 게임 화면과 다를 수 있습니다.</small></div></footer>'''
card_html=[]
for g in DATA:
 new_mark = '<span class="cover-new">NEW GAME</span>' if g.get('new') else ''
 cover_kind = '사용자가 제공한 타이틀 일러스트' if g.get('supplied_art') else '테마 콘셉트 일러스트'
 card_html.append(f'''<article class="game-card" data-game="{g['id']}" data-genre="{' '.join(g['genres'])}" data-name="{H(g['name']+' '+g['en']+' '+g['description'])}" style="--accent:var(--{g['color']})">
   <a class="card-cover" href="{g['guide']}" aria-label="{H(g['name'])} 게임 안내 보기"><img src="assets/covers/{g['id']}.webp" width="1200" height="675" decoding="async" alt="{H(g['name'])} {cover_kind}">{new_mark}<span class="cover-label">{H(g['eyebrow'])}</span></a>
   <div class="card-content"><div class="card-top"><span class="genre-chip">{H(g['genre'])}</span><button class="favorite-btn" type="button" data-favorite="{g['id']}" aria-label="{H(g['name'])} 즐겨찾기에 추가" aria-pressed="false" title="즐겨찾기">♡</button></div><h3>{H(g['name'])}</h3><p class="game-en">{H(g['en'])}</p><p class="card-desc">{H(g['description'])}</p>
   <div class="card-actions"><a class="btn btn-play" href="{g['play']}" target="_blank" rel="noopener noreferrer" aria-label="{H(g['name'])} 새 탭에서 플레이">▶ 플레이</a><a class="btn btn-guide" href="{g['guide']}">게임 안내 <span aria-hidden="true">↗</span></a><a class="btn btn-repo" href="{g['repo']}" target="_blank" rel="noopener noreferrer" aria-label="{H(g['name'])} GitHub 소스 보기" title="GitHub 소스 보기">GH</a></div></div></article>''')
index=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080d1c"><meta name="description" content="{H('EON Games — '+', '.join(g['name'] for g in DATA)+'를 한곳에서 만나세요.')}"><title>EON GAMES — 8개의 세계, 하나의 포털</title><link rel="manifest" href="manifest.webmanifest"><link rel="icon" type="image/svg+xml" href="favicon.svg"><link rel="stylesheet" href="styles.css"><meta property="og:title" content="EON Games · 게임 포털"><meta property="og:description" content="서로 다른 게임 세계. 원하는 게임을 찾아 바로 플레이하세요."><meta property="og:type" content="website"></head><body><a class="skip-link" href="#games">게임 목록으로 건너뛰기</a>{header}
<main><section class="hero"><div class="hero-grid-lines" aria-hidden="true"></div><div class="container hero-inner"><div class="hero-copy"><p class="eyebrow"><span class="pulse-dot"></span> A WORLD OF PLAY · 2026</p><h1>{len(DATA)}개의 세계.<br><em>플레이는 한곳에서.</em></h1><p class="hero-desc">마녀의 마법과 힐링 산책부터 시간여행 슈팅, 카드 전략과 서부 탐험까지. 오늘 즐길 세계를 골라보세요.</p><div class="hero-ctas"><a class="btn btn-primary btn-large" href="#games">모든 게임 탐색 <span aria-hidden="true">↘</span></a><button class="btn btn-ghost btn-large" id="randomBtn" type="button">✦ 랜덤 게임 추천</button></div><div class="hero-stats"><div><strong>{len(DATA):02d}</strong><span>GAME WORLDS</span></div><div><strong>{len(set(tag for g in DATA for tag in g["genres"])):02d}</strong><span>GENRES</span></div><div><strong>∞</strong><span>FUN TO EXPLORE</span></div></div></div><div class="hero-visual"><img src="assets/portal-hero.webp" alt="밤하늘의 네온빛 게임 세계 포털과 아케이드 조작판" width="1500" height="900" fetchpriority="high"><div class="hero-floating hero-floating-top"><span>●</span> EON LIBRARY <b>{len(DATA)} GAMES IN THE COLLECTION</b></div><div class="hero-floating hero-floating-bottom"><span>✦</span><div><b>CHOOSE YOUR ADVENTURE</b><small>YOUR NEXT GAME IS ONE CLICK AWAY</small></div></div></div></div><div class="container hero-note">* 각 게임은 독립 사이트에서 실행되며 인터넷 연결이 필요합니다.</div></section>
<section class="world-section" id="games"><div class="container"><div class="section-heading"><div><p class="eyebrow">EXPLORE THE COLLECTION</p><h2>게임 라이브러리 <span>{len(DATA):02d}</span></h2><p>장르를 고르거나 이름으로 검색하세요. <b>게임 안내</b>에서 방법을 읽고 바로 시작할 수 있습니다.</p></div><span class="section-spark" aria-hidden="true">✳</span></div>
<div class="toolbar" role="search"><label class="search-box"><span aria-hidden="true">⌕</span><span class="sr-only">게임 검색</span><input type="search" id="searchInput" placeholder="게임 이름, 장르, 키워드 검색" autocomplete="off" spellcheck="false"><kbd>/</kbd></label><div class="toolbar-bottom"><div class="filters" id="filters" role="group" aria-label="장르 필터"><button class="filter active" type="button" data-filter="전체" aria-pressed="true">모두 보기</button>{GENRE_BUTTONS}<button class="filter" type="button" data-filter="최근 실행" aria-pressed="false">◷ 최근 실행</button><button class="filter" type="button" data-filter="즐겨찾기" aria-pressed="false">♡ 즐겨찾기</button></div><label class="sort-box">정렬 <select id="sortSelect"><option value="default">기본 순서</option><option value="name">이름순</option><option value="recent">최근 실행순</option></select></label></div></div>
<div class="results-line"><p id="resultsText" role="status" aria-live="polite">전체 {len(DATA)}개 게임</p><span>PLAY • LEARN • EXPLORE</span></div><div class="cards-grid" id="gameGrid">{''.join(card_html)}</div><div class="empty-state" id="emptyState" hidden><span aria-hidden="true">✳</span><h3>조건에 맞는 게임이 없습니다.</h3><p>검색어 또는 장르를 바꾸면 다른 세계를 찾을 수 있습니다.</p><button class="btn btn-primary" id="resetBtn" type="button">전체 게임 보기</button></div></div></section>
<section class="guide-section" id="how"><div class="container"><div class="guide-heading"><p class="eyebrow">YOUR PORTAL, YOUR RULES</p><h2>게임은 가볍게. 탐험은 자유롭게.</h2><p>모든 게임은 각자의 사이트에서 독립 실행됩니다. 포털은 소개와 길찾기를 담당합니다.</p></div><div class="guide-panels"><div class="guide-panel"><span class="guide-icon">01</span><h3>게임 찾아보기</h3><p>{len(DATA)}개 게임을 장르별로 분류하고, 검색이나 즐겨찾기로 빠르게 찾을 수 있습니다.</p></div><div class="guide-panel"><span class="guide-icon">02</span><h3>방법 먼저 확인</h3><p>각 게임의 안내 페이지에서 스토리, 목표, PC·모바일 조작 방법을 확인하세요.</p></div><div class="guide-panel"><span class="guide-icon">03</span><h3>새 탭에서 플레이</h3><p>플레이 버튼을 누르면 원래 게임 사이트가 새 탭에서 열립니다. 원본 게임에는 영향이 없습니다.</p></div></div><div class="guide-bottom"><span>✦ 새로운 게임을 추가할 때도 카드와 안내 페이지를 쉽게 확장할 수 있도록 구성했습니다.</span><a href="https://github.com/teamprotofelix" target="_blank" rel="noopener noreferrer">프로젝트 소스 둘러보기 ↗</a></div></div></section></main>{foot}
<div class="toast" id="toast" role="status" aria-live="polite" aria-atomic="true"></div><script src="data/games.js"></script><script src="app.js" defer></script></body></html>'''
(R/'index.html').write_text(index,encoding='utf-8')

for i,g in enumerate(DATA):
 prev=DATA[(i-1)%len(DATA)]; nxt=DATA[(i+1)%len(DATA)]
 steps=''.join(f'<li><span class="step-index">0{j}</span><div><h3>{H(t)}</h3><p>{H(desc)}</p></div></li>' for j,(t,desc) in enumerate(g['steps'],1))
 controls=''.join(f'<tr><th scope="row">{H(t)}</th><td>{H(desc)}</td></tr>' for t,desc in g['controls'])
 features=''.join(f'<li>{H(v)}</li>' for v in g['features']);tips=''.join(f'<li>{H(v)}</li>' for v in g['tips'])
 detail_art=g.get('detail_art',f"assets/covers/{g['id']}.webp")
 art_class=' detail-art-full' if g.get('detail_art') else ''
 art_caption='USER-PROVIDED TITLE ART' if g.get('supplied_art') else 'CONCEPT ART · NOT A GAME SCREENSHOT'
 alt_description=' 사용자가 제공한 타이틀 일러스트' if g.get('supplied_art') else '의 안내용 테마 일러스트. 실제 게임 화면은 아님'
 detail=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080d1c"><meta name="description" content="{H(g['description'])}"><title>{H(g['name'])} | EON GAMES 게임 안내</title><link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../styles.css"><link rel="manifest" href="../manifest.webmanifest"></head><body class="detail-page" data-game-id="{g['id']}" style="--accent:var(--{g['color']})"><a class="skip-link" href="#main">본문으로 건너뛰기</a><header class="site-header"><div class="container header-row"><a class="brand" href="../index.html"><span class="brand-mark" aria-hidden="true">E</span><span class="brand-copy"><b>EON<span>GAMES</span></b><small>GUIDE / GAME COLLECTION</small></span></a><nav class="site-nav" aria-label="주요 메뉴"><a class="nav-link" href="../index.html#games">전체 게임</a><a class="nav-link nav-outline" href="{g['repo']}" target="_blank" rel="noopener noreferrer">원본 GitHub ↗</a></nav><a class="mobile-nav-link" href="../index.html#games">← 목록으로</a></div></header><main id="main"><div class="detail-hero"><div class="container"><div class="detail-breadcrumb"><a href="../index.html">EON GAMES</a><span>›</span><a href="../index.html#games">GAME LIBRARY</a><span>›</span><strong>{H(g['name'])}</strong></div><div class="detail-layout"><div class="detail-heading"><span class="detail-label">NO. 0{g['order']} / {H(g['eyebrow'])}</span><span class="detail-genre">{H(g['genre'])}</span><h1>{H(g['name'])}</h1><p class="detail-en">{H(g['en'])}</p><p class="detail-short">{H(g['short'])}</p><p class="detail-description">{H(g['description'])}</p><div class="detail-actions"><a class="btn btn-primary btn-large" href="{g['play']}" data-play-link target="_blank" rel="noopener noreferrer">▶ 지금 플레이 <span aria-hidden="true">↗</span></a><a class="btn btn-ghost btn-large" href="{g['repo']}" target="_blank" rel="noopener noreferrer">GitHub 소스 ↗</a></div><p class="external-note">게임은 독립 사이트의 새 탭에서 열립니다.</p></div><div class="detail-art{art_class}"><img src="../{detail_art}" alt="{H(g['name'])}{alt_description}" width="{1280 if g.get('detail_art') else 1200}" height="{960 if g.get('detail_art') else 675}"><span>{art_caption}</span></div></div></div></div>
<section class="detail-content container"><div class="detail-main"><section class="detail-block"><p class="eyebrow">01 / THE STORY</p><h2>어떤 게임인가요?</h2><p class="rich-paragraph">{H(g['world'])}</p></section><section class="detail-block"><p class="eyebrow">02 / HOW TO PLAY</p><h2>처음 시작하는 방법</h2><ol class="steps-list">{steps}</ol></section><section class="detail-block"><p class="eyebrow">03 / CONTROLS</p><h2>조작 방법</h2><div class="controls-wrap"><table class="controls-table"><tbody>{controls}</tbody></table></div></section><section class="detail-block"><p class="eyebrow">04 / TIPS</p><h2>알아두면 좋은 팁</h2><ul class="tips-list">{tips}</ul></section></div><aside class="detail-aside"><div class="aside-card"><p class="eyebrow">HIGHLIGHTS</p><h2>이 게임의 매력</h2><ul class="features-list">{features}</ul><a class="btn btn-primary full-width" href="{g['play']}" data-play-link target="_blank" rel="noopener noreferrer">게임으로 이동 ↗</a></div><div class="aside-card aside-plain"><p class="eyebrow">DESTINATION</p><p class="link-label">게임 사이트</p><a class="url-link" href="{g['play']}" target="_blank" rel="noopener noreferrer">{H(g['play'].removeprefix('https://'))} ↗</a><p class="link-label">GitHub 저장소</p><a class="url-link" href="{g['repo']}" target="_blank" rel="noopener noreferrer">{H(g['repo'].removeprefix('https://github.com/'))} ↗</a></div></aside></section>
<section class="detail-next"><div class="container"><p class="eyebrow">THE NEXT WORLD</p><h2>다음 게임도 탐험해 보세요.</h2><div class="next-grid"><a class="next-card" href="{prev['id']}.html"><img src="../assets/covers/{prev['id']}.webp" decoding="async" alt="" width="1200" height="675"><div><small>← PREVIOUS GAME</small><b>{H(prev['name'])}</b></div></a><a class="next-card" href="{nxt['id']}.html"><img src="../assets/covers/{nxt['id']}.webp" decoding="async" alt="" width="1200" height="675"><div><small>NEXT GAME →</small><b>{H(nxt['name'])}</b></div></a></div><a class="back-library" href="../index.html#games">← 모든 게임으로 돌아가기</a></div></section></main><footer class="detail-footer"><div class="container">© 2026 EON Games Portal <span>·</span> <a href="../index.html">게임 목록으로 돌아가기 ↑</a></div></footer><script src="../detail.js" defer></script></body></html>'''
 (R/'games'/f"{g['id']}.html").write_text(detail,encoding='utf-8')
print('Generated index + game detail pages + data; game links:',len(DATA))

# Keep the installable offline shell in sync with newly added/removed games.
# Cache revision changes with data, HTML, CSS, scripts and artwork (no manual bump).
import hashlib, re
shell = [
    './', './index.html', './styles.css', './app.js', './detail.js', './data/games.js',
    './manifest.webmanifest', './favicon.svg', './assets/portal-hero.webp',
    './assets/icon-192.png', './assets/icon-512.png'
]
shell += [f'./games/{g["id"]}.html' for g in DATA]
shell += [f'./assets/covers/{g["id"]}.webp' for g in DATA]
shell += ['./'+g['detail_art'] for g in DATA if g.get('detail_art')]
rev = hashlib.sha256()
for rel in shell[1:]:
    file = R / rel[2:]
    rev.update(rel.encode('utf-8'))
    rev.update(file.read_bytes())
cache_name = f'eon-games-portal-{rev.hexdigest()[:12]}'
sw = (R / 'sw.js').read_text(encoding='utf-8')
sw = re.sub(r"const CACHE = '[^']+';", f"const CACHE = '{cache_name}';", sw)
sw = re.sub(r'const SHELL = \[.*?\];', 'const SHELL = ' + json.dumps(shell, ensure_ascii=False, indent=2) + ';', sw, flags=re.S)
(R / 'sw.js').write_text(sw, encoding='utf-8')
print(f'Offline shell: {len(shell)} files, cache {cache_name}')
