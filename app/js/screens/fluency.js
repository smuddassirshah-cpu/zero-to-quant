/* Fluency sets (ENGINE-BACKLOG 808, 809; author side docs/AUTHORING.md section 16).
   Route: #fluency/<course>/<set id>[/<seed>]. The set is content/courses/<course>/fluency-<lesson>.json: families of generated
   typed-answer items. ZQ.gen draws n items from a fresh seed (a seed in the route repeats an attempt), ZQ.player.runSet plays them
   (one item a screen, one try, no hints; a wrong answer shows the matched `wrong` line and then the solution steps), and the shared
   set page (ZQ.setPage, js/screens/review.js) frames it. The result goes to ZQ.state.fluency (attempts, best score, last pass date,
   right and wrong per family). A fluency pass changes no skill score, streak, XP, met rule or gate. */
(function () {
  'use strict';
  const ZQ = window.ZQ;

  function mountFluency(root, Z, params) {
    const cid = params[0], id = params[1];
    const seed = params[2] != null && /^\d+$/.test(params[2]) ? Number(params[2]) : (Math.random() * 4294967296) >>> 0;
    const S = () => ZQ.state, C = () => ZQ.content;
    const co = (() => { try { return C().course(cid); } catch { return null; } })();
    let mark = 0;
    const families = (items, res) => {
      const f = {};
      items.forEach((it, j) => { const r = res[j]; if (!r || !it.fluency) return; const x = f[it.fluency.family] || (f[it.fluency.family] = [0, 0]); if (r.ok) x[0]++; else x[1]++; });
      return f;
    };
    const hours = (seconds) => { const m = seconds / 60; if (m >= 0.1) { try { S().hours.log({ block: 'review', minutes: m, source: 'fluency' }); } catch (e) { console.error(e); } } };
    const cfg = {
      title: 'Fluency', sub: '', over: `${co ? co.name : cid} · Fluency`, heading: 'Fluency', track: (co && co.track) || 'maths', perItem: 0.5, overview: false,
      back: `course/${cid}`, backLabel: 'the course', again: 'Go again', againRoute: () => `fluency/${cid}/${id}`,
      lede: 'Fresh numbers every time, so the only way through is to be fluent. Type each answer; it is checked at once.',
      emptyTitle: 'Not found', emptyText: 'There is no fluency set with this name. Open it from the course map.',
      doneTitle: 'Fluency set done', setTitle: 'Fluency',
      load: () => C().fluencySet(cid, id).then((d) => {
        if (!d || !Array.isArray(d.families)) return [];
        const items = ZQ.gen.generate(d, seed).map((it, k) => ZQ.gen.playerItem(it, d, k));
        mark = ZQ.gen.passMark(d, items.length);
        cfg.title = d.title || 'Fluency'; cfg.heading = d.title || 'Fluency'; cfg.sub = co ? co.name : '';
        cfg.perItem = (d.minutes || 10) / Math.max(1, d.n || items.length);
        cfg.facts = [['target', `Pass at ${mark} of ${items.length}. Passing is practice you can keep: it changes no progress.`], ['replay', 'Go again for new numbers; the same questions never come back.']];
        return items;
      }),
      record: (items, res, seconds) => {
        const right = res.filter((r) => r && r.ok).length, passed = right >= mark;
        const rec = S().fluency.result({ course: cid, id, right, n: items.length, passed, families: families(items, res) });
        hours(seconds);
        return {
          verdict: passed ? `Passed: ${right} of ${items.length}. The pass mark is ${mark}.` : `Not passed: ${right} of ${items.length}. The pass mark is ${mark}.`,
          badges: [[rec.best, 'best score'], [rec.attempts, rec.attempts === 1 ? 'attempt' : 'attempts']],
          note: passed ? 'Well done. Go again any time for fresh numbers.' : 'Each miss showed its working. Go again for new numbers when you are ready.',
        };
      },
      partial: (items, res, seconds) => { S().fluency.result({ course: cid, id, right: 0, n: items.length, families: families(items, res), partial: true }); hours(seconds); },
    };
    return ZQ.setPage(root, Z, cfg);
  }

  ZQ.screen({ id: 'fluency', title: 'Fluency', group: 'Practice', hidden: true, shell: false, render: (root, Z, params = []) => mountFluency(root, Z, params) });

  /* ENGINE-BACKLOG 843: the full list Today's "More Fluency sets" row leads to. Route #fluency-list. Every real set, grouped by course in
     course order; each row says whether its lesson is done and whether the set is passed, and opens the set (a set whose lesson is not done
     is listed but dimmed: practice follows the lesson). Reads ZQ.content.fluencyList and ZQ.state; nothing here gates anything. */
  ZQ.screen({
    id: 'fluency-list', title: 'Fluency sets', group: 'Practice', hidden: true, shell: true, tab: 'today',
    render(root, Z) {
      const C = Z.content, S = Z.state, esc = Z.esc;
      const rows = C.fluencyList ? C.fluencyList() : [];
      const stat = (r) => { const l = S.lesson(r.course, r.lesson), f = S.fluency.get(r.course, r.id), done = !!(l && l.done); return { done, passed: !!(f && f.passedAt), tried: !!(f && f.attempts) }; };
      const courses = [...new Set(rows.map(r => r.course))];
      const item = (r) => {
        const st = stat(r), lab = !st.done ? 'Lesson not done yet' : st.passed ? 'Passed' : st.tried ? 'Tried, not passed' : 'Not started';
        return `<li><button class="zt-row${st.done ? '' : ' muted'}" type="button" data-go="fluency/${esc(r.course)}/${esc(r.id)}" data-fluency-item="${esc(r.course)}/${esc(r.id)}" data-status="${st.done ? (st.passed ? 'passed' : 'open') : 'locked'}">
          <span class="zt-row-t"><span class="t-label">${esc(r.title || 'Fluency')}</span><span class="t-caption muted">${r.n} fresh questions · about ${r.minutes} minutes · ${lab}</span></span>
          ${Z.icon('chevronR', 'sm zt-chev')}</button></li>`;
      };
      const group = (c) => { const co = (() => { try { return C.course(c); } catch { return null; } })(); return `<h2 class="t-overline muted">${esc(co ? co.name : c)}</h2><ul>${rows.filter(r => r.course === c).map(item).join('')}</ul>`; };
      root.innerHTML = `<div class="card pad" data-fluency-list>
        <h1 class="t-h2">Fluency sets</h1>
        <p class="t-body secondary">Fresh numbers every time. Passing changes no progress.</p>
        ${rows.length ? courses.map(group).join('') : '<p class="t-body secondary">No Fluency sets are written yet.</p>'}
        <a class="btn secondary" href="#today">Back to Today</a></div>`;
      root.addEventListener('click', (e) => { const g = e.target.closest('[data-go]'); if (g) { if (Z.sound) Z.sound('tap'); Z.go(g.dataset.go); } });
      return null;
    },
  });
})();
