/**
 * 35명 동시 부하 테스트
 * 사용법: node load-test.js [firebase-url] [인원수]
 * 예)    node load-test.js https://yourproject-default-rtdb.firebaseio.com 35
 *
 * 실행 후 operator.html에서 평소처럼 게임 시작 → 봇이 자동 답변
 * 종료: Ctrl+C (자동 정리)
 */

const FIREBASE_URL = process.argv[2] || 'https://worldcup-minigame-default-rtdb.firebaseio.com';
const BASE = FIREBASE_URL + '/wc_live';
const N = parseInt(process.argv[3] || '35');
const NAMES = Array.from({length: N}, (_, i) => `봇${String(i+1).padStart(2,'0')}`);

function enc(n) { return n.replace(/[.#$[\]/]/g, '_'); }

// ── Firebase REST helpers ─────────────────────────────────────────────
async function fbPatch(path, data, ms = 9000) {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), ms);
  try {
    const r = await fetch(`${BASE}${path}.json`, {
      method: 'PATCH',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data),
      signal: ac.signal,
      cache: 'no-store',
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return r.json();
  } finally { clearTimeout(t); }
}

async function fbDelete(path) {
  return fetch(`${BASE}${path}.json`, {method: 'DELETE', cache: 'no-store'}).catch(() => {});
}

// ── Manual SSE parser (Node.js has no built-in EventSource) ──────────
async function connectSSE(url, handlers, signal) {
  while (!signal.aborted) {
    try {
      const r = await fetch(url, {
        headers: {'Accept': 'text/event-stream', 'Cache-Control': 'no-cache'},
        cache: 'no-store',
        signal,
      });
      if (!r.ok || !r.body) { await sleep(3000); continue; }

      const reader = r.body.getReader();
      const dec = new TextDecoder();
      let buf = '';
      let evtType = 'message';

      while (!signal.aborted) {
        const {done, value} = await reader.read();
        if (done) break;
        buf += dec.decode(value, {stream: true});
        const lines = buf.split('\n');
        buf = lines.pop(); // keep incomplete last line

        for (const line of lines) {
          if (line.startsWith('event:')) {
            evtType = line.slice(6).trim();
          } else if (line.startsWith('data:')) {
            const data = line.slice(5).trim();
            try { handlers[evtType]?.({data}); } catch {}
            evtType = 'message';
          } else if (line === '') {
            evtType = 'message';
          }
        }
      }
      reader.cancel().catch(() => {});
    } catch (e) {
      if (signal.aborted) break;
      await sleep(3000 + Math.random() * 2000); // reconnect back-off
    }
  }
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ── Stats ─────────────────────────────────────────────────────────────
const stats = {
  connected: 0,
  registered: 0,
  regErrors: 0,
  answers: 0,
  answerErrors: 0,
  skipped: 0,         // answered too slowly (simulated timeout)
  byQuestion: {},     // qKey → {ok, fail, skip}
  latencies: [],
  startTime: Date.now(),
  currentState: '대기 중 (operator.html에서 게임을 시작하세요)',
};

function bar(val, max, len = 20) {
  const f = Math.min(Math.round(val / max * len), len);
  return '[' + '█'.repeat(f) + '░'.repeat(len - f) + '] ' + val + '/' + max;
}

function printStats() {
  const elapsed = ((Date.now() - stats.startTime) / 1000).toFixed(0);
  const lats = stats.latencies;
  const avgLat = lats.length ? Math.round(lats.reduce((a,b)=>a+b,0)/lats.length) : 0;
  const p99 = lats.length ? lats.slice().sort((a,b)=>a-b)[Math.floor(lats.length*0.99)|0] : 0;

  const lines = [
    `\x1b[1m=== ${N}명 Firebase 부하 테스트 (${elapsed}s 경과) ===\x1b[0m`,
    `DB: ${FIREBASE_URL}`,
    `현재 상태: \x1b[33m${stats.currentState}\x1b[0m`,
    '',
    `SSE 연결:   ${bar(stats.connected, N)}`,
    `등록 완료:  ${bar(stats.registered, N)}${stats.regErrors ? `  \x1b[31m오류:${stats.regErrors}\x1b[0m` : ''}`,
    `답변 합계:  ${stats.answers}건  오류:${stats.answerErrors}  타임아웃:${stats.skipped}`,
    lats.length ? `레이턴시:   평균 ${avgLat}ms  /  p99 ${p99}ms` : '',
  ];

  const qKeys = Object.keys(stats.byQuestion).sort((a,b) => +a - +b);
  if (qKeys.length) {
    lines.push('', '문제별 답변:');
    qKeys.forEach(k => {
      const q = stats.byQuestion[k];
      const total = q.ok + q.fail + q.skip;
      const pct = Math.round(q.ok / N * 100);
      const color = pct >= 90 ? '\x1b[32m' : pct >= 60 ? '\x1b[33m' : '\x1b[31m';
      lines.push(`  Q${k}: ${color}${bar(q.ok, N)}\x1b[0m  실패:${q.fail} 타임아웃:${q.skip}`);
    });
  }

  lines.push('', '\x1b[2mCtrl+C 로 종료 및 정리\x1b[0m');
  process.stdout.write('\x1Bc' + lines.filter(l => l !== '').join('\n') + '\n');
}

// ── Bot Player ────────────────────────────────────────────────────────
class Bot {
  constructor(name) {
    this.name = name;
    this.e = enc(name);
    this.state = null;
    this.joinedAt = Date.now();
    this.answeredKeys = new Set();
    this.ac = new AbortController();
    this._hbInt = null;
  }

  async register() {
    const now = Date.now();
    await fbPatch(`/players/${this.e}`, {name: this.name, joinedAt: now, lastSeen: now});
  }

  start() {
    const url = `${BASE}/session.json`;
    connectSSE(url, {
      put: e => {
        try {
          const d = JSON.parse(e.data);
          const s = d.data;
          if (!s) return;
          // New session started — re-register
          if (s.lastClearedAt && s.lastClearedAt > this.joinedAt) {
            this.joinedAt = Date.now();
            fbPatch(`/players/${this.e}`, {name: this.name, joinedAt: this.joinedAt, lastSeen: this.joinedAt}).catch(()=>{});
            this.answeredKeys.clear();
          }
          this.state = s;
          this.onSession(s);
          stats.connected = Math.min(stats.connected + 1, N);
        } catch {}
      },
      patch: e => {
        try {
          const d = JSON.parse(e.data);
          if (d.data) {
            this.state = Object.assign(this.state || {}, d.data);
            this.onSession(this.state);
          }
        } catch {}
      },
    }, this.ac.signal).catch(() => {});

    // Heartbeat every 12s
    this._hbInt = setInterval(() => {
      fbPatch(`/players/${this.e}`, {lastSeen: Date.now()}).catch(() => {});
    }, 12000);
  }

  onSession(s) {
    if (!s) return;
    const stateLabel = {lobby:'대기실', question:`Q${s.questionIdx+1} 진행 중`, reveal:`Q${s.questionIdx+1} 정답 공개`, done:'게임 종료'}[s.state] || s.state;
    stats.currentState = stateLabel;

    if (s.state !== 'question') return;
    const fullKey = `${s.questionIdx}_${s.game}`;
    if (this.answeredKeys.has(fullKey)) return;
    this.answeredKeys.add(fullKey);

    const qKey = String(s.questionIdx + 1);
    if (!stats.byQuestion[qKey]) stats.byQuestion[qKey] = {ok:0, fail:0, skip:0};

    // Random delay 0.3–11s (simulate human answer speed)
    const timeLimit = (s.question?.timeLimit || 15) * 1000;
    const delay = 300 + Math.random() * 10700;

    if (delay > timeLimit - 800) {
      stats.skipped++;
      stats.byQuestion[qKey].skip++;
      return;
    }

    setTimeout(() => this._submit(s, qKey), delay);
  }

  async _submit(s, qKey) {
    // State may have changed during the delay
    if (this.state?.state !== 'question' || this.state?.questionIdx !== s.questionIdx) {
      stats.answerErrors++;
      stats.byQuestion[qKey].fail++;
      return;
    }

    const opts = s.question?.options?.length || 4;
    const idx = Math.floor(Math.random() * opts);
    const t0 = Date.now();
    try {
      await fbPatch(`/answers/${this.e}`, {idx, name: this.name, at: Date.now(), qIdx: s.questionIdx});
      stats.answers++;
      stats.latencies.push(Date.now() - t0);
      stats.byQuestion[qKey].ok++;
    } catch {
      stats.answerErrors++;
      stats.byQuestion[qKey].fail++;
    }
    fbPatch(`/players/${this.e}`, {lastSeen: Date.now()}).catch(() => {});
  }

  async stop() {
    clearInterval(this._hbInt);
    this.ac.abort();
    await fbDelete(`/players/${this.e}`);
  }
}

// ── Main ──────────────────────────────────────────────────────────────
async function main() {
  console.log(`Firebase: ${FIREBASE_URL}`);
  console.log(`${N}명 봇 등록 중 (배치 10명씩)...`);

  const bots = NAMES.map(n => new Bot(n));

  // Register in batches of 10 to avoid rate limiting
  for (let i = 0; i < N; i += 10) {
    const batch = bots.slice(i, i + 10);
    const results = await Promise.allSettled(batch.map(b => b.register()));
    results.forEach(r => {
      if (r.status === 'fulfilled') stats.registered++;
      else stats.regErrors++;
    });
    process.stdout.write(`  등록 완료: ${Math.min(i+10, N)}/${N}\r`);
    if (i + 10 < N) await sleep(200);
  }

  console.log(`\n모든 봇 SSE 연결 중...`);
  bots.forEach(b => b.start());
  await sleep(2500);
  stats.connected = N;

  const printInt = setInterval(printStats, 600);
  printStats();

  const cleanup = async () => {
    clearInterval(printInt);
    process.stdout.write('\n\n봇 데이터 삭제 중...\n');
    await Promise.allSettled(bots.map(b => b.stop()));

    // Final summary
    const qKeys = Object.keys(stats.byQuestion).sort((a,b)=>+a-+b);
    if (qKeys.length) {
      console.log('\n=== 최종 결과 ===');
      qKeys.forEach(k => {
        const q = stats.byQuestion[k];
        const pct = Math.round(q.ok / N * 100);
        console.log(`Q${k}: ${q.ok}/${N}명 제출 (${pct}%) | 실패:${q.fail} | 타임아웃:${q.skip}`);
      });
      const lats = stats.latencies;
      if (lats.length) {
        const avg = Math.round(lats.reduce((a,b)=>a+b,0)/lats.length);
        const sorted = lats.slice().sort((a,b)=>a-b);
        console.log(`\n레이턴시 — 평균:${avg}ms  p50:${sorted[sorted.length>>1]}ms  p99:${sorted[Math.floor(sorted.length*0.99)]||0}ms  최대:${sorted[sorted.length-1]}ms`);
      }
    } else {
      console.log('문제가 시작되지 않아 답변 데이터 없음.');
    }
    process.exit(0);
  };

  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);
}

main().catch(e => { console.error(e); process.exit(1); });
