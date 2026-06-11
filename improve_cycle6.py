#!/usr/bin/env python3
"""사이클 6: 로컬 고득점 저장 시스템"""
import os, re

REPO = "/home/claude/worldcup_minigame"

HIGHSCORE_JS = """
// ── High Score System ───────────────────────────────────
function getHighScores(game) {
  try { return JSON.parse(localStorage.getItem('wc_hs_' + game) || '[]'); } catch { return []; }
}
function saveHighScore(game, score) {
  const scores = getHighScores(game);
  scores.push({ score, date: new Date().toLocaleDateString('ko-KR') });
  scores.sort((a,b) => b.score - a.score);
  const top5 = scores.slice(0, 5);
  localStorage.setItem('wc_hs_' + game, JSON.stringify(top5));
  return top5;
}
function renderHighScores(game, containerId) {
  const scores = getHighScores(game);
  const el = document.getElementById(containerId);
  if (!el || scores.length === 0) return;
  el.innerHTML = '<div style="font-size:12px;color:var(--muted);letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">🏅 역대 최고점</div>' +
    scores.map((s,i) => `<div style="display:flex;justify-content:space-between;font-size:14px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
      <span style="color:${i===0?'#FFD700':i===1?'#aaa':i===2?'#cd7f32':'var(--muted)'}">${['🥇','🥈','🥉','4위','5위'][i]}</span>
      <span style="font-weight:700">${s.score.toLocaleString()}점</span>
      <span style="color:var(--muted)">${s.date}</span>
    </div>`).join('');
}
// ────────────────────────────────────────────────────────
"""

HIGHSCORE_HTML = """
    <div id="highscore-box" style="width:100%;max-width:600px;background:var(--card);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:20px;margin-bottom:20px;"></div>
"""

games = {
    "player-country.html": "player",
    "uniform-quiz.html": "uniform",
    "champion-tournament.html": "champion",
}

for filename, game_id in games.items():
    filepath = os.path.join(REPO, "games", filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'getHighScores' not in content:
        content = content.replace('<script>', '<script>\n' + HIGHSCORE_JS)
        # Add highscore box before result buttons
        content = content.replace(
            '<button class="btn-restart"',
            HIGHSCORE_HTML + '    <button class="btn-restart"'
        )
        # Call save + render in showResult
        content = content.replace(
            "document.getElementById('result-screen').classList.add('show');",
            f"saveHighScore('{game_id}', score);\n  document.getElementById('result-screen').classList.add('show');\n  renderHighScores('{game_id}', 'highscore-box');"
        )
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 사이클 6: {filename} 고득점 추가")
    else:
        print(f"이미 고득점 있음: {filename}")
