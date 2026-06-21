/**
 * 35명 동시 부하 테스트 (자동화 — 오퍼레이터 불필요)
 * 사용법: node load-test.js [firebase-url] [인원수]
 *
 * 봇 35명이 자동 등록/연결하고, 스크립트가 직접 3문제를 출제·채점·공개
 * 종료: 자동 (전 문제 완료 후) 또는 Ctrl+C
 */

const FIREBASE_URL = process.argv[2] || 'https://worldcup-minigame-default-rtdb.firebaseio.com';
const BASE = FIREBASE_URL + '/wc_live';
const N = parseInt(process.argv[3] || '35');
const NAMES = Array.from({length: N}, (_, i) => `봇${String(i+1).padStart(2,'0')}`);

const TEST_QUESTIONS = [
  {text:'1번: 2002 한일 월드컵에서 한국이 4강에 진출했나요?', options:['진출함','안함','결승진출','3위'],       correct:0, emoji:'🏆', timeLimit:15},
  {text:'2번: FIFA 월드컵은 몇 년마다 열리나요?',            options:['2년','4년','3년','5년'],               correct:1, emoji:'⚽', timeLimit:15},
  {text:'3번: 2026 월드컵 개최국이 아닌 나라는?',           options:['미국','캐나다','멕시코','브라질'],       correct:3, emoji:'🌎', timeLimit:15},
  {text:'4번: 역대 월드컵 최다 우승국은?',                  options:['독일','아르헨티나','브라질','이탈리아'], correct:2, emoji:'🇧🇷', timeLimit:15},
  {text:'5번: 2022 카타르 월드컵 우승국은?',               options:['프랑스','브라질','아르헨티나','포르투갈'],correct:2, emoji:'🏅', timeLimit:15},
  {text:'6번: 한국의 2026 월드컵 조별리그 첫 상대는?',      options:['멕시코','체코','남아공','캐나다'],       correct:1, emoji:'🇨🇿', timeLimit:15},
  {text:'7번: 월드컵 역대 최다 득점자는?',                  options:['호나우두','메시','미로슬라프 클로제','펠레'], correct:2, emoji:'⚽', timeLimit:15},
  {text:'8번: 2026 월드컵 본선 진출국 수는?',              options:['32개국','36개국','48개국','40개국'],     correct:2, emoji:'🌍', timeLimit:15},
  {text:'9번: 한국 국가대표팀 별명은?',                     options:['태극전사','붉은악마','청룡군단','호랑이'], correct:0, emoji:'🇰🇷', timeLimit:15},
  {text:'10번: 이강인이 속한 클럽은?',                     options:['레알마드리드','맨시티','PSG','바르셀로나'], correct:2, emoji:'⚽', timeLimit:15},
];

