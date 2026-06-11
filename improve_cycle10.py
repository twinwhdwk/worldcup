#!/usr/bin/env python3
"""사이클 10: UX 개선 - 결과 공유 텍스트 + 스코어보드 바로가기"""
import os

REPO = os.path.dirname(os.path.abspath(__file__))
games_dir = os.path.join(REPO, 'games')

SCOREBOARD_LINK = """
    <br>
    <a href="../scoreboard.html" style="display:inline-flex;align-items:center;gap:8px;background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.3);border-radius:100px;padding:12px 24px;text-decoration:none;color:#FFD700;font-weight:700;font-size:15px;margin-top:8px;">
      🏆 내 점수 랭킹에 등록하기
    </a>
"""

SHARE_JS = """
function shareResult(score, gameName) {
  const text = `⚽ 월드컵 미니게임\\n🎮 ${gameName}\\n🏆 ${score.toLocaleString()}점 달성!\\n\\nhttps://twinwhdwk.github.io/worldcup_minigame`;
  if (navigator.share) {
    navigator.share({ title: '월드컵 미니게임', text });
  } else if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => alert('클립보드에 복사됐어요!'));
  }
}
"""

for filename in os.listdir(games_dir):
    if not filename.endswith('.html'): continue
    filepath = os.path.join(games_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'scoreboard.html' in content:
        print(f"  이미 있음: {filename}"); continue

    content = content.replace('<script>', '<script>\n' + SHARE_JS)

    # Add scoreboard link before "다른 게임 하기"
    content = content.replace(
        '← 다른 게임 하기',
        SCOREBOARD_LINK + '\n    <br><a href="../index.html" style="color:var(--muted);font-size:14px;">← 다른 게임 하기</a>\n    <a'
    )
    # Remove duplicate closing tag that may appear
    content = content.replace(
        '<a href="../index.html" style="color:var(--muted);font-size:14px;">← 다른 게임 하기</a>\n    <a href="../index.html" style="color:var(--muted);font-size:14px;">← 다른 게임 하기</a>',
        '<a href="../index.html" style="color:var(--muted);font-size:14px;">← 다른 게임 하기</a>'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ UX 개선: {filename}")

print("사이클 10 완료")
