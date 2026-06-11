#!/bin/bash

# ⚽ 월드컵 미니게임 자동 개선 루프
# 1시간마다 실행되어 게임 품질을 단계적으로 향상

REPO_DIR="/home/claude/worldcup_minigame"
TOKEN="${GH_TOKEN}"
REMOTE="https://${TOKEN}@github.com/twinwhdwk/worldcup_minigame.git"
LOG="$REPO_DIR/improve_log.txt"

cd "$REPO_DIR"

echo "=============================" | tee -a "$LOG"
echo "🚀 루프 시작: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG"
echo "=============================" | tee -a "$LOG"

CYCLE=1

while true; do
  echo "" | tee -a "$LOG"
  echo "🔄 사이클 $CYCLE 시작: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG"

  # ── 사이클별 개선 항목 ──────────────────────────────────────
  case $CYCLE in
    1)
      echo "📦 사이클 1: 공통 CSS + 사운드 효과 추가" | tee -a "$LOG"
      python3 "$REPO_DIR/improve_cycle1.py" >> "$LOG" 2>&1
      MSG="✨ 사이클1: 공통 사운드 & CSS 개선"
      ;;
    2)
      echo "🎮 사이클 2: 선수 퀴즈 문제 확장 + 콤보 시스템" | tee -a "$LOG"
      python3 "$REPO_DIR/improve_cycle2.py" >> "$LOG" 2>&1
      MSG="🎮 사이클2: 선수 퀴즈 문제 40개로 확장, 콤보 배율 강화"
      ;;
    3)
      echo "🏆 사이클 3: 우승국 퀴즈 힌트 시스템 강화" | tee -a "$LOG"
      python3 "$REPO_DIR/improve_cycle3.py" >> "$LOG" 2>&1
      MSG="🏆 사이클3: 우승국 퀴즈 타이머 추가, 힌트 단계별 공개"
      ;;
    4)
      echo "⚽ 사이클 4: 페널티킥 게임 AI 패턴 학습 + 난이도 조절" | tee -a "$LOG"
      python3 "$REPO_DIR/improve_cycle4.py" >> "$LOG" 2>&1
      MSG="⚽ 사이클4: 페널티킥 AI 패턴 학습, 레벨 10까지 확장"
      ;;
    5)
      echo "👕 사이클 5: 유니폼 퀴즈 팀 24개로 확장" | tee -a "$LOG"
      python3 "$REPO_DIR/improve_cycle5.py" >> "$LOG" 2>&1
      MSG="👕 사이클5: 유니폼 퀴즈 원정 유니폼 추가, 팀 24개로 확장"
      ;;
    6)
      echo "🏅 사이클 6: 글로벌 리더보드 + 로컬 고득점 저장" | tee -a "$LOG"
      python3 "$REPO_DIR/improve_cycle6.py" >> "$LOG" 2>&1
      MSG="🏅 사이클6: 리더보드 & 고득점 로컬 저장 시스템"
      ;;
    *)
      echo "✅ 모든 개선 사이클 완료! 유지보수 모드" | tee -a "$LOG"
      MSG="🔧 유지보수: 버그 수정 및 UX 미세 조정"
      CYCLE=0
      ;;
  esac

  # git push
  git add -A
  if git diff --cached --quiet; then
    echo "  변경 없음, 스킵" | tee -a "$LOG"
  else
    git commit -m "$MSG [auto $(date '+%m/%d %H:%M')]"
    git push "$REMOTE" main 2>&1 | tee -a "$LOG"
    echo "  ✅ 커밋 & 푸시 완료" | tee -a "$LOG"
  fi

  CYCLE=$((CYCLE + 1))
  echo "⏰ 다음 실행까지 1시간 대기..." | tee -a "$LOG"
  sleep 3600
done
