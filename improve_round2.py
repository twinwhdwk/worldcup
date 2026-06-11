#!/usr/bin/env python3
"""라운드 2: 선수 퀴즈 - 난이도별 문제 분류 + 국기 크게 표시"""
import os

REPO = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(REPO, 'games', 'player-country.html')

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if 'difficulty' in content:
    print("이미 적용됨"); exit()

# Add difficulty badges and flag display to player data
OLD_PLAYERS_START = "const PLAYERS = ["
NEW_PLAYERS = """const PLAYERS = [
  // ⭐ 쉬움
  { name: "리오넬 메시", country: "🇦🇷 아르헨티나", flag: "🇦🇷", emoji: "🐐", diff: 1, hints: ["발롱도르 8회", "PSG, 바르셀로나", "왼발잡이"] },
  { name: "크리스티아누 호날두", country: "🇵🇹 포르투갈", flag: "🇵🇹", emoji: "💪", diff: 1, hints: ["발롱도르 5회", "맨유, 레알, 유벤투스", "CR7"] },
  { name: "킬리안 음바페", country: "🇫🇷 프랑스", flag: "🇫🇷", emoji: "⚡", diff: 1, hints: ["2018 월드컵 우승", "파리 출신", "레알 마드리드"] },
  { name: "네이마르", country: "🇧🇷 브라질", flag: "🇧🇷", emoji: "🎪", diff: 1, hints: ["삼바 드리블", "바르셀로나 출신", "노란 유니폼"] },
  { name: "손흥민", country: "🇰🇷 대한민국", flag: "🇰🇷", emoji: "🦁", diff: 1, hints: ["토트넘 전설", "프리미어리그 득점왕", "왼발잡이"] },
  { name: "엘링 홀란", country: "🇳🇴 노르웨이", flag: "🇳🇴", emoji: "🤖", diff: 1, hints: ["득점 기계", "맨시티", "아버지도 프로선수"] },
  { name: "케빈 데 브루이너", country: "🇧🇪 벨기에", flag: "🇧🇪", emoji: "🎯", diff: 1, hints: ["패스 마스터", "맨시티 미드필더", "적혈마"] },
  { name: "모하메드 살라", country: "🇪🇬 이집트", flag: "🇪🇬", emoji: "🌙", diff: 1, hints: ["이집트의 왕", "리버풀", "왼발잡이 윙어"] },
  // ⭐⭐ 보통
  { name: "비르힐 판 다이크", country: "🇳🇱 네덜란드", flag: "🇳🇱", emoji: "🗼", diff: 2, hints: ["리버풀 수비수", "189cm", "오렌지 군단"] },
  { name: "루카 모드리치", country: "🇭🇷 크로아티아", flag: "🇭🇷", emoji: "🌟", diff: 2, hints: ["2018 황금공", "레알 미드필더", "체스 천재"] },
  { name: "로베르트 레반도프스키", country: "🇵🇱 폴란드", flag: "🇵🇱", emoji: "🎯", diff: 2, hints: ["분데스리가 득점왕", "바이에른 출신", "바르셀로나"] },
  { name: "해리 케인", country: "🏴󠁧󠁢󠁥󠁮󠁧󠁿 잉글랜드", flag: "🏴󠁧󠁢󠁥󠁮󠁧󠁿", emoji: "👑", diff: 2, hints: ["토트넘 전설", "바이에른 뮌헨", "잉글랜드 스트라이커"] },
  { name: "안토인 그리즈만", country: "🇫🇷 프랑스", flag: "🇫🇷", emoji: "💃", diff: 2, hints: ["춤 세리머니", "아틀레티코 마드리드", "2018 우승"] },
  { name: "부카요 사카", country: "🏴󠁧󠁢󠁥󠁮󠁧󠁿 잉글랜드", flag: "🏴󠁧󠁢󠁥󠁮󠁧󠁿", emoji: "🚀", diff: 2, hints: ["아스날 에이스", "멀티 포지션", "어린 스타"] },
  { name: "페드리", country: "🇪🇸 스페인", flag: "🇪🇸", emoji: "🎭", diff: 2, hints: ["바르셀로나 미드필더", "어린 천재", "2020 올림픽"] },
  { name: "이강인", country: "🇰🇷 대한민국", flag: "🇰🇷", emoji: "⚽", diff: 2, hints: ["PSG 미드필더", "2019 U-20 황금공", "마요르카 출신"] },
  { name: "카림 벤제마", country: "🇫🇷 프랑스", flag: "🇫🇷", emoji: "🔥", diff: 2, hints: ["2022 발롱도르", "레알 마드리드", "메시 없는 사이 최고"] },
  { name: "비니시우스 주니오르", country: "🇧🇷 브라질", flag: "🇧🇷", emoji: "💃", diff: 2, hints: ["레알 마드리드 윙어", "춤 세리머니 논란", "2022 UCL 결승골"] },
  // ⭐⭐⭐ 어려움
  { name: "파울로 디발라", country: "🇦🇷 아르헨티나", flag: "🇦🇷", emoji: "💎", diff: 3, hints: ["라호야", "로마 공격수", "타투 많음"] },
  { name: "알리송 베케르", country: "🇧🇷 브라질", flag: "🇧🇷", emoji: "🧤", diff: 3, hints: ["리버풀 골키퍼", "세계 최고 GK", "2019 UCL 우승"] },
  { name: "가레스 베일", country: "🏴󠁧󠁢󠁷󠁬󠁳󠁿 웨일스", flag: "🏴󠁧󠁢󠁷󠁬󠁳󠁿", emoji: "🦅", diff: 3, hints: ["레알 마드리드", "골프 애호가", "드래곤 나라"] },
  { name: "크리스티안 에릭센", country: "🇩🇰 덴마크", flag: "🇩🇰", emoji: "💪", diff: 3, hints: ["심장마비 생존", "맨유 미드필더", "유로 2020 사고"] },
  { name: "엔조 페르난데스", country: "🇦🇷 아르헨티나", flag: "🇦🇷", emoji: "💎", diff: 3, hints: ["2022 월드컵 영플레이어", "첼시 미드필더", "엔조 프란체스콜리 이름"] },
  { name: "가비", country: "🇪🇸 스페인", flag: "🇪🇸", emoji: "🎭", diff: 3, hints: ["바르셀로나 미드필더", "부상으로 오래 결장", "어린 레전드 후보"] },
  { name: "오렐리앙 추아메니", country: "🇫🇷 프랑스", flag: "🇫🇷", emoji: "🛡️", diff: 3, hints: ["레알 마드리드 수비형", "21세기 비에이라", "2022 결승 출전"] },
  { name: "잔루이지 부폰", country: "🇮🇹 이탈리아", flag: "🇮🇹", emoji: "🧤", diff: 3, hints: ["이탈리아 GK 레전드", "2006 우승", "유벤투스 수호신"] },
  { name: "다비드 베컴", country: "🏴󠁧󠁢󠁥󠁮󠁧󠁿 잉글랜드", flag: "🏴󠁧󠁢󠁥󠁮󠁧󠁿", emoji: "💇", diff: 3, hints: ["프리킥 마스터", "패션 아이콘", "빅토리아 남편"] },
  { name: "마르코스 아센시오", country: "🇪🇸 스페인", flag: "🇪🇸", emoji: "⚡", diff: 3, hints: ["레알 마드리드 출신", "PSG 이적", "미드필더 겸 윙어"] },
];
"""

