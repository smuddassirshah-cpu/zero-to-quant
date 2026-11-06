/* Mock assessments: marking and trend helpers shared by the exam screen, Review and You (ENGINE-BACKLOG 450 to 453).
   A mock is content/exams/mock-<id>.json; its papers may carry scoring { right, wrong, blank } and passNet.
     ZQ.mock.is(id)                  true for a mock exam id
     ZQ.mock.style(name)             { label, track } for trader, research, developer or strats
     ZQ.mock.scoring(paper)          { right, wrong, blank } with the defaults 1, 0, 0
     ZQ.mock.scored(paper)           true when marking is not plain right-or-nothing
     ZQ.mock.tally(paper, results)   { n, right, wrong, blank, net, max } from per-item { ok, done, credit? }; an item with parts that is
                                     not right in full counts its credit (the share of parts right) as right and the rest as wrong; a written item marked by its rubric (result.rubric) counts ticks over points the same way, pass or not (ENGINE-BACKLOG 589)
     ZQ.mock.draw(entries, opts)     async: a paper's `draw` entries resolved to items (ENGINE-BACKLOG 468): see the block below
     ZQ.mock.passed(paper, tally, results?)  net against passNet, else the net share against pass (default 0.7); with results, false while an item
                                     with required: true is not right (ENGINE-BACKLOG 592). ZQ.mock.requiredMissed(paper, results) lists those indices
     ZQ.mock.roleOf(track)           the role id of a profile track (Trader trader, Researcher research, Developer developer, Strats strats), else null
     ZQ.mock.paperFor(paper, role)   true when the paper has no `tracks` or lists the role ("researcher" reads as "research"; ENGINE-BACKLOG 593)
     ZQ.mock.need(paper, max)        the pass mark as a net score
     ZQ.mock.signed(n)               a score with a true minus sign
     ZQ.mock.trend(values, opts)     a small SVG column trend of net scores, oldest first (opts: pass, label, max)
     ZQ.mock.family(item, names)     { id, label } for an item: its first `tags` entry, else its first skill (label from names), else mental-arithmetic for a generated item, else null
     ZQ.mock.fmtSeconds(s)           "41 s", or "2 min 05 s" from 120 s
     ZQ.mock.pacing(rows)            the results line for a timed set (ENGINE-BACKLOG 457): rows are { label, seconds, pace?, family?, familyLabel? };
                                     returns { n, total, avg, families, over, text } where text names the average, the slowest families
                                     (by mean seconds, at most three) and the items over their `pace`. Time never affects grading. */
