# EON Games — Game Portal

9개의 독립 게임 사이트를 연결하는 **GitHub Pages용 순수 정적 포털**입니다. 원본 게임 코드와 데이터는 수정하지 않습니다.

## 포함 기능

- **게임 9종 소개**: 메인 카드, 별도 안내 페이지 9개, 원본 GitHub 링크, 게임 바로 실행
- **빠른 탐색**: 키워드 검색(단축키 `/`), 장르 필터, 이름·최근 실행 정렬
- **브라우저 편의 기능**: 즐겨찾기, 최근 실행 게임, 조건에 맞는 랜덤 추천
- **모바일 지원**: 320px부터 레이아웃 대응, 터치 접근, 모바일 상단 '게임 목록/이용 안내' 링크
- **EON Games 브랜드**: 메인·안내 페이지·PWA 이름·아이콘·메타데이터 통일
- **PWA**: HTTPS에서 설치 가능한 포털, 포털 페이지/이미지 오프라인 캐시. *외부 게임은 별도의 온라인 사이트입니다.*
- **보안**: 외부 CDN, 원격 코드, 추적 SDK, 키/계정/백엔드 없음. 게임은 새 탭에서 열며 `noopener noreferrer`를 사용합니다.

## 연결 게임

| 게임 | 실제 사이트 | 원본 저장소 |
| --- | --- | --- |
| 마녀의 사냥 | https://game-witch.moip.ai.kr/ | https://github.com/teamprotofelix/Game_Witch_Ara |
| 2045 크로노 스트라이커 | https://game-2045.moip.ai.kr/ | https://github.com/teamprotofelix/Game_2045_Shooting |
| 스파이더 아케이드 | https://game-spider.moip.ai.kr/ | https://github.com/teamprotofelix/Game_Spider_Card |
| 스킬 코어 | https://game-skills.moip.ai.kr/ | https://github.com/teamprotofelix/Game_EQ_Skill |
| 별빛 공녀 | https://game-starlight.moip.ai.kr/ | https://github.com/teamprotofelix/Starlight_Princess_Games |
| 금광을 찾아서 | https://game-lostdutchman.moip.ai.kr/ | https://github.com/teamprotofelix/Game_LostDutchman |
| 배틀최강전 | https://enter.moip.ai.kr/battles/index.html | https://github.com/teamprotofelix/enter |
| 심사기준 스트라이커 | https://enter.moip.ai.kr/exam_striker/index.html | https://github.com/teamprotofelix/enter |
| **마녀의 여행** | https://game-witch-heal.moip.ai.kr/ | https://github.com/teamprotofelix/Game_Witch_Heal |

**안내용 콘셉트 그림은 원본 게임 화면과 다를 수 있습니다.** 단, 마녀의 여행 카드와 안내 페이지 이미지는 사용자가 제공한 게임 타이틀 이미지를 WebP로 최적화한 것입니다. 각 게임 설명은 저장소의 공개 README 및 HTML을 바탕으로 제작했습니다. 실제 운영 버전에서 변경되었을 수 있습니다.

## GitHub Pages 업로드

1. 이 ZIP 압축을 해제합니다.
2. 압축을 푼 폴더 **안의 파일 및 하위 폴더 전체**(`index.html`, `games/`, `assets/`, `data/`, `.nojekyll` 등)를 GitHub 저장소 **루트**에 올립니다.
3. GitHub에서 `Settings → Pages → Build and deployment → Deploy from a branch → main → /(root)`를 선택합니다.
4. GitHub Pages 주소 (`https://<사용자>.github.io/<저장소>/`)로 접속합니다. 프로젝트 경로에서도 상대 경로가 유지됩니다.
5. 커스텀 도메인을 사용할 경우 Pages에서 Custom domain과 DNS를 별도로 설정합니다. **현재 사용자 지정 도메인 `game-collection.moip.ai.kr`의 `CNAME` 파일이 포함되어 있습니다.** DNS 설정은 운영자가 별도로 관리합니다.

### 로컬 실행

```bash
python -m http.server 8000
# http://localhost:8000/
```

로컬에서 `index.html`을 직접 열어도 주요 정적 기능이 실행되지만, PWA와 서비스워커는 `https://` 또는 `localhost`에서만 작동합니다.

## 새 게임을 추가하는 방법

