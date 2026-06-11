#!/usr/bin/env python3
"""라운드 4: 우승국 퀴즈 - 득점왕/MVP 힌트 추가 + 최종 보스 문제"""
import os, re

REPO = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(REPO, 'games', 'champion-tournament.html')

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if 'topScorer' in content:
    print("이미 적용됨"); exit()

# Expand world cup data with top scorer + MVP info
NEW_WC_DATA = """const WORLD_CUPS = [
  { year: 1930, host: "우루과이", winner: "🇺🇾 우루과이", flag: "🇺🇾", topScorer: "기예르모 스타빌레 (아르헨 8골)", mvp: "호세 나소치", hints: ["첫 번째 월드컵", "남미 개최", "우루과이 vs 아르헨티나 결승"], extra: "13개국만 참가한 역대 최소 규모" },
  { year: 1950, host: "브라질", winner: "🇺🇾 우루과이", flag: "🇺🇾", topScorer: "아데미르 (브라질 9골)", mvp: "오베두리오 바렐라", hints: ["브라질 개최", "마라카낭의 비극", "결승전 없는 리그전"], extra: "브라질이 우승 직전 충격적 패배" },
  { year: 1954, host: "스위스", winner: "🇩🇪 서독", flag: "🇩🇪", topScorer: "샌도르 코치시 (헝가리 11골)", mvp: "프리츠 발터", hints: ["스위스 개최", "베른의 기적", "헝가리 꺾음"], extra: "역대 최다 득점 대회 (평균 5.38골)" },
  { year: 1958, host: "스웨덴", winner: "🇧🇷 브라질", flag: "🇧🇷", topScorer: "저스트 퐁테인 (프랑스 13골)", mvp: "디지 (브라질)", hints: ["스웨덴 개최", "17세 펠레 데뷔", "브라질의 첫 우승"], extra: "퐁테인의 13골은 역대 단일 대회 최다" },
  { year: 1966, host: "잉글랜드", winner: "🏴󠁧󠁢󠁥󠁮󠁧󠁿 잉글랜드", flag: "🏴󠁧󠁢󠁥󠁮󠁧󠁿", topScorer: "에우제비우 (포르투갈 9골)", mvp: "보비 찰턴", hints: ["웸블리 결승", "잉글랜드 유일 우승", "바비 무어 주장"], extra: "3-2 연장 끝 서독 꺾고 유일한 우승" },
  { year: 1970, host: "멕시코", winner: "🇧🇷 브라질", flag: "🇧🇷", topScorer: "제르졸트 뮐러 (서독 10골)", mvp: "펠레", hints: ["멕시코 개최", "펠레의 마지막 월드컵", "화려한 공격 축구"], extra: "브라질이 줄리메 트로피 영구 소장" },
  { year: 1974, host: "서독", winner: "🇩🇪 서독", flag: "🇩🇪", topScorer: "제르졸트 뮐러 (서독 4골)", mvp: "요한 크루이프", hints: ["서독 개최", "토털 사커 대결", "홈 우승"], extra: "크루이프는 무릎을 꿇지 않겠다며 불참" },
  { year: 1978, host: "아르헨티나", winner: "🇦🇷 아르헨티나", flag: "🇦🇷", topScorer: "마리오 켐페스 (6골)", mvp: "마리오 켐페스", hints: ["아르헨티나 개최", "마리오 켐페스", "홈 우승"], extra: "아르헨티나의 첫 번째 월드컵 우승" },
  { year: 1982, host: "스페인", winner: "🇮🇹 이탈리아", flag: "🇮🇹", topScorer: "파올로 로시 (6골)", mvp: "파올로 로시", hints: ["스페인 개최", "파올로 로시 6골", "카테나치오"], extra: "이탈리아가 조별리그 부진에서 우승까지" },
  { year: 1986, host: "멕시코", winner: "🇦🇷 아르헨티나", flag: "🇦🇷", topScorer: "게리 리네커 (잉글랜드 6골)", mvp: "디에고 마라도나", hints: ["멕시코 개최", "마라도나의 대회", "신의 손 & 세기의 골"], extra: "마라도나 혼자 아르헨티나를 우승으로 이끔" },
  { year: 1990, host: "이탈리아", winner: "🇩🇪 서독", flag: "🇩🇪", topScorer: "살바토레 스킬라치 (6골)", mvp: "살바토레 스킬라치", hints: ["이탈리아 개최", "역대 최저 득점 대회", "독일의 3번째 우승"], extra: "평균 득점 2.21골로 역대 최저" },
  { year: 1994, host: "미국", winner: "🇧🇷 브라질", flag: "🇧🇷", topScorer: "흐리스토 스토이치코프 (불가리아 6골)", mvp: "호마리우", hints: ["미국 개최", "로마리오 & 베베토", "승부차기 결승"], extra: "이탈리아와 결승전 승부차기로 결정" },
  { year: 1998, host: "프랑스", winner: "🇫🇷 프랑스", flag: "🇫🇷", topScorer: "다보르 수케르 (크로아티아 6골)", mvp: "호나우두", hints: ["프랑스 개최", "지단의 결승 헤딩 2골", "홈 우승"], extra: "지단이 결승에서 헤딩골 2개를 넣음" },
  { year: 2002, host: "한국·일본", winner: "🇧🇷 브라질", flag: "🇧🇷", topScorer: "호나우두 (8골)", mvp: "올리버 칸", hints: ["아시아 공동 개최", "한국 4강 신화", "호나우두 8골"], extra: "한국이 4강에 오른 역대 최고 성적" },
  { year: 2006, host: "독일", winner: "🇮🇹 이탈리아", flag: "🇮🇹", topScorer: "미로슬라프 클로제 (독일 5골)", mvp: "지네딘 지단", hints: ["독일 개최", "지단의 박치기", "이탈리아 4번째 우승"], extra: "지단의 머리박기 퇴장으로 유명한 대회" },
  { year: 2010, host: "남아프리카공화국", winner: "🇪🇸 스페인", flag: "🇪🇸", topScorer: "토마스 뮐러 (독일 5골)", mvp: "디에고 포를란", hints: ["아프리카 첫 개최", "부부젤라", "스페인 첫 우승"], extra: "부부젤라 소리로 기억되는 대회" },
  { year: 2014, host: "브라질", winner: "🇩🇪 독일", flag: "🇩🇪", topScorer: "하메스 로드리게스 (콜롬비아 6골)", mvp: "리오넬 메시", hints: ["브라질 개최", "미네이랑의 비극 7-1", "독일 4번째 우승"], extra: "브라질이 준결승에서 독일에 1-7로 대패" },
  { year: 2018, host: "러시아", winner: "🇫🇷 프랑스", flag: "🇫🇷", topScorer: "해리 케인 (잉글랜드 6골)", mvp: "루카 모드리치", hints: ["러시아 개최", "음바페 19살 우승", "프랑스 2번째 우승"], extra: "음바페가 역대 2번째로 어린 결승골 선수" },
  { year: 2022, host: "카타르", winner: "🇦🇷 아르헨티나", flag: "🇦🇷", topScorer: "킬리안 음바페 (프랑스 8골)", mvp: "리오넬 메시", hints: ["중동 첫 개최", "메시의 꿈 실현", "프랑스와 승부차기"], extra: "메시가 마침내 월드컵 트로피를 들어올림" },
];"""

content = re.sub(r'const WORLD_CUPS = \[.*?\];', NEW_WC_DATA, content, flags=re.DOTALL)

# Show topScorer + MVP in hint row
content = content.replace(
    "const hintRow = document.getElementById('hint-row');\n    hintRow.innerHTML = q.hints.map(h => `<span class=\"hint-chip\">${h}</span>`).join('');",
    """const hintRow = document.getElementById('hint-row');
    hintRow.innerHTML = q.hints.map(h => `<span class="hint-chip">${h}</span>`).join('') +
      (q.topScorer ? `<span class="hint-chip" style="border-color:rgba(255,215,0,0.3);color:#FFD700;">⚽ 득점왕: ${q.topScorer}</span>` : '');"""
)

# Show MVP in extra hint
content = content.replace(
    "document.getElementById('extra-hint').textContent = '💡 ' + questions[currentQ].extra;",
    "document.getElementById('extra-hint').textContent = '💡 ' + questions[currentQ].extra + (questions[currentQ].mvp ? ` | 🌟 MVP: ${questions[currentQ].mvp}` : '');"
)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ 라운드 4: 우승국 퀴즈 득점왕/MVP 정보 추가")