(function () {
  'use strict';
  const Z = window.ZQ = window.ZQ || {};
  const STYLES = { trader: { label: 'Trader', track: 'speed' }, research: { label: 'Research', track: 'ml' }, developer: { label: 'Developer', track: 'code' }, strats: { label: 'Strats', track: 'fin' } };
  const num = (v, d) => (typeof v === 'number' && Number.isFinite(v) ? v : d);
  const scoring = (p) => { const s = (p && p.scoring) || {}; return { right: num(s.right, 1), wrong: num(s.wrong, 0), blank: num(s.blank, 0) }; };
  const scored = (p) => { const s = scoring(p); return s.right !== 1 || s.wrong !== 0 || s.blank !== 0; };
  const round = (x) => Math.round(x * 1e6) / 1e6;
  /* results[i] = { ok, done }: done means the learner gave an answer (blank otherwise) */
  const tally = (p, results) => {
    const s = scoring(p), n = (p.items || []).length;
    let right = 0, wrong = 0, blank = 0;
    for (let i = 0; i < n; i++) {
      const r = (results || [])[i];
      if (r && r.done && (r.rubric || r.fractional) && typeof r.credit === 'number') { right += r.credit; wrong += 1 - r.credit; }   // a written item (marked by its rubric) or an item with parts that holds a written part (fractional): ticks over points, pass or not
      else if (r && r.ok) right++;
      else if (r && r.done && typeof r.credit === 'number' && r.credit > 0 && r.credit < 1) { right += r.credit; wrong += 1 - r.credit; }   // an item with parts: equal credit per part
      else if (r && r.done) wrong++;
      else blank++;
    }
    return { n, right, wrong, blank, net: round(right * s.right + wrong * s.wrong + blank * s.blank), max: round(n * s.right) };
  };
  const need = (p, max) => (typeof p.passNet === 'number' ? p.passNet : round((typeof p.pass === 'number' ? p.pass : 0.7) * max));
  /* ENGINE-BACKLOG 592: an item with required: true must be right (result.ok) whatever the share; requiredMissed lists the indices that were not */
  const requiredMissed = (p, results) => (p.items || []).map((it, i) => (it && it.required === true && !((results || [])[i] && results[i].ok) ? i : -1)).filter(i => i >= 0);
  const passed = (p, t, results) => (t.n > 0 && t.net >= need(p, t.max) - 1e-9 && (!results || !requiredMissed(p, results).length));
  const ROLE_OF = { Trader: 'trader', Researcher: 'research', Developer: 'developer', Strats: 'strats' };
  const roleOf = (track) => ROLE_OF[track] || null;
  const paperFor = (p, role) => { const t = p && Array.isArray(p.tracks) ? p.tracks.map(x => (x === 'researcher' ? 'research' : x)) : null; return !t || !t.length || (role != null && t.includes(role === 'researcher' ? 'research' : role)); };
  const signed = (n) => String(round(n)).replace('-', '−');

  /* Net scores as columns from a zero line; the dashed line is the pass mark. Text alternative in aria-label. */
  const trend = (values, o = {}) => {
    const vs = (values || []).filter(v => typeof v === 'number' && Number.isFinite(v)).slice(-10);
    if (!vs.length) return '';
    const W = 132, H = 40, pad = 3, n = vs.length;
    const hi = Math.max(...vs, o.pass == null ? -Infinity : o.pass, o.max == null ? -Infinity : o.max, 1), lo = Math.min(0, ...vs);
    const y = (v) => pad + (H - 2 * pad) * (1 - (v - lo) / (hi - lo || 1));
    const band = (W - 2 * pad) / n, bw = Math.max(3, Math.min(16, band * 0.62));
    const bars = vs.map((v, i) => { const x = pad + band * i + (band - bw) / 2, y0 = y(0), y1 = y(v), top = Math.min(y0, y1), h = Math.max(1.5, Math.abs(y0 - y1)); return `<rect class="mk-col${i === n - 1 ? ' now' : ''}${v < 0 ? ' neg' : ''}" x="${x.toFixed(1)}" y="${top.toFixed(1)}" width="${bw.toFixed(1)}" height="${h.toFixed(1)}" rx="2"/>`; }).join('');
    const line = o.pass == null ? '' : `<line class="mk-pass" x1="${pad}" x2="${W - pad}" y1="${y(o.pass).toFixed(1)}" y2="${y(o.pass).toFixed(1)}"/>`;
    const label = `${o.label || 'Net score'}${n > 1 ? ', oldest first' : ''}: ${vs.map(signed).join(', ')}${o.pass == null ? '' : `. Pass mark ${signed(o.pass)}`}.`;
    return `<svg class="mk-trend" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="${String(label).replace(/"/g, '&quot;')}"><line class="mk-zero" x1="${pad}" x2="${W - pad}" y1="${y(0).toFixed(1)}" y2="${y(0).toFixed(1)}"/>${bars}${line}</svg>`;
  };

  /* ---------- Per-item timing (ENGINE-BACKLOG 457) ---------- */
  const fmtSeconds = (s) => { const r = Math.round(s); return r < 120 ? `${r} s` : `${Math.floor(r / 60)} min ${String(r % 60).padStart(2, '0')} s`; };
  const family = (it, names) => {
    if (!it) return null;
    const t = Array.isArray(it.tags) && typeof it.tags[0] === 'string' ? it.tags[0] : null;
    if (t) return { id: t, label: t };
    const s = Array.isArray(it.skills) && it.skills[0];
    if (s) return { id: s, label: (names && names[s]) || s };
    return it.generated ? { id: 'mental-arithmetic', label: 'mental-arithmetic' } : null;   // a generated arithmetic item
  };
  const listAnd = (a) => (a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1]);
  const pacing = (rows) => {
    const list = (rows || []).filter(r => r && typeof r.seconds === 'number' && Number.isFinite(r.seconds) && r.seconds >= 0);
    if (!list.length) return { n: 0, total: 0, avg: 0, families: [], over: [], paced: 0, text: '' };
    const total = list.reduce((a, r) => a + r.seconds, 0), avg = total / list.length;
    const byFam = new Map();
    list.forEach(r => { if (!r.family) return; const f = byFam.get(r.family) || { id: r.family, label: r.familyLabel || r.family, n: 0, seconds: 0 }; f.n++; f.seconds += r.seconds; byFam.set(r.family, f); });
    const families = [...byFam.values()].map(f => ({ ...f, avg: f.seconds / f.n })).sort((a, b) => b.avg - a.avg || a.label.localeCompare(b.label));
    const paced = list.filter(r => typeof r.pace === 'number' && r.pace > 0);
    const over = paced.filter(r => r.seconds > r.pace + 1e-9);
    const out = [`Average ${fmtSeconds(avg)} a question, ${fmtSeconds(total)} in all.`];
    if (families.length) {
      const top = families.slice(0, 3);
      out.push(`${families.length > 1 ? 'Slowest families' : 'Family'}: ${top.map(f => `${f.label} ${fmtSeconds(f.avg)}`).join(', ')}.`);
    }
    if (paced.length) out.push(over.length ? `Over pace: ${over.length} of ${paced.length} (${listAnd(over.map(r => `question ${r.label}, ${fmtSeconds(r.seconds)} against ${fmtSeconds(r.pace)}`))}).` : `Every paced question was inside its pace (${paced.length}).`);
    return { n: list.length, total, avg, families, over, paced: paced.length, text: out.join(' ') };
  };


  /* ---------- Exam item draws (ENGINE-BACKLOG 468, docs/AUTHORING.md 5 "Drawn items") ----------
     A paper's `draw: [{ from, tags?, difficulty?, n }]` adds n items per entry after the paper's own `items`, chosen when the
     attempt begins from the seed (and so fixed by #exam/<id>/<seed>). `from` is "bank/<file>" (a bank file, or "bank/<prefix>"
     for every file named <prefix>-<n>, or "bank/*"), or "drills/<pack>" (drills whose `pack` is <pack>, or whose id it is, or
     "drills/*"), each drill becoming a `code` item with its hidden tests. `tags` keeps an item holding any of them (an item's
     first tag is its family); `difficulty` is a number or [low, high]. Never-seen items come before any seen one, whatever the
     family; "seen" is a drill the learner verified in the library or an item drawn in an earlier attempt of this exam (546), and a
     later sitting ranks higher, so the least recently seen comes next. Inside each tier the pick is balanced across families (round
     robin, the families in seeded order). Items `requires` and sample files are ignored unless the exam is itself a sample. An item is never drawn twice
     in one attempt. The uids drawn are stored on the attempt (`drawn`) by exam.js, which is what "seen" reads. */
  const hash32 = (str) => { let h = 2166136261; for (const c of String(str)) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; };
  const rngOf = (seed) => { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
  const shuffled = (list, rng) => list.map(x => ({ x, k: rng() })).sort((a, b) => a.k - b.k).map(o => o.x);
  const asList = (v) => (Array.isArray(v) ? v : v == null || v === '' ? [] : [v]);
  const CODE_FIELDS = ['language', 'starter', 'examples', 'tests', 'how', 'solution', 'budget', 'caseBudget', 'signature', 'testkit', 'leakCheck', 'allocCheck', 'files', 'flags', 'data', 'postlude', 'setup'];
  /* A drill file as an exam item: its brief is the prose, its code fields the code widget. A Python drill's `prelude` runs after
     the learner's code (the helpers its tests call), which the widget calls `postlude`; a C++ drill's fields pass as they are. */
  const drillItem = (d) => {
    const w = { kind: 'code' };
    CODE_FIELDS.forEach(k => { if (d[k] !== undefined) w[k] = d[k]; });
    if (d.prelude !== undefined) { if ((d.language || 'python') === 'python') w.postlude = [d.prelude, d.postlude].filter(Boolean).join('\n'); else w.prelude = d.prelude; }
    /* tags first (the family is the first tag), then the pattern, so a draw can filter by pattern; mirrored by drillTags in tools/validate.mjs */
    const tags = asList(d.tags), pat = asList(d.pattern || d.patterns).slice(0, 1), all = [...tags, ...pat.filter(x => !tags.includes(x))];
    return { id: `drill-${d.id}`, difficulty: d.difficulty || 3, skills: d.skills || [], tags: all.length ? all : asList(d.pack || d.id).slice(0, 1),
      ...(d.pace ? { pace: d.pace } : {}), prose: d.brief, question: d.name, widget: w,
      feedback: { correct: 'Every hidden test passes.', generic: 'A hidden test failed. Run the examples, then check the edge cases.' },
      explain: { text: Array.isArray(d.notes) && d.notes.length ? d.notes.join(' ') : 'The model solution is on the drill page.' } };
  };
  const matchFile = (name, id) => name === '*' || id === name || id.startsWith(name + '-');
  const candidates = async (from, { sample }) => {
    const C = Z.content, [kind, name] = String(from).split('/'), out = [];
    const listed = (prefix) => (C.fileList ? C.fileList(prefix, { sample }) : []);
    if (kind === 'bank') {
      for (const id of listed('bank/').map(f => f.slice(5, -5)).filter(id => matchFile(name, id))) {
        let D = null; try { D = await C.bank(id); } catch { D = null; }
        ((D && D.items) || []).forEach(it => {
          if (!it || !it.id) return;
          const x = Object.assign({}, it); delete x.hints;
          out.push({ uid: `bank/${id}/${it.id}`, item: Object.assign(x, { drawn: { from: `bank/${id}`, uid: `bank/${id}/${it.id}` }, ref: { bank: id, item: it.id } }) });
        });
      }
    } else if (kind === 'drills') {
      for (const id of listed('drills/').map(f => f.slice(7, -5)).filter(id => id !== 'index')) {
        let d = null; try { d = await C.drill(id); } catch { d = null; }
        if (!d || !(name === '*' || d.pack === name || d.id === name || String(d.id).startsWith(name + '-'))) continue;
        const it = drillItem(d);
        out.push({ uid: `drills/${id}`, item: Object.assign(it, { drawn: { from: `drills/${name}`, uid: `drills/${id}` } }) });
      }
    }
    return out;
  };
  const familyOf = (it) => (Array.isArray(it.tags) && typeof it.tags[0] === 'string' ? it.tags[0] : (it.skills && it.skills[0]) || 'item');
  /* entries: the paper's draw list. opts: { seed, salt (the paper's index), exam (id), sample, seen (uid -> how recent), used (a Set shared across papers) } */
  const draw = async (entries, { seed = 0, salt = 0, exam = '', sample = false, seen = {}, used = new Set() } = {}) => {
    const out = [];
    for (let e = 0; e < (entries || []).length; e++) {
      const spec = entries[e], rng = rngOf(hash32(`${exam}|${seed}|${salt}|${e}`));
      const want = asList(spec.tags), band = Array.isArray(spec.difficulty) ? spec.difficulty : spec.difficulty != null ? [spec.difficulty, spec.difficulty] : null;
      const pool = (await candidates(spec.from, { sample })).filter(c => !used.has(c.uid)
        && (!want.length || (Array.isArray(c.item.tags) && c.item.tags.some(t => want.includes(t))))
        && (!band || (c.item.difficulty >= band[0] && c.item.difficulty <= band[1])));
      /* never seen first, then the least recently seen (546): one tier per "seen" rank, lowest first, and the families
         balanced by round robin inside a tier, so a seen problem is drawn only once no unseen one is left in the pool */
      const n = Math.max(1, Math.round(+spec.n || 1)), got = [], order = shuffled(pool, rng);
      for (const rank of [...new Set(order.map(c => seen[c.uid] || 0))].sort((a, b) => a - b)) {
        if (got.length >= n) break;
        const byFam = new Map();
        order.filter(c => (seen[c.uid] || 0) === rank).forEach(c => { const f = familyOf(c.item), q = byFam.get(f) || []; q.push(c); byFam.set(f, q); });
        const queues = shuffled([...byFam.values()], rng);
        while (got.length < n && queues.some(q => q.length)) queues.forEach(q => { if (got.length < n && q.length) got.push(q.shift()); });
      }
      if (got.length < n) console.warn(`draw ${spec.from}: ${got.length} of ${n} items available`);
      got.forEach(c => { used.add(c.uid); out.push(c.item); });
    }
    return out;
  };
  /* uid -> why and when an item counts as seen (ENGINE-BACKLOG 546): { why: 'sat', at, rank } for a uid drawn in an earlier attempt of
     this exam (rank is the attempt number, later is higher), or { why: 'solved', at, rank: 0.5 } for a drill the learner has verified in
     the drill library (state.drills[id].verified; the uid is "drills/<id>"). A sitting wins over a solve. */
  const seenInfo = (examId) => {
    const m = {};
    try {
      const S = Z.state;
      /* a draw seen in any other exam or mock counts as seen too (ENGINE-BACKLOG 594): rank 0.75, below a sitting of this exam */
      Object.keys(S.exams || {}).forEach(id => { if (id !== examId) (((S.exams || {})[id] || {}).attempts || []).forEach(a => (a.drawn || []).forEach(u => { if (!m[u] || m[u].why !== 'other' || (a.at || '') > (m[u].at || '')) m[u] = { why: 'other', at: a.at || null, rank: 0.75, exam: id }; })); });
      (((S.exams || {})[examId] || {}).attempts || []).forEach((a, i) => (a.drawn || []).forEach(u => { m[u] = { why: 'sat', at: a.at || null, rank: i + 1 }; }));
      const dr = (S.drills && S.drills.get && S.drills.get()) || {};
      Object.keys(dr).forEach(id => { const u = `drills/${id}`; if (dr[id] && dr[id].verified && !m[u]) m[u] = { why: 'solved', at: dr[id].at || null, rank: 0.5 }; });
    } catch { /* no state */ }
    return m;
  };
  /* uid -> how recent (a number), for draw: never seen is absent (0), a solve ranks 0.5, a sitting its attempt number, so the least recently seen is drawn first */
  const seenOf = (examId) => { const m = {}, info = seenInfo(examId); Object.keys(info).forEach(u => { m[u] = info[u].rank; }); return m; };
  /* The label for a seen item: "Previously seen: solved in the drill library" or "Previously seen: sat on 3 Nov 2026" */
  const seenLabel = (s) => {
    if (!s) return '';
    if (s.why === 'solved') return 'Previously seen: solved in the drill library';
    if (s.why === 'other') return 'Previously seen: sat in another exam';
    const d = s.at ? new Date(s.at) : null;
    return d && !isNaN(d) ? `Previously seen: sat on ${d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}` : 'Previously seen: sat in an earlier attempt';
  };

  Z.mock = { draw, seenOf, seenInfo, seenLabel, fmtSeconds, family, pacing, is: (id) => /^mock-/.test(String(id || '')), style: (s) => STYLES[s] || { label: s ? String(s) : 'Mock', track: 'speed' }, STYLES, scoring, scored, tally, need, passed, requiredMissed, roleOf, paperFor, signed, trend };
})();
