#!/usr/bin/env python3
"""라운드 9: 우승국 퀴즈 - 최종 보스(전설 문제) + 진행바 애니메이션"""
import os, re

REPO = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(REPO, 'games', 'champion-tournament.html')

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if 'BOSS_QUESTIONS' in content:
    print("이미 적용됨"); exit()

BOSS_JS = """
// ── Boss Question System ────────────────────────
const BOSS_QUESTIONS = [
  {
    year: "??", host: "???", winner: "🇧🇷 브라질", flag: "🇧🇷",
    topScorer: "저스트 퐁테인 13골 (역대 최다)", mvp: "디지",
    hints: ["득점왕이 13골을 넣은 대회", "유럽 개최", "17세 슈퍼스타 데뷔"],
    extra: "퐁테인의 13골 기록은 60년 넘게 깨지지 않음",
    isBoss: true, bossLabel: "🔥 LEGEND QUESTION"
  },
  {
    year: "??", host: "???", winner: "🇦🇷 아르헨티나", flag: "🇦🇷",
    topScorer: "게리 리네커 (잉글랜드 6골)", mvp: "디에고 마라도나",
    hints: ["신의 손 골이 나온 대회", "세기의 골 선정", "중미 개최"],
    extra: "마라도나가 혼자 팀을 우승으로 이끈 대회",
    isBoss: true, bossLabel: "🔥 LEGEND QUESTION"
  },
  {
    year: "??", host: "???", winner: "🇩🇪 독일", flag: "🇩🇪",
    topScorer: "하메스 로드리게스 6골", mvp: "리오넬 메시",
    hints: ["개최국이 1-7로 대패한 대회", "남미 개최", "브라질의 치욕"],
    extra: "미네이랑의 비극 - 브라질 7골 허용",
    isBoss: true, bossLabel: "🔥 LEGEND QUESTION"
  },
];

let bossUsed = false;
function maybeInjectBoss(questionsArr) {
  if (bossUsed) return questionsArr;
  // Replace last question with a boss question
  const boss = BOSS_QUESTIONS[Math.floor(Math.random() * BOSS_QUESTIONS.length)];
  const result = [...questionsArr];
  result[result.length - 1] = boss;
  bossUsed = true;
  return result;
}
// ────────────────────────────────────────────────
"""

content = content.replace('<script>', '<script>\n' + BOSS_JS)

# Inject boss into questions after shuffle
content = content.replace(
    "questions = shuffle(WORLD_CUPS).slice(0, TOTAL);",
    "questions = maybeInjectBoss(shuffle(WORLD_CUPS).slice(0, TOTAL));"
)

# Reset boss used on restart
content = content.replace(
    "score = 0; correctCount = 0; currentQ = 0; history = [];",
    "score = 0; correctCount = 0; currentQ = 0; history = []; bossUsed = false;"
)

# Show boss label in UI
content = content.replace(
    "document.getElementById('year-badge').textContent = q.year;",
    """const isBoss = q.isBoss;
    const badge = document.getElementById('year-badge');
    badge.textContent = q.year;
    badge.style.background = isBoss ? '#ef4444' : 'var(--gold)';
    badge.style.color = isBoss ? '#fff' : '#000';
    badge.style.fontSize = isBoss ? '28px' : '48px';
    const bossEl = document.getElementById('boss-label');
    if (bossEl) bossEl.textContent = isBoss ? (q.bossLabel || '🔥 BOSS') : '';"""
)

# Add boss label HTML
content = content.replace(
    '<div class="year-badge" id="year-badge">????</div>',
    '<div id="boss-label" style="color:#ef4444;font-size:13px;font-weight:700;letter-spacing:2px;margin-bottom:4px;min-height:18px;"></div>\n      <div class="year-badge" id="year-badge">????</div>'
)

# Boss questions give 200pts
content = content.replace(
    "const pts = hintRevealed ? 50 : 100;",
    "const pts = q.isBoss ? (hintRevealed ? 100 : 200) : (hintRevealed ? 50 : 100);"
)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 라운드 9: 우승국 퀴즈 최종 보스 문제 추가 (200점)")