# Replace entire PLAYERS array
import re
content = re.sub(r'const PLAYERS = \[.*?\];', NEW_PLAYERS, content, flags=re.DOTALL)

# Update setQuestion to show difficulty + flag
content = content.replace(
    "document.getElementById('player-emoji').textContent = player.emoji;",
    """document.getElementById('player-emoji').textContent = player.emoji;
  // Show difficulty
  const diffEl = document.getElementById('diff-badge');
  if (diffEl) {
    const stars = '⭐'.repeat(player.diff || 1);
    const colors = ['','#22c55e','#f59e0b','#ef4444'];
    diffEl.textContent = stars;
    diffEl.style.color = colors[player.diff || 1];
  }"""
)

# Add diff badge to HTML
content = content.replace(
    '<div class="player-name" id="player-name">로딩중...</div>',
    '<div id="diff-badge" style="font-size:16px;margin-bottom:8px;min-height:20px;"></div>\n      <div class="player-name" id="player-name">로딩중...</div>'
)

# Update answer options to show flags
content = content.replace(
    "optEl.innerHTML = opts.map(o => `\n    <button class=\"opt-btn\" onclick=\"answer(this, '${o.replace(/'/g,\\\"\\\\'\\\")}')\">\\n      ${o}\\n    </button>\\n  `).join('');",
    """optEl.innerHTML = opts.map(o => {
    const flagMatch = o.match(/^(\\S+)/);
    const flag = flagMatch ? flagMatch[1] : '';
    const name = o.replace(/^\\S+\\s*/, '');
    return `<button class="opt-btn" onclick="answer(this, '${o.replace(/'/g,"\\\\'")}')">
      <span style="font-size:24px">${flag}</span> ${name}
    </button>`;
  }).join('');"""
)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 라운드 2: 선수 퀴즈 난이도 분류 + 국기 표시 완료")
