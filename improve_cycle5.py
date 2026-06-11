#!/usr/bin/env python3
"""사이클 5: 유니폼 퀴즈 팀 추가"""
import os

REPO = "/home/claude/worldcup_minigame"
FILE = os.path.join(REPO, "games/uniform-quiz.html")

EXTRA_TEAMS = """
  {
    name: "🇸🇳 세네갈", flag: "🇸🇳",
    home: { colors: ["#ffffff","#00853F","#FDEF42"], pattern: "sash", label: "홈 유니폼" },
    clues: ["흰색 + 초록 사선", "아프리카 사자", "마네의 나라"],
    decoy: ["🇮🇪 아일랜드","🇸🇦 사우디아라비아","🇯🇲 자메이카"],
  },
  {
    name: "🇳🇬 나이지리아", flag: "🇳🇬",
    home: { colors: ["#008751","#ffffff","#008751"], pattern: "stripes", label: "홈 유니폼" },
    clues: ["초록+흰 세로줄", "슈퍼 이글스", "나이키 특별 에디션"],
    decoy: ["🇲🇽 멕시코","🇧🇦 보스니아","🇸🇦 사우디아라비아"],
  },
  {
    name: "🇩🇰 덴마크", flag: "🇩🇰",
    home: { colors: ["#C60C30","#ffffff","#C60C30"], pattern: "collar-stripe", label: "홈 유니폼" },
    clues: ["빨간색 단색", "덴마크의 역동성", "에릭센의 나라"],
    decoy: ["🇨🇭 스위스","🇹🇳 튀니지","🇧🇾 벨라루스"],
  },
  {
    name: "🇺🇾 우루과이", flag: "🇺🇾",
    home: { colors: ["#5EB6E4","#ffffff","#5EB6E4"], pattern: "solid", label: "홈 유니폼" },
    clues: ["연한 하늘색", "하늘색 단색", "첫 번째 챔피언"],
    decoy: ["🇦🇷 아르헨티나","🇸🇻 엘살바도르","🇫🇮 핀란드"],
  },
"""

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if '세네갈' not in content:
    content = content.replace('];  // END TEAMS', EXTRA_TEAMS + '];  // END TEAMS')
    # If that didn't work, find the end of the TEAMS array differently
    if '세네갈' not in content:
        content = content.replace(
            "  {\n    name: \"🇲🇽 멕시코\"",
            EXTRA_TEAMS + "  {\n    name: \"🇲🇽 멕시코\""
        )
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 사이클 5: 유니폼 퀴즈 팀 4개 추가")
else:
    print("이미 팀 추가됨")
