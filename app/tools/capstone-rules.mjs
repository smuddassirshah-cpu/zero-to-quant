/* Capstone records (ENGINE-BACKLOG 565, PLAN 2c item 8): the shape of content/capstones.json, one record per role.
   checkCapstones(list) returns an array of { where, msg } errors. A missing file is the caller's concern (not an error). */
export const CAPSTONE_ROLES = ['trader', 'researcher', 'developer', 'strats', 'strats-deriv'];
const FIELDS = { role: 'string', project: 'string', repo: 'string', reviewer: 'string', date: 'string', rerun: 'string', defence: 'string', external: 'boolean', equivalentOf: 'string' };
const isObj = (x) => x && typeof x === 'object' && !Array.isArray(x);
const blank = (s) => typeof s !== 'string' || !s.trim();

export const checkCapstones = (list) => {
  const out = [], e = (where, msg) => out.push({ where, msg });
  if (!Array.isArray(list)) { e('', 'capstones.json is an array of records, one per role'); return out; }
  const seen = new Set();
  list.forEach((r, i) => {
    const at = `[${i}]`;
    if (!isObj(r)) { e(at, 'a record is an object'); return; }
    Object.keys(r).forEach(k => { if (!(k in FIELDS)) e(`${at}.${k}`, `unknown field "${k}" (fields: ${Object.keys(FIELDS).join(', ')})`); else if (typeof r[k] !== FIELDS[k]) e(`${at}.${k}`, `${k} must be a ${FIELDS[k]}`); });
    if (typeof r.role === 'string') {
      if (!CAPSTONE_ROLES.includes(r.role)) e(`${at}.role`, `unknown role "${r.role}" (${CAPSTONE_ROLES.join(', ')})`);
      else if (seen.has(r.role)) e(`${at}.role`, `duplicate record for role "${r.role}"`);
      seen.add(r.role);
    } else e(`${at}.role`, 'role is required');
    if (typeof r.repo === 'string' && r.repo.trim() && !/^https:\/\/[^\s/]+\.[^\s/]+(\/\S*)?$/.test(r.repo.trim())) e(`${at}.repo`, 'repo is an https URL or empty');
    if (typeof r.date === 'string' && r.date.trim()) {
      const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(r.date.trim()), d = m && new Date(`${r.date.trim()}T00:00:00Z`);
      if (!m || isNaN(d) || d.toISOString().slice(0, 10) !== r.date.trim()) e(`${at}.date`, 'date is an ISO date (YYYY-MM-DD) or empty');
    }
    if (typeof r.rerun === 'string' && r.rerun.trim() && !['pass', 'fail'].includes(r.rerun.trim())) e(`${at}.rerun`, 'rerun is "pass", "fail" or empty');
    if (r.external === true) ['repo', 'reviewer', 'date', 'rerun'].forEach(k => { if (blank(r[k])) e(`${at}.${k}`, `external: true needs a non-empty ${k}`); });
    if (r.role === 'researcher' && typeof r.project === 'string' && r.project.trim() && r.project.trim() !== 'momentum-rep' && r.equivalentOf !== 'momentum-rep')
      e(`${at}.project`, 'the researcher project is "momentum-rep" or carries equivalentOf: "momentum-rep"');
    if (r.equivalentOf !== undefined && r.equivalentOf !== 'momentum-rep') e(`${at}.equivalentOf`, 'equivalentOf is "momentum-rep"');
  });
  return out;
};
