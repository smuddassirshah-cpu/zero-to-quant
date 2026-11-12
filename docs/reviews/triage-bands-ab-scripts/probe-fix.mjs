/* Fix-pass probe: grades the refused value, the wrong[] values and the answer one step short on the real grader.
   node probe-fix.mjs --local-cdn <pkgs> */
import path from 'node:path';
import { boot, gradeText, resolve, readJson, APP, cdnArg } from './lib.mjs';
const { reg } = boot(cdnArg());
const T = [
  ['alpha/l7-ranks-and-z', 'quiz[3].widget', [2.47, 2.475, 2.4749, 2.46, 2.6458, 0]],
  ['conditional/review-5', 'items[4].widget', [0.46, '6/13', 0.4615, 0.45, 0.6, 0.8571, 0]],
  ['cpp-pricing/l6-binomial-cpp', 'quiz[1].widget', [11.9, 11.9048, 11.89, 12.5, 9.5238, 0]],
  ['cpp-pricing/review-2', 'items[1].widget', [3.92, 3.9216, 3.91, 4.0, 5.8824, 0]],
  ['regression/l5-how-sure', 'quiz[3].widget', [0.25, 0.254, 0.2535, 0.24, 0.0107, 1.0, 0]],
];
for (const [f, p, vals] of T) {
  const d = readJson(path.join(APP, 'content/courses', f + '.json'));
  const { node } = resolve(d, p);
  console.log(f, 'tol', JSON.stringify(node.tol));
  for (const v of vals) console.log('  ', v, JSON.stringify(await gradeText(reg, node, v)));
}
