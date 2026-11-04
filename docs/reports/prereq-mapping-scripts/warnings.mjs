// Usage (from repo root): node docs/reports/prereq-mapping-scripts/warnings.mjs <validate-output.txt>
// Prints the validator's requires warnings as "dependent -> reference" lines, with the level numbered from 1.
import fs from 'fs';
const out = [];
for (const l of fs.readFileSync(process.argv[2], 'utf8').split('\n')) {
  const m = l.match(/^warning content\/courses\/([a-z-]+)\/course\.json\s+levels\[(\d+)\]\.requires\[\d+\]: "([^"]+)" (.*)$/);
  if (m && /no written lesson/.test(m[4])) out.push(`- \`${m[1]}/L${+m[2] + 1}\` requires \`${m[3]}\``);
  else if (m) out.push(`- \`${m[1]}/L${+m[2] + 1}\` -> \`${m[3]}\`: ${m[4]}`);
}
console.log(out.join('\n'));
