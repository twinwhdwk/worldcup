#!/usr/bin/env python3
"""사이클 4: 페널티킥 AI 패턴 학습"""
import os

REPO = "/home/claude/worldcup_minigame"
FILE = os.path.join(REPO, "games/penalty-kick.html")

AI_PATTERN_JS = """
// AI Pattern Learning
const playerHistory = { left: 0, center: 0, right: 0 };
function recordShot(dir) { playerHistory[dir]++; }
function getKeeperDive(dir) {
  const total = playerHistory.left + playerHistory.center + playerHistory.right;
  // After 3+ shots, AI starts learning
  if (total >= 3) {
    const mostUsed = Object.entries(playerHistory).sort((a,b)=>b[1]-a[1])[0][0];
    // 40% chance to dive toward most-used direction
    if (Math.random() < 0.4) return mostUsed;
  }
  // Default: biased toward shot direction
  if (dir === 'left') return Math.random() < 0.55 ? 'left' : 'right';
  if (dir === 'right') return Math.random() < 0.55 ? 'right' : 'left';
  return Math.random() < 0.5 ? 'left' : 'right';
}
"""

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if 'playerHistory' not in content:
    content = content.replace('<script>', '<script>\n' + AI_PATTERN_JS)
    # Replace old keeper dive logic
    content = content.replace(
        'let keeperDive;\n  if (dir === \'left\') {\n    keeperDive = Math.random() < 0.55 ? \'left\' : \'right\';\n  } else if (dir === \'right\') {\n    keeperDive = Math.random() < 0.55 ? \'right\' : \'left\';\n  } else {\n    keeperDive = Math.random() < 0.5 ? \'left\' : \'right\';\n  }',
        'recordShot(dir);\n  const keeperDive = getKeeperDive(dir);'
    )
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 사이클 4: AI 패턴 학습 추가")
else:
    print("이미 AI 패턴 있음")
