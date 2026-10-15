/* table canvas: a static or highlightable data table, rendered as an HTML table inside the canvas wrapper (not SVG).
   Ids, one-based over the body rows: r{i} a row, c{j} a column (its header and every cell), r{i}c{j} a cell.
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
    const tbl = document.createElement('table'); tbl.className = 'cv-tbl';
    if (P.label) tbl.setAttribute('aria-label', P.label);
    const cap = document.createElement('div'); cap.className = 't-caption cv-caption'; cap.hidden = true;
    const html = (v) => (v == null ? '' : typeof v === 'number' ? Z.esc(C.fmtNum(v, 4)) : Z.md(Z.esc(String(v)).replace(/&#39;/g, "'")));
    if (columns.length) {
      const thead = document.createElement('thead'), tr = document.createElement('tr');
      columns.forEach((c, k) => { const th = document.createElement('th'); th.scope = 'col'; th.className = 'cv-obj'; th.dataset.id = `c${k + 1}`; th.dataset.col = `c${k + 1}`; th.style.textAlign = alignOf(k + 1); th.innerHTML = html(c); tr.append(th); });
      thead.append(tr); tbl.append(thead);
    }
    const tbody = document.createElement('tbody'), inputs = [];
    rows.forEach((row, i) => {
      const tr = document.createElement('tr'); tr.className = 'cv-obj'; tr.dataset.id = `r${i + 1}`;
      row.forEach((v, j) => {
        const id = `r${i + 1}c${j + 1}`, td = document.createElement(j === 0 && P.rowHeads ? 'th' : 'td');
        if (td.tagName === 'TH') td.scope = 'row';
        td.className = 'cv-obj cv-td'; td.dataset.id = id; td.dataset.col = `c${j + 1}`; td.dataset.row = `r${i + 1}`; td.style.textAlign = alignOf(j + 1);
        const edit = editable.has(id) || (v && typeof v === 'object' && v.edit);
        if (edit) {
          const inp = document.createElement('input'); inp.className = 'cv-in'; inp.type = 'text'; inp.dataset.id = id; inp.autocomplete = 'off'; inp.spellcheck = false;
          inp.setAttribute('inputmode', 'decimal'); inp.setAttribute('aria-label', `${columns[j] ? String(columns[j]).replace(/\$/g, '') : 'Column ' + (j + 1)}, row ${i + 1}`);
          if (v && typeof v === 'object' && v.placeholder) inp.placeholder = v.placeholder;
          if (ctx.static) inp.disabled = true;
          td.classList.add('is-edit'); td.append(inp); inputs.push(inp);
        } else {
          td.dataset.tap = ''; td.dataset.label = `Row ${i + 1}, ${columns[j] ? String(columns[j]).replace(/\$/g, '') : 'column ' + (j + 1)}: ${v && typeof v === 'object' ? v.text ?? '' : v ?? ''}`;
          td.innerHTML = html(v && typeof v === 'object' ? v.text : v);
        }
        tr.append(td);
      });
      tbody.append(tr);
    });
    tbl.append(tbody); scroller.append(tbl); wrap.append(scroller, cap); host.append(wrap);
    const fr = { wrap, caption: (t) => { cap.hidden = !t; cap.innerHTML = t ? Z.md(t) : ''; } };

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
      for (const [id, v] of Object.entries(st.values || {})) {
        const inp = inputs.find(x => x.dataset.id === id);
        if (inp) { if (inp.value !== String(v)) inp.value = v; }
        else resolve(id).forEach(n => { if (n.tagName !== 'TR') n.innerHTML = html(v); });
      }
    };
    const I = C.instance({ kind: 'table', factory: table, params, ctx, fr, draw, resolve, highlightIds: toIds });
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
