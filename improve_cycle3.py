#!/usr/bin/env python3
"""사이클 3: 우승국 퀴즈 - 타이머 추가"""
import os, re

REPO = "/home/claude/worldcup_minigame"
FILE = os.path.join(REPO, "games/champion-tournament.html")

TIMER_CSS = """
    .q-timer-bar-wrap {
      width: 100%;
      height: 4px;
      background: rgba(255,215,0,0.1);
      border-radius: 100px;
      margin-bottom: 16px;
      overflow: hidden;
    }
    #q-timer-bar {
      height: 100%;
      background: var(--gold);
      border-radius: 100px;
      transition: width 0.2s linear;
      width: 100%;
    }
"""

TIMER_HTML = '      <div class="q-timer-bar-wrap"><div id="q-timer-bar"></div></div>\n'

TIMER_JS = """
let qTimeLeft = 15, qTimerInterval;
function startQTimer() {
  clearInterval(qTimerInterval);
  qTimeLeft = 15;
  const bar = document.getElementById('q-timer-bar');
  if (!bar) return;
  bar.style.width = '100%';
  bar.style.background = 'var(--gold)';
  qTimerInterval = setInterval(() => {
    qTimeLeft--;
    if (!bar) return;
    bar.style.width = (qTimeLeft / 15 * 100) + '%';
    if (qTimeLeft <= 5) bar.style.background = '#ef4444';
    if (qTimeLeft <= 0) {
      clearInterval(qTimerInterval);
      // Auto-wrong if not answered
      const btns = document.querySelectorAll('.opt-btn:not(:disabled)');
      if (btns.length > 0) {
        document.querySelectorAll('.opt-btn').forEach(b => b.disabled = true);
        const q = questions[currentQ];
        const fb = document.getElementById('feedback');
        document.querySelectorAll('.opt-btn').forEach(b => {
          if (b.textContent.includes(q.winner.replace(/^.+? /, ''))) b.classList.add('correct');
        });
        fb.className = 'feedback-area wrong';
        fb.textContent = `⏰ 시간 초과! 정답: ${q.winner}`;
        history.push({ year: q.year, winner: q.winner, correct: false });
        currentQ++;
        updateHUD();
        setTimeout(() => { if (currentQ >= TOTAL) showResult(); else setQuestion(); }, 1200);
      }
    }
  }, 1000);
}
"""

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if 'q-timer-bar' not in content:
    content = content.replace('</style>', TIMER_CSS + '\n    </style>')
    content = content.replace('<div class="q-card">', TIMER_HTML + '    <div class="q-card">')
    content = content.replace('<script>', '<script>\n' + TIMER_JS)
    content = content.replace('function setQuestion() {', 'function setQuestion() {\n  startQTimer();')
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 사이클 3: 문제별 타이머 추가")
else:
    print("이미 타이머 있음")
