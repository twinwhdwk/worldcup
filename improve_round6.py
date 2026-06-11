#!/usr/bin/env python3
"""라운드 6: 인덱스 페이지 - 라이브 랭킹 미리보기 + 게임 설명 강화"""
import os

REPO = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(REPO, 'index.html')

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if 'live-rank-preview' in content:
    print("이미 적용됨"); exit()

# Add live rank preview section before game grid
RANK_PREVIEW = """
  <div style="width:100%;max-width:1100px;margin:0 auto 32px;padding:0 24px;position:relative;z-index:1;">
    <div style="background:#13141f;border:1px solid rgba(255,215,0,0.15);border-radius:20px;padding:24px 28px;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:12px;">
        <div style="display:flex;align-items:center;gap:12px;">
          <span style="font-family:'Black Han Sans',sans-serif;font-size:20px;">🏆 실시간 TOP 5</span>
          <span style="background:#ef4444;color:#fff;font-size:10px;font-weight:700;letter-spacing:2px;padding:3px 8px;border-radius:100px;animation:pulse 1.5s infinite;">LIVE</span>
        </div>
        <a href="scoreboard.html" style="background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.25);border-radius:100px;padding:8px 20px;text-decoration:none;color:#FFD700;font-size:13px;font-weight:700;">점수 입력 →</a>
      </div>
      <div id="live-rank-preview" style="display:flex;flex-direction:column;gap:8px;">
        <div style="color:#555;font-size:14px;text-align:center;padding:16px;">아직 기록이 없어요. 게임 후 점수를 등록하세요!</div>
      </div>
    </div>
  </div>
"""

content = content.replace(
    '<div class="container">\n    <div class="game-grid">',
    RANK_PREVIEW + '\n  <div class="container">\n    <div class="game-grid">'
)

# Add JS to load and display ranks from localStorage
RANK_JS = """
<script>
(function() {
  const STORAGE_KEY = 'wc_scoreboard_v1';
  const AVATAR_COLORS = ['#ef4444','#f97316','#eab308','#22c55e','#06b6d4'];
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{"players":[]}');
    const sorted = (data.players || []).sort((a,b)=>b.bestScore-a.bestScore).slice(0,5);
    const el = document.getElementById('live-rank-preview');
    if (!el) return;
    if (sorted.length === 0) return;
    const maxScore = sorted[0].bestScore || 1;
    el.innerHTML = sorted.map((p,i) => {
      const medal = ['🥇','🥈','🥉','4위','5위'][i];
      const barW = Math.round(p.bestScore/maxScore*100);
      const col = AVATAR_COLORS[i % AVATAR_COLORS.length];
      return `<div style="display:flex;align-items:center;gap:12px;">
        <div style="width:28px;text-align:center;font-size:16px;">${medal}</div>
        <div style="width:36px;height:36px;border-radius:50%;background:${col};display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:#000;flex-shrink:0;">${p.name.slice(0,2)}</div>
        <div style="flex:1;min-width:0;">
          <div style="font-weight:700;font-size:14px;">${p.name}</div>
          <div style="height:4px;background:rgba(255,255,255,0.06);border-radius:100px;margin-top:4px;overflow:hidden;">
            <div style="height:100%;width:${barW}%;background:${col};border-radius:100px;"></div>
          </div>
        </div>
        <div style="font-family:'Black Han Sans',sans-serif;font-size:18px;color:#FFD700;flex-shrink:0;">${p.bestScore.toLocaleString()}<span style="font-size:11px;color:#555;font-family:'Noto Sans KR',sans-serif;font-weight:400;">점</span></div>
      </div>`;
    }).join('');
  } catch(e) {}
})();
</script>
"""

content = content.replace('</body>', RANK_JS + '\n</body>')

# Add game time info to each card
content = content.replace(
    '<div class="play-btn">▶ 플레이</div>\n      </a>\n\n      <a href="games/champion-tournament.html"',
    '<div style="font-size:11px;color:#555;margin-top:8px;">⏱ 20초</div>\n        <div class="play-btn">▶ 플레이</div>\n      </a>\n\n      <a href="games/champion-tournament.html"'
)
content = content.replace(
    '<div class="play-btn">▶ 플레이</div>\n      </a>\n\n      <a href="games/penalty-kick.html"',
    '<div style="font-size:11px;color:#555;margin-top:8px;">⏱ 10문제</div>\n        <div class="play-btn">▶ 플레이</div>\n      </a>\n\n      <a href="games/penalty-kick.html"'
)
content = content.replace(
    '<div class="play-btn">▶ 플레이</div>\n      </a>\n\n      <a href="games/uniform-quiz.html"',
    '<div style="font-size:11px;color:#555;margin-top:8px;">⏱ 5킥</div>\n        <div class="play-btn">▶ 플레이</div>\n      </a>\n\n      <a href="games/uniform-quiz.html"'
)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 라운드 6: 인덱스 라이브 랭킹 미리보기 + 게임 소요시간 표시")
