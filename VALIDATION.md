# EON Games 검증 기록 — 2026-10-31

## 실제로 통과한 검사

1. 총 9개의 HTML (`index.html` + `games/*.html` 8개)의 로컬 CSS/JS/이미지 참조 확인: 누락 없음.
2. 게임 8개 각각에 맞는 게임 주소/저장소 링크, 8개 안내 페이지, 제목·표지·조작 표 구성 확인.
3. Node.js `--check`: `app.js`, `detail.js`, `sw.js`, `data/games.js` 구문 검사 통과.
4. Python `py_compile`: `build_site.py` 통과.
5. Chromium 인메모리 HTML/CSS/JavaScript 렌더링: **320×700, 390×844, 768×1024, 1440×900** 메인에서 가로 넘침 및 JavaScript 런타임 오류 없음.
6. 같은 Chromium에서 키워드 검색(스파이더 1개), 결과 없음/검색 초기화, 교육 장르(2개), 즐겨찾기·최근 실행 필터(각 1개) 동작 확인.
7. 8개 안내 페이지를 Chromium에서 모바일 폭으로 렌더링, 표지/제목/가로 넘침/JS 오류 검사 통과.
8. 이전 버전에서 존재하던 모바일 조작 표에 의한 가로 넘침을 수정.
9. EON Games로 메인·안내·PWA 이름을 변경. 메인 및 게임 안내 이미지 WebP 경로 확인.
10. PWA 서비스워커 목록은 `build_site.py`가 게임 데이터와 에셋을 토대로 자동 생성하며 캐시 버전은 해시 기반으로 갱신되도록 정리.

## 환경상 미검증

- 실제 GitHub Pages URL에 방문해 버튼으로 **게임 사이트 8곳이 열리는지** 확인하는 네트워크 테스트.
- HTTPS 환경에서 PWA 설치 및 실제 서비스워커의 캐시 설치/오프라인 복구/업데이트 테스트.
- Android·iOS 및 Safari 실기기 화면 및 터치 조작 검증.
- 브라우저 간 `localStorage` 즐겨찾기 이전 검증: 로직을 검토했지만 인메모리 테스트의 브라우저 정책상 실저장소 이전은 시연하지 못함.

**참고:** 로컬 URL 탐색이 `ERR_BLOCKED_BY_ADMINISTRATOR`로 거부되어 Chromium `set_content`로 로컬 CSS/JS/WebP를 인라인 주입해 테스트했습니다. 실제 네트워크 로드 및 외부 URL 접속과 동일하다고 간주하지 않았습니다.
