---
name: frontend-design
description: |
  Visual frontend design subrouter. Use when `frontend-ux-router` routes visual execution here, or when the user explicitly asks for visual UI design, frontend code polish, layout, spacing, typography, color, icons, component polish, landing/hero/marketing visuals, accessibility visual checks, interaction-state visuals, or web interface guideline review.
  Do not use for architecture/plan risk review; route that to codex-reviewer.
  Supports multi-guide execution for complex requests.
  For broad UI/UX, product feel, usability, flow, state, navigation, or Korean feel-language requests such as "뭔가 별로", "감성없다", "하마 스타일이 아니다", "네이버지도처럼", or "라벨이 안 따라다녀", use `frontend-ux-router` first.
---

# Frontend Design Router

Classify the user's design request, then read only the guides that address a distinct part of it. The guides provide evidence and quality lenses, not a house style.

## Available Guides

| Guide | File | When |
|-------|------|------|
| **Product UI** | `ui-polish.md` | Dashboard, SaaS, admin, form, data table, settings, game UI |
| **Creative UI** | `creative.md` | Landing page, portfolio, marketing, hero, showcase |
| **Web Design Guide** | `web-design-guide.md` | Visual design, accessibility, interaction-state, and UI guideline review |

## Classification

For each request, check ALL applicable categories (multiple OK):

```
1. Does it involve BUILDING product UI? (dashboard, game, form, etc.)
   → YES: add `ui-polish.md`

2. Does it involve CREATIVE/marketing design? (landing, hero, showcase)
   → YES: add `creative.md`

3. Does it involve REVIEWING UI code against visual design, accessibility, interaction-state, or web interface guidelines?
   → YES: add `web-design-guide.md`
```

Use one primary guide. Add another only when the request genuinely contains a separate build or review need.

## Semantic Triggering

This skill is visual/frontend-focused. If the request is about broader UX, product feel, flow, information structure, state coverage, or native-feeling interaction quality, start with `frontend-ux-router` first.

For Maplog-like 지도/캔버스/미디어/실시간 UI, visual styling is not enough when the issue is native-feeling interaction quality. Route through `frontend-ux-router` so layer fit, state, and heuristic checks happen before visual polish.

For architecture, migration, data-flow, security, or plan-risk review, do not run this router. Use `codex-reviewer` instead.

## Execution

1. Run classification above → collect list of matching guides
2. If the current project root or user-specified task root has `DESIGN.md` or `design.md`, read it before the matched guides
3. If no project-local design file exists, do not run a broad search; continue without it
4. Read ALL matched guide files from this directory
5. Resolve conflicts in this order: explicit user direction, project identity and hard constraints, observed artifact, platform behavior, then general guidance
6. If only 1 guide matched, follow it directly
7. If 2+ guides matched, apply them sequentially (build first, review after)

## Composition Examples

| Request | Guides |
|---------|--------|
| "게임 UI 만들어줘" | `ui-polish.md` |
| "랜딩 페이지 만들어줘" | `creative.md` |
| "이 컴포넌트 리뷰해줘" | `web-design-guide.md` |
| "대시보드 만들고 리뷰까지" | `ui-polish.md` → `web-design-guide.md` |
| "랜딩 페이지 만들고 디자인 가이드 체크" | `creative.md` → `web-design-guide.md` |
| "전체 UI 리뉴얼 + 감사" | Choose `ui-polish.md` or `creative.md` from the product surface, then `web-design-guide.md` |

## Ambiguous Case

If classification is ambiguous, inspect the actual surface and choose the guide that matches its primary job. Do not load a guide merely to add more rules.
