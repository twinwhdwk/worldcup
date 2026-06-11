#!/usr/bin/env python3
"""라운드 7: 페널티킥 - 동점시 연장전(서든데스) + 결과 애니메이션"""
import os, re

REPO = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(REPO, 'games', 'penalty-kick.html')

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if 'suddenDeath' in content:
    print("이미 적용됨"); exit()

SUDDEN_DEATH_JS = """
// ── Sudden Death Overtime ───────────────────────
let isSuddenDeath = false;
let sdRound = 0;
const MAX_SD = 3; // max 3 sudden death rounds

function checkSuddenDeath() {
  const saves = MAX_KICKS - goals;
  // If 2-2 or 3-3 after 5 kicks → sudden death
  if (goals === saves && goals >= 2) {
    isSuddenDeath = true;
    sdRound = 0;
    document.getElementById('instruction').textContent = '⚡ 연장전! 서든데스 시작!';
    // Flash overlay
    const flash = document.createElement('div');
    flash.style.cssText = 'position:fixed;inset:0;background:rgba(239,68,68,0.15);z-index:50;pointer-events:none;';
    document.body.appendChild(flash);
    setTimeout(() => flash.remove(), 600);
    // Add extra dots
    const ks = document.getElementById('kick-score');
    const sep = document.createElement('div');
    sep.style.cssText = 'color:#ef4444;font-size:12px;font-weight:700;align-self:center;';
    sep.textContent = '⚡SD';
    ks.appendChild(sep);
    for (let i = 0; i < MAX_SD; i++) {
      const d = document.createElement('div');
      d.className = 'kick-dot';
      d.id = 'dot-sd-' + i;
      d.textContent = '⚽';
      ks.appendChild(d);
    }
    return true;
  }
  return false;
}

function recordSuddenDeath(isGoal) {
  const dot = document.getElementById('dot-sd-' + sdRound);
  if (dot) {
    dot.textContent = isGoal ? '✅' : '❌';
    dot.classList.add(isGoal ? 'goal' : 'miss');
  }
  sdRound++;
  if (isGoal) {
    goals++;
    setTimeout(showResult, 1200);
    return true;
  }
  if (sdRound >= MAX_SD) {
    setTimeout(showResult, 1200);
    return true;
  }
  return false;
}
// ────────────────────────────────────────────────
"""

content = content.replace('<script>', '<script>\n' + SUDDEN_DEATH_JS)

# Modify showResult call in shoot() to check sudden death first
content = content.replace(
    '      if (kickNum >= MAX_KICKS) {\n        setTimeout(showResult, 300);\n      } else {',
    """      if (kickNum >= MAX_KICKS) {
        if (isSuddenDeath) {
          // continue sudden death
          document.getElementById('shoot-btn').disabled = false;
          document.getElementById('instruction').textContent = '⚡ 서든데스! 슛 버튼을 누르세요';
        } else if (checkSuddenDeath()) {
          setTimeout(() => {
            document.getElementById('shoot-btn').disabled = false;
          }, 800);
        } else {
          setTimeout(showResult, 300);
        }
      } else {"""
)

# Modify shoot to handle sudden death scoring
content = content.replace(
    '    if (isGoal) {\n      goals++;\n      flash.className = \'goal-flash goal-anim\';',
    """    if (isGoal) {
      if (!isSuddenDeath) goals++;
      flash.className = 'goal-flash goal-anim';"""
)

# After miss in sudden death
old_miss_block = "    } else {\n      flash.className = 'goal-flash miss-anim';"
new_miss_block = """    } else {
      flash.className = 'goal-flash miss-anim';"""
content = content.replace(old_miss_block, new_miss_block, 1)

# Add sudden death info to result screen
content = content.replace(
    "document.getElementById('res-msg').textContent = msg;",
    """document.getElementById('res-msg').textContent = msg + (isSuddenDeath ? ' (서든데스 포함)' : '');"""
)

# Sudden death in restart
content = content.replace(
    'function resetGame() {\n  kickNum = 0; goals = 0; level = 1; keeperSpeed = 0.4;',
    'function resetGame() {\n  kickNum = 0; goals = 0; level = 1; keeperSpeed = 0.4; isSuddenDeath = false; sdRound = 0;'
)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 라운드 7: 페널티킥 서든데스 연장전 추가")
