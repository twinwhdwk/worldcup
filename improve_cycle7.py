#!/usr/bin/env python3
"""사이클 7: 애니메이션 강화 + 파티클 효과"""
import os, re

REPO = os.path.dirname(os.path.abspath(__file__))

CONFETTI_JS = """
// ── Confetti System ─────────────────────────────
function launchConfetti(x, y, count=18) {
  const colors = ['#FFD700','#00843D','#ef4444','#3b82f6','#a855f7','#fff'];
  for (let i = 0; i < count; i++) {
    const el = document.createElement('div');
    el.style.cssText = `
      position:fixed; width:${6+Math.random()*6}px; height:${6+Math.random()*6}px;
      background:${colors[Math.floor(Math.random()*colors.length)]};
      border-radius:${Math.random()>0.5?'50%':'2px'};
      left:${x}px; top:${y}px; pointer-events:none; z-index:9999;
      transform:rotate(${Math.random()*360}deg);
    `;
    document.body.appendChild(el);
    const angle = (Math.random() * 360) * Math.PI / 180;
    const speed = 80 + Math.random() * 120;
    const vx = Math.cos(angle) * speed;
    const vy = Math.sin(angle) * speed - 60;
    let px = x, py = y, vy2 = vy, t = 0;
    const tick = () => {
      t += 0.016; px += vx * 0.016; vy2 += 200 * 0.016; py += vy2 * 0.016;
      el.style.left = px + 'px'; el.style.top = py + 'px';
      el.style.opacity = Math.max(0, 1 - t * 1.5);
      el.style.transform = `rotate(${t*200}deg)`;
      if (t < 0.8) requestAnimationFrame(tick); else el.remove();
    };
    requestAnimationFrame(tick);
  }
}
function launchFullConfetti() {
  for (let i = 0; i < 4; i++) setTimeout(() => launchConfetti(Math.random()*window.innerWidth, -10, 12), i*150);
}
// ────────────────────────────────────────────────
"""

SCORE_POP_CSS = """
    @keyframes scorePop {
      0% { transform: scale(0) translateY(0); opacity: 1; }
      60% { transform: scale(1.3) translateY(-30px); opacity: 1; }
      100% { transform: scale(1) translateY(-60px); opacity: 0; }
    }
    .score-pop {
      position: fixed; font-family: 'Black Han Sans', sans-serif;
      font-size: 28px; font-weight: 900; pointer-events: none; z-index: 9998;
      animation: scorePop 0.7s ease forwards;
      text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }
"""

def add_score_pop(filepath, score_color='#FFD700'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'launchConfetti' in content:
        print(f"  이미 있음: {filepath}"); return
    content = content.replace('</style>', SCORE_POP_CSS + '\n    </style>')
    content = content.replace('<script>', '<script>\n' + CONFETTI_JS)

    # Inject confetti on correct answer in each game
    content = content.replace(
        "fb.className = 'feedback correct';",
        "fb.className = 'feedback correct'; launchFullConfetti();"
    )
    content = content.replace(
        "fb.className = 'feedback-area correct';",
        "fb.className = 'feedback-area correct'; launchFullConfetti();"
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ 파티클 추가: {filepath}")

games_dir = os.path.join(REPO, 'games')
for f in ['player-country.html', 'champion-tournament.html', 'uniform-quiz.html']:
    add_score_pop(os.path.join(games_dir, f))

# Penalty kick: confetti on goal
pk = os.path.join(games_dir, 'penalty-kick.html')
with open(pk, 'r', encoding='utf-8') as f:
    content = f.read()
if 'launchConfetti' not in content:
    content = content.replace('<script>', '<script>\n' + CONFETTI_JS)
    content = content.replace(
        "flash.className = 'goal-flash goal-anim'; sfxGoal();",
        "flash.className = 'goal-flash goal-anim'; sfxGoal(); launchFullConfetti();"
    )
    with open(pk, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ 파티클 추가: {pk}")

print("사이클 7 완료: 파티클/애니메이션 강화")
