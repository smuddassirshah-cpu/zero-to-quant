// Builds the STANDS waiver entries of review-pkg3-reuse-hits from the reader's verdicts and the checker's own hit list.
// Run from app/:
//   node tools/same-course-reuse.mjs --all --all-exams --json > hits.json
//   node ../docs/reviews/review-pkg3-reuse-hits-scripts/waivers.mjs hits.json [merged-out.json]
// Prints the new entries as JSON (gate entries first). With a second argument it also writes the current waiver file
// plus the new entries there, for a trial run with ZQ_WAIVERS=<merged-out.json>.
import fs from 'fs';
const hits = JSON.parse(fs.readFileSync(process.argv[2])).filter((h) => !h.waived);
const REF = ' (review-pkg3-reuse-hits)';
// item id | kind -> reason; FAULT marks the two hits that get no waiver
const V = {
  'p-daylight-model|ratio': 'FAULT',
  'p-spread-blocks|chain-union': 'FAULT',
  'p-probe-stride|ratio': 'slot 13 of a 56-slot table against 65% of 280 in a mental arithmetic mock; a chance match',
  'p-sum-law-band|rate': '4/311 is a term of a limit gap and 0.04 its epsilon, against a Kelly growth of 1.29% and a stake of 0.04; a chance match',
  'p-smoothed-fund|rate': 'a root-12 volatility of 10.0% and a variance weight 0.52, against 1,000 labels worth 100 and a base rate of 52%; a chance match',
  'p-screen-real-share|rate': 'a slip value of 19.4% (36 of 186) against 7/36 in a meeting-time item and a dice item; a chance match',
  'p-takeover-rumour|ratio': '180 of 456 rumoured stocks against trades of £15 and £38 in a mental sum; a chance match',
  'p-two-houses|question': 'the survivorship gap asked in its natural words; own data (25 of 50 funds, 8% and −2%, against 60%, 8% and −5%), and the part feeds a Simpson comparison of two houses that the homework lacks',
  'p-crab-sizes|ratio': 'claw lengths 88 and 118 against terms 44 and 59 of a digit-sum sequence; a chance match',
  'p-site-anomalies|rate': 'a variance share 0.769 against a logistic slip of 76.85%; a chance match',
  'p-florist-prices|ratio': 'matrix entries 13 and 19 against the product 38 × 26; a chance match',
  'p-interest-split|ratio': '£660 of interest and the multiplier 1000 against share prices of £8.25 and £12.50; a chance match',
  'p-sapling-log|ratio': 'heights 29 and 32 cm against the product 58 × 64; a chance match',
  'p-two-filters-one-score|rate': 'a starting variance of 1.44 %² against 0.12 squared inside a Ljung-Box sum; a chance match',
  'p-bank-index-flat-var|rate': 'a starting variance of 2.25 %² and a leverage cap of 1.25 against a KKT multiplier and a covariance entry; a chance match',
  'p-runner-heart|ratio': 'a slope of 5.9 against terms 40 and 59 of a digit-sum sequence; a chance match',
  'p-relative-strength|pair': '0.0004 and 0.02 are a ratio\'s slope and level, against a variance and its root in a standard error; different quantities',
  'p-fund-months|numbers': 'both reach t = 1.8 and are told Φ(1.8) = 0.9641; the set asks a two-sided tail from a monthly mean and σ/√n, the exam a one-sided p from a Sharpe ratio and 1/√T, so neither deciding step gives the other',
  'p-maker-edge|ratio': 'a standard deviation of £39.80 over 400 trades against 10 units and a limit of 100.5; a chance match',
  'p-cycle-commute|transform': 'four commute times against four returns inside a code task; a chance affine match',
  'p-float32-overnight|ratio': 'a relative error of 3.16e-8 against a quote of 3.95% moved 10 bp; a chance match',
  'p-pilot-control|ratio': 'a covariance of 77 from 2,000 paths against 2.31e18 and the exponent 60; a chance match',
  'p-grid-node-budget|ratio': 'a volatility of 30% and a spot of 76 against trades of £15 and £38 in a mental sum; a chance match',
  'p-tightest-quote|rate': '0.6 to the 9th, 0.0101, against a trading cost of 1.01% and £0.60 traded; a chance match',
  'p-file-retry|ratio': 'waits of 3.2 and 7.4 seconds against terms 16 and 37 of a digit-square sequence; a chance match',
  'p-partners-profit|ratio': '£2,850 of £12,000 against a 95% interval on 400 days; a chance match',
  'p-stopping-distances|ratio': 'stopping distances of 23 m and 36 m against fitted values 2.3 and 3.6 of an SSR screen; a chance match',
  'p-car-prices|ratio': 'prices of £15,400 and £18,000 against closes of 77.0 and 90.0 in a drawdown assert; a chance match',
  'p-bouncing-ball|rate': '0.6 to the 9th, 0.010078, against a trading cost of 1.01%; a chance match',
  'p-heat-demand|ratio': 'a training MSE of 3.10 and degree 6 against 31 May and a 60-day volatility; a chance match',
  'p-loaves-k|ratio': 'expected errors of 5.8 and 10.4 against terms 29 and 52 of a digit-sum sequence; a chance match',
  'p-two-looks|rate': 'a planned level of 0.0107 and 37 patterns against a VaR line of a breach chart; a chance match',
  'p-spread-day-tail|ratio': 'normal arguments 2.003 and 2.819 against trades of £27 and £38 in a mental sum; a chance match',
  'p-gas-demand|ratio': 'block errors of 5.2 and 6.1 against terms of two number sequences; a chance match',
  'p-spread-blocks|ratio': 'errors of 3.85 and 4.62 against closes of 77.0 and 100.0 in a drawdown assert; a chance match (moot once the item is re-authored, fault 2)',
  'p-rectangle-edges|function': 'y³ − 4y is one component of a field whose curl is asked, against f′(x) = x³ − 4x read off a graph for its maxima; a small cubic, different questions',
  'p-charging-robot|ratio': 'a dot product of 42 and a squared length of 68 against price moves of £2.10 and £3.40; a chance match',
};
const groups = new Map(); const counts = {};
for (const h of hits) {
  const key = `${h.itemId}|${h.kind}`; const v = V[key];
  if (!v) throw new Error('no verdict for ' + key);
  const tag = h.allExams ? 'all-exams' : h.kind; counts[tag] ??= { FAULT: 0, STANDS: 0 }; counts[tag][v === 'FAULT' ? 'FAULT' : 'STANDS']++;
  if (v === 'FAULT') continue;
  const g = groups.get(h.file + '|' + key) ?? { file: h.file, item: h.itemId, kind: h.kind, sources: new Set(), gate: false, reason: 'stands: ' + v + REF };
  g.sources.add(h.source.split(':')[0]); g.gate ||= !h.allExams; groups.set(h.file + '|' + key, g);
}
const used = Object.keys(V).filter((k) => !hits.some((h) => `${h.itemId}|${h.kind}` === k));
if (used.length) throw new Error('verdicts without a hit: ' + used.join(', '));
const entries = [...groups.values()].sort((a, b) => b.gate - a.gate || a.file.localeCompare(b.file)).map((g) => ({ file: g.file, item: g.item, kind: g.kind, source: g.sources.size === 1 ? [...g.sources][0] : [...g.sources], reason: g.reason, _gate: g.gate }));
const cur = JSON.parse(fs.readFileSync(new URL('../../../app/tools/same-course-waivers.json', import.meta.url)));
for (const e of entries) if (cur.some((w) => w.file === e.file && w.item === e.item && w.kind === e.kind)) console.error('note: an entry of this file, item and kind exists already:', e.file, e.item, e.kind);
const strip = ({ _gate, ...e }) => e;
console.error('counts by tag:', JSON.stringify(counts), '| entries:', entries.length, '| gate entries:', entries.filter((e) => e._gate).length);
console.log(JSON.stringify(entries.map(strip), null, 2));
if (process.argv[3]) fs.writeFileSync(process.argv[3], JSON.stringify([...cur, ...entries.map(strip)], null, 2) + '\n');
