#!/usr/bin/env python3
"""사이클 1: Web Audio API 사운드 + 공통 애니메이션 개선"""
import re, os

REPO = "/home/claude/worldcup_minigame"

SOUND_JS = """
// ── Web Audio Sound System ──────────────────────────────
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let _ctx = null;
function getCtx() {
  if (!_ctx) _ctx = new AudioCtx();
  if (_ctx.state === 'suspended') _ctx.resume();
  return _ctx;
}
function playTone(freq, type, duration, vol=0.3, decay=0.8) {
  try {
    const ctx = getCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain); gain.connect(ctx.destination);
    osc.type = type; osc.frequency.value = freq;
    gain.gain.setValueAtTime(vol, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
    osc.start(); osc.stop(ctx.currentTime + duration);
  } catch(e) {}
}
function sfxCorrect() {
  playTone(523, 'sine', 0.12, 0.35);
  setTimeout(() => playTone(659, 'sine', 0.12, 0.35), 80);
  setTimeout(() => playTone(784, 'sine', 0.18, 0.35), 160);
}
function sfxWrong() {
  playTone(220, 'sawtooth', 0.25, 0.25);
  setTimeout(() => playTone(180, 'sawtooth', 0.2, 0.2), 120);
}
function sfxGoal() {
  [523,659,784,1047].forEach((f,i) => setTimeout(()=>playTone(f,'sine',0.22,0.4),i*70));
}
function sfxClick() { playTone(440, 'sine', 0.06, 0.15); }
// ────────────────────────────────────────────────────────
"""

def inject_sound(filepath, correct_calls, wrong_calls, extra=""):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'sfxCorrect' in content:
        print(f"  이미 사운드 있음: {filepath}")
        return
    # Inject before first <script> closing tag
    content = content.replace('<script>', '<script>\n' + SOUND_JS, 1)
    for c in correct_calls:
        content = content.replace(c, f'sfxCorrect(); {c}')
    for w in wrong_calls:
        content = content.replace(w, f'sfxWrong(); {w}')
    content += extra
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ 사운드 주입: {filepath}")

# player-country.html
pc = os.path.join(REPO, "games/player-country.html")
inject_sound(pc,
    correct_calls=["btn.classList.add('correct');"],
    wrong_calls=["btn.classList.add('wrong');"]
)

# champion-tournament.html
ct = os.path.join(REPO, "games/champion-tournament.html")
inject_sound(ct,
    correct_calls=["btn.classList.add('correct');"],
    wrong_calls=["btn.classList.add('wrong');"]
)

# penalty-kick.html
pk = os.path.join(REPO, "games/penalty-kick.html")
with open(pk, 'r', encoding='utf-8') as f:
    content = f.read()
if 'sfxGoal' not in content:
    content = content.replace('<script>', '<script>\n' + SOUND_JS, 1)
    content = content.replace("flash.className = 'goal-flash goal-anim';", "flash.className = 'goal-flash goal-anim'; sfxGoal();")
    content = content.replace("flash.className = 'goal-flash miss-anim';", "flash.className = 'goal-flash miss-anim'; sfxWrong();")
    with open(pk, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ 사운드 주입: {pk}")

# uniform-quiz.html
uq = os.path.join(REPO, "games/uniform-quiz.html")
inject_sound(uq,
    correct_calls=["btn.classList.add('correct');"],
    wrong_calls=["btn.classList.add('wrong');"]
)

print("사이클 1 완료: 사운드 효과 추가됨")
