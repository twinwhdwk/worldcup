# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

2026 FIFA World Cup themed real-time multiplayer quiz game. No build system — pure HTML/CSS/JS files served via GitHub Pages.

**Live URL**: `https://twinwhdwk.github.io/worldcup`

## Development

No build step. Open HTML files directly in a browser or push to GitHub Pages to deploy.

```bash
# Deploy all changes
git add <files> && git commit -m "message" && git push
```

The repo is a GitHub Pages site (`main` branch → root). Changes to `operator.html`, `play.html`, `scoreboard.html`, etc. go live immediately after push.

## Architecture: Multiplayer System

Three-screen Kahoot-style system synced via **Firebase Realtime Database (RTDB)**:

| File | Role |
|---|---|
| `operator.html` | Host UI (TV/PC): runs the session, controls questions, triggers reveal |
| `play.html` | Player UI (phone): submits answers, shows results |
| `scoreboard.html` | Read-only leaderboard, auto-refreshes from Firebase |

### Firebase Data Layout

All data lives under `/wc_live/` in RTDB:

```
/wc_live/session      — current state machine state: lobby | question | reveal
/wc_live/answers      — player answers for current question (reset on each question)
/wc_live/players      — registered players with lastSeen heartbeat
/wc_live/scores       — cumulative per-player scores (total, streak, correct)
```

Firebase URL is stored in `localStorage` as `wc_fb_url`. The `?db=<base64url>` query parameter on `play.html` carries the URL from operator to players (embedded in the QR code).

### State Machine

`operator.html` drives state transitions:
1. `lobby` → `question` (via `nextQuestion()` → `fbPut('/answers', null)` then `fbPatch('/session', {state:'question',...})`)
2. `question` → `reveal` (via `revealAnswer()` → `fbPatch('/session', {state:'reveal', scoreGains, allRanks,...})`)
3. `reveal` → `lobby` (end of game) or → `question` (next question)

### SSE (Server-Sent Events) Pattern

Both `operator.html` and `play.html` use Firebase's SSE endpoint (`/session.json`) to receive real-time updates:
- `put` events: full replace of `_sessState`
- `patch` events: `Object.assign(_sessState, d.data)` merge

A 2.5-second poll (`setInterval`) serves as a fallback for missed SSE events.

**Critical race condition guards:**
- `operator.html`: `allAnsweredPending` (prevents double auto-reveal) and `revealInProgress` (prevents double `revealAnswer()` call)
- `operator.html` → `nextQuestion()`: clears `currentAnswers={}; allAnsweredPending=false;` in synchronous code after all `await`s, before calling `renderAnswerDist()` — prevents stale Q(n) answers from triggering auto-reveal at Q(n+1) start
- `play.html` → `answer()`: returns early if `_sessState?.state !== 'question'` — prevents `show('s-wait')` from overriding a reveal screen already in progress via `showReveal`'s internal `setTimeout`
- `play.html`: `_revealQId` string prevents `showReveal()` from re-running for the same question

### Score Calculation

Done entirely in `operator.html`'s `revealAnswer()` at reveal time:
- Correct answer: 100 pts base + speed bonus (up to 50 pts, linear based on elapsed time vs time limit)
- `gains` object keyed by encoded player name → sent to Firebase at `/session.scoreGains` and `/scores`
- Players read their own gain from `s.scoreGains[enc(myName)]` in `showReveal()`

## Question Banks (`QB` object in `operator.html`)

Three quiz types, each a function returning a shuffled array:

- `'선수퀴즈'` (~20+ questions): player-to-country matching; each entry has `{emoji, text, options[], correct, hint, img?, name?}`
- `'유니폼퀴즈'` (~10 questions): uniform color/pattern identification; local images like `체코유니폼.png` use relative paths
- `'한국퀴즈'` (7 questions, fixed): Korea 2026 WC specific questions; always shown as 7 (set as default in `selectGame()`)

`correct` is the 0-based index into `options[]` **after** `shuffleOptions()` runs. `shuffleOptions()` shuffles options and remaps `correct` accordingly. All question images support `bigImg:true` flag for full-width display.

## Individual Mini-games

Seven standalone games in `games/`:
- `player-country.html` — player nationality quiz (combo + speed bonus)
- `uniform-quiz.html` — standalone version of uniform quiz
- `flag-quiz.html`, `record-quiz.html`, `wins-quiz.html`, `champion-tournament.html`, `penalty-kick.html`

These also POST scores to Firebase `/scores` when a Firebase URL is configured, feeding the shared leaderboard.

## Key Utilities

- `enc(name)` — sanitizes Firebase path keys (replaces `.#$[]/` with `_`)
- `fbPut/fbPatch/fbDelete/fbGet` — thin Firebase REST wrappers with 9s AbortController timeout
- `renderOptHtml(text)` — converts flag emoji to `<img>` tags using flagcdn.com
- `_fimg(code, h)` — returns `<img>` for a flag CDN image by ISO country code
- `show(id)` in `play.html` — hides all `.screen` elements and unhides the target
- `tvShow(id)` in `operator.html` — toggles between `tv-lobby`, `tv-question`, `tv-reveal` panels

## Image Sources

- Country flags: `https://flagcdn.com/w40/{code}.png` with fallback to `cdn.jsdelivr.net/npm/flag-icons`
- Player photos: Wikipedia Commons URLs or `news.nateimg.co.kr` direct image URLs
- Local images (e.g. `체코유니폼.png`) use relative paths and must exist in the repo root
