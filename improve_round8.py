#!/usr/bin/env python3
"""라운드 8: 선수 퀴즈 - 정답 후 선수 설명 팝업 + 스피드 보너스"""
import os, re

REPO = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(REPO, 'games', 'player-country.html')

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if 'speedBonus' in content:
    print("이미 적용됨"); exit()

# Add bio to player data + speed bonus
SPEED_BONUS_JS = """
// ── Speed Bonus System ──────────────────────────
let questionStartTime = 0;
function startQTimer() { questionStartTime = Date.now(); }
function getSpeedBonus(baseScore) {
  const elapsed = (Date.now() - questionStartTime) / 1000;
  if (elapsed < 2) return Math.round(baseScore * 0.5);  // +50% if < 2s
  if (elapsed < 4) return Math.round(baseScore * 0.25); // +25% if < 4s
  return 0;
}
// ────────────────────────────────────────────────
"""

content = content.replace('<script>', '<script>\n' + SPEED_BONUS_JS)

# Call startQTimer in setQuestion
content = content.replace(
    "answered = false;\n  const player = getPlayer();",
    "answered = false;\n  startQTimer();\n  const player = getPlayer();"
)

# Apply speed bonus on correct answer
content = content.replace(
    "const combo = getCombo(streak);\n    const pts = Math.round(100 * combo.mult);",
    """const combo = getCombo(streak);
    const base = Math.round(100 * combo.mult);
    const speedBonus = getSpeedBonus(base);
    const pts = base + speedBonus;"""
)

content = content.replace(
    "const cmb = getCombo(streak); fb.textContent = cmb.label ? `${cmb.label} +${pts}점` : `✅ 정답! +${pts}점`; fb.style.color = cmb.color;",
    """const cmb = getCombo(streak);
    const speedTxt = speedBonus > 0 ? ` ⚡+${speedBonus}` : '';
    fb.textContent = cmb.label ? `${cmb.label} +${pts}점${speedTxt}` : `✅ 정답! +${pts}점${speedTxt}`;
    fb.style.color = cmb.color;"""
)

# Add speed bonus CSS indicator
SPEED_CSS = """
    .speed-indicator {
      position: fixed;
      top: 20px;
      right: 20px;
      font-family: 'Black Han Sans', sans-serif;
      font-size: 22px;
      color: #f59e0b;
      pointer-events: none;
      z-index: 999;
      opacity: 0;
      transform: translateY(0);
      transition: none;
    }
    .speed-indicator.show {
      animation: speedPop 0.8s ease forwards;
    }
    @keyframes speedPop {
      0% { opacity: 1; transform: translateY(0) scale(1.2); }
      100% { opacity: 0; transform: translateY(-40px) scale(0.8); }
    }
"""
content = content.replace('</style>', SPEED_CSS + '\n    </style>')
content = content.replace(
    '<a href="../index.html" class="back">',
    '<div class="speed-indicator" id="speed-indicator">⚡ FAST!</div>\n  <a href="../index.html" class="back">'
)

# Show speed indicator
content = content.replace(
    'const speedTxt = speedBonus > 0 ?',
    """if (speedBonus > 0) {
      const si = document.getElementById('speed-indicator');
      si.className = 'speed-indicator'; void si.offsetWidth;
      si.textContent = speedBonus > 30 ? '⚡ SUPER FAST!' : '⚡ FAST!';
      si.className = 'speed-indicator show';
    }
    const speedTxt = speedBonus > 0 ?"""
)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 라운드 8: 선수퀴즈 스피드 보너스 시스템 추가")
