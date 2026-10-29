/* Topic, stage and mock exams (docs/PLAN.md 7 and 10; AUTHORING.md 5; design-research 4.7, 5.4, 6.2, 8.2, 8.4, 9.4).
   Route: #exam/<examId>, for content/exams/<examId>.json (topic-<topic>, stage-<n> or mock-<id>); an optional second
   segment, #exam/<examId>/<seed>, fixes the seed of generated items (otherwise a new seed per attempt).
   A paper may score { right, wrong, blank } with passNet (ENGINE-BACKLOG 450), run forward only with navigation
   "forward" and skip: false (451), and hold { generator: "arith" } entries that expand to seeded choice items (452).
   A mock exam (453) has a style and a models line, earns no XP, and every attempt is kept with a net score and trend.
   Start card, then the timed paper: one question at a time through ZQ.player.renderItem in exam mode (nothing is marked
   until you submit, one attempt, questions can be marked to come back to), a question navigator, a timer from the file
   and a finish-early path. A stage exam runs each paper in turn, then the checks the app cannot mark as self-ticks.
   The result: count-up, pass stamp, per-skill breakdown, per-paper marks and every question with its marking and worked
   explanation. Recorded once with ZQ.state.examFinished({ id, score, items, passed, bySkill, results, seconds }).
   Misses join the redo queue with ref { exam, item } (examFinished; ZQ.select.resolve reads them back).
   Test hooks: window.ZQ.test from the start card to the result (current, answerCorrect, check, continue), and while a
   paper is open window.ZQExam = { handles(), go(i), setRemaining(s), submit(), part() }. setRemaining moves the clock
   without waiting; nothing in the tools waits out a real timer.
   Every class carries the exm- prefix. */