function enc(n) { return n.replace(/[.#$[\]/]/g, '_'); }
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ── Firebase helpers ──────────────────────────────────────────────────
async function fbReq(method, path, data, ms = 10000) {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), ms);
  try {
    const r = await fetch(`${BASE}${path}.json`, {
      method,
      headers: data ? {'Content-Type': 'application/json'} : undefined,
      body: data ? JSON.stringify(data) : undefined,
      signal: ac.signal,
      cache: 'no-store',
    });
    if (!r.ok) throw new Error(`HTTP ${r.status} ${method} ${path}`);
    return r.json();
  } finally { clearTimeout(t); }
}
const fbPatch  = (p, d) => fbReq('PATCH',  p, d);
const fbPut    = (p, d) => fbReq('PUT',    p, d);
const fbGet    = (p)    => fbReq('GET',    p, null);
const fbDelete = (p)    => fetch(`${BASE}${p}.json`, {method:'DELETE', cache:'no-store'}).catch(()=>{});

// ── SSE ───────────────────────────────────────────────────────────────
async function connectSSE(url, handlers, signal) {
  while (!signal.aborted) {
    try {
      const r = await fetch(url, {
        headers: {'Accept': 'text/event-stream', 'Cache-Control': 'no-cache'},
        cache: 'no-store', signal,
      });
      if (!r.ok || !r.body) { await sleep(3000); continue; }
      const reader = r.body.getReader();
      const dec = new TextDecoder();
      let buf = '', evtType = 'message';
      while (!signal.aborted) {
        const {done, value} = await reader.read();
        if (done) break;
        buf += dec.decode(value, {stream: true});
        const lines = buf.split('\n'); buf = lines.pop();
        for (const line of lines) {
          if (line.startsWith('event:'))      { evtType = line.slice(6).trim(); }
          else if (line.startsWith('data:'))  { handlers[evtType]?.({data: line.slice(5).trim()}); evtType = 'message'; }
          else if (line === '')               { evtType = 'message'; }
        }
      }
      reader.cancel().catch(() => {});
    } catch { if (signal.aborted) break; await sleep(3000); }
  }
}

// ── Stats ─────────────────────────────────────────────────────────────
const stats = {
  registered: 0, regErrors: 0,
  byQuestion: {},   // qIdx → {attempted, ok, fail, skip, latencies:[]}
  sseErrors: 0,
  startTime: Date.now(),
};

function bar(v, max, len=22) {
  const f = Math.min(Math.round(v/max*len), len);
  return '[' + '█'.repeat(f) + '░'.repeat(len-f) + '] ' + v + '/' + max;
}

function printLive(phase, qIdx) {
  const elapsed = ((Date.now() - stats.startTime)/1000).toFixed(1);
  const lines = [
    `\x1b[1m=== ${N}명 Firebase 부하 테스트 (${elapsed}s) ===\x1b[0m`,
    `단계: \x1b[33m${phase}\x1b[0m`,
    `등록: ${bar(stats.registered, N)}`,
    '',
  ];
  const qs = Object.keys(stats.byQuestion).sort((a,b)=>+a-+b);
  qs.forEach(k => {
    const q = stats.byQuestion[k];
    const lats = q.latencies;
    const avg = lats.length ? Math.round(lats.reduce((a,b)=>a+b,0)/lats.length) : 0;
    const pct = Math.round(q.ok/N*100);
    const col = pct>=90?'\x1b[32m':pct>=60?'\x1b[33m':'\x1b[31m';
    lines.push(`Q${+k+1}: ${col}${bar(q.ok, N)}\x1b[0m  실패:${q.fail} 타임아웃:${q.skip}  평균레이턴시:${avg}ms`);
  });
  if (qIdx !== undefined && stats.byQuestion[qIdx]) {
    const cur = stats.byQuestion[qIdx];
    lines.push(`\n  → 현재 답변 접수 중: ${cur.ok+cur.fail}/${N}명`);
  }
  process.stdout.write('\x1Bc' + lines.join('\n') + '\n');
}

// ── Bot ───────────────────────────────────────────────────────────────
class Bot {
  constructor(name) {
    this.name = name; this.e = enc(name);
    this.state = null; this.answeredKeys = new Set();
    this.joinedAt = Date.now(); this.ac = new AbortController();
  }

  async register() {
    const now = Date.now();
    await fbPatch(`/players/${this.e}`, {name:this.name, joinedAt:now, lastSeen:now});
  }

  start() {
    connectSSE(`${BASE}/session.json`, {
      put: e => {
        try {
          const d = JSON.parse(e.data); const s = d.data;
          if (!s) return;
          if (s.lastClearedAt && s.lastClearedAt > this.joinedAt) {
            this.joinedAt = Date.now(); this.answeredKeys.clear();
            fbPatch(`/players/${this.e}`, {name:this.name, joinedAt:this.joinedAt, lastSeen:this.joinedAt}).catch(()=>{});
          }
          this.state = s; this.onSession(s);
        } catch {}
      },
      patch: e => {
        try {
          const d = JSON.parse(e.data);
          if (d.data) { this.state = Object.assign(this.state||{}, d.data); this.onSession(this.state); }
        } catch {}
      },
    }, this.ac.signal).catch(() => {});
  }

  onSession(s) {
    if (s?.state !== 'question') return;
    const key = `${s.questionIdx}_${s.game||''}`;
    if (this.answeredKeys.has(key)) return;
    this.answeredKeys.add(key);

    const qi = s.questionIdx;
    if (!stats.byQuestion[qi]) stats.byQuestion[qi] = {attempted:0, ok:0, fail:0, skip:0, latencies:[]};
    stats.byQuestion[qi].attempted++;

    const tl = (s.question?.timeLimit || 15) * 1000;
    const delay = 300 + Math.random() * 12700;   // 0.3s ~ 13s
    if (delay > tl) { stats.byQuestion[qi].skip++; return; }

    setTimeout(() => this._submit(s, qi), delay);
  }

  async _submit(s, qi) {
    if (this.state?.state !== 'question' || this.state?.questionIdx !== s.questionIdx) {
      if (stats.byQuestion[qi]) stats.byQuestion[qi].fail++;
      return;
    }
    const idx = Math.floor(Math.random() * (s.question?.options?.length || 4));
    const t0 = Date.now();
    try {
      await fbPatch(`/answers/${this.e}`, {idx, name:this.name, at:Date.now(), qIdx:s.questionIdx});
      stats.byQuestion[qi].ok++;
      stats.byQuestion[qi].latencies.push(Date.now() - t0);
    } catch { stats.byQuestion[qi].fail++; }
    fbPatch(`/players/${this.e}`, {lastSeen:Date.now()}).catch(()=>{});
  }

  async stop() {
    this.ac.abort();
    await fbDelete(`/players/${this.e}`);
  }
}

// ── Operator simulation ───────────────────────────────────────────────
async function runQuestion(q, qIdx, total, bots) {
  const startAt = Date.now() + 1200;
  await fbDelete('/answers');
  await fbPatch('/session', {
    state: 'question',
    game: '부하테스트',
    questionIdx: qIdx,
    totalQuestions: total,
    question: {
      text: q.text, options: q.options, emoji: q.emoji,
      timeLimit: q.timeLimit, startAt, correctIdx: null,
      hint: '부하 테스트 자동 문제',
    },
    scoreGains: {},
  });

  // Wait for all bots to answer or time is up
  const deadline = startAt + q.timeLimit * 1000;
  const printInt = setInterval(() => printLive(`Q${qIdx+1} 진행 중 (${q.timeLimit}초)`, qIdx), 500);
  while (Date.now() < deadline) {
    const answered = (stats.byQuestion[qIdx]?.ok || 0) + (stats.byQuestion[qIdx]?.fail || 0);
    if (answered >= N) break;
    await sleep(300);
  }
  clearInterval(printInt);

  // Reveal
  const answers = await fbGet('/answers') || {};
  const gains = {};
  Object.entries(answers).forEach(([k, v]) => {
    if (v && typeof v === 'object' && v.idx !== undefined)
      gains[k] = v.idx === q.correct ? 100 : 0;
  });
  await fbPatch('/session', {
    state: 'reveal',
    question: {...q, correctIdx: q.correct},
    scoreGains: gains,
    allRanks: {},
  });
  printLive(`Q${qIdx+1} 정답 공개`, undefined);
  await sleep(3000);
}

// ── Main ──────────────────────────────────────────────────────────────
async function main() {
  console.log(`Firebase: ${FIREBASE_URL}`);
  console.log(`테스트 시작: ${N}명 봇, ${TEST_QUESTIONS.length}문제\n`);

  // 1. Clear session
  await fbPut('/session', {state:'lobby', lastClearedAt: Date.now()}).catch(()=>{});

  // 2. Register bots
  const bots = NAMES.map(n => new Bot(n));
  process.stdout.write('봇 등록 중...');
  for (let i = 0; i < N; i += 10) {
    const batch = bots.slice(i, i+10);
    const res = await Promise.allSettled(batch.map(b => b.register()));
    res.forEach(r => r.status==='fulfilled' ? stats.registered++ : stats.regErrors++);
    process.stdout.write(` ${Math.min(i+10,N)}`);
    if (i+10 < N) await sleep(150);
  }
  console.log(`\n등록 완료 (성공:${stats.registered} 오류:${stats.regErrors})\n`);

  // 3. Connect SSE
  bots.forEach(b => b.start());
  printLive('SSE 연결 대기 (2초)...', undefined);
  await sleep(2000);

  // 4. Run questions
  for (let i = 0; i < TEST_QUESTIONS.length; i++) {
    await runQuestion(TEST_QUESTIONS[i], i, TEST_QUESTIONS.length, bots);
  }

  // 5. End
  await fbPatch('/session', {state:'done'}).catch(()=>{});

  // 6. Final report
  process.stdout.write('\x1Bc');
  console.log(`\x1b[1m=== 최종 결과 (${N}명, ${TEST_QUESTIONS.length}문제) ===\x1b[0m\n`);
  console.log(`등록: 성공 ${stats.registered}명  오류 ${stats.regErrors}명\n`);

  let totalOk = 0, totalFail = 0, totalSkip = 0, allLats = [];
  Object.keys(stats.byQuestion).sort((a,b)=>+a-+b).forEach(k => {
    const q = stats.byQuestion[k]; const lats = q.latencies;
    const pct = Math.round(q.ok/N*100);
    const avg = lats.length ? Math.round(lats.reduce((a,b)=>a+b,0)/lats.length) : 0;
    const p99 = lats.length ? lats.slice().sort((a,b)=>a-b)[Math.floor(lats.length*0.99)|0]||0 : 0;
    const col = pct>=90?'\x1b[32m':pct>=60?'\x1b[33m':'\x1b[31m';
    console.log(`Q${+k+1}: ${col}제출 ${q.ok}/${N}명 (${pct}%)\x1b[0m  실패:${q.fail}  타임아웃:${q.skip}  레이턴시 평균:${avg}ms p99:${p99}ms`);
    totalOk+=q.ok; totalFail+=q.fail; totalSkip+=q.skip; allLats.push(...lats);
  });

  const totalExpected = N * TEST_QUESTIONS.length;
  const overallPct = Math.round(totalOk/totalExpected*100);
  const avgAll = allLats.length ? Math.round(allLats.reduce((a,b)=>a+b,0)/allLats.length) : 0;
  const sortedAll = allLats.slice().sort((a,b)=>a-b);
  const p99All = sortedAll[Math.floor(sortedAll.length*0.99)|0] || 0;
  const maxLat = sortedAll[sortedAll.length-1] || 0;

  console.log(`\n합계: ${totalOk}/${totalExpected}건 제출 (${overallPct}%)  실패:${totalFail}  타임아웃:${totalSkip}`);
  console.log(`전체 레이턴시: 평균 ${avgAll}ms  p99 ${p99All}ms  최대 ${maxLat}ms`);
  if (overallPct >= 90) console.log('\n\x1b[32m✅ 35명 동시 사용 안정적 — 실제 이벤트 운영 가능\x1b[0m');
  else                  console.log('\n\x1b[31m⚠️  제출률이 낮습니다. Firebase 설정 또는 네트워크 확인 필요\x1b[0m');

  // 7. Cleanup
  console.log('\n봇 데이터 삭제 중...');
  await Promise.allSettled(bots.map(b => b.stop()));
  console.log('완료.');
}

main().catch(e => { console.error(e); process.exit(1); });
