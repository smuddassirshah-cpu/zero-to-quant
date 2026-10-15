/* Widget base: registry and shared helpers for answer widgets (docs/PLAN.md section 8).
   Loaded after core.js and canvas/_base.js. Each widget file calls ZQ.widgets.register(kind, factory).
   factory(host, spec, ctx) -> { el, value(), set(v), grade(), lock(), unlock(), markGraded(res), reveal(), showWhy(key), reset(), focus(), destroy(), onChange(fn) }
   ctx: { Z, canvas, rng, reducedMotion, mode: 'lesson'|'set'|'exam' } */
(function () {
  'use strict';
  const Z = window.ZQ;
  const kinds = {};
  const register = (kind, factory) => { kinds[kind] = factory; };

  /* Fill in the optional methods so the player can call every one of them without checks. */
  const complete = (w) => {
    const noop = () => {};
    return Object.assign({ set: noop, lock: noop, unlock: noop, markGraded: noop, reveal: noop, showWhy: null, reset: noop, focus: noop, destroy: noop, onChange: (fn) => { w._change = fn; } }, w);
  };
  const create = (host, spec, ctx = {}) => {
    const f = kinds[spec.kind];
    if (!f) { host.append(Z.h(`<div class="wd wd-missing t-caption">Widget "${Z.esc(spec.kind)}" is not available.</div>`)); return null; }
    const listeners = [];
    const api = complete(f(host, spec, { ...ctx, Z, change: (d) => listeners.forEach(fn => fn(d)) }));
    api.onChange = (fn) => listeners.push(fn);
    api.kind = spec.kind; api.spec = spec;
    return api;
  };

  /* Shared grading helpers */
  const parseNum = (s) => {
    const v = String(s ?? '').trim().replace(/\s+/g, '').replace(/,/g, '').replace(/−/g, '-');
    if (!v) return NaN;
    let m = v.match(/^(-?\d+(?:\.\d+)?)\/(-?\d+(?:\.\d+)?)$/); if (m) return +m[2] ? +m[1] / +m[2] : NaN;
    m = v.match(/^(-?\d+)\s+(\d+)\/(\d+)$/); if (m) return +m[1] + Math.sign(+m[1] || 1) * (+m[2] / +m[3]);
    if (/^-?(\d+\.?\d*|\.\d+)(e-?\d+)?$/i.test(v)) return parseFloat(v);
    if (/^-?(\d+\.?\d*|\.\d+)%$/.test(v)) return parseFloat(v) / 100;
    return NaN;
  };
  const within = (value, answer, tol = { abs: 0 }) => {
    if (!Number.isFinite(value)) return false;
    if (tol.rel != null) return Math.abs(value - answer) <= Math.abs(answer) * tol.rel + 1e-12;
    return Math.abs(value - answer) <= (tol.abs ?? 0) + 1e-12;
  };
  const sameSet = (a, b) => { const A = new Set(a), B = new Set(b); return A.size === B.size && [...A].every(x => B.has(x)); };
  const shuffle = (arr, rng = Math.random) => { const a = arr.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rng() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  /* Normalise a typed expression for the fallback comparison: strip spaces, unify ^ and **, lower-case, sort nothing (authors list accepted forms). */
  const normExpr = (s) => String(s ?? '').toLowerCase().replace(/\s+/g, '').replace(/\*\*/g, '^').replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-').replace(/\\frac\{([^}]*)\}\{([^}]*)\}/g, '($1)/($2)').replace(/\\cdot/g, '*').replace(/\\left|\\right/g, '').replace(/\{/g, '(').replace(/\}/g, ')').replace(/\\/g, '');
  /* Option card HTML shared by choice and multi (design-research 5.3 no. 1) */
  const optionCard = (opt, { multi = false, index = 0 } = {}) => {
    const body = opt.image ? `<span class="wd-opt-img" data-art="${Z.esc(opt.image)}"></span>` : Z.md(opt.text ?? '');
    return `<button type="button" class="opt-card wd-opt" role="${multi ? 'checkbox' : 'radio'}" aria-checked="false" data-id="${Z.esc(opt.id)}" data-key="${index + 1}">${multi ? '<span class="wd-check" aria-hidden="true"></span>' : ''}<span class="wd-opt-body">${body}</span><span class="wd-badge" aria-hidden="true"></span></button>`;
  };

  Z.widgets = { register, create, kinds, parseNum, within, sameSet, shuffle, normExpr, optionCard };
})();
