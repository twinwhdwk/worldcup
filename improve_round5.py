#!/usr/bin/env python3
"""라운드 5: 스코어보드 - 게임별 TOP3 탭 + 실시간 그래프"""
import os

REPO = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(REPO, 'scoreboard.html')

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if 'tab-btn' in content:
    print("이미 탭 있음"); exit()

# Add tab CSS
TAB_CSS = """
    /* Tabs */
    .tabs {
      display: flex;
      gap: 6px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }
    .tab-btn {
      padding: 8px 16px;
      border-radius: 100px;
      border: 1.5px solid rgba(255,255,255,0.08);
      background: transparent;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      font-family: 'Noto Sans KR', sans-serif;
      transition: all 0.2s;
    }
    .tab-btn.active {
      background: var(--green);
      border-color: var(--green);
      color: #fff;
    }
    .tab-btn:hover:not(.active) { border-color: rgba(255,255,255,0.2); color: var(--text); }

    /* Prize section */
    .prize-section {
      background: linear-gradient(135deg, rgba(255,215,0,0.08), rgba(255,215,0,0.02));
      border: 1px solid rgba(255,215,0,0.15);
      border-radius: 16px;
      padding: 16px 20px;
      margin-bottom: 16px;
    }
    .prize-header {
      font-size: 12px;
      color: var(--gold);
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 10px;
      font-weight: 700;
    }
    .prize-row {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 6px 0;
      font-size: 14px;
      border-bottom: 1px solid rgba(255,255,255,0.04);
    }
    .prize-row:last-child { border-bottom: none; }
"""

content = content.replace('</style>', TAB_CSS + '\n  </style>')

# Add tabs HTML before rank-list
TABS_HTML = """  <div class="tabs" id="tabs">
    <button class="tab-btn active" onclick="setTab('all')">🌐 전체 종합</button>
    <button class="tab-btn" onclick="setTab('선수퀴즈')">🕵️ 선수퀴즈</button>
    <button class="tab-btn" onclick="setTab('우승국퀴즈')">🏆 우승국</button>
    <button class="tab-btn" onclick="setTab('페널티킥')">🥅 페널티킥</button>
    <button class="tab-btn" onclick="setTab('유니폼퀴즈')">👕 유니폼</button>
  </div>
  <div class="prize-section" id="prize-section" style="display:none;">
    <div class="prize-header">🏅 상품 수여 대상 (TOP 10)</div>
    <div id="prize-list"></div>
  </div>

"""

content = content.replace(
    '<div class="rank-list" id="rank-list">',
    TABS_HTML + '<div class="rank-list" id="rank-list">'
)

# Add tab JS
TAB_JS = """
let currentTab = 'all';
function setTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  const prizeSection = document.getElementById('prize-section');
  if (tab === 'all') {
    prizeSection.style.display = 'block';
    renderPrize();
  } else {
    prizeSection.style.display = 'none';
  }
  render(loadData());
}

function renderPrize() {
  const data = loadData();
  const sorted = [...data.players].sort((a,b) => b.bestScore - a.bestScore).slice(0, 10);
  const list = document.getElementById('prize-list');
  if (!list) return;
  list.innerHTML = sorted.map((p, i) => {
    const icons = ['🥇','🥈','🥉','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'];
    return `<div class="prize-row">
      <span>${icons[i]}</span>
      <span style="font-weight:700;flex:1">${p.name}</span>
      <span style="color:var(--gold);font-weight:700">${p.bestScore.toLocaleString()}점</span>
    </div>`;
  }).join('') || '<div style="color:var(--muted);font-size:13px;">아직 기록 없음</div>';
}
"""

content = content.replace('// ── Data ─────────────────────────────────────────', TAB_JS + '\n// ── Data ─────────────────────────────────────────')

# Modify render to filter by tab
content = content.replace(
    '  const sorted = [...data.players].sort((a, b) => b.bestScore - a.bestScore).slice(0, MAX_RANK);',
    """  let filtered = data.players;
  if (currentTab !== 'all') {
    // Filter log for this game, rebuild player list
    const gameLog = data.log.filter(e => e.game === currentTab);
    const tempPlayers = {};
    gameLog.forEach(e => {
      if (!tempPlayers[e.name] || e.score > tempPlayers[e.name]) tempPlayers[e.name] = e.score;
    });
    filtered = Object.entries(tempPlayers).map(([name, bestScore]) => ({
      name, bestScore, games: gameLog.filter(e=>e.name===name).length, lastGame: currentTab,
      totalScore: gameLog.filter(e=>e.name===name).reduce((a,b)=>a+b.score,0)
    }));
  }
  const sorted = [...filtered].sort((a, b) => b.bestScore - a.bestScore).slice(0, MAX_RANK);"""
)

# Update addScore to also refresh prize
content = content.replace(
    'render(data);\n\n  nameEl.value',
    'render(data);\n  if (currentTab === "all") renderPrize();\n\n  nameEl.value'
)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 라운드 5: 스코어보드 게임별 탭 + TOP10 상품 목록 추가")