(function () {
  'use strict';

  const LOW = 5 * 60;
  const MARK = 'M7 3.5h10a1 1 0 0 1 1 1V20.5l-6-4.25-6 4.25V4.5a1 1 0 0 1 1-1z';
  const CALC = 'M7 3h10a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zM8.5 6.5h7v3h-7zM8.5 13.5h.01M12 13.5h.01M15.5 13.5h.01M8.5 17h.01M12 17h.01M15.5 17h.01';
  const KIND = { choice: 'Single choice', multi: 'Select all that apply', numeric: 'Numeric answer', expression: 'Expression', order: 'Put in order', table: 'Fill in the table',
    place: 'Place the pieces', 'tap-regions': 'Tap the regions', slider: 'Set the value', 'drag-point': 'Drag the point', manipulate: 'Step by step', longform: 'Written answer', code: 'Code', sketch: 'Sketch', balance: 'Balance' };

  const clock = (s) => { s = Math.max(0, Math.ceil(s)); const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60); return h ? `${h}:${String(m).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}` : `${m}:${String(s % 60).padStart(2, '0')}`; };
  const listAnd = (xs) => (xs.length < 2 ? xs.join('') : xs.slice(0, -1).join(', ') + ' and ' + xs[xs.length - 1]);
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
  const icon = (Z, name, cls = '') => (name === 'calc' || name === 'mark' ? `<svg class="icon ${cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="${name === 'calc' ? CALC : MARK}"/></svg>` : Z.icon(name, cls));
  const G = () => ZQ.grade;
  const md = (s) => G().inline(s || '');
  const kindOf = (it) => (it.kind === 'longform' ? 'longform' : (it.widget || {}).kind || 'choice');
  const skillNames = () => { const out = {}; try { ZQ.content.courses().forEach(c => Object.assign(out, c.skills || {})); } catch { /* not loaded */ } return out; };

  /* The authored answer, written out for the result page */
  const correctHTML = (it) => {
    const w = it.widget || {};
    switch (w.kind) {
      case 'choice': { const o = (w.options || []).find(x => x.correct); return o ? md(o.text) : ''; }
      case 'multi': return (w.options || []).filter(x => x.correct).map(o => md(o.text)).join('<br>');
      case 'numeric': return w.accept ? md(w.accept) : G().fmtNum(+w.answer * (w.unit === '%' ? 100 : 1)) + (w.unit === '%' ? '%' : '');
      case 'expression': return ZQ.tex(w.answer || '');
      case 'order': return `<ol class="exm-ri-opts">${(w.answer || []).map(id => { const l = (w.lines || []).find(x => x.id === id); return `<li>${l ? md(l.text) : ''}</li>`; }).join('')}</ol>`;
      case 'table': { const out = []; (w.rows || []).forEach((r, i) => (r || []).forEach((c, j) => { if (c && typeof c === 'object' && c.edit) out.push(`${md(String((w.rows[i] || [])[0] ?? ''))}: ${G().fmtNum(+c.answer)}`); })); return out.join('<br>'); }
      case 'slider': return G().fmtNum(+w.answer);
      default: return '';
    }
  };

  /* ================================================================== */
  /* Exam: start card, papers, checks                                     */
  /* ================================================================== */
  function mountExam(root, Z, params) {
    const id = params[0];
    const cleanups = [];
    let alive = true;
    const shell = (inner) => `<div class="exm" data-track="prob"><header class="exm-top"><button type="button" class="icon-btn exm-close" aria-label="Close and return to Review">${Z.icon('close')}</button><p class="exm-top-t t-label">Exam</p><span></span></header>
      <div class="exm-frame"><main class="exm-main"><div class="exm-scroll"><div class="exm-col exm-intro">${inner}</div></div></main></div></div>`;
    const bail = (title, text) => { root.innerHTML = shell(`<h1 class="t-lesson-title">${Z.esc(title)}</h1><p class="t-prose exm-lede">${Z.esc(text)}</p><a class="btn" href="#review">Back to Review</a>`); root.querySelector('.exm-close').addEventListener('click', () => Z.go('review')); };
    if (!id) { bail('Choose an exam', 'Topic exams and stage exit tests are listed on the Review screen.'); return null; }
    root.innerHTML = shell('<p class="t-caption">Loading the exam</p>');
    root.querySelector('.exm-close').addEventListener('click', () => Z.go('review'));

    ZQ.content.exam(id).then((doc) => (doc && ZQ.arith ? ZQ.arith.ready.then(() => doc) : doc)).then((doc) => {
      if (!alive) return;
      if (!doc) { bail('Not yet written', `The exam ${id} has not been written yet.`); return; }
      run(doc);
    }).catch((e) => { console.error(e); if (alive) bail('The exam did not load', e.message); });

    function run(doc) {
      const M = ZQ.mock;
      const mock = M.is(doc.id);
      const stage = Array.isArray(doc.parts) && !mock;
      /* A mock has parts, or the fields of one paper at the top level */
      const raw = Array.isArray(doc.parts) ? doc.parts
        : [{ kind: 'paper', id: 'paper', name: doc.name, minutes: doc.minutes || 60, pass: doc.pass, passNet: doc.passNet, scoring: doc.scoring, navigation: doc.navigation, skip: doc.skip, items: doc.items || [] }];
      /* The seed fixes every generated item of this attempt; it is stored with the attempt */
      const seed = params[1] != null && /^\d+$/.test(params[1]) ? Number(params[1]) % 4294967296 : Math.floor(Math.random() * 4294967296);
      let paperNo = 0;
      const parts = raw.map(p => (p.kind === 'paper' ? Object.assign({}, p, { pass: p.pass == null && p.passNet == null ? 0.7 : p.pass, items: ZQ.arith ? ZQ.arith.expand(p.items || [], seed, paperNo++) : (p.items || []) }) : p));
      const papers = parts.filter(p => p.kind === 'paper');
      const checks = parts.filter(p => p.kind === 'check');
      const multi = stage || (mock && (papers.length > 1 || checks.length > 0));
      const generated = papers.some(p => p.items.some(it => it && it.generated));
      const scored = papers.some(M.scored);
      const topic = !stage && !mock && ZQ.content.topic(doc.topic);
      const mstyle = M.style(doc.style);
      const track = mock ? mstyle.track : (topic && topic.track) || (stage ? 'maths' : 'prob');
      const over = mock ? `Mock assessment · ${mstyle.label}` : stage ? `Stage ${doc.stage} · ${(ZQ.content.stage(doc.stage) || {}).name || ''}` : `Topic ${doc.topic} · ${topic ? topic.name : ''}`;
      const title = mock ? (doc.name || 'Mock assessment') : stage ? (doc.name || `Stage ${doc.stage} exit test`) : 'Topic exam';
      const names = Object.assign(skillNames(), doc.skills || {});
      const A = { results: [], used: [], flags: [], handles: [], ticks: new Set(), t0: Date.now(), seed };
      /* Test hook (docs/PLAN.md 7): kind 'start' on the start card, between papers and on the checks page (continue()
         begins, or ticks every check and shows the result), 'item' in a paper (check() grades the shown question without
         marking it; continue() moves on and submits after the last), 'done' on the result page. */
      let T = { kind: 'loading' };
      const hook = {
        current: () => (T.kind === 'item' ? T.cur() : { kind: T.kind, phase: 'exam', state: T.kind === 'done' ? 'done' : 'read', screenIndex: -1, ...(T.info || {}) }),
        answerCorrect: () => (T.answer ? T.answer() : false),
        check: async () => (T.check ? T.check() : null),
        continue: async () => { if (T.go) await T.go(); },
      };
      window.ZQ.test = hook;
      cleanups.push(() => { if (window.ZQ.test === hook) delete window.ZQ.test; });

      /* ---------- How a paper is marked and moved through (scoring, navigation, skip) ---------- */
      const fwd = (p) => p.navigation === 'forward';
      const noSkip = (p) => p.skip === false;
      const markLine = (p) => { const s = M.scoring(p); const f = (v) => (v > 0 ? '+' : v < 0 ? '\u2212' : '') + M.signed(Math.abs(v)); return `${f(s.right)} for a right answer, ${f(s.wrong)} for a wrong one, ${f(s.blank)} for a blank.`; };
      /* The pass mark as a heading and a sentence: a net score, or a share of the marks */
      const passOf = (p) => {
        const max = M.tally(p, []).max, need = M.need(p, max);
        if (typeof p.passNet === 'number') return [`Pass mark ${M.signed(need)} net`, `Out of ${M.signed(max)} marks.${M.scored(p) ? ' ' + markLine(p) : ''}`];
        return [`Pass mark ${Math.round(p.pass * 100)}%`, `That is ${M.signed(Math.ceil(max * p.pass - 1e-9))} of ${M.signed(max)} ${M.scored(p) ? 'marks' : 'correct'}.${M.scored(p) ? ' ' + markLine(p) : ''}`];
      };
      const wayOf = (p) => [fwd(p) ? 'forward only' : null, noSkip(p) ? 'no skipping' : null, M.scored(p) ? 'negative marking' : null].filter(Boolean);

      /* ---------- Start card ---------- */
      const intro = () => {
        const allItems = papers.flatMap(p => p.items || []);
        const mix = mock ? [] : [2, 3, 4, 5].map(d => [d, allItems.filter(it => it.difficulty === d).length]).filter(([, n]) => n);
        const kinds = [...new Set(allItems.map(kindOf))].map(k => (KIND[k] || k).toLowerCase());
        const minutes = papers.reduce((a, p) => a + (p.minutes || 0), 0);
        const p0 = papers[0], anyFwd = papers.some(fwd), allFwd = papers.every(fwd), anySkip0 = papers.some(noSkip);
        const rules = [
          ['clock', multi ? `${minutes} minutes in ${plural(papers.length, 'paper', 'papers')}` : `${minutes} minutes`, 'Each paper has its own clock. It starts when you begin and does not pause.'],
          ['clipboard', plural(allItems.length, 'question', 'questions'), generated ? `${kinds.length ? listAnd(kinds).replace(/^./, c => c.toUpperCase()) + '. ' : ''}Questions are generated afresh for each attempt.` : kinds.length ? `${listAnd(kinds).replace(/^./, c => c.toUpperCase())}.` : 'Mixed formats.'],
          ['bulb', 'No hints', 'Hints, explanations and animated aids are switched off.'],
          allFwd ? ['replay', 'No going back', `Each answer is final once you move on.${anySkip0 ? ' You must answer a question before the next one opens.' : ' A question you skip scores as blank.'}`]
            : ['replay', 'No retries', anyFwd ? 'One attempt. Some papers are forward only; the others let you change an answer until you submit.' : 'One attempt. You can change an answer until you submit.'],
          ['check', 'Marked when you submit', 'No feedback until then. Worked explanations follow.'],
          multi ? ['target', 'Pass every part', papers.map(p => `${p.name}: ${passOf(p)[0].replace(/^Pass mark /, '')}`).join('. ') + '.']
            : ['target', passOf(p0)[0], `${passOf(p0)[1]}${mock ? ' Every attempt is kept.' : ' A pass earns 200 XP.'}`],
          ...(scored && multi ? [['flag', 'Negative marking', papers.filter(M.scored).map(p => `${p.name}: ${markLine(p)}`).join(' ')]] : scored && !multi && typeof p0.passNet !== 'number' ? [['flag', 'Marking', markLine(p0)]] : []),
          ...(allFwd ? [] : [['mark', 'Mark questions', 'Mark any question to come back to before you submit.']]),
          ['calc', 'Finish early', allFwd ? 'The last question submits the paper. Time left over is not counted against you.' : 'Submit whenever you are done. Time left over is not counted against you.'],
        ];
        root.innerHTML = `<div class="exm" data-track="${track}">
          <header class="exm-top"><button type="button" class="icon-btn exm-close" aria-label="Close and return to Review">${Z.icon('close')}</button><p class="exm-top-t t-label">${Z.esc(title)}</p><span></span></header>
          <div class="exm-frame"><main class="exm-main">
            <div class="exm-scroll"><div class="exm-col exm-intro enter">
              <div class="exm-art">${window.ZQArt ? ZQArt(multi ? 'tree' : 'die', { label: 'Exam art' }) : ''}</div>
              <p class="t-overline exm-ov">${Z.esc(over)}</p>
              <h1 class="t-lesson-title">${Z.esc(title)}</h1>
              <p class="t-prose exm-lede">${Z.esc(mock ? (doc.description || 'A timed mock assessment. Sit it as often as you like: every attempt is kept.') : stage ? (doc.description || 'The exit test for this stage. Sit it first to skip the stage.') : `${doc.name || 'The topic exam'} covers every course in the topic. Sit it now to test out, or after the last course.`)}</p>
              ${mock && doc.models ? `<p class="t-caption exm-models"><b class="t-label">Models</b> ${Z.esc(doc.models)}</p>` : ''}
              ${multi ? `<ol class="exm-parts">${parts.map((p, i) => `<li><span class="exm-ri-n tnum">${i + 1}</span><span class="exm-parts-t"><b class="t-label">${Z.esc(p.name)}</b><span class="t-caption">${p.kind === 'paper' ? `${plural((p.items || []).length, 'question', 'questions')} · ${p.minutes} minutes · ${passOf(p)[0].replace(/^Pass mark/, 'pass')}${wayOf(p).length ? ' · ' + wayOf(p).join(', ') : ''}` : 'You tick this yourself at the end'}</span></span></li>`).join('')}</ol>` : ''}
              <ul class="exm-rules">${rules.map(([ic, h, t]) => `<li><span class="exm-rule-ic">${icon(Z, ic)}</span><div><b class="t-label">${Z.esc(h)}</b><p class="t-caption">${Z.esc(t)}</p></div></li>`).join('')}</ul>
              ${mix.length ? `<p class="t-caption exm-mix">Difficulty, on a scale of 1 to 5: ${listAnd(mix.map(([d, n]) => `${n} at level ${d}`))}.</p>` : ''}
            </div></div>
            <div class="exm-foot"><p class="t-caption exm-foot-note">Leaving after you begin ends the attempt.</p><div class="exm-actions"><button type="button" class="btn exm-begin">${multi ? 'Begin part 1' : 'Begin exam'}</button></div></div>
          </main></div></div>`;
        root.querySelector('.exm-close').addEventListener('click', () => Z.go('review'));
        root.querySelector('.exm-begin').addEventListener('click', () => paper(0));
        T = { kind: 'start', go: () => paper(0) };
      };

      /* ---------- Between papers ---------- */
      const between = (next) => {
        const p = papers[next];
        root.innerHTML = `<div class="exm" data-track="${track}">
          <header class="exm-top"><button type="button" class="icon-btn exm-close" aria-label="Leave the exam">${Z.icon('close')}</button><p class="exm-top-t t-label">${Z.esc(title)}</p><span></span></header>
          <div class="exm-frame"><main class="exm-main">
            <div class="exm-scroll"><div class="exm-col exm-intro enter">
              <p class="t-overline exm-ov">Part ${next} done</p>
              <h1 class="t-lesson-title">Next: ${Z.esc(p.name)}</h1>
              <p class="t-prose exm-lede">Your answers to part ${next} are saved and will be marked with the rest. Take a short break if you need one: the next clock starts when you begin.</p>
              <ul class="exm-rules"><li><span class="exm-rule-ic">${Z.icon('clock')}</span><div><b class="t-label">${p.minutes} minutes</b><p class="t-caption">${plural((p.items || []).length, 'question', 'questions')}${wayOf(p).length ? ', ' + wayOf(p).join(', ') : ''}.</p></div></li>
                <li><span class="exm-rule-ic">${Z.icon('target')}</span><div><b class="t-label">${Z.esc(passOf(p)[0])}</b><p class="t-caption">${Z.esc(passOf(p)[1])}</p></div></li></ul>
            </div></div>
            <div class="exm-foot"><div class="exm-actions"><button type="button" class="btn exm-begin">Begin part ${next + 1}</button></div></div>
          </main></div></div>`;
        root.querySelector('.exm-close').addEventListener('click', confirmLeave);
        root.querySelector('.exm-begin').addEventListener('click', () => paper(next));
        T = { kind: 'start', go: () => paper(next) };
      };

      /* ---------- The checks the app cannot mark ---------- */
      const checksPage = () => {
        root.innerHTML = `<div class="exm" data-track="${track}">
          <header class="exm-top"><button type="button" class="icon-btn exm-close" aria-label="Leave the exam">${Z.icon('close')}</button><p class="exm-top-t t-label">${Z.esc(title)}</p><span></span></header>
          <div class="exm-frame"><main class="exm-main">
            <div class="exm-scroll"><div class="exm-col exm-intro enter">
              <p class="t-overline exm-ov">Last part</p>
              <h1 class="t-lesson-title">What the app cannot mark</h1>
              <p class="t-prose exm-lede">Tick each one you have done. Be honest: the ${mock ? 'mock' : 'stage'} counts as passed only when every paper passes and every box is ticked.</p>
              <div class="exm-checks">${checks.map((c, i) => `<label class="hw-rb exm-chk"><input type="checkbox" data-chk="${i}"><span class="hw-box" aria-hidden="true">${Z.icon('check')}</span><span class="exm-chk-t"><b class="t-label">${Z.esc(c.name)}</b>${c.detail ? `<span class="t-caption">${Z.esc(c.detail)}</span>` : ''}</span></label>`).join('')}</div>
            </div></div>
            <div class="exm-foot"><div class="exm-actions"><button type="button" class="btn exm-begin">See results</button></div></div>
          </main></div></div>`;
        root.querySelector('.exm-close').addEventListener('click', confirmLeave);
        root.querySelectorAll('[data-chk]').forEach(cb => cb.addEventListener('change', () => { if (cb.checked) A.ticks.add(+cb.dataset.chk); else A.ticks.delete(+cb.dataset.chk); }));
        root.querySelector('.exm-begin').addEventListener('click', finish);
        T = { kind: 'start', go: () => { checks.forEach((c, i) => A.ticks.add(i)); finish(); } };
      };
      const dialogOpen = () => !!document.querySelector('.scrim');
      function confirmLeave() {
        if (dialogOpen()) return;
        const box = Z.h(`<div class="exm-dlg">
          <h2 class="t-sheet-title">Leave the exam?</h2>
          <p class="t-body exm-dlg-sub">Leaving ends this attempt. Nothing is marked or recorded.</p>
          <div class="exm-dlg-act"><button type="button" class="btn secondary" data-leave>End attempt</button><button type="button" class="btn" data-close>Keep going</button></div>
        </div>`);
        Z.sheet(box, { label: 'Leave the exam' });
        box.addEventListener('click', (e) => { if (e.target.closest('[data-leave]')) Z.go('review'); });
        setTimeout(() => box.querySelector('.btn[data-close]').focus(), 60);
      }

      /* ---------- A timed paper ---------- */
      function paper(pi) {
        const P = papers[pi], QS = P.items || [], N = QS.length, MINUTES = P.minutes || 60;
        const FWD = fwd(P), NOSKIP = noSkip(P), LOWAT = Math.min(LOW, MINUTES * 15);   // low-time warning: 5 minutes, or a quarter of a short paper
        const S = { cur: 0, flags: new Set(), t0: performance.now(), offset: 0, tick: null, low: false, over: false, anim: null };
        const local = [];
        const $ = (sel) => root.querySelector(sel);
        const label = multi ? `Part ${pi + 1} · ${P.name}` : title;
        root.innerHTML = `<div class="exm is-paper${FWD ? ' is-fwd' : ''}" data-track="${track}">
          <header class="exm-top">
            <button type="button" class="icon-btn exm-close" aria-label="Leave the exam">${Z.icon('close')}</button>
            <div class="exm-mid">
              <p class="exm-qof t-label">Question <span data-qn>1</span> of ${N}</p>
              <button type="button" class="exm-navbtn" aria-haspopup="dialog" aria-label="Question 1 of ${N}. Open the question navigator">${Z.icon('grid', 'sm')}<span><span class="exm-navbtn-w">Question </span><span data-qn>1</span> of ${N}</span>${Z.icon('chevronD', 'xs')}</button>
            </div>
            <div class="exm-right">
              <span class="exm-timer" role="timer" aria-label="Time left">${Z.icon('clock', 'sm')}<span data-time>${clock(MINUTES * 60)}</span></span>
              <button type="button" class="exm-markbtn" aria-pressed="false" aria-label="Mark question 1 to come back to">${icon(Z, 'mark', 'sm')}<span class="exm-mark-l">Mark</span></button>
            </div>
          </header>
          <div class="exm-frame">
            <main class="exm-main">
              <div class="exm-scroll"><div class="exm-col" data-col></div></div>
              <div class="exm-foot"><div class="exm-actions">
                <button type="button" class="btn secondary exm-prev" aria-label="Back to the previous question">${Z.icon('chevronL', 'sm')}<span class="exm-prev-l">Back</span></button>
                <button type="button" class="btn exm-next"><span>Next</span>${Z.icon('chevronR', 'sm')}</button>
              </div></div>
            </main>
            <aside class="exm-aside" aria-label="Question navigator">
              <p class="t-overline exm-ov">${Z.esc(label)}</p>
              <h2 class="t-h2">Questions</h2>
              <p class="t-caption exm-count" data-count></p>
              <div data-grid></div>
              ${legend()}
              <div class="exm-aside-foot"><button type="button" class="btn secondary block exm-submit">Finish early</button><p class="t-caption exm-zero">${M.scored(P) ? Z.esc(markLine(P)) : 'Unanswered questions score zero.'}</p></div>
            </aside>
          </div>
          <div class="sr-only" aria-live="polite" data-live></div>
        </div>`;
        const col = $('[data-col]');
        /* Every question is rendered once and kept, so answers survive moving between questions */
        QS.forEach((it, i) => {
          const wrap = Z.h(`<section class="exm-q" data-q-i="${i}" aria-label="Question ${i + 1}" hidden>
            <div class="exm-qhead"><span class="t-overline exm-ov">Question ${i + 1} · ${Z.esc(KIND[kindOf(it)] || 'Question')}</span><span class="exm-marked" hidden>${icon(Z, 'mark', 'xs')}Marked</span></div>
            <div class="exm-item" data-host></div></section>`);
          col.append(wrap);
          let h = null;
          try { h = ZQ.player.renderItem(Object.assign({}, it, { title: undefined }), wrap.querySelector('[data-host]'), { mode: 'exam', key: `exm-${pi}-${i}` }); } catch (e) { console.error(e); }
          local[i] = h;
          if (h) h.onChange(() => renderChrome());
        });
        A.handles[pi] = local;
        Z.mathify(col);
        const isAns = (i) => { const h = local[i]; if (!h) return false; try { return h.ready ? !!h.ready() : false; } catch { return false; } };
        const remaining = () => MINUTES * 60 - ((performance.now() - S.t0) / 1000 + S.offset);
        const announce = (t) => { const l = $('[data-live]'); if (l) { l.textContent = ''; setTimeout(() => { l.textContent = t; }, 30); } };
        const sqLabel = (i) => `Question ${i + 1}, ${isAns(i) ? 'answered' : 'not answered'}${S.flags.has(i) ? ', marked' : ''}`;
        const markBadge = () => `<span class="exm-sq-m" aria-hidden="true">${icon(Z, 'mark')}</span>`;
        const grid = (cls = '') => `<div class="exm-grid ${cls}" role="group" aria-label="Questions">${QS.map((q, i) => {
          const f = S.flags.has(i), c = i === S.cur;
          return `<button type="button" class="exm-sq${isAns(i) ? ' is-ans' : ''}${c ? ' is-cur' : ''}${f ? ' is-mark' : ''}" data-q="${i}" aria-label="${sqLabel(i)}"${c ? ' aria-current="step"' : ''}>${i + 1}${f ? markBadge() : ''}</button>`;
        }).join('')}</div>`;
        const syncGrid = (g) => g && g.querySelectorAll('[data-q]').forEach(b => {
          const i = +b.dataset.q, f = S.flags.has(i), c = i === S.cur;
          b.classList.toggle('is-ans', isAns(i)); b.classList.toggle('is-cur', c); b.classList.toggle('is-mark', f);
          b.setAttribute('aria-label', sqLabel(i));
          if (c) b.setAttribute('aria-current', 'step'); else b.removeAttribute('aria-current');
          const m = b.querySelector('.exm-sq-m');
          if (f && !m) b.insertAdjacentHTML('beforeend', markBadge()); else if (!f && m) m.remove();
        });
        const counts = () => { const a = QS.filter((q, i) => isAns(i)).length; return `${a} of ${N} answered${S.flags.size ? ` · ${S.flags.size} marked` : ''}`; };
        $('[data-grid]').innerHTML = grid();

        function renderChrome() {
          if (S.over) return;
          const i = S.cur, f = S.flags.has(i);
          root.querySelectorAll('[data-qn]').forEach(n => { n.textContent = i + 1; });
          $('.exm-navbtn').setAttribute('aria-label', `Question ${i + 1} of ${N}. Open the question navigator`);
          const mb = $('.exm-markbtn');
          mb.setAttribute('aria-pressed', String(f));
          mb.setAttribute('aria-label', `Mark question ${i + 1} to come back to`);
          mb.querySelector('.exm-mark-l').textContent = f ? 'Marked' : 'Mark';
          const prev = $('.exm-prev'), nx = $('.exm-next'), last = i === N - 1;
          prev.disabled = i === 0 || FWD;
          if (prev.disabled && document.activeElement === prev) nx.focus();
          /* A forward-only paper offers Skip on an unanswered question; with skip: false the button waits for an answer */
          const skipping = FWD && !NOSKIP && !last && !isAns(i), key = `${last}:${skipping}`;
          if (nx.dataset.last !== key) { nx.dataset.last = key; nx.innerHTML = last ? `<span>${multi && pi < papers.length - 1 ? `Submit part ${pi + 1}` : 'Submit exam'}</span>` : `<span>${skipping ? 'Skip' : 'Next'}</span>${Z.icon('chevronR', 'sm')}`; }
          nx.disabled = NOSKIP && !isAns(i);
          syncGrid($('[data-grid]'));
          $('[data-count]').textContent = counts();
          col.querySelectorAll('.exm-q').forEach((q, k) => { const tag = q.querySelector('.exm-marked'); if (tag) tag.hidden = !S.flags.has(k); });
        }
        function show(first) {
          const cur = col.querySelector(`[data-q-i="${S.cur}"]`);
          col.querySelectorAll('.exm-q').forEach(q => { q.hidden = q !== cur; });
          $('.exm-scroll').scrollTop = 0;
          if (!first && !Z.reducedMotion() && cur) cur.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: 200, easing: 'cubic-bezier(0.05, 0.7, 0.1, 1)' });
          renderChrome();
        }
        function go(i) {
          if (i < 0 || i >= N || S.over) return;
          if (i === S.cur) { renderChrome(); return; }
          if (FWD && i !== S.cur + 1) return;                                   // forward only: one step on, never back
          if (i > S.cur && NOSKIP) for (let k = S.cur; k < i; k++) if (!isAns(k)) return;   // skip: false: answer before moving on
          if (FWD) { try { local[S.cur] && local[S.cur].step.lock(); } catch (e) { console.error(e); } }   // the answer is final once you leave it
          S.cur = i; show(false);
          announce(`Question ${i + 1} of ${N}${S.flags.has(i) ? ', marked' : ''}`);
        }
        function toggleMark() {
          if (FWD) return;
          const i = S.cur;
          if (S.flags.has(i)) S.flags.delete(i); else S.flags.add(i);
          renderChrome();
          announce(S.flags.has(i) ? `Question ${i + 1} marked to come back to` : `Mark removed from question ${i + 1}`);
        }
        function onKey(e) {
          if (S.over || dialogOpen() || e.metaKey || e.ctrlKey || e.altKey) return;
          const t = e.target instanceof Element ? e.target : document.body;
          if (t.matches('input, textarea, select, math-field') || t.isContentEditable) return;
          if (/^[1-9]$/.test(e.key)) { const h = local[S.cur]; if (h && h.pick) { e.preventDefault(); h.pick(+e.key - 1); } }
          else if (FWD) { if (e.key === 'Enter' && !e.repeat && (t === document.body || t.classList.contains('opt')) && !$('.exm-next').disabled) { e.preventDefault(); $('.exm-next').click(); } }
          else if (e.key === 'ArrowRight' && !t.closest('[role="radiogroup"], .wd-opts')) { e.preventDefault(); go(S.cur + 1); }
          else if (e.key === 'ArrowLeft' && !t.closest('[role="radiogroup"], .wd-opts')) { e.preventDefault(); go(S.cur - 1); }
          else if (e.key === 'm' || e.key === 'M') { e.preventDefault(); toggleMark(); }
        }
        function updateTime() {
          if (S.over) return;
          const r = remaining(), el = $('[data-time]');
          if (!el) return;
          el.textContent = clock(r);
          const dt = document.querySelector('[data-dlg-time]'); if (dt) dt.textContent = clock(r);
          const low = r <= LOWAT;
          if (low !== S.low) {
            S.low = low;
            const tm = $('.exm-timer');
            tm.classList.toggle('is-low', low);
            tm.setAttribute('aria-label', low ? (LOWAT === LOW ? 'Time left, under 5 minutes' : 'Time left, running low') : 'Time left');
            if (low) announce(LOWAT === LOW ? 'Five minutes left.' : 'A quarter of the time is left.');
          }
          if (r <= 0) submit(true);
        }
        function openNav() {
          if (dialogOpen() || FWD) return;
          const box = Z.h(`<div class="exm-dlg exm-navsheet"><h2 class="t-sheet-title">Questions</h2><p class="t-caption exm-count">${counts()}</p>${grid('exm-grid-6')}${legend()}
            <div class="exm-dlg-act"><button type="button" class="btn secondary" data-submit>Finish early</button></div></div>`);
          const close = Z.sheet(box, { label: 'Question navigator' });
          box.addEventListener('click', (e) => {
            const b = e.target.closest('[data-q]');
            if (b) { close(); go(+b.dataset.q); } else if (e.target.closest('[data-submit]')) { close(); setTimeout(confirmSubmit, 60); }
          });
        }
        function confirmSubmit() {
          if (dialogOpen() || S.over) return;
          const un = QS.map((q, i) => i).filter(i => !isAns(i));
          const fl = FWD ? [] : [...S.flags].sort((a, b) => a - b);
          const jumps = (xs) => `<div class="exm-jumps">${xs.map(i => `<button type="button" class="exm-sq${isAns(i) ? ' is-ans' : ''}" data-q="${i}" aria-label="Go to question ${i + 1}">${i + 1}</button>`).join('')}</div>`;
          const what = multi && pi < papers.length - 1 ? `part ${pi + 1}` : 'your exam';
          const blank = M.signed(M.scoring(P).blank);
          const box = Z.h(`<div class="exm-dlg">
            <h2 class="t-sheet-title">Submit ${what}?</h2>
            <p class="t-body exm-dlg-sub">You cannot change answers after you submit. Time left: <b class="tnum" data-dlg-time>${clock(remaining())}</b>.</p>
            ${un.length ? `<div class="exm-dlg-sec"><h3 class="t-h2">Not answered: ${un.length}</h3><p class="t-caption exm-dlg-cap">${FWD ? `These score ${blank}. You cannot go back.` : `These score ${blank}. Choose one to go back to it.`}</p>${FWD ? '' : jumps(un)}</div>` : ''}
            ${fl.length ? `<div class="exm-dlg-sec"><h3 class="t-h2 exm-dlg-mh">${icon(Z, 'mark', 'xs')}Marked: ${fl.length}</h3><p class="t-caption exm-dlg-cap">You marked these to come back to.</p>${jumps(fl)}</div>` : ''}
            ${!un.length && !fl.length ? `<p class="exm-allset t-body">${Z.icon('check', 'sm')}All ${N} answered${FWD ? '' : ', none marked'}.</p>` : ''}
            <div class="exm-dlg-act"><button type="button" class="btn secondary" data-close>${FWD ? 'Not yet' : 'Keep working'}</button><button type="button" class="btn" data-submit>Submit</button></div>
          </div>`);
          const close = Z.sheet(box, { label: 'Submit' });
          box.addEventListener('click', (e) => {
            const b = e.target.closest('[data-q]');
            if (b) { close(); go(+b.dataset.q); } else if (e.target.closest('[data-submit]')) { close(); submit(false); }
          });
          setTimeout(() => box.querySelector('.btn[data-close]').focus(), 60);
        }
        async function submit(timeUp) {
          if (S.over) return;
          S.over = true;
          stop();
          document.querySelectorAll('.scrim, .sheet, .modal').forEach(n => n.remove());
          const used = Math.min(MINUTES * 60, Math.round((performance.now() - S.t0) / 1000 + S.offset));
          const res = [];
          for (let i = 0; i < N; i++) {
            const h = local[i];
            let r = { ok: false, key: null };
            if (h && isAns(i)) { try { r = await h.check(); } catch (e) { console.error(e); } }
            if (!r || r.pending) r = { ok: false, key: null };
            res[i] = { ok: !!r.ok, key: r.key ?? null, done: isAns(i), flag: S.flags.has(i), line: r.line || null };
          }
          A.results[pi] = res; A.used[pi] = used; A.flags[pi] = [...S.flags]; A.timeUp = A.timeUp || timeUp;
          /* Detach the rendered questions so the result page can show them, marked */
          local.forEach(h => { if (h && h.el) h.el.remove(); });
          if (pi + 1 < papers.length) between(pi + 1);
          else if (checks.length) checksPage();
          else finish();
          window.scrollTo(0, 0);
        }
        const stop = () => { clearInterval(S.tick); document.removeEventListener('keydown', onKey); delete window.ZQExam; };
        $('.exm-close').addEventListener('click', confirmLeave);
        $('.exm-navbtn').addEventListener('click', openNav);
        $('.exm-markbtn').addEventListener('click', toggleMark);
        $('.exm-prev').addEventListener('click', () => go(S.cur - 1));
        $('.exm-next').addEventListener('click', () => { if (!$('.exm-next').disabled) (S.cur === N - 1 ? confirmSubmit() : go(S.cur + 1)); });
        $('.exm-submit').addEventListener('click', confirmSubmit);
        $('[data-grid]').addEventListener('click', (e) => { const b = e.target.closest('[data-q]'); if (b) go(+b.dataset.q); });
        document.addEventListener('keydown', onKey);
        S.tick = setInterval(updateTime, 250);
        cleanups.push(stop);
        window.ZQExam = {
          handles: () => local.slice(), go, part: () => ({ index: pi, name: P.name, current: S.cur, total: N }),
          setRemaining: (s) => { S.offset = MINUTES * 60 - s - (performance.now() - S.t0) / 1000; updateTime(); },
          submit: () => submit(false),
        };
        T = {
          kind: 'item',
          cur: () => ({ kind: S.over ? 'loading' : 'item', phase: 'exam', state: isAns(S.cur) ? 'engaged' : 'idle', screenIndex: S.cur, total: N, paper: pi, forward: FWD, noSkip: NOSKIP }),
          answer: () => { const h = local[S.cur]; if (!h) return false; const ok = h.answerCorrect(); renderChrome(); return ok; },
          check: async () => { const h = local[S.cur]; return h ? h.step.grade() : null; },
          go: () => (S.cur < N - 1 ? go(S.cur + 1) : (NOSKIP && !isAns(S.cur) ? null : submit(false))),
        };
        show(true);
        updateTime();
        announce(`${multi ? `Part ${pi + 1} started` : 'Exam started'}. ${MINUTES} minutes. Question 1 of ${N}.`);
      }

      /* ---------- Mark, record, show ---------- */
      function finish() {
        if (!alive) return;
        const rows = [];
        papers.forEach((p, pi) => (p.items || []).forEach((it, i) => rows.push({ pi, i, it, r: (A.results[pi] || [])[i] || { ok: false, done: false }, h: ((A.handles[pi] || [])[i]) || null })));
        const bySkill = {};
        rows.forEach(({ it, r }) => (it.skills || []).forEach(s => { const b = bySkill[s] || (bySkill[s] = [0, 0]); b[1]++; if (r.ok) b[0]++; }));
        /* Each paper is marked by its own scoring (default +1, 0, 0) against passNet, else pass as a share of the marks */
        const paperScores = papers.map((p, pi) => { const t = M.tally(p, A.results[pi] || []); return { p, ...t, c: t.right, share: t.n ? t.right / t.n : 0, need: M.need(p, t.max), passed: M.passed(p, t) }; });
        const score = rows.filter(x => x.r.ok).length, total = rows.length;
        const sum = (k) => Math.round(paperScores.reduce((a, s) => a + s[k], 0) * 1e6) / 1e6;
        const net = sum('net'), max = sum('max'), wrong = sum('wrong'), blank = sum('blank');
        const checksOk = checks.every((c, i) => A.ticks.has(i));
        const passed = multi ? paperScores.every(s => s.passed) && checksOk : paperScores[0].passed;
        const seconds = A.used.reduce((a, b) => a + (b || 0), 0);
        let out = {};
        try {
          out = ZQ.state.examFinished({ id: doc.id, score, items: total, passed, bySkill, seconds,
            results: rows.map(({ it, r }) => ({ id: it.generated ? null : it.id, ok: !!r.ok, difficulty: it.difficulty || 3, skills: it.skills || [], ref: it.id != null && !it.generated ? { exam: doc.id, item: it.id } : null })),
            extra: mock || scored || generated ? { net, max, wrong, blank, seconds, ...(generated ? { seed: A.seed } : {}) } : undefined }) || {};
        } catch (e) { console.error(e); }
        T = { kind: 'done', info: { score, total, passed, net, max, wrong, blank, seed: A.seed } };
        cleanups.push(mountResult(root, Z, { doc, stage, mock, multi, scored, title, over, track, names, rows, bySkill, paperScores, checks, ticks: A.ticks, checksOk, score, total, net, max, wrong, blank, passed, seconds, xp: out.xp || 0, mp: out.mp || 0, timeUp: !!A.timeUp,
          minutes: papers.reduce((a, p) => a + (p.minutes || 0), 0) }));
      }

      intro();
    }

    const legend = () => `<ul class="exm-legend" aria-label="Key">
      <li><i class="exm-sq-k is-ans"></i>Answered</li><li><i class="exm-sq-k"></i>Not answered</li>
      <li><i class="exm-sq-k is-cur"></i>Current</li><li><i class="exm-sq-k exm-sq-km">${icon(Z, 'mark')}</i>Marked</li></ul>`;

    return () => { alive = false; cleanups.splice(0).forEach(f => { try { f && f(); } catch (e) { console.error(e); } }); };
  }

  /* ================================================================== */
  /* Result: count-up, stamp, breakdown, review                          */
  /* ================================================================== */
  function mountResult(root, Z, at) {
    const { rows, names, paperScores, stage, multi, mock, scored, score, total, passed } = at;
    const M = ZQ.mock;
    /* The headline is the net score when a paper is marked with wrong or blank marks, else the count of right answers */
    const heroN = scored ? at.net : score, heroMax = scored ? at.max : total;
    const pct = Math.max(0, Math.round(heroN / Math.max(1, heroMax) * 100));
    const p0 = paperScores[0];
    const PASS = multi || typeof p0.p.passNet === 'number' ? null : p0.p.pass;
    const passRef = multi ? 0.7 : PASS != null ? PASS : p0.max > 0 ? Math.min(1, Math.max(0, p0.need / p0.max)) : 0.7;
    const sgn = (v) => M.signed(v);
    const wrong = rows.filter(x => !x.r.ok);
    const flagged = rows.filter(x => x.r.flag);
    const bySkill = Object.entries(at.bySkill).map(([id, [c, t]]) => ({ id, name: names[id] || id, c, t, p: t ? c / t : 0, qs: rows.map((x, k) => ((x.it.skills || []).includes(id) ? k : -1)).filter(k => k >= 0) }))
      .sort((a, b) => a.p - b.p || a.name.localeCompare(b.name));
    const under = bySkill.filter(s => s.p < passRef);
    const timers = []; let raf = 0, final = false;
    const later = (fn, ms) => timers.push(setTimeout(fn, ms));
    const qlabel = (k) => (multi ? `${rows[k].pi + 1}.${rows[k].i + 1}` : String(k + 1));
    const hasSkills = Object.keys(at.bySkill).length > 0;
    /* This mock's attempts so far, newest last, with the one just recorded */
    const attempts = mock ? ((ZQ.state.exams[at.doc.id] || {}).attempts || []) : [];
    const nets = attempts.map(a => (typeof a.net === 'number' ? a.net : a.score));
    const marksOf = (x) => { const s = M.scoring(paperScores[x.pi].p); return x.r.ok ? s.right : x.r.done ? s.wrong : s.blank; };

    const skillRow = (s) => {
      const w = (s.p * 100).toFixed(2) + '%', near = Math.abs(s.p - passRef) < 0.06;
      const lab = `${s.name}: ${s.c} of ${s.t} correct, ${Math.round(s.p * 100)}%. Questions ${listAnd(s.qs.map(qlabel))}.`;
      return `<div class="exm-row" tabindex="0" role="listitem" aria-label="${Z.esc(lab)}" data-skill="${Z.esc(s.id)}">
        <span class="exm-row-l" aria-hidden="true">${Z.esc(s.name)}</span>
        <span class="exm-plot" aria-hidden="true"><i class="exm-bar" style="--w:${w}"></i><span class="exm-row-v tnum${near ? ' is-near' : ''}" style="--w:${w}">${s.c} of ${s.t}</span></span>
      </div>`;
    };
    const reviewItem = (x, k) => {
      const { it, r } = x;
      const fb = it.feedback || {};
      const line = r.ok ? fb.correct : (r.key != null && fb.byKey && fb.byKey[r.key]) || (r.done ? fb.generic : '');
      const mk = scored ? ` ${marksOf(x) > 0 ? '+' : ''}${sgn(marksOf(x))}` : '';
      const v = r.ok ? `<span class="exm-v is-ok">${Z.icon('check')}<span>Correct${mk}</span></span>` : `<span class="exm-v is-no">${Z.icon('cross')}<span>${r.done ? 'Not correct' : 'No answer'}${mk}</span></span>`;
      const ans = correctHTML(it);
      return `<article class="exm-ri${r.ok ? '' : ' is-no'}" data-ok="${r.ok}" data-flag="${!!r.flag}" data-k="${k}">
        <button type="button" class="exm-ri-h" aria-expanded="${!r.ok}" aria-controls="exm-rb-${k}">
          <span class="exm-ri-n tnum">${qlabel(k)}</span>
          <span class="exm-ri-t"><span class="t-label">${Z.esc(it.title || (it.question || '').replace(/\$[^$]*\$/g, '…').slice(0, 80))}</span><span class="t-caption exm-ri-meta">${it.generated ? 'Generated question' : `${Z.esc((it.skills || []).map(s => names[s] || s).join(', '))} · Difficulty ${it.difficulty || 3} of 5`}${r.flag ? ` · <span class="exm-ri-mark">${icon(Z, 'mark', 'xs')}Marked</span>` : ''}</span></span>
          ${v}
          <span class="exm-ri-chev" aria-hidden="true">${Z.icon('chevronD', 'sm')}</span>
        </button>
        <div class="exm-ri-b" id="exm-rb-${k}" ${r.ok ? 'hidden' : ''}>
          <div class="exm-ri-qrow"><div class="exm-ri-item" data-item="${k}"></div>
            <button type="button" class="icon-btn exm-report" data-report="${qlabel(k)}" aria-label="Report a problem with question ${qlabel(k)}" title="Report a problem with this question">${Z.icon('flag')}</button></div>
          ${ans ? `<dl class="exm-ans exm-ans-1"><div><dt class="t-caption">Correct answer</dt><dd>${ans}</dd></div></dl>` : ''}
          ${line ? `<p class="t-body ${r.ok ? 'exm-accept' : 'exm-diag'}">${md(line)}</p>` : ''}
          ${it.explain && it.explain.text ? `<p class="t-overline exm-ws-h">Worked explanation</p><p class="t-body exm-ws">${md(it.explain.text)}</p>` : ''}
        </div>
      </article>`;
    };

    const timeNote = at.timeUp ? 'Time ran out, so your answers were submitted automatically. ' : '';
    const needLine = (x) => (typeof x.p.passNet === 'number' ? `${sgn(x.need)} net` : `${Math.round(x.p.pass * 100)}% of the marks`);
    const heroNote = timeNote + (mock
      ? (multi
        ? (passed ? 'Every paper reached its pass mark and every check is ticked.' : `To pass, every paper must reach its pass mark${at.checks.length ? ' and every check must be ticked' : ''}.${paperScores.filter(x => !x.passed).length ? ` Short of the mark: ${listAnd(paperScores.filter(x => !x.passed).map(x => x.p.name))}.` : ''}`)
        : (passed ? `Pass mark ${needLine(p0)}. You scored ${sgn(at.net)} net.` : `Pass mark ${needLine(p0)}, which is ${sgn(p0.need)} of ${sgn(p0.max)}. You need ${sgn(Math.max(0, Math.round((p0.need - p0.net) * 1e6) / 1e6))} more net. Sit it again when you are ready.`))
        + (nets.length > 1 ? ` Attempt ${nets.length}; your best net is ${sgn(Math.max(...nets))}.` : '')
      : stage
      ? (passed ? 'Every paper passed and every check ticked. This stage counts as passed.' : `To pass, every paper must reach its pass mark and every check must be ticked.${at.checksOk ? '' : ' A check is not ticked yet.'}`)
      : (passed ? `Pass mark ${Math.round(PASS * 100)}%. This topic now counts as passed, so Today moves on. Its lessons stay open on Learn.`
        : `Pass mark ${Math.round(PASS * 100)}%, which is ${Math.ceil(total * PASS)} of ${total}. You need ${Math.max(0, Math.ceil(total * PASS) - score)} more. Study the skills below, then sit it again.`));

    root.innerHTML = `<div class="exm-res" data-track="${at.track}">
      <header class="exm-top exm-rtop">
        <button type="button" class="icon-btn exm-close" aria-label="Close results and return to Review">${Z.icon('close')}</button>
        <p class="exm-top-t t-label">${Z.esc(at.title)} · Result</p><span></span>
      </header>
      <main class="exm-rcol">
        <section class="exm-hero" aria-labelledby="exm-rh">
          <p class="t-overline exm-ov">${Z.esc(at.over)}</p>
          <h1 class="t-complete" id="exm-rh">${Z.esc(stage || mock ? at.title : (at.doc.name || 'Topic exam'))}</h1>
          <div class="exm-scorerow">
            <p class="exm-score"><span class="sr-only">${scored ? `Net score ${sgn(heroN)} of ${sgn(heroMax)}: ${score} right, ${at.wrong} wrong, ${at.blank} blank` : `${score} of ${total} correct, ${pct}%`}. ${passed ? 'Pass' : 'Not passed'}.</span>
              <span aria-hidden="true" class="exm-score-n"><b class="t-stat" data-score>0</b><span class="exm-of"> of ${sgn(heroMax)}${scored ? ' net' : ''}</span></span>
              <span aria-hidden="true" class="exm-pct tnum">${scored ? `${score} right · ${at.wrong} wrong · ${at.blank} blank` : `<span data-pct>0</span>% correct`}</span>
            </p>
            <div class="exm-stamp ${passed ? 'is-pass' : 'is-fail'}" aria-hidden="true">${Z.icon(passed ? 'check' : 'cross')}<span>${passed ? 'Pass' : 'Not passed'}</span></div>
          </div>
          <p class="t-body exm-hero-note exm-later" data-l="0">${Z.esc(heroNote)}</p>
          <div class="exm-badges">
            ${mock ? `<div class="exm-badge exm-later" data-l="1"><span class="t-caption exm-badge-l">${Z.icon('replay', 'xs')}Attempt</span><span class="exm-badge-v tnum">${nets.length}</span><span class="t-caption exm-badge-s">${nets.length > 1 ? `best net ${sgn(Math.max(...nets))}` : 'every attempt is kept'}</span></div>`
            : `<div class="exm-badge exm-xp exm-later" data-l="1"><span class="t-caption exm-badge-l">${Z.spark(at.xp > 0)}XP</span><span class="exm-badge-v tnum">${at.xp ? '+' + at.xp.toLocaleString('en-GB') : '0'}</span><span class="t-caption exm-badge-s">${passed ? (at.xp ? (stage ? 'Stage exam passed' : 'Topic exam passed') : 'Passed before') : `${stage ? '1,000' : '200'} on a pass`}</span></div>`}
            <div class="exm-badge exm-later" data-l="2"><span class="t-caption exm-badge-l">${Z.icon('clock', 'xs')}Time used</span><span class="exm-badge-v tnum">${clock(at.seconds)}</span><span class="t-caption exm-badge-s">of ${clock(at.minutes * 60)}${mock && total > 0 ? `, ${(at.seconds / total).toFixed(1)} s each` : ''}</span></div>
            <div class="exm-badge exm-later" data-l="3"><span class="t-caption exm-badge-l">${Z.icon('target', 'xs')}Mastery</span><span class="exm-badge-v tnum">+${at.mp}</span><span class="t-caption exm-badge-s">mastery points</span></div>
          </div>
          <button type="button" class="btn exm-back exm-later" data-l="3">Back to Review</button>
        </section>

        ${mock ? `<section class="exm-card exm-trend exm-later" data-l="4" aria-labelledby="exm-tr-h">
          <div class="exm-sec-h"><h2 class="t-h2" id="exm-tr-h">Score trend</h2></div>
          <p class="t-caption exm-sec-c">${multi ? 'Total net score' : 'Net score'} for each attempt, oldest first${multi ? '' : '. The dashed line is the pass mark'}.</p>
          <div class="exm-trend-row">${M.trend(nets, { pass: multi ? null : p0.need, label: 'Net score by attempt' })}<p class="t-body exm-trend-t tnum">${nets.length > 1 ? `Latest ${sgn(nets[nets.length - 1])}, previous ${sgn(nets[nets.length - 2])}, best ${sgn(Math.max(...nets))}.` : `First attempt: ${sgn(nets[0] == null ? at.net : nets[0])}. Sit it again to see a trend.`}</p></div>
        </section>` : ''}

        ${multi ? `<section class="exm-card exm-parts-r exm-later" data-l="4" aria-labelledby="exm-pt-h">
          <div class="exm-sec-h"><h2 class="t-h2" id="exm-pt-h">Part by part</h2></div>
          <ul class="exm-pres">${paperScores.map((s, i) => `<li class="${s.passed ? 'ok' : 'no'}"><span class="exm-ri-n tnum">${i + 1}</span><span class="exm-parts-t"><b class="t-label">${Z.esc(s.p.name)}</b><span class="t-caption">${M.scored(s.p) ? `${sgn(s.net)} net: ${s.c} right, ${s.wrong} wrong, ${s.blank} blank. Pass mark ${needLine(s)}.` : `${s.c} of ${s.n} correct, ${Math.round(s.share * 100)}%. Pass mark ${Math.round(s.p.pass * 100)}%.`}</span></span><span class="exm-v ${s.passed ? 'is-ok' : 'is-no'}">${Z.icon(s.passed ? 'check' : 'cross')}<span>${s.passed ? 'Passed' : 'Not passed'}</span></span></li>`).join('')}
            ${at.checks.map((c, i) => `<li class="${at.ticks.has(i) ? 'ok' : 'no'}"><span class="exm-ri-n tnum">${paperScores.length + i + 1}</span><span class="exm-parts-t"><b class="t-label">${Z.esc(c.name)}</b><span class="t-caption">Self-ticked check</span></span><span class="exm-v ${at.ticks.has(i) ? 'is-ok' : 'is-no'}">${Z.icon(at.ticks.has(i) ? 'check' : 'cross')}<span>${at.ticks.has(i) ? 'Ticked' : 'Not ticked'}</span></span></li>`).join('')}</ul>
        </section>` : ''}

        ${hasSkills ? `<section class="exm-card exm-skills exm-later" data-l="4" aria-labelledby="exm-sk-h">
          <div class="exm-sec-h"><h2 class="t-h2" id="exm-sk-h">By skill</h2><button type="button" class="link-btn exm-tbl-t" aria-pressed="false">Show as table</button></div>
          <p class="t-caption exm-sec-c" data-cap>Share of questions correct in each skill, weakest first. The dashed line is the ${Math.round(passRef * 100)}% pass mark.</p>
          <div class="exm-chart" style="--pass:${passRef}">
            <div class="exm-gl" aria-hidden="true"><i style="--x:0"></i><i style="--x:0.5"></i><i style="--x:1"></i></div>
            <div class="exm-ref" aria-hidden="true" style="--x:${passRef}"><span class="t-caption">Pass mark ${Math.round(passRef * 100)}%</span></div>
            <div class="exm-rows" role="list" aria-label="Correct answers by skill">${bySkill.map(skillRow).join('')}</div>
            <div class="exm-axis t-caption" aria-hidden="true"><span style="--x:0">0%</span><span style="--x:0.5">50%</span><span style="--x:1">100%</span></div>
            <div class="exm-tip" role="presentation" hidden><b></b><span></span></div>
          </div>
          <table class="exm-table" hidden>
            <caption class="sr-only">Correct answers by skill</caption>
            <thead><tr><th scope="col">Skill</th><th scope="col" class="num">Correct</th><th scope="col" class="num">Share</th><th scope="col">Questions</th></tr></thead>
            <tbody>${bySkill.map(s => `<tr><th scope="row">${Z.esc(s.name)}</th><td class="num">${s.c} of ${s.t}</td><td class="num">${Math.round(s.p * 100)}%</td><td>${s.qs.map(qlabel).join(', ')}</td></tr>`).join('')}</tbody>
          </table>
          <p class="t-body exm-sk-note">${under.length ? `Under the pass mark: ${Z.esc(listAnd(under.slice(0, 6).map(s => `${s.name} (${s.c} of ${s.t})`)))}${under.length > 6 ? `, and ${under.length - 6} more` : ''}. Start there before you sit it again.` : 'Every skill is at or above the pass mark.'}</p>
        </section>` : ''}

        <section class="exm-review exm-later" data-l="5" aria-labelledby="exm-rv-h">
          <h2 class="t-h1" id="exm-rv-h">Your answers</h2>
          <p class="t-body exm-sec-c">Each question shows your answer as marked, the accepted answer and a worked explanation.</p>
          <div class="exm-filter" role="group" aria-label="Show">
            <button type="button" class="chip on" data-f="all" aria-pressed="true">All <span class="tnum">${total}</span></button>
            <button type="button" class="chip" data-f="wrong" aria-pressed="false">Not correct <span class="tnum">${wrong.length}</span></button>
            <button type="button" class="chip" data-f="flag" aria-pressed="false">Marked <span class="tnum">${flagged.length}</span></button>
          </div>
          <div class="exm-list">${rows.map(reviewItem).join('')}</div>
          <p class="t-body exm-empty" hidden>Nothing here.</p>
          <button type="button" class="btn exm-back exm-back-end">Back to Review</button>
        </section>
      </main>
    </div>`;

    const res = root.querySelector('.exm-res');
    const q = (s) => res.querySelector(s);
    /* Put each rendered question back, marked, inside its review card */
    rows.forEach((x, k) => {
      const slot = res.querySelector(`[data-item="${k}"]`);
      if (!slot || !x.h || !x.h.el) return;
      try { x.h.step.lock(); if (x.r.done) x.h.step.mark({ ok: x.r.ok, key: x.r.key, final: true }); } catch (e) { console.error(e); }
      slot.append(x.h.el);
    });
    Z.mathify(res);
    const scoreEl = q('[data-score]'), pctEl = q('[data-pct]'), stamp = q('.exm-stamp');

    q('.exm-close').addEventListener('click', () => Z.go('review'));
    res.querySelectorAll('.exm-back').forEach(b => b.addEventListener('click', () => Z.go('review')));
    res.querySelectorAll('.exm-ri-h').forEach(b => b.addEventListener('click', () => {
      const open = b.getAttribute('aria-expanded') !== 'true';
      b.setAttribute('aria-expanded', String(open));
      b.nextElementSibling.hidden = !open;
    }));
    res.addEventListener('click', (e) => {
      const b = e.target.closest('[data-report]'); if (!b || b.classList.contains('is-sent')) return;
      b.classList.add('is-sent');
      b.setAttribute('aria-label', `Problem reported on question ${b.dataset.report}`); b.title = 'Reported';
      Z.toast(`Noted. Question ${b.dataset.report} and its answer key are flagged for checking.`);
    });
    const filter = q('.exm-filter');
    filter.addEventListener('click', (e) => {
      const c = e.target.closest('[data-f]'); if (!c) return;
      filter.querySelectorAll('[data-f]').forEach(x => { const on = x === c; x.classList.toggle('on', on); x.setAttribute('aria-pressed', String(on)); });
      let n = 0;
      res.querySelectorAll('.exm-ri').forEach(it => {
        const show = c.dataset.f === 'all' || (c.dataset.f === 'wrong' && it.dataset.ok === 'false') || (c.dataset.f === 'flag' && it.dataset.flag === 'true');
        it.hidden = !show; if (show) n++;
      });
      q('.exm-empty').hidden = n > 0;
    });
    if (hasSkills) {
      const tblBtn = q('.exm-tbl-t');
      tblBtn.addEventListener('click', () => {
        const on = tblBtn.getAttribute('aria-pressed') !== 'true';
        tblBtn.setAttribute('aria-pressed', String(on));
        tblBtn.textContent = on ? 'Show as chart' : 'Show as table';
        q('.exm-chart').hidden = on; q('.exm-table').hidden = !on;
      });
      const chart = q('.exm-chart'), tip = q('.exm-tip');
      const showTip = (row) => {
        const s = bySkill.find(x => x.id === row.dataset.skill); if (!s) return;
        tip.querySelector('b').textContent = `${Math.round(s.p * 100)}%`;
        tip.querySelector('span').textContent = `${s.name} · ${s.c} of ${s.t} correct · Questions ${listAnd(s.qs.map(qlabel))}`;
        tip.hidden = false;
        const cr = chart.getBoundingClientRect(), br = row.querySelector('.exm-plot').getBoundingClientRect();
        const x = br.left - cr.left + br.width * s.p, tw = tip.offsetWidth;
        tip.style.left = Math.max(tw / 2, Math.min(cr.width - tw / 2, x)) + 'px';
        tip.style.top = (br.top - cr.top - 8) + 'px';
      };
      const hideTip = () => { tip.hidden = true; };
      chart.addEventListener('pointerover', (e) => { const r = e.target.closest('.exm-row'); if (r) showTip(r); });
      chart.addEventListener('pointerleave', hideTip);
      chart.addEventListener('focusin', (e) => { const r = e.target.closest('.exm-row'); if (r) showTip(r); });
      chart.addEventListener('focusout', hideTip);
    }

    /* Celebration (spec 4.7): count-up 900ms, stamp on spring-snap, breakdown fades in. Tap skips. */
    const finish = () => {
      if (final) return;
      final = true;
      timers.splice(0).forEach(clearTimeout); cancelAnimationFrame(raf);
      scoreEl.textContent = sgn(heroN); if (pctEl) pctEl.textContent = pct;
      res.classList.add('final');
      stamp.classList.add('on');
      res.querySelectorAll('.exm-later').forEach(n => n.classList.add('on'));
    };
    const countUp = (ms) => new Promise(done => {
      const t0 = performance.now();
      const step = (now) => {
        const p = Math.min(1, (now - t0) / ms);
        const e = p < 0.8 ? p / 0.8 * 0.9 : 0.9 + (1 - Math.pow(1 - (p - 0.8) / 0.2, 3)) * 0.1;
        scoreEl.textContent = sgn(Math.round(heroN * e)); if (pctEl) pctEl.textContent = Math.round(pct * e);
        if (p < 1) raf = requestAnimationFrame(step); else done();
      };
      raf = requestAnimationFrame(step);
    });
    let onKey = null;
    if (Z.reducedMotion()) { res.classList.add('rm'); finish(); }
    else {
      countUp(900).then(() => {
        if (final) return;
        stamp.classList.add('on');
        if (passed) Z.sound('complete');
        res.querySelectorAll('.exm-later').forEach(n => later(() => n.classList.add('on'), 260 + (+n.dataset.l) * 80));
        later(finish, 1200);
      });
      res.addEventListener('pointerdown', (e) => { if (!final && !e.target.closest('.exm-top')) finish(); });
      onKey = (e) => { if (!final && (e.key === 'Enter' || e.key === ' ' || e.key === 'Escape')) finish(); };
      document.addEventListener('keydown', onKey);
    }
    window.scrollTo(0, 0);
    return () => { timers.forEach(t => t && clearTimeout(t)); cancelAnimationFrame(raf); if (onKey) document.removeEventListener('keydown', onKey); rows.forEach(x => { try { x.h && x.h.destroy(); } catch (e) { console.error(e); } }); };
  }

  ZQ.screen({ id: 'exam', title: 'Exam', group: 'Assessment', shell: false, render: (root, Z, params = []) => mountExam(root, Z, params) });
})();
