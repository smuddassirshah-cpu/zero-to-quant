/* table canvas: a static or highlightable data table, rendered as an HTML table inside the canvas wrapper (not SVG).
   Ids are zero-based over the body rows and the columns, as E2's table widget and the matrix canvas use:
   r{i} a row, c{j} a column (its header and every cell), r{i}c{j} a cell; r0c0 is the first body cell.
   Cells listed in params.editable, or written as { "edit": true, ... }, hold an <input>; cells() returns those inputs
   (each with data-id) for the table widget to drive. Params and state: engine/canvas/README.md. */
(function () {
  'use strict';
  const Z = window.ZQ, C = Z.canvas;

  function table(host, params, ctx = {}) {
    const P = params || {};
    const columns = P.columns || [], rows = P.rows || [];
    const editable = new Set(P.editable || []);
    const alignOf = (j) => (Array.isArray(P.align) ? P.align[j - 1] : P.align) || (j === 1 ? 'left' : 'right');
    const wrap = document.createElement('div'); wrap.className = 'cv';
    const scroller = document.createElement('div'); scroller.className = 'cv-tbl-wrap';
    /* compact (or more than 6 columns): tighter cells so a wide table fits the 540px column; it still scrolls sideways if not */
    const tbl = document.createElement('table'); tbl.className = 'cv-tbl' + (P.compact || (columns.length || (rows[0] || []).length) > 6 ? ' is-compact' : '');
    if (P.label) tbl.setAttribute('aria-label', P.label);
    const cap = document.createElement('div'); cap.className = 't-caption cv-caption'; cap.hidden = true;
    /* numbers, and text that starts as a negative number ("-3", "-0.5 kg"), use the minus sign U+2212 */
    const minus = (t) => t.replace(/^-(?=\d|\.\d)/, '−');
    /* text cells and the caption read like prose (items 145, 158): maths, inline code, bold; spaces are kept (CSS pre-wrap) */
    const inl = (t) => (Z.grade && Z.grade.inline ? Z.grade.inline(t) : Z.md(Z.esc(t).replace(/&#39;/g, "'")));
    const html = (v) => (v == null ? '' : typeof v === 'number' ? Z.esc(minus(C.fmtNum(v, 4))) : inl(minus(String(v))));
    const rowTap = P.tap === 'rows'; // item 153: tapping any cell selects the row id r{i}
    if (columns.length) {
      const thead = document.createElement('thead'), tr = document.createElement('tr');
      columns.forEach((c, k) => { const th = document.createElement('th'); th.scope = 'col'; th.className = 'cv-obj'; th.dataset.id = `c${k}`; th.dataset.col = `c${k}`; th.style.textAlign = alignOf(k + 1); th.innerHTML = html(c); tr.append(th); });
      thead.append(tr); tbl.append(thead);
    }
    const tbody = document.createElement('tbody'), inputs = [];
    rows.forEach((row, i) => {
      const tr = document.createElement('tr'); tr.className = 'cv-obj'; tr.dataset.id = `r${i}`;
      if (rowTap) { tr.dataset.tap = ''; tr.dataset.label = `Row ${i + 1}: ${row.map(v => (v && typeof v === 'object' ? v.text ?? '' : v ?? '')).join(', ')}`; }
      row.forEach((v, j) => {
        const id = `r${i}c${j}`, td = document.createElement(j === 0 && P.rowHeads ? 'th' : 'td');
        if (td.tagName === 'TH') td.scope = 'row';
        td.className = 'cv-obj cv-td'; td.dataset.id = id; td.dataset.col = `c${j}`; td.dataset.row = `r${i}`; td.style.textAlign = alignOf(j + 1);
        const edit = editable.has(id) || (v && typeof v === 'object' && v.edit);
        if (edit) {
          const inp = document.createElement('input'); inp.className = 'cv-in'; inp.type = 'text'; inp.dataset.id = id; inp.autocomplete = 'off'; inp.spellcheck = false;
          inp.setAttribute('inputmode', 'decimal'); inp.setAttribute('aria-label', `${columns[j] ? String(columns[j]).replace(/\$/g, '') : 'Column ' + (j + 1)}, row ${i + 1}`);
          if (v && typeof v === 'object' && v.placeholder) inp.placeholder = v.placeholder;
          if (ctx.static) inp.disabled = true;
          td.classList.add('is-edit'); td.append(inp); inputs.push(inp);
        } else {
          if (!rowTap) td.dataset.tap = '';
          td.dataset.label = `Row ${i + 1}, ${columns[j] ? String(columns[j]).replace(/\$/g, '') : 'column ' + (j + 1)}: ${v && typeof v === 'object' ? v.text ?? '' : v ?? ''}`;
          td.innerHTML = html(v && typeof v === 'object' ? v.text : v);
        }
        tr.append(td);
      });
      tbody.append(tr);
    });
    tbl.append(tbody); scroller.append(tbl);
    /* ENGINE-BACKLOG 607: a table wider than its column scrolls sideways; a fade on the right edge says there is more */
    const hold = document.createElement('div'); hold.className = 'cv-tbl-hold'; hold.append(scroller);
    const moreCue = () => requestAnimationFrame(() => hold.classList.toggle('has-more', scroller.scrollWidth > scroller.clientWidth + 2 && scroller.scrollLeft + scroller.clientWidth < scroller.scrollWidth - 2));
    scroller.addEventListener('scroll', moreCue, { passive: true });
    wrap.append(hold, cap); host.append(wrap);
    if (typeof ResizeObserver === 'function') new ResizeObserver(moreCue).observe(scroller);
    moreCue();
    const fr = { wrap, caption: (t) => { cap.hidden = !t; cap.innerHTML = t ? inl(String(t)) : ''; } };

    const q = (sel) => Array.from(tbl.querySelectorAll(sel));
    const resolve = (id) => {
      const s = String(id);
      if (/^r\d+$/.test(s)) return q(`[data-row="${s}"]`);
      if (/^c\d+$/.test(s)) return q(`[data-col="${s}"]`);
      return q(`[data-id="${CSS.escape(s)}"]`);
    };
    const toIds = (h) => [...(h.rows || []).map(r => (typeof r === 'number' ? `r${r}` : r)), ...(h.cols || []).map(c => (typeof c === 'number' ? `c${c}` : c)), ...(h.cells || []).map(c => (Array.isArray(c) ? `r${c[0]}c${c[1]}` : c))];
    const draw = (st) => {
      const sets = Array.isArray(st.shade) ? [st.shade] : Object.values(st.shade || {});
      q('.is-shaded').forEach(n => n.classList.remove('is-shaded', 'cv-sh1', 'cv-sh2', 'cv-sh3', 'cv-sh4', 'cv-sh5', 'cv-sh6'));
      sets.forEach((ids, k) => (ids || []).flatMap(resolve).forEach(n => { if (!n.classList.contains('is-shaded')) n.classList.add('is-shaded', 'cv-sh' + (k + 1)); }));
      /* item 180: dim: [ids] greys rows, columns or cells (a dropped row in a join) without blanking them */
      q('.is-out').forEach(n => n.classList.remove('is-out'));
      [].concat(st.dim || []).flatMap(resolve).forEach(n => n.classList.add('is-out'));
      for (const [id, v] of Object.entries(st.values || {})) {
        const inp = inputs.find(x => x.dataset.id === id);
        if (inp) { if (inp.value !== String(v)) inp.value = v; }
        else resolve(id).forEach(n => { if (n.tagName !== 'TR') n.innerHTML = html(v); });
      }
    };
    /* Highlight: one ring around the union of the highlighted cells (edges only where a neighbour is not highlighted) */
    const pos = (n) => { const tr = n.parentElement; return [tr.parentElement.tagName === 'THEAD' ? 0 : [...tbody.children].indexOf(tr) + 1, [...tr.children].indexOf(n)]; };
    const hlSet = new Set();
    const paintRing = () => {
      const keys = new Set([...hlSet].map(n => pos(n).join(',')));
      q('th, td').forEach(n => { if (!hlSet.has(n)) { n.classList.remove('cv-hl', 'cv-hl-on'); ['--hl-t', '--hl-b', '--hl-l', '--hl-r'].forEach(v => n.style.removeProperty(v)); } });
      for (const n of hlSet) {
        const [r, c] = pos(n); n.classList.add('cv-hl');
        n.style.setProperty('--hl-t', keys.has(`${r - 1},${c}`) ? 0 : 1); n.style.setProperty('--hl-b', keys.has(`${r + 1},${c}`) ? 0 : 1);
        n.style.setProperty('--hl-l', keys.has(`${r},${c - 1}`) ? 0 : 1); n.style.setProperty('--hl-r', keys.has(`${r},${c + 1}`) ? 0 : 1);
      }
    };
    const onHighlight = (ids, on, { instant }) => {
      const els = (ids || []).flatMap(resolve).filter(n => n.tagName !== 'TR');
      if (!on) { if (!ids || !ids.length) hlSet.clear(); else els.forEach(n => hlSet.delete(n)); paintRing(); return true; }
      els.forEach(n => hlSet.add(n)); paintRing();
      if (!instant && !I.isStatic) els.forEach(n => C.pulse(n));
      return true;
    };
    const I = C.instance({ kind: 'table', factory: table, params, ctx, fr, draw, resolve, highlightIds: toIds, onHighlight });
    const api = I.api;
    api.cells = () => inputs.slice();
    api.input = (id) => inputs.find(x => x.dataset.id === id) || null;
    const baseLock = api.lock;
    api.lock = (on = true) => { inputs.forEach(x => { x.readOnly = !!on; }); return baseLock(on); };
    api.set({}, { instant: true });
    return api;
  }

  C.register('table', table);
})();
