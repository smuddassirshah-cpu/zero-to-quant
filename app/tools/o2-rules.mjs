/* PLAN 2c item O2 (ENGINE-BACKLOG 523 to 527): finding classes that recur in docs/reviews/, as validator warnings.
   scanO2(json, emit) walks one parsed content file and calls emit(code, where, msg). Warnings only: they never fail the build. */
export const O2_CODES = ['O2-long-sentence', 'O2-long-explain', 'O2-unshuffled-numeric', 'O2-no-slip', 'O2-prose-prompt', 'O2-explain-answer'];

const isObj = (x) => x && typeof x === 'object' && !Array.isArray(x);
const strip = (s) => String(s).replace(/```[\s\S]*?```/g, ' ').replace(/`[^`]*`/g, ' ').replace(/\$\$[\s\S]*?\$\$/g, ' ').replace(/\$[^$]*\$/g, ' ');
const wordCount = (s) => s.split(/\s+/).filter(w => /[A-Za-z0-9]/.test(w)).length;
const sentencesOf = (s) => strip(s).split(/\n+|(?<=[.?!:;])\s+/).map(x => x.trim()).filter(x => /[A-Za-z]/.test(x));

/* Numbers in text: plain, thousands commas, per cent, fractions a/b and \frac{a}{b}, inside or outside maths. */
export const numbersIn = (text) => {
  const t = String(text).replace(/\\[td]frac/g, '\\frac').replace(/\\frac(\d)(\d)\b/g, '\\frac{$1}{$2}').replace(/\\frac(\d)\{/g, '\\frac{$1}{').replace(/\\sqrt\{\\pi\}/g, '1.7725').replace(/\\pi\b/g, '3.14159').replace(/\\sqrt\s*\{?(\d+)\}?/g, (_, d) => String(Math.sqrt(+d))).replace(/\\text\{([^}]*)\}/g, '$1').replace(/\\(?:pounds|%|,|;|!|left|right|approx|times|cdot)/g, ' ').replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, '$1/$2').replace(/\{,\}/g, '').replace(/[£$€]/g, ' ').replace(/(\d),(?=\d{3}\b)/g, '$1').replace(/−/g, '-');
  const out = [];
  for (const m of t.matchAll(/(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*(?:\/\s*(\d+(?:\.\d+)?))?\s*(%|k\b|m\b|bn\b|million|billion|thousand)?/g)) {
    let v = parseFloat(m[1]);
    if (m[2] != null) v = v / parseFloat(m[2]);
    const u = m[3];
    out.push(v);
    if (u === '%') out.push(v / 100);
    else if (u === 'k' || u === 'thousand') out.push(v * 1e3);
    else if (u === 'm' || u === 'million') out.push(v * 1e6);
    else if (u === 'bn' || u === 'billion') out.push(v * 1e9);
  }
  return out;
};
const close = (a, b, abs = 0) => Math.abs(a - b) <= Math.max(abs, 0.006 * Math.abs(b), 1e-9);
const numOf = (text) => { const t = String(text).replace(/\\text\{[^}]*\}/g, '').replace(/\\(?:pounds|%|,|;|!)/g, '').replace(/[£$€\s]/g, '').replace(/(\d),(?=\d{3}\b)/g, '$1').replace(/\{,\}/g, '').replace(/−/g, '-'); const m = t.match(/^(-?\d+(?:\.\d+)?)(%?)$/); return m ? (m[2] ? parseFloat(m[1]) / 100 : parseFloat(m[1])) : null; };
const fracOf = (text) => { const m = String(text).replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, '$1/$2').replace(/[$\s]/g, '').match(/^(-?\d+(?:\.\d+)?)\/(\d+(?:\.\d+)?)$/); return m ? parseFloat(m[1]) / parseFloat(m[2]) : null; };
const optNum = (o) => { const t = o && (o.text ?? o.label); if (typeof t !== 'string') return null; const n = numOf(t); return n != null ? n : fracOf(t); };
const RANGE = /^\s*(?:\[\s*-?\d[\d.]*\s*,\s*-?\d[\d.]*\s*[\])]|-?\d[\d.]*\s*%?\s*(?:to|–|—|-)\s*-?\d[\d.]*\s*%?)\s*\.?\s*$/;
const rangeOf = (o) => {
  const t = o && o.text; if (typeof t !== 'string') return null;
  const s = t.replace(/\\text\{([^}]*)\}/g, '$1').replace(/\\(?:pounds|,|;|!)/g, '').replace(/\{,\}/g, '').replace(/[£$€]/g, '').replace(/(\d),(?=\d{3}\b)/g, '$1').replace(/^\s*(?:between|from)\s+/i, '').replace(/^(\S+)\s+and\s+/i, (m, a, off, str) => (/^\s*(?:between|from)\s+/i.test(t) ? a + ' to ' : m)).trim();
  if (!RANGE.test(s)) return null;
  const n = s.match(/-?\d[\d.]*/g); return n && n.length === 2 ? n.map(parseFloat) : null;
};

/* A distractor is reachable when it is the key put through a common slip: scale by 10, 100, 2, 3; reciprocal; sign; one minus; off by one; squared; root; half; per cent for fraction. */
const slips = (k) => {
  const r = [k * 10, k / 10, k * 100, k / 100, k * 2, k / 2, k * 3, k / 3, k * 4, k / 4, -k, 1 - k, 100 - k, k + 1, k - 1, k + 2, k - 2, k * k, Math.sqrt(Math.abs(k)), k + 10, k - 10, k * 1.5, k * 0.9, k * 1.1, k * 12, k / 12, k * 365, k / 365, k * 252, k / 252, k * 52, k / 52];
  if (k !== 0) r.push(1 / k, k * 60, k / 60, k * 7, k / 7);
  return r;
};
const nums = (o) => { const out = []; (function w(x) { if (typeof x === 'string') out.push(...numbersIn(x)); else if (typeof x === 'number') out.push(x); else if (Array.isArray(x)) x.forEach(w); else if (isObj(x)) Object.values(x).forEach(w); })(o); return out; };
const CALC = /=|×|\\times|\\cdot|divid|multipl|forgot|instead|rather than|used|add|subtract|squar|root|half|twice|doubl|rounded|counted/i;

export const scanO2 = (json, emit) => {
  const visit = (n, where) => {
    if (Array.isArray(n)) { n.forEach((x, i) => visit(x, `${where}[${i}]`)); return; }
    if (!isObj(n)) return;
    if (isObj(n.widget) || isObj(n.explain)) node(n, isObj(n.widget) ? n.widget : null, where);
    for (const [k, v] of Object.entries(n)) if (v && typeof v === 'object') visit(v, where ? `${where}.${k}` : k);
  };
  const longs = (text, where) => { if (typeof text !== 'string') return; const n = sentencesOf(text).filter(s => wordCount(s) >= 20).length; if (n) emit('O2-long-sentence', where, `${n} sentence${n === 1 ? '' : 's'} of 20 words or more (the voice rule is under 20)`); };
  const node = (n, w, where) => {
    /* 1: long sentences over the learner-facing strings of this node */
    ['prose', 'question'].forEach(f => longs(n[f], `${where}.${f}`));
    if (isObj(n.feedback)) { ['correct', 'generic'].forEach(f => longs(n.feedback[f], `${where}.feedback.${f}`)); Object.entries(n.feedback.byKey || {}).forEach(([k, v]) => longs(v, `${where}.feedback.byKey.${k}`)); }
    (Array.isArray(n.hints) ? n.hints : []).forEach((h, i) => longs(h && h.text, `${where}.hints[${i}]`));
    if (w && Array.isArray(w.options)) w.options.forEach((o, i) => longs(o && o.why, `${where}.widget.options[${i}].why`));
    const ex = isObj(n.explain) ? n.explain : null;
    if (ex && typeof ex.text === 'string') {
      longs(ex.text, `${where}.explain.text`);
      const c = strip(ex.text).split(/(?<=[.?!])\s+|\n+/).filter(x => /[A-Za-z]/.test(x)).length;
      if (c > 3) emit('O2-long-explain', `${where}.explain.text`, `explanation has ${c} sentences (at most three)`);
    }
    if (!w) return;
    const opts = Array.isArray(w.options) ? w.options : [];
    /* 2: unshuffled interval or ordered numeric choices */
    if ((w.kind === 'choice' || w.kind === 'multi') && opts.length >= 3 && w.shuffle !== true) {
      const vs = opts.map(optNum);
      let why = null;
      const rs = opts.map(rangeOf);
      if (rs.every(Boolean) && (rs.every((r, i) => i === 0 || r[0] > rs[i - 1][0]) || rs.every((r, i) => i === 0 || r[0] < rs[i - 1][0]))) why = 'interval options in order';
      else if (vs.every(v => v != null)) { const up = vs.every((v, i) => i === 0 || v > vs[i - 1]), dn = vs.every((v, i) => i === 0 || v < vs[i - 1]); if (up || dn) why = 'numeric options in order'; }
      if (why) emit('O2-unshuffled-numeric', `${where}.widget`, `${why} without shuffle: true: the key sits at a fixed place`);
    }
    /* 3: numeric distractors that match no slip */
    const given = [...nums(n.prose), ...nums(n.question), ...nums(n.canvas)];
    if (w.kind === 'choice' && opts.length >= 3) {
      const key = opts.find(o => o && o.correct), kv = key ? optNum(key) : null;
      if (kv != null && opts.every(o => o && optNum(o) != null)) {
        const sl = slips(kv);
        opts.forEach((o, i) => {
          if (o.correct) return;
          const v = optNum(o);
          if (sl.some(s => close(s, v)) || given.some(g => close(g, v))) return;
          if (!o.why || !String(o.why).trim()) emit('O2-no-slip', `${where}.widget.options[${i}]`, `distractor ${o.text} has no slip note and is not reachable from the key ${key.text}`);
          else if (wordCount(String(o.why)) < 9 && !CALC.test(o.why) && !nums(o.why).length) emit('O2-no-slip', `${where}.widget.options[${i}]`, `distractor ${o.text} is no common slip from the key ${key.text}, and its why names no calculation`);
        });
      }
    }
    if (w.kind === 'numeric' && typeof w.answer === 'number' && Array.isArray(w.wrong)) {
      const sl = slips(w.answer), bk = (n.feedback && n.feedback.byKey) || {};
      w.wrong.forEach((x, i) => {
        if (!isObj(x) || typeof x.value !== 'number') return;
        if (sl.some(s => close(s, x.value)) || given.some(g => close(g, x.value)) || (x.id && bk[x.id])) return;
        emit('O2-no-slip', `${where}.widget.wrong[${i}]`, `wrong value ${x.value} is no common slip from the answer ${w.answer} and feedback.byKey has no "${x.id || ''}" note`);
      });
    }
    /* 4: prose and prompt both present where the schema intends one */
    if (typeof n.prose === 'string' && n.prose.trim()) {
      const p = typeof n.prompt === 'string' ? n.prompt : (typeof w.prompt === 'string' ? w.prompt : null);
      const q = typeof n.question === 'string' ? strip(n.question).replace(/\s+/g, ' ').trim() : '';
      if (p && p.trim() && w.kind !== 'longform' && n.kind !== 'longform') emit('O2-prose-prompt', where, 'this has both prose and a prompt: the schema takes the question from "question", so one of the two is redundant');
      else if (q.length > 20 && strip(n.prose).replace(/\s+/g, ' ').includes(q)) emit('O2-prose-prompt', where, 'the question repeats a sentence of the prose word for word');
    }
    /* 5: explain never states the answer */
    if (ex && typeof ex.text === 'string') {
      let target = null, abs = 0, shown = '';
      if (w.kind === 'numeric' && typeof w.answer === 'number' && Number.isFinite(w.answer)) { target = [w.answer]; shown = String(w.answer); abs = (isObj(w.tol) && typeof w.tol.abs === 'number') ? w.tol.abs : 0; if (w.unit === '%' && Math.abs(w.answer) <= 1) target.push(w.answer * 100); }
      else if (w.kind === 'choice') { const key = opts.find(o => o && o.correct); const v = key ? optNum(key) : null; if (v != null) { target = [v, v * 100, v / 100]; shown = key.text; } }
      if (target && !target.every(t => t === 0)) {
        const got = numbersIn(ex.text);
        if (!target.some(t => got.some(g => close(Math.abs(g), Math.abs(t), abs)))) emit('O2-explain-answer', `${where}.explain.text`, `the explanation never states the answer (${shown})`);
      }
    }
  };
  visit(json, '');
};
