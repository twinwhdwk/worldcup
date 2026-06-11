#!/usr/bin/env python3
"""라운드 3: 유니폼 퀴즈 - 원정 유니폼 추가 + 스트릭 보너스"""
import os, re

REPO = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(REPO, 'games', 'uniform-quiz.html')

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if 'away' in content and 'awayJersey' in content:
    print("이미 원정 유니폼 있음"); exit()

# Add away jerseys to teams - inject after each home definition
AWAY_ADDITIONS = [
    ("🇧🇷 브라질", "away", ["#003087","#003087","#FFD700"], "solid", "원정 유니폼", ["파란 유니폼", "원정 착용", "삼바의 나라"]),
    ("🇩🇪 독일", "away", ["#000000","#ffffff","#cc0000"], "solid", "원정 유니폼", ["검은 상의", "어웨이 유니폼", "독수리 엠블럼"]),
    ("🇦🇷 아르헨티나", "away", ["#003189","#74ACDF","#003189"], "solid", "원정 유니폼", ["진한 파란색", "남미 강국", "메시의 나라"]),
    ("🇫🇷 프랑스", "away", ["#ffffff","#003189","#ffffff"], "collar-stripe", "원정 유니폼", ["흰색 상의", "파란 포인트", "레 블뢰"]),
    ("🇰🇷 대한민국", "away", ["#ffffff","#C60C30","#003478"], "collar-stripe", "원정 유니폼", ["흰색 상의", "붉은 포인트", "태극 마크"]),
]

# Add away jersey toggle to JS
AWAY_JS = """
let showAway = false;
function toggleJersey() {
  showAway = !showAway;
  const btn = document.getElementById('toggle-jersey-btn');
  if (btn) btn.textContent = showAway ? '🔄 홈 유니폼 보기' : '🔄 원정 유니폼 보기';
  setQuestion();
}
"""

if 'toggleJersey' not in content:
    content = content.replace('<script>', '<script>\n' + AWAY_JS)

# Add toggle button in jersey card
if 'toggle-jersey-btn' not in content:
    content = content.replace(
        '<div class="clues" id="clues">',
        '<div style="text-align:center;margin-bottom:12px;"><button id="toggle-jersey-btn" onclick="toggleJersey()" style="background:rgba(168,85,247,0.15);border:1px solid rgba(168,85,247,0.3);color:var(--purple);border-radius:100px;padding:8px 18px;font-size:13px;cursor:pointer;font-family:\'Noto Sans KR\',sans-serif;">🔄 원정 유니폼 보기</button></div>\n      <div class="clues" id="clues">'
    )

# Update setQuestion to use away jersey when toggled
content = content.replace(
    "const jd = document.getElementById('jersey-display');\n    const j = currentTeam.home;",
    """const jd = document.getElementById('jersey-display');
    const j = (showAway && currentTeam.away) ? currentTeam.away : currentTeam.home;"""
)

# Add away data to a few teams
content = content.replace(
    '    name: "🇧🇷 브라질", flag: "🇧🇷",\n    home:',
    '    name: "🇧🇷 브라질", flag: "🇧🇷",\n    away: { colors: ["#003087","#003087","#FFD700"], pattern: "solid", label: "원정 유니폼" },\n    home:'
)
content = content.replace(
    '    name: "🇩🇪 독일", flag: "🇩🇪",\n    home:',
    '    name: "🇩🇪 독일", flag: "🇩🇪",\n    away: { colors: ["#000000","#ffffff","#cc0000"], pattern: "solid", label: "원정 유니폼" },\n    home:'
)
content = content.replace(
    '    name: "🇦🇷 아르헨티나", flag: "🇦🇷",\n    home:',
    '    name: "🇦🇷 아르헨티나", flag: "🇦🇷",\n    away: { colors: ["#003189","#74ACDF","#003189"], pattern: "solid", label: "원정 유니폼" },\n    home:'
)
content = content.replace(
    '    name: "🇫🇷 프랑스", flag: "🇫🇷",\n    home:',
    '    name: "🇫🇷 프랑스", flag: "🇫🇷",\n    away: { colors: ["#ffffff","#003189","#ffffff"], pattern: "collar-stripe", label: "원정 유니폼" },\n    home:'
)
content = content.replace(
    '    name: "🇰🇷 대한민국", flag: "🇰🇷",\n    home:',
    '    name: "🇰🇷 대한민국", flag: "🇰🇷",\n    away: { colors: ["#ffffff","#C60C30","#003478"], pattern: "collar-stripe", label: "원정 유니폼" },\n    home:'
)

# Add streak bonus CSS
STREAK_CSS = """
    .streak-bar {
      text-align: center;
      font-size: 13px;
      color: #f97316;
      min-height: 20px;
      margin-bottom: 4px;
      font-weight: 700;
    }
"""
if 'streak-bar' not in content:
    content = content.replace('</style>', STREAK_CSS + '\n    </style>')
    content = content.replace(
        '<div class="timer-bar-wrap">',
        '<div class="streak-bar" id="streak-bar"></div>\n    <div class="timer-bar-wrap">'
    )
    # Track streak in JS
    content = content.replace(
        'let score = 0, timeLeft = 30, qNum = 0, totalQ = 0, correctQ = 0;',
        'let score = 0, timeLeft = 30, qNum = 0, totalQ = 0, correctQ = 0, streak = 0;'
    )
    content = content.replace(
        "  document.getElementById('score-val').textContent = score;",
        """  document.getElementById('score-val').textContent = score;
  const sb = document.getElementById('streak-bar');
  if (sb) { sb.textContent = streak >= 3 ? '🔥 ' + streak + '연속 정답!' : ''; }"""
    )
    # Increment streak on correct
    content = content.replace(
        "correctQ++;\n    btn.classList.add('correct');",
        "correctQ++; streak++;\n    btn.classList.add('correct');"
    )
    content = content.replace(
        "  document.querySelectorAll('.opt-btn').forEach(b => {\n      if (b.textContent.trim() === currentTeam.name) b.classList.add('correct');\n    });\n    fb.className = 'feedback wrong';",
        "  streak = 0;\n  document.querySelectorAll('.opt-btn').forEach(b => {\n      if (b.textContent.trim() === currentTeam.name) b.classList.add('correct');\n    });\n    fb.className = 'feedback wrong';"
    )

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 라운드 3: 유니폼 퀴즈 원정 유니폼 + 스트릭 추가")
