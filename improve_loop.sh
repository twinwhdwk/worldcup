#!/bin/bash

# ⚽ 월드컵 미니게임 자동 개선 루프 (15분마다)
REPO_DIR="/home/claude/worldcup_minigame"
REMOTE="https://${GH_TOKEN}@github.com/twinwhdwk/worldcup_minigame.git"
LOG="$REPO_DIR/improve_log.txt"

cd "$REPO_DIR"

echo "=============================" >> "$LOG"
echo "🚀 루프 시작: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG"
echo "=============================" >> "$LOG"

CYCLE=1

while true; do
  echo "" >> "$LOG"
  echo "🔄 사이클 $CYCLE 시작: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG"

  case $CYCLE in
    1)
      echo "사이클 1: 사운드 & CSS" >> "$LOG"
      python3 "$REPO_DIR/improve_cycle1.py" >> "$LOG" 2>&1
      MSG="✨ 사이클1: 사운드 효과 보완"
      ;;
    2)
      echo "사이클 2: 선수 퀴즈 확장" >> "$LOG"
      python3 "$REPO_DIR/improve_cycle2.py" >> "$LOG" 2>&1
      MSG="🎮 사이클2: 선수 퀴즈 40명 확장"
      ;;
    3)
      echo "사이클 3: 우승국 퀴즈 타이머" >> "$LOG"
      python3 "$REPO_DIR/improve_cycle3.py" >> "$LOG" 2>&1
      MSG="🏆 사이클3: 우승국 퀴즈 타이머"
      ;;
    4)
      echo "사이클 4: 페널티킥 AI" >> "$LOG"
      python3 "$REPO_DIR/improve_cycle4.py" >> "$LOG" 2>&1
      MSG="⚽ 사이클4: 페널티킥 AI 패턴 학습"
      ;;
    5)
      echo "사이클 5: 유니폼 팀 확장" >> "$LOG"
      python3 "$REPO_DIR/improve_cycle5.py" >> "$LOG" 2>&1
      MSG="👕 사이클5: 유니폼 팀 확장"
      ;;
    6)
      echo "사이클 6: 리더보드" >> "$LOG"
      python3 "$REPO_DIR/improve_cycle6.py" >> "$LOG" 2>&1
      MSG="🏅 사이클6: 고득점 저장 시스템"
      ;;
    *)
      echo "유지보수 모드" >> "$LOG"
      MSG="🔧 유지보수: UX 미세 조정"
      CYCLE=0
      ;;
  esac

  git add -A
  if git diff --cached --quiet; then
    echo "  변경 없음, 스킵" >> "$LOG"
  else
    git commit -m "$MSG [auto $(date '+%m/%d %H:%M')]"
    git push "$REMOTE" main >> "$LOG" 2>&1
    echo "  ✅ 푸시 완료" >> "$LOG"
  fi

  CYCLE=$((CYCLE + 1))
  echo "⏰ 15분 대기..." >> "$LOG"
  sleep 900
done
