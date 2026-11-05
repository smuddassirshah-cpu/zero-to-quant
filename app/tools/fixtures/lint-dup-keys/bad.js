/* fixture: must be reported (3 findings) */
const readiness = {
  status(course) { return 1; },
  other: 2,
  status(course, role) { return 2; },
};
const api = { run: () => 1, name: 'x' };
api.run = function () { return 2; };
const s = { 'a-b': 1, "a-b": 2 };
