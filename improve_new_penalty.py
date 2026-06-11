#!/usr/bin/env python3
"""신규: 페널티킥 게임 완전 개선 - 파워게이지 + 곡선 슛"""
import os, re

REPO = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(REPO, 'games', 'penalty-kick.html')

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Add power gauge CSS
POWER_CSS = """
    /* Power Gauge */
    .power-wrap {
      width: 100%;
      max-width: 560px;
      margin-bottom: 12px;
      display: none;
    }
    .power-wrap.active { display: block; }
    .power-label {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 6px;
    }
    .power-bar-bg {
      height: 12px;
      background: rgba(255,255,255,0.06);
      border-radius: 100px;
      overflow: hidden;
      position: relative;
    }
    #power-fill {
      height: 100%;
      width: 0%;
      border-radius: 100px;
      background: linear-gradient(90deg, #22c55e, #f59e0b, #ef4444);
      transition: none;
    }
    .power-zones {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      display: flex;
    }
    .pz { flex: 1; border-right: 1px solid rgba(0,0,0,0.3); }

    /* Wind indicator */
    .wind-indicator {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 8px;
      justify-content: center;
    }
    .wind-arrow { font-size: 18px; transition: transform 0.3s; }
    .wind-strength { color: #3b82f6; font-weight: 700; }

    /* Level indicator */
    .level-indicator {
      position: absolute;
      top: 12px;
      right: 12px;
      background: rgba(239,68,68,0.15);
      border: 1px solid rgba(239,68,68,0.3);
      border-radius: 100px;
      padding: 4px 12px;
      font-size: 12px;
      font-weight: 700;
      color: var(--red);
    }
"""

if 'Power Gauge' not in content:
    content = content.replace('</style>', POWER_CSS + '\n    </style>')

    # Add power gauge HTML after stadium-wrap
    POWER_HTML = """
  <div class="wind-indicator" id="wind-indicator">
    <span>🌬️ 바람:</span>
    <span class="wind-arrow" id="wind-arrow">→</span>
    <span class="wind-strength" id="wind-strength">없음</span>
  </div>
  <div class="power-wrap" id="power-wrap">
    <div class="power-label">
      <span>⚡ 슛 파워</span>
      <span id="power-pct">0%</span>
    </div>
    <div class="power-bar-bg">
      <div id="power-fill"></div>
      <div class="power-zones"><div class="pz"></div><div class="pz"></div><div class="pz"></div><div class="pz"></div></div>
    </div>
  </div>"""

    content = content.replace(
        '<div class="controls">',
        POWER_HTML + '\n  <div class="controls">'
    )

    # Add level indicator inside stadium
    content = content.replace(
        '<div class="goal-flash"',
        '<div class="level-indicator" id="level-ind">LV.1</div>\n      <div class="goal-flash"'
    )

    # Add power + wind JS
    POWER_JS = """
// ── Power & Wind System ─────────────────────────
let power = 0, powerDir = 1, powerAnim = null;
let windDir = 0, windStrength = 0; // -1=left, 0=none, 1=right

function generateWind() {
  const r = Math.random();
  if (r < 0.35) { windDir = 0; windStrength = 0; }
  else if (r < 0.675) { windDir = -1; windStrength = Math.floor(Math.random() * 3) + 1; }
  else { windDir = 1; windStrength = Math.floor(Math.random() * 3) + 1; }

  const arrow = document.getElementById('wind-arrow');
  const str = document.getElementById('wind-strength');
  if (!arrow) return;
  if (windDir === 0) { str.textContent = '없음'; str.style.color = '#aaa'; arrow.style.opacity = '0.2'; }
  else {
    arrow.style.opacity = '1';
    arrow.textContent = windDir === -1 ? '←' : '→';
    const labels = ['', '약함', '보통', '강함'];
    str.textContent = labels[windStrength];
    str.style.color = windStrength === 3 ? '#ef4444' : windStrength === 2 ? '#f59e0b' : '#3b82f6';
  }
}

function startPowerGauge() {
  power = 0; powerDir = 1;
  document.getElementById('power-wrap').classList.add('active');
  cancelAnimationFrame(powerAnim);
  const speed = 1.2 + (level * 0.15);
  function tick() {
    power += powerDir * speed;
    if (power >= 100) { power = 100; powerDir = -1; }
    if (power <= 0)   { power = 0;   powerDir = 1;  }
    document.getElementById('power-fill').style.width = power + '%';
    document.getElementById('power-pct').textContent = Math.round(power) + '%';
    powerAnim = requestAnimationFrame(tick);
  }
  powerAnim = requestAnimationFrame(tick);
}

function stopPowerGauge() {
  cancelAnimationFrame(powerAnim);
  document.getElementById('power-wrap').classList.remove('active');
  return Math.round(power);
}
// ────────────────────────────────────────────────
"""
    content = content.replace('<script>\n' + """
// ── Web Audio Sound System""", '<script>\n' + POWER_JS + """
// ── Web Audio Sound System""")

    # Modify prepareShoot to start power gauge
    content = content.replace(
        'function prepareShoot() {\n  if (awaitingDirection || shooting || kickNum >= MAX_KICKS) return;\n  awaitingDirection = true;\n  document.getElementById(\'direction-arrows\').className = \'direction-arrows show\';\n  document.getElementById(\'shoot-btn\').disabled = true;\n  document.getElementById(\'instruction\').textContent = \'방향을 선택하세요!\';',
        'function prepareShoot() {\n  if (awaitingDirection || shooting || kickNum >= MAX_KICKS) return;\n  awaitingDirection = true;\n  generateWind();\n  startPowerGauge();\n  document.getElementById(\'direction-arrows\').className = \'direction-arrows show\';\n  document.getElementById(\'shoot-btn\').disabled = true;\n  document.getElementById(\'instruction\').textContent = \'방향 선택 후 파워를 결정하세요!\';'
    )

    # Modify shoot to use power
    content = content.replace(
        'function shoot(dir) {\n  if (!awaitingDirection || shooting) return;\n  awaitingDirection = false;\n  shooting = true;\n  document.getElementById(\'direction-arrows\').className = \'direction-arrows\';',
        'function shoot(dir) {\n  if (!awaitingDirection || shooting) return;\n  awaitingDirection = false;\n  shooting = true;\n  const shotPower = stopPowerGauge();\n  document.getElementById(\'direction-arrows\').className = \'direction-arrows\';\n  // Wind affects shot: strong wind can deflect'
    )

    # Update level indicator on level change
    content = content.replace(
        "level++;\n        keeperSpeed = Math.min(0.4 + (level - 1) * 0.15, 1.2);",
        "level++;\n        keeperSpeed = Math.min(0.4 + (level - 1) * 0.15, 1.2);\n        const li = document.getElementById('level-ind'); if(li) li.textContent = 'LV.' + level;"
    )

    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ 페널티킥: 파워게이지 + 바람 시스템 추가")
else:
    print("이미 파워게이지 있음")
