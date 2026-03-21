# factory-factory-boardgame-v1

> Engine: **E-FACTORY** | Created: 2026-03-20 | Status: 🟢 Game 1 Complete

## Overview

보드게임 3종 MVP (ORDER-003 P0). 순수 HTML+CSS+JS, 외부 의존성 0, GitHub Pages 배포.

## Games

| # | Game | Status | Tech |
|---|------|--------|------|
| 1 | **Reversi (오셀로)** | ✅ Complete | HTML+CSS+JS, Minimax AI |
| 2 | TBD | ⏳ Planned | — |
| 3 | TBD | ⏳ Planned | — |

## Play

- **Live**: https://pure-flon.github.io/factory-factory-boardgame-v1/
- **Local**: `python3 -m http.server 8765 --directory src` → http://localhost:8765

## Game 1: Reversi

- AI 대전 (minimax + alpha-beta pruning)
- 3단계 난이도: Easy / Normal / Hard
- 돌 배치·뒤집기 애니메이션
- 유효 수 표시, 점수판, 되돌리기
- 반응형 모바일 지원
- $0 스택 (GitHub Pages)

## SEO & Analytics

- Open Graph + Twitter Card 메타태그
- JSON-LD 구조화 데이터 (VideoGame schema)
- sitemap.xml + robots.txt
- GA4 placeholder (계정 설정 후 활성화)
- AdSense placeholder (승인 후 활성화)

## Structure

```
src/
├── index.html      # Game 1: Reversi (단일 파일)
├── sitemap.xml     # SEO
├── robots.txt      # 크롤러 허용
└── game/           # Python 코어 엔진
    ├── board.py    # Board state machine
    └── dice.py     # Dice roller
```

## Deployment

```bash
# GitHub Pages (Settings → Pages → Source: main, /src)
# 또는 gh-pages branch 사용:
git subtree push --prefix src origin gh-pages
```

## Links

| 항목 | URL |
|------|-----|
| GitHub | https://github.com/pure-flon/factory-factory-boardgame-v1 |
| Live | https://pure-flon.github.io/factory-factory-boardgame-v1/ |
| Parent | https://github.com/ops-self-factory/factory-ops-self-evolution-governance |
| Tracker | MVP_TRACKER.md (EXP-1005) |

## Metrics (EXP-1005)

| Metric | Kill | Scale |
|--------|------|-------|
| 7일 신규 UV | < 50 | >= 200 |
| 평균 세션 시간 | < 30초 | >= 120초 |
| 재방문율 | — | 추적 |
