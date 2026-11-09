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
})();
