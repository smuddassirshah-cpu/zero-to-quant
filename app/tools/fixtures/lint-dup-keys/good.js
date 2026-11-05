/* fixture: must pass (strings, comments, templates, regex and state updates hold decoys) */
const a = { x: 1, y: 2, get z() { return 1; }, set z(v) {} };
const t = `${ { k: 1, k2: 2 }.k } { k: 1, k: 2 } ${`${1}`}`;
const re = /{ a: 1, a: 2 }/g, d = 4 / 2;
// { q: 1, q: 2 }
/* { q: 1, q: 2 } */
const str = "{ w: 1, w: 2 }";
const state = { n: 0, fn: null };
state.n = 5;
state.fn = () => 1;
function f(x) { switch (x) { case 1: { return { p: 1, r: 2 }; } default: return { p: 1 }; } }
const nested = { a: { k: 1 }, b: { k: 2 } };
