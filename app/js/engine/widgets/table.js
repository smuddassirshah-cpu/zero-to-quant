/* Table widget (docs/AUTHORING.md 3, design-research 5.3 no. 14). Fixed cells are text (KaTeX allowed);
   editable cells { edit: true, answer, tol } take the numeric grading rules. Every editable cell must be within
   tolerance; key is the first wrong cell id r{i}c{j} (zero-based, as the table canvas). After grading each
   editable cell is marked: right cells take green, wrong ones amber, so a retry only touches what is wrong.
   Item 118: a cell whose answer is text ("True", "AAPL") is graded as text, ignoring case and outer spaces;
   accept: [..] lists other spellings.
   Pass 7: a cell's wrong: [{ id, value, tol } | { id, text }] names a specific wrong entry, and the key is that id
   (items 356, 360); an answer written O(...) is compared as big-O, ignoring the O, spaces, case and the log base, so
   "n log n" matches "O(n log n)" (item 390); deps: [canvas ids] highlights the cells a cell depends on while it has
   focus, so a DP table can be filled beside its grid (item 408). */
(function () {
  'use strict';
  const Z = window.ZQ;

  const fixedCell = (c) => (typeof c === 'number' ? Z.esc(Z.grade.fmtNum(c)).replace(/^-/, '−') : Z.grade.inline(String(c ?? '').replace(/^-(?=\d|\.\d)/, '−')));
  Z.widgets.register('table', (host, spec, ctx) => {
    const cols = spec.columns || [];
    const rows = spec.rows || [];
    const cells = [];
    const el = Z.h(`<div class="wd-tablewrap"><table class="wd-table">
      ${cols.length ? `<thead><tr>${cols.map(c => `<th scope="col">${Z.grade.inline(c)}</th>`).join('')}</tr></thead>` : ''}
      <tbody>${rows.map((row, i) => `<tr>${row.map((c, j) => {
        if (c && typeof c === 'object' && c.edit) {
          cells.push({ id: `r${i}c${j}`, spec: c, text: typeof c.answer === 'string' && (!Number.isFinite(Z.grade.parseNum(c.answer)) || c.compare === 'bigO'), bigO: c.compare === 'bigO' || (typeof c.answer === 'string' && /^\s*O\s*\(.*\)\s*$/i.test(c.answer)) });
          const label = `${cols[j] ? String(cols[j]).replace(/\$/g, '') : 'Column ' + (j + 1)}, row ${i + 1}`;
          return `<td class="wd-td-edit${c.unit === '%' ? ' has-unit' : ''}"><input type="text" inputmode="${typeof c.answer === 'string' && !Number.isFinite(Z.grade.parseNum(c.answer)) ? 'text' : 'decimal'}" autocomplete="off" spellcheck="false" data-cell="r${i}c${j}" aria-label="${Z.esc(label)}${c.unit === '%' ? ', in percent' : ''}" placeholder="${Z.esc(c.placeholder || '?')}">${c.unit === '%' ? '<span class="wd-td-unit" aria-hidden="true">%</span>' : ''}</td>`;
        }
        const t = fixedCell(c); // item 234: numbers and negative-number text use the minus sign
        return j === 0 ? `<th scope="row">${t}</th>` : `<td>${t}</td>`;
      }).join('')}</tr>`).join('')}</tbody></table>
      <p class="t-caption wd-accept" hidden></p></div>`);
    host.append(el);
    const input = (id) => el.querySelector(`[data-cell="${id}"]`);
    const acc = el.querySelector('.wd-accept');
    el.addEventListener('input', () => ctx.change && ctx.change(value()));
    el.addEventListener('keydown', (e) => {
      // Arrow keys move between editable cells when the caret is at the edge
      const t = e.target; if (!t.dataset || !t.dataset.cell) return;
      const ins = [...el.querySelectorAll('[data-cell]')], i = ins.indexOf(t);
      if ((e.key === 'ArrowDown' || (e.key === 'ArrowRight' && t.selectionStart === t.value.length)) && ins[i + 1]) { e.preventDefault(); ins[i + 1].focus(); }
      if ((e.key === 'ArrowUp' || (e.key === 'ArrowLeft' && t.selectionStart === 0)) && ins[i - 1]) { e.preventDefault(); ins[i - 1].focus(); }
    });
    const value = () => Object.fromEntries(cells.map(c => [c.id, input(c.id).value.trim()]));
    const norm = (t) => String(t ?? '').trim().replace(/\s+/g, ' ').toLowerCase();
    /* item 287: unit "%" on a cell: the answer is a fraction (0.25) and the learner types a percentage (25) */
    const pct = (c) => c.spec.unit === '%';
    const numIn = (c) => { const v = Z.grade.parseNum(String(input(c.id).value).replace('%', '')); return pct(c) ? v / 100 : v; };
    const bigO = (t) => norm(t).replace(/^o\s*\((.*)\)$/, '$1').replace(/\*\*/g, '^').replace(/²/g, '^2').replace(/³/g, '^3').replace(/\s+|\*|·|×/g, '').replace(/log_?\{?\d+\}?|lg|ln/g, 'log').replace(/[{}]/g, '');
    const textEq = (c, a, b) => (c.bigO ? bigO(a) === bigO(b) : norm(a) === norm(b));
    const check = (c) => (c.text ? [c.spec.answer, ...(Array.isArray(c.spec.accept) ? c.spec.accept : [])].some(a => textEq(c, a, input(c.id).value)) : Z.grade.within(numIn(c), +c.spec.answer, c.spec.tol)); // tol is in the answer's units (a fraction for %)
    /* the wrong[] entry a cell's input matches, if any */
    const wrongOf = (c) => (Array.isArray(c.spec.wrong) ? c.spec.wrong.find(w => w && (w.text != null ? textEq(c, w.text, input(c.id).value) : w.value != null && !c.text && Z.grade.within(numIn(c), +w.value, w.tol ?? { abs: 1e-9 }))) : null) || null;
    const shown = (c) => (c.text ? String(c.spec.answer) : pct(c) ? Z.grade.fmtNum(+(+c.spec.answer * 100).toFixed(8)) : Z.grade.fmtNum(+c.spec.answer));
    /* item 275: bind: "p.a-b" (a state path) on a cell writes what the learner types to the screen's canvas as they
       type, so a tree shows each probability on its branch; tapping that branch focuses the cell */
    const bound = cells.filter((c) => typeof c.spec.bind === 'string' && c.spec.bind);
    /* inbox (fin-ml 3): a number typed into a cell bound to a numeric path (values.<category> on bars, points.<id>.y on a
       plane) is written as a number, so the bar or point moves as the learner types */
    const pushCanvas = (c) => { const cv = ctx.canvas; if (!cv || !cv.set) return; const raw = input(c.id).value.trim(), num = Z.grade.parseNum(raw.replace('%', '')), v = /^(values|points|params|strike|spot|cells\b)/.test(String(c.spec.bind)) && !/^cells\./.test(String(c.spec.bind)) && raw !== '' && Number.isFinite(num) ? (pct(c) ? num / 100 : num) : raw; cv.set(String(c.spec.bind).split('.').reduceRight((acc, k) => ({ [k]: acc }), v), { instant: true }); };
    if (bound.length && ctx.canvas) {
      el.addEventListener('input', (e) => { const c = bound.find((q) => q.id === (e.target.dataset || {}).cell); if (c) pushCanvas(c); });
      if (ctx.canvas.enable && ctx.canvas.on) {
        try { ctx.canvas.enable('tap', { max: 1, only: bound.map((c) => String(c.spec.bind).split('.').slice(1).join('.')) }); } catch { /* no tap mode */ }
        ctx.canvas.on('change', (e) => { if (!e || !e.id) return; const c = bound.find((q) => String(q.spec.bind).split('.').slice(1).join('.') === String(e.id)); if (c) input(c.id).focus(); });
      }
    }
    /* item 408: deps highlight on the canvas while the cell has focus */
    const depsOf = (t) => { const c = cells.find((q) => q.id === (t && t.dataset ? t.dataset.cell : null)); return c && Array.isArray(c.spec.deps) ? c.spec.deps.map(String) : null; };
    el.addEventListener('focusin', (e) => { const d = depsOf(e.target); if (d && ctx.canvas && ctx.canvas.highlight) ctx.canvas.highlight(d, true); });
    el.addEventListener('focusout', (e) => { const d = depsOf(e.target); if (d && ctx.canvas && ctx.canvas.highlight) ctx.canvas.highlight(d, false); });
    const strip = () => cells.forEach(c => input(c.id).parentElement.classList.remove('ok', 'bad', 'wd-rev'));
    const showAccept = () => {
      const lines = cells.map(c => (c.spec.accept && !Array.isArray(c.spec.accept) ? Z.grade.inline(c.spec.accept) : Z.esc(shown(c))));
      acc.innerHTML = 'Accepted: ' + lines.map((t, k) => (pct(cells[k]) ? t + '%' : t)).join(', ') + (cells.some(c => c.spec.tol && (c.spec.tol.abs || c.spec.tol.rel)) ? ', within the stated tolerance' : '');
      acc.hidden = false;
    };
    return {
      el,
      value,
      set(v) { Object.entries(v || {}).forEach(([id, x]) => { const n = input(id); if (n) n.value = x; }); bound.forEach(pushCanvas); ctx.change && ctx.change(value()); },
      answer: () => Object.fromEntries(cells.map(c => [c.id, shown(c)])),
      ready: () => cells.every(c => (c.text ? input(c.id).value.trim() !== '' : Number.isFinite(numIn(c)))),
      dirty: () => cells.some(c => input(c.id).value !== ''),
      grade() {
        const wrong = cells.filter(c => !check(c)), w0 = wrong.length ? wrongOf(wrong[0]) : null;
        return { ok: !wrong.length, key: wrong.length ? (w0 && w0.id ? w0.id : wrong[0].id) : null, detail: { wrong: wrong.map(c => c.id), value: value() } };
      },
      lock() { cells.forEach(c => { input(c.id).readOnly = true; }); },
      unlock() { strip(); acc.hidden = true; cells.forEach(c => { input(c.id).readOnly = false; }); },
      markGraded(res) { strip(); cells.forEach(c => input(c.id).parentElement.classList.add(check(c) ? 'ok' : 'bad')); if (res.ok || res.final) showAccept(); },
      reveal() { strip(); cells.forEach(c => { const n = input(c.id); n.value = shown(c); n.readOnly = true; n.parentElement.classList.add('wd-rev'); }); bound.forEach(pushCanvas); showAccept(); },
      reset() { strip(); acc.hidden = true; cells.forEach(c => { const n = input(c.id); n.value = ''; n.readOnly = false; }); bound.forEach(pushCanvas); },
      focus() { const n = cells[0] && input(cells[0].id); n && n.focus({ preventScroll: true }); },
      destroy() {},
    };
  });
})();