**`data/games.json` 파일이 유일한 편집 원본**입니다. `data/games.js`, 메인 카드, 게임 안내 페이지, PWA 캐시는 생성됩니다.

1. `data/games.json` 배열에 기존 항목을 복사해 새 게임 정보(`id`, `order`, `name`, `en`, `eyebrow`, `genre`, `genres`, `color`, `play`, `repo`, `description`, `short`, `world`, `features`, `steps`, `controls`, `tips`)를 추가합니다. 새 `id`는 소문자 영문·숫자·하이픈만 허용됩니다.
2. `assets/covers/<새 id>.webp`를 추가합니다. 권장 크기는 **1200×675px**, 적절한 WebP 품질/용량으로 최적화합니다.
3. Python 3 환경에서 실행합니다.

```bash
python build_site.py
```

4. `index.html`, `games/*.html`, `data/games.js`, `sw.js`가 자동 업데이트됩니다. `sw.js` 캐시 버전도 파일 내용의 해시로 갱신됩니다. 원본 JSON은 덮어쓰지 않습니다.
5. 새 게임을 열어 링크·게임 설명·이미지를 확인하고 저장소에 업로드합니다.

새로운 장르를 `genres`에 사용하면 장르 선택 버튼도 자동 생성됩니다. `color`는 `styles.css`의 팔레트(`violet`, `blue`, `green`, `amber`, `pink`, `gold`, `coral`, `cyan`) 중에서 선택하세요.

## 폴더 구조

```text
index.html / styles.css / app.js   포털 메인 화면 및 기능
 detail.js                         게임 안내 페이지의 최근 실행 기록
 data/games.json                   게임 콘텐츠의 단일 편집 원본
 data/games.js                     브라우저에서 사용하는 자동 생성 목록
 games/*.html                      각 게임별 안내 페이지
 assets/covers/*.webp              게임 표지 9장
 assets/details/witch-heal-full.webp 신규 게임 전체 타이틀 아트
 assets/portal-hero.webp           메인 비주얼
 assets/icon-192.png, icon-512.png  PWA용 EON 앱 아이콘
 favicon.svg                       브라우저 아이콘
 manifest.webmanifest / sw.js      PWA/오프라인 캐시
 .nojekyll                         GitHub Pages Jekyll 비활성화
 build_site.py                     게임 추가용 정적 페이지 생성기
 README.md / VALIDATION.md         문서
 CNAME / .nojekyll                 커스텀 도메인 및 GitHub Pages 설정
```

## 저장 정책 및 이전 버전 즐겨찾기

즐겨찾기와 최근 실행 정보는 현재 브라우저의 `localStorage`에만 저장됩니다. 다른 기기로 동기화하거나 서버에 수집하지 않습니다. 이전 MOIP Games 버전의 즐겨찾기는 **동일한 브라우저·동일한 도메인에서 접근 가능한 경우 최초 1회 EON Games 저장 키로 가져옵니다.** 도메인이 바뀌면 브라우저의 보안 정책상 자동 이전할 수 없습니다.

## 배포 검증 주의

이번 v3은 Chromium 인메모리 UI 검사를 수행했습니다. 로컬 HTTP 접속은 실행 환경의 정책으로 차단되어 실제 서버 접속 검사는 수행하지 못했습니다. **GitHub Pages 실배포, PWA 설치/오프라인 갱신, Android/iOS 실기기, 각 운영 게임 URL 접속 검증은 완료되지 않았습니다.** 확인 범위는 `VALIDATION.md`를 참고하세요.

## v3.0 — 마녀의 여행 추가 (2026-10-31)

- **9번째 게임: 마녀의 여행** (`witch-heal`) 추가. 종전 마녀의 사냥과 서로 다른 독립 게임입니다.
- 첨부된 타이틀 이미지를 1200×675 WebP 카드 + 1280×960 WebP 상세 이미지로 변환했습니다. 원본 대용량 PNG는 배포 ZIP에 포함하지 않습니다.
- 9번째 게임 개별 안내 페이지에 4개 장소·아이템·동물 친구·장애물 점프·PC/모바일 조작 설명을 포함했습니다.
- `build_site.py`의 이전/다음 게임 탐색에서 하드코딩된 8개 순환을 실제 게임 수로 변경했습니다.
- 사용자 지정 도메인의 `CNAME`을 최신 저장소와 동일하게 유지합니다.
