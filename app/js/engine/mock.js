/* Mock assessments: marking and trend helpers shared by the exam screen, Review and You (ENGINE-BACKLOG 450 to 453).
   A mock is content/exams/mock-<id>.json; its papers may carry scoring { right, wrong, blank } and passNet.
     ZQ.mock.is(id)                  true for a mock exam id
     ZQ.mock.style(name)             { label, track } for trader, research, developer or strats
     ZQ.mock.scoring(paper)          { right, wrong, blank } with the defaults 1, 0, 0
     ZQ.mock.scored(paper)           true when marking is not plain right-or-nothing
     ZQ.mock.tally(paper, results)   { n, right, wrong, blank, net, max } from per-item { ok, done }
     ZQ.mock.passed(paper, tally)    net against passNet, else the net share against pass (default 0.7)
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
    for (let i = 0; i < n; i++) { const r = (results || [])[i]; if (r && r.ok) right++; else if (r && r.done) wrong++; else blank++; }
    return { n, right, wrong, blank, net: round(right * s.right + wrong * s.wrong + blank * s.blank), max: round(n * s.right) };
  };
  const need = (p, max) => (typeof p.passNet === 'number' ? p.passNet : round((typeof p.pass === 'number' ? p.pass : 0.7) * max));
  const passed = (p, t) => (t.n > 0 && t.net >= need(p, t.max) - 1e-9);
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

  Z.mock = { fmtSeconds, family, pacing, is: (id) => /^mock-/.test(String(id || '')), style: (s) => STYLES[s] || { label: s ? String(s) : 'Mock', track: 'speed' }, STYLES, scoring, scored, tally, need, passed, signed, trend };
})();
