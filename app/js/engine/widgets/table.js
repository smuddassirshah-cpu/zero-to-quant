/* Table widget (docs/AUTHORING.md 3, design-research 5.3 no. 14). Fixed cells are text (KaTeX allowed);
   editable cells { edit: true, answer, tol } take the numeric grading rules. Every editable cell must be within
   tolerance; key is the first wrong cell id r{i}c{j} (zero-based, as the table canvas). After grading each
   editable cell is marked: right cells take green, wrong ones amber, so a retry only touches what is wrong. */
(function () {
  'use strict';
  const Z = window.ZQ;

  Z.widgets.register('table', (host, spec, ctx) => {
    const cols = spec.columns || [];
    const rows = spec.rows || [];
    const cells = [];
    const el = Z.h(`<div class="wd-tablewrap"><table class="wd-table">
      ${cols.length ? `<thead><tr>${cols.map(c => `<th scope="col">${Z.grade.inline(c)}</th>`).join('')}</tr></thead>` : ''}
      <tbody>${rows.map((row, i) => `<tr>${row.map((c, j) => {
        if (c && typeof c === 'object' && c.edit) {
          cells.push({ id: `r${i}c${j}`, spec: c });
          const label = `${cols[j] ? String(cols[j]).replace(/\$/g, '') : 'Column ' + (j + 1)}, row ${i + 1}`;
          return `<td class="wd-td-edit"><input type="text" inputmode="decimal" autocomplete="off" spellcheck="false" data-cell="r${i}c${j}" aria-label="${Z.esc(label)}" placeholder="${Z.esc(c.placeholder || '?')}"></td>`;
        }
        return j === 0 ? `<th scope="row">${Z.grade.inline(c ?? '')}</th>` : `<td>${Z.grade.inline(c ?? '')}</td>`;
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
    const check = (c) => Z.grade.within(Z.grade.parseNum(input(c.id).value), +c.spec.answer, c.spec.tol);
    const strip = () => cells.forEach(c => input(c.id).parentElement.classList.remove('ok', 'bad', 'wd-rev'));
    const showAccept = () => {
      const lines = cells.map(c => (c.spec.accept ? Z.grade.inline(c.spec.accept) : Z.grade.fmtNum(+c.spec.answer)));
      acc.innerHTML = 'Accepted: ' + lines.join(', ') + (cells.some(c => c.spec.tol && (c.spec.tol.abs || c.spec.tol.rel)) ? ', within the stated tolerance' : '');
      acc.hidden = false;
    };
    return {
      el,
      value,
      set(v) { Object.entries(v || {}).forEach(([id, x]) => { const n = input(id); if (n) n.value = x; }); ctx.change && ctx.change(value()); },
      answer: () => Object.fromEntries(cells.map(c => [c.id, Z.grade.fmtNum(+c.spec.answer)])),
      ready: () => cells.every(c => Number.isFinite(Z.grade.parseNum(input(c.id).value))),
      dirty: () => cells.some(c => input(c.id).value !== ''),
      grade() {
        const wrong = cells.filter(c => !check(c));
        return { ok: !wrong.length, key: wrong.length ? wrong[0].id : null, detail: { wrong: wrong.map(c => c.id), value: value() } };
      },
      lock() { cells.forEach(c => { input(c.id).readOnly = true; }); },
      unlock() { strip(); acc.hidden = true; cells.forEach(c => { input(c.id).readOnly = false; }); },
      markGraded(res) { strip(); cells.forEach(c => input(c.id).parentElement.classList.add(check(c) ? 'ok' : 'bad')); if (res.ok || res.final) showAccept(); },
      reveal() { strip(); cells.forEach(c => { const n = input(c.id); n.value = Z.grade.fmtNum(+c.spec.answer); n.readOnly = true; n.parentElement.classList.add('wd-rev'); }); showAccept(); },
      reset() { strip(); acc.hidden = true; cells.forEach(c => { const n = input(c.id); n.value = ''; n.readOnly = false; }); },
      focus() { const n = cells[0] && input(cells[0].id); n && n.focus({ preventScroll: true }); },
      destroy() {},
    };
  });
})();
