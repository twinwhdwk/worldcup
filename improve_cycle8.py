#!/usr/bin/env python3
"""사이클 8: 모바일 최적화 - 터치 친화적 버튼, 뷰포트 개선"""
import os

REPO = os.path.dirname(os.path.abspath(__file__))

MOBILE_CSS = """
    /* ── Mobile Optimization ── */
    @media (max-width: 480px) {
      body { padding: 12px; }
      .options { grid-template-columns: 1fr 1fr; gap: 8px; }
      .opt-btn { padding: 14px 8px; font-size: 14px; min-height: 64px; }
      .question-card, .q-card, .jersey-card { padding: 24px 16px; }
      .hud { gap: 8px; }
      .hud-box { padding: 10px 6px; }
      .hud-value { font-size: 22px; }
      .player-emoji, .jersey-display { font-size: 56px; }
      .hints, .clues, .hint-row { gap: 6px; }
      .hint-chip, .clue-chip { font-size: 11px; padding: 4px 10px; }
      .shoot-btn { padding: 16px 40px; font-size: 18px; }
      h1 { font-size: 28px; }
    }
    /* Larger touch targets */
    .opt-btn { min-height: 56px; -webkit-tap-highlight-color: transparent; }
    .shoot-btn { -webkit-tap-highlight-color: transparent; }
    .arrow-btn { min-width: 80px; min-height: 48px; }
"""

games_dir = os.path.join(REPO, 'games')
for filename in os.listdir(games_dir):
    if not filename.endswith('.html'): continue
    filepath = os.path.join(games_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'Mobile Optimization' in content:
        print(f"  이미 있음: {filename}"); continue
    content = content.replace('</style>', MOBILE_CSS + '\n    </style>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ 모바일 최적화: {filename}")

# index.html mobile
idx = os.path.join(REPO, 'index.html')
with open(idx, 'r', encoding='utf-8') as f:
    content = f.read()
if 'Mobile Optimization' not in content:
    content = content.replace('</style>', """
    @media (max-width: 480px) {
      .hero { padding: 40px 16px 30px; }
      .game-grid { grid-template-columns: 1fr; }
      .game-card { padding: 24px 20px; }
    }
    </style>""")
    with open(idx, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  ✅ 모바일 최적화: index.html")

print("사이클 8 완료: 모바일 최적화")
