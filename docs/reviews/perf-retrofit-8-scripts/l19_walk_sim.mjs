// Replays the walk canvas of markov l19 screens 5 and 9 (run 0) with the engine's mulberry32 and draw order
// (per path: for each step one uniform, then one Box-Muller normal), stopping at the barriers.
// Prints the average stopped value and the counts, to check the explain text. Run: node l19_walk_sim.mjs
const rng = (seed) => { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
const gauss = (r) => { let u = 0; while (u <= 1e-12) u = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * r()); };
function run({ seed, paths, steps, p, start, lower, upper }, f = (x) => x) {
  const r = rng((seed * 7919 + 0 * 104729) >>> 0);
  let sum = 0, up = 0, down = 0, open = 0, fsum = 0;
  for (let j = 0; j < paths; j++) {
    const u = new Float64Array(steps);
    for (let i = 0; i < steps; i++) { u[i] = r(); gauss(r); }
    let x = start, done = false;
    for (let i = 0; i < steps && !done; i++) { x += u[i] < p ? 1 : -1; if (x <= lower || x >= upper) done = true; }
    if (x >= upper) up++; else if (x <= lower) down++; else open++;
    sum += x; fsum += f(x);
  }
  return { mean: sum / paths, fmean: fsum / paths, up, down, open };
}
const s9 = run({ seed: 6, paths: 200, steps: 8000, p: 0.49, start: 50, lower: 0, upper: 100 });
console.log('screen 9:', JSON.stringify(s9));
const s5 = run({ seed: 11, paths: 300, steps: 300, p: 0.4, start: 5, lower: 0, upper: 10 }, (x) => Math.pow(1.5, x));
console.log('screen 5:', JSON.stringify(s5));
const ok = s9.up === 23 && Math.abs(s9.mean - 11.75) < 0.005;
console.log(ok ? 'ok   screen 9 explain figures (23 of 200, average 11.75) match run 0' : 'MISMATCH screen 9 explain figures');
process.exit(ok ? 0 : 1);
