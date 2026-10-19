/* console canvas (item 159): a monospace block for terminal sessions, pytest output and tracebacks. Lines keep their
   indentation and scroll sideways when long; each line is an object with id l{i}, one-based (l1 is the first line),
   so it can be highlighted, shaded, tapped (tap mode, for "tap the line that failed") and marked. Lines starting with
   "$ " or ">>> " show the prompt muted. HTML inside the canvas wrapper, like the table. Params and state:
   engine/canvas/README.md. */
(function () {
  'use strict';
  const Z = window.ZQ, C = Z.canvas;
  const PROMPT = /^(\$ |>>> |\.\.\. )/;

  function consoleKind(host, params, ctx = {}) {
    const P = params || {};
    const wrap = document.createElement('div'); wrap.className = 'cv';
    const box = document.createElement('div'); box.className = 'cv-con' + (P.numbers ? ' has-numbers' : '');
    if (P.label) { box.setAttribute('role', 'group'); box.setAttribute('aria-label', P.label); }
    const title = P.title ? Object.assign(document.createElement('div'), { className: 'cv-con-title t-caption', textContent: String(P.title) }) : null;
    const cap = document.createElement('div'); cap.className = 't-caption cv-caption'; cap.hidden = true;
    wrap.append(...(title ? [title] : []), box, cap); host.append(wrap);
    const fr = { wrap, caption: (t) => { cap.hidden = !t; cap.innerHTML = t ? (Z.grade && Z.grade.inline ? Z.grade.inline(String(t)) : Z.md(t)) : ''; } };
    const base = Array.isArray(P.lines) ? P.lines.map(String) : String(P.text ?? '').replace(/\n$/, '').split('\n');

    let shownKey = null;
    const build = (lines) => {
      const key = JSON.stringify(lines); if (key === shownKey) return; shownKey = key;
      box.replaceChildren(...lines.map((t, k) => {
        const ln = document.createElement('div'); ln.className = 'cv-obj cv-con-line'; ln.dataset.id = `l${k + 1}`; ln.dataset.tap = '';
        ln.dataset.label = `Line ${k + 1}: ${t}`;
        if (P.numbers) { const n = document.createElement('span'); n.className = 'cv-con-n'; n.setAttribute('aria-hidden', 'true'); n.textContent = String(k + 1); ln.append(n); }
        const m = t.match(PROMPT);
        if (m) { const p = document.createElement('span'); p.className = 'cv-con-prompt'; p.textContent = m[1]; ln.append(p); ln.classList.add('is-cmd'); }
        ln.append(document.createTextNode((m ? t.slice(m[1].length) : t) || '​'));
        return ln;
      }));
    };
    const draw = (st) => {
      build(Array.isArray(st.lines) ? st.lines.map(String) : base);
      const sets = Array.isArray(st.shade) ? [st.shade] : Object.values(st.shade || {});
      const slot = new Map(); sets.forEach((ids, k) => (ids || []).forEach(id => { if (!slot.has(String(id))) slot.set(String(id), k + 1); }));
      const tone = st.tone || {};
      box.querySelectorAll('.cv-con-line').forEach(n => {
        for (let k = 1; k <= 6; k++) n.classList.toggle('cv-sh' + k, slot.get(n.dataset.id) === k);
        n.classList.toggle('is-shaded', slot.has(n.dataset.id));
        ['err', 'ok', 'muted'].forEach(t => n.classList.toggle('tone-' + t, tone[n.dataset.id] === t));
      });
    };
    const I = C.instance({ kind: 'console', factory: consoleKind, params, ctx, fr, draw });
    I.api.lines = () => [...box.querySelectorAll('.cv-con-line')].map(n => n.dataset.id);
    I.api.set({}, { instant: true });
    return I.api;
  }

  C.register('console', consoleKind);
})();
