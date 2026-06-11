#!/usr/bin/env python3
"""라운드 10: 피날레 - 결과 공유 + 스코어보드 자동 이름 기억"""
import os

REPO = os.path.dirname(os.path.abspath(__file__))

NAME_MEMORY_JS = """
// ── Name Memory ─────────────────────────────────
function getSavedName() {
  return localStorage.getItem('wc_player_name') || '';
}
function saveName(name) {
  if (name) localStorage.setItem('wc_player_name', name);
}
// ────────────────────────────────────────────────
"""

# Apply to each game: remember last entered name in scoreboard
sb_file = os.path.join(REPO, 'scoreboard.html')
with open(sb_file, 'r', encoding='utf-8') as f:
    content = f.read()

if 'getSavedName' not in content:
    content = content.replace('// ── Add Score ─────────────────────────────────────', NAME_MEMORY_JS + '\n// ── Add Score ─────────────────────────────────────')
    # Pre-fill name from memory
    content = content.replace(
        '// ── Init ──────────────────────────────────────────',
        """// ── Init ──────────────────────────────────────────
  const savedName = getSavedName();
  if (savedName) document.getElementById('player-name').value = savedName;"""
    )
    # Save name on submit
    content = content.replace(
        "showToast(`✅ ${name} — ${score.toLocaleString()}점 등록!`);",
        "saveName(name);\n  showToast(`✅ ${name} — ${score.toLocaleString()}점 등록!`);"
    )
    with open(sb_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 스코어보드: 이름 자동 기억")

# Add "내 이름 기억" hint to each game's result screen scoreboard link
games_dir = os.path.join(REPO, 'games')
for filename in os.listdir(games_dir):
    if not filename.endswith('.html'): continue
    fpath = os.path.join(games_dir, filename)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'wc_player_name' in content:
        print(f"  이미 있음: {filename}"); continue

    NAME_PASS_JS = """
function goToScoreboard(score) {
  const name = localStorage.getItem('wc_player_name') || '';
  const url = '../scoreboard.html' + (name ? `?prefill=${encodeURIComponent(name)}&score=${score}` : '');
  window.location.href = url;
}
"""
    content = content.replace('<script>', '<script>\n' + NAME_PASS_JS)

    # Replace scoreboard link to use goToScoreboard with score
    content = content.replace(
        'href="../scoreboard.html"',
        'href="#" onclick="goToScoreboard(score)"'
    )
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ 이름 전달: {filename}")

# Scoreboard: auto-fill from URL params
with open(sb_file, 'r', encoding='utf-8') as f:
    content = f.read()

if 'URLSearchParams' not in content:
    URLPARAM_JS = """
  // Auto-fill from URL params (coming from game result)
  const urlParams = new URLSearchParams(window.location.search);
  const prefillName = urlParams.get('prefill');
  const prefillScore = urlParams.get('score');
  if (prefillName) {
    document.getElementById('player-name').value = prefillName;
    saveName(prefillName);
  }
  if (prefillScore) {
    document.getElementById('player-score').value = prefillScore;
    // Highlight the score input
    setTimeout(() => document.getElementById('player-score').focus(), 300);
  }"""
    content = content.replace(
        "  const savedName = getSavedName();",
        URLPARAM_JS + "\n  const savedName = getSavedName();"
    )
    with open(sb_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 스코어보드: URL 파라미터 자동입력")

print("라운드 10 완료: 이름 기억 + 점수 자동 전달")
