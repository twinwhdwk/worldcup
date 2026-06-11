#!/usr/bin/env python3
"""사이클 9: 난이도 조절 + 콤보 배율 강화"""
import os

REPO = os.path.dirname(os.path.abspath(__file__))

# player-country: 더 복잡한 콤보 시스템
COMBO_UPGRADE = """
// ── Upgraded Combo System ───────────────────────
const COMBO_THRESHOLDS = [
  { min: 0,  mult: 1,   label: '',        color: '#aaa' },
  { min: 3,  mult: 1.5, label: '🔥 콤보!', color: '#f97316' },
  { min: 5,  mult: 2,   label: '💥 더블!', color: '#ef4444' },
  { min: 8,  mult: 3,   label: '⚡ 트리플!',color: '#a855f7' },
  { min: 12, mult: 4,   label: '🌟 GODMODE!',color: '#FFD700' },
];
function getCombo(streak) {
  let tier = COMBO_THRESHOLDS[0];
  for (const t of COMBO_THRESHOLDS) { if (streak >= t.min) tier = t; }
  return tier;
}
// ────────────────────────────────────────────────
"""

pc_path = os.path.join(REPO, 'games', 'player-country.html')
with open(pc_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'COMBO_THRESHOLDS' not in content:
    content = content.replace('<script>', '<script>\n' + COMBO_UPGRADE)
    # Replace simple pts calculation
    old_pts = "const bonus = Math.floor(streak / 3);\n    const pts = 100 + bonus * 50;"
    new_pts = "const combo = getCombo(streak);\n    const pts = Math.round(100 * combo.mult);"
    if old_pts in content:
        content = content.replace(old_pts, new_pts)
        content = content.replace(
            "fb.textContent = streak >= 3 ? `🔥 정답! +${pts}점 (콤보!)` : `✅ 정답! +${pts}점`;",
            "const cmb = getCombo(streak); fb.textContent = cmb.label ? `${cmb.label} +${pts}점` : `✅ 정답! +${pts}점`; fb.style.color = cmb.color;"
        )
    with open(pc_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 사이클 9: 선수퀴즈 콤보 시스템 강화")
else:
    print("이미 콤보 시스템 있음")

# uniform-quiz: 연속 오답시 힌트 자동 공개
uq_path = os.path.join(REPO, 'games', 'uniform-quiz.html')
with open(uq_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'wrongStreak' not in content:
    WRONG_STREAK = """
let wrongStreak = 0;
function checkAutoHint() {
  if (wrongStreak >= 2) {
    const hintEl = document.getElementById('auto-hint');
    if (hintEl && currentTeam) {
      hintEl.textContent = '💡 자동 힌트: ' + currentTeam.clues[0];
      hintEl.style.display = 'block';
    }
  }
}
"""
    content = content.replace('<script>', '<script>\n' + WRONG_STREAK)
    content = content.replace(
        "btn.classList.add('wrong');",
        "btn.classList.add('wrong'); wrongStreak++; checkAutoHint();"
    )
    content = content.replace(
        "btn.classList.add('correct');",
        "btn.classList.add('correct'); wrongStreak = 0; document.getElementById('auto-hint') && (document.getElementById('auto-hint').style.display='none');"
    )
    content = content.replace(
        '<div class="feedback" id="feedback"></div>',
        '<div id="auto-hint" style="display:none;font-size:13px;color:#f97316;margin-bottom:8px;"></div>\n      <div class="feedback" id="feedback"></div>'
    )
    with open(uq_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 사이클 9: 유니폼 퀴즈 자동 힌트 추가")

print("사이클 9 완료")
