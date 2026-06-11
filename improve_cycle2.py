#!/usr/bin/env python3
"""사이클 2: 선수 퀴즈 문제 40개로 확장"""
import re, os

REPO = "/home/claude/worldcup_minigame"
FILE = os.path.join(REPO, "games/player-country.html")

EXTRA_PLAYERS = """
  { name: "가레스 베일", country: "🏴󠁧󠁢󠁷󠁬󠁳󠁿 웨일스", emoji: "🦅", hints: ["레알 마드리드", "골프 애호가", "드래곤 나라"] },
  { name: "티에리 앙리", country: "🇫🇷 프랑스", emoji: "👑", hints: ["아스날 레전드", "2006 월드컵", "손 핸드볼 논란"] },
  { name: "지네딘 지단", country: "🇫🇷 프랑스", emoji: "💫", hints: ["1998 결승 헤딩 2골", "이탈리아전 박치기", "세계 최고 감독"] },
  { name: "펠레", country: "🇧🇷 브라질", emoji: "🌟", hints: ["월드컵 3회 우승", "17세 첫 우승", "축구 황제"] },
  { name: "디에고 마라도나", country: "🇦🇷 아르헨티나", emoji: "🤌", hints: ["신의 손", "세기의 골", "나폴리 레전드"] },
  { name: "호나우두", country: "🇧🇷 브라질", emoji: "👾", hints: ["2002 월드컵 8골", "이빨 헤어스타일", "진짜 호나우두"] },
  { name: "로나우지뉴", country: "🇧🇷 브라질", emoji: "😁", hints: ["바르셀로나 마술사", "화려한 드리블", "웃는 천재"] },
  { name: "올리버 지루", country: "🇫🇷 프랑스", emoji: "🎯", hints: ["골 못 넣어도 공헌", "잘생긴 스트라이커", "2018 우승"] },
  { name: "다비드 베컴", country: "🏴󠁧󠁢󠁥󠁮󠁧󠁿 잉글랜드", emoji: "💇", hints: ["프리킥 마스터", "패션 아이콘", "빅토리아 남편"] },
  { name: "카카", country: "🇧🇷 브라질", emoji: "✝️", hints: ["AC 밀란 레전드", "2007 발롱도르", "빠른 공격형 미드"] },
  { name: "잔루이지 부폰", country: "🇮🇹 이탈리아", emoji: "🧤", hints: ["이탈리아 GK 레전드", "2006 우승", "유벤투스 수호신"] },
  { name: "카림 벤제마", country: "🇫🇷 프랑스", emoji: "🔥", hints: ["2022 발롱도르", "레알 마드리드", "메시 없는 사이 최고"] },
  { name: "엔조 페르난데스", country: "🇦🇷 아르헨티나", emoji: "💎", hints: ["2022 월드컵 영플레이어", "첼시 미드필더", "엔조 프란체스콜리 이름"] },
  { name: "크리스티안 에릭센", country: "🇩🇰 덴마크", emoji: "💪", hints: ["심장마비 생존", "맨유 미드필더", "유로 2020 사고"] },
  { name: "알바로 모라타", country: "🇪🇸 스페인", emoji: "😤", hints: ["스페인 스트라이커", "비판 많이 받음", "유로 우승"] },
  { name: "도미니크 칼버트-르윈", country: "🏴󠁧󠁢󠁥󠁮󠁧󠁿 잉글랜드", emoji: "📸", hints: ["에버턴 스트라이커", "패션 모델 부업", "헤딩 능력자"] },
  { name: "마르코스 아센시오", country: "🇪🇸 스페인", emoji: "⚡", hints: ["레알 마드리드 출신", "PSG 이적", "미드필더 겸 윙어"] },
  { name: "오렐리앙 추아메니", country: "🇫🇷 프랑스", emoji: "🛡️", hints: ["레알 마드리드 수비형", "21세기 비에이라", "2022 결승 출전"] },
  { name: "가비", country: "🇪🇸 스페인", emoji: "🎭", hints: ["바르셀로나 미드필더", "부상으로 오래 결장", "어린 레전드 후보"] },
  { name: "비니시우스 주니오르", country: "🇧🇷 브라질", emoji: "💃", hints: ["레알 마드리드 윙어", "춤 세리머니 논란", "2022 UCL 결승골"] },
"""

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if "가레스 베일" in content:
    print("이미 확장됨")
else:
    # Insert extra players before closing bracket of PLAYERS array
    content = content.replace(
        "  { name: \"이강인\"",
        EXTRA_PLAYERS + "  { name: \"이강인\""
    )
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 선수 퀴즈 20명 추가 (총 40명)")
