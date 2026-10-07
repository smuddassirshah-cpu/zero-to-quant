// Spike S1 probe, module 'caps': the capabilities the page declares (user with scope profile, permissions,
// db with its rule set, sample), measured on the device (docs/PLAN.md stage 2).
// Decision notes:
// - Every namespace comes through ctx.claude(name). A null namespace makes a check skipped, never a pass.
// - The viewer's id is never stored, logged or shown: data keeps its type and length only, every stored error
//   message has the id replaced by <own id>, and names, avatars and emails are reduced to booleans.
// - db paths are built with the ref builders (collection, then doc) so the segment parity is right. Every
//   document a check writes is deleted. A transient 'unavailable' gets the one retry the db contract advises,
//   and the retry is recorded. Each db or user call has its own 6 s limit, so one hung call leaves the rest of
//   the evidence instead of the harness timeout.
// - The round trip passes only on a server-definitive read (fromCache and hasPendingWrites both false), so a
//   page-side cache cannot pass it. The rules check writes the own-subtree case first: the other viewer's case
//   then differs from it only in the path, so its rejection is attributable to the path.
// - As the owner, every level rule is met, so most outcomes equal the platform's defaults [sourced: db.d.ts].
//   The rules check therefore carries a canary that only a declared rule can produce: s1canary/{self} with no
//   rule at its prefix keeps siblings private, the owner included, so the owner's write to s1canary/zz-not-me
//   must be refused. Without that refusal the check cannot tell a declared rule set from the defaults. The
//   levels below owner need a second participant and stay with the emulator (PLAN.md 7.3).
// - The meta/release watch starts in resume(), before any check runs, and needs no clock: a s1-v2 delivery
//   counts only when an earlier server-definitive delivery in this page had another release or no document,
//   or when its `at` differs from the s1-v2 value of the first definitive delivery; the first delivery never
//   counts. A value left by an earlier run cannot pass, whatever the clocks of the phone and of Claude's
//   machine. A watch the bridge drops with 'unavailable' is subscribed again, twice at most, 5 s apart.
// - Sample calls pass cache: false, except the tools call, which omits cache (the contract rejects any other
//   value with tools). Model output reaches the page through textContent only and is never stored: data keeps
//   what the checks derived from it (whether it said the word asked for, lengths, counts), so no reply reaches
//   db (PLAN.md 8.4).
// - Streaming uses the default tier [our choice]: the quick tier can write 120 words inside one or two onText
//   windows (a few a second at most), which would measure generation speed rather than streaming.

const MODULE_START = Date.now();
const MARKER = `${MODULE_START.toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
const CALL_TIMEOUT_MS = 6_000;
const RULES_BUDGET_MS = 22_000;
const RELEASE_DOC = 'meta/release';
const RELEASE_TARGET = 's1-v2';
const RELEASE_WAIT_MS = 90_000;
const RELEASE_TIMEOUT_MS = 120_000; // the harness limit this check declares: above the 90 s wait from the signal
const RESUBSCRIBES = 2;
const RESUBSCRIBE_GAP_MS = 5_000;
const NOT_ME = 'zz-not-me';
const CANARY = 's1canary';
const TIERS = ['quick', 'default', 'complex'];
const TRANSIENT = new Set(['unavailable', 'resource_exhausted']);
const PROBE_VALUE = '4217';

let ownId = null; // in memory only, to scrub it from stored messages; never stored, logged or shown
let sampleCalls = 0; // sample() calls this page has made, so the consent check knows whether it was first

// ---- helpers

const r0 = v => Math.round(v);
const clip = (s, n) => (s.length > n ? `${s.slice(0, n)}...` : s);
const scrub = s => (ownId ? s.split(ownId).join('<own id>') : s);
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const bool = v => (typeof v === 'boolean' ? v : null);
const codeOf = e => (e && typeof e === 'object' && typeof e.code === 'string' ? e.code : null);
const textLen = e => (e && typeof e === 'object' && typeof e.text === 'string' ? e.text.length : 0);

function errInfo(e) {
  if (e && typeof e === 'object') {
    const out = { code: codeOf(e), message: scrub(clip(typeof e.message === 'string' ? e.message : String(e), 240)) };
    if (e instanceof Error) out.name = e.name;
    return out;
  }
  return { code: null, message: scrub(clip(String(e), 240)) };
}

// A JSON-safe copy of a platform value, or a marked preview when it is over max characters.
function jsonCopy(v, max) {
  try {
    const s = JSON.stringify(v);
    if (s === undefined) return null;
    return s.length <= max ? JSON.parse(s) : { truncated: true, preview: clip(s, max) };
  } catch (e) {
    return { notSerialisable: errInfo(e).message };
  }
}

// A short JSON-safe copy of a field read from a document: strings clipped, other objects named by type.
function short(v) {
  if (v === undefined || v === null) return null;
  if (typeof v === 'string') return clip(v, 60);
  if (typeof v === 'number' || typeof v === 'boolean') return v;
  return `(${Array.isArray(v) ? 'array' : typeof v})`;
}

// Epoch ms from an ISO string or an epoch in seconds or ms; null otherwise (as the harness reads `at`).
function parseAt(at) {
  if (typeof at === 'number' && Number.isFinite(at)) return at > 1e12 ? at : at > 1e9 ? at * 1000 : null;
  if (typeof at === 'string') {
    const t = Date.parse(at);
    return Number.isNaN(t) ? null : t;
  }
  return null;
}

// Key-order-independent JSON, for comparing a body with what the store returns.
function canon(v) {
  if (Array.isArray(v)) return `[${v.map(canon).join(',')}]`;
  if (v && typeof v === 'object') return `{${Object.keys(v).sort().map(k => `${JSON.stringify(k)}:${canon(v[k])}`).join(',')}}`;
  return JSON.stringify(v) ?? 'undefined';
}

// Resolves { ok: true, value, ms } | { ok: false, error, ms } | { ok: false, timedOut: true, ms }; never rejects.
function attempt(fn, ms, now) {
  const t0 = now();
  return new Promise(resolve => {
    const timer = ms ? setTimeout(() => resolve({ ok: false, timedOut: true, ms: r0(now() - t0) }), ms) : 0;
    let p;
    try {
      p = Promise.resolve(fn());
    } catch (error) {
      clearTimeout(timer);
      resolve({ ok: false, error, ms: r0(now() - t0), threw: true });
      return;
    }
    p.then(
      value => { clearTimeout(timer); resolve({ ok: true, value, ms: r0(now() - t0) }); },
      error => { clearTimeout(timer); resolve({ ok: false, error, ms: r0(now() - t0) }); },
    );
  });
}

// One db call with the contract's single retry on 'unavailable', after a short randomised delay.
async function dbCall(fn, now) {
  const first = await attempt(fn, CALL_TIMEOUT_MS, now);
  if (first.ok || codeOf(first.error) !== 'unavailable') return { ...first, attempts: 1 };
  await sleep(250 + Math.random() * 500);
  const second = await attempt(fn, CALL_TIMEOUT_MS, now);
  return { ...second, attempts: 2, firstError: errInfo(first.error), firstMs: first.ms };
}

const brief = o => {
  const b = { ok: o.ok, ms: o.ms };
  if (o.attempts > 1) Object.assign(b, { attempts: o.attempts, firstError: o.firstError, firstMs: o.firstMs });
  if (o.timedOut) b.timedOut = true;
  else if (!o.ok) b.error = errInfo(o.error);
  return b;
};

const metaOf = snap => (snap && snap.metadata && typeof snap.metadata === 'object'
  ? { fromCache: bool(snap.metadata.fromCache), hasPendingWrites: bool(snap.metadata.hasPendingWrites) }
  : null);
const definitive = m => !!m && m.fromCache === false && m.hasPendingWrites === false;

function snapBody(snap) {
  if (!snap || snap.exists !== true || typeof snap.data !== 'function') return { body: null };
  try {
    return { body: snap.data() ?? null };
  } catch (e) {
    return { body: null, error: errInfo(e) };
  }
}

// The check's output area: a label and a pre whose text is set with textContent only.
function show(ctx, label, text) {
  if (!ctx.mount || typeof document === 'undefined') return null;
  const head = document.createElement('p');
  head.textContent = label;
  const pre = document.createElement('pre');
  pre.className = 'data';
  pre.textContent = text;
  const box = document.createElement('div');
  box.append(head, pre);
  ctx.mount.replaceChildren(box);
  return pre;
}

async function getSample(ctx) {
  const sample = await ctx.claude('sample');
  if (!sample) return { skip: { status: 'skipped', summary: "claude.use('sample') resolved null, so this view cannot ask Claude.", data: { namespace: false } } };
  if (typeof sample !== 'function') {
    return { skip: { status: 'fail', summary: 'The sample namespace resolved but is not callable.', data: { namespace: true, type: typeof sample } } };
  }
  return { sample };
}

function sampleFailure(e, ms, what) {
  const error = errInfo(e);
  const why = error.code === 'not_granted' ? ': consent was declined, or the organisation does not allow it' : '';
  return { status: 'fail', summary: `${what} rejected with ${error.code ?? 'no code'}${why}.`, data: { ms, error, partialChars: textLen(e) } };
}

// ---- caps.user

const userCheck = {
  id: 'caps.user',
  title: 'The user capability',
  kind: 'auto',
  what: 'Reads isOwner, canEdit, can, id, me and profiles from the user namespace and records the answers, keeping only the id length and whether names were present.',
  async run(ctx) {
    const user = await ctx.claude('user');
    if (!user) return { status: 'skipped', summary: "claude.use('user') resolved null, so this view has no user namespace.", data: { namespace: false } };
    const scopes = ctx.lock?.capabilities?.user?.scopes;
    const data = { namespace: true, calls: {}, declaredScopes: Array.isArray(scopes) ? scopes.map(String).slice(0, 5) : 'lock.json lists no declaration' };
    const read = async (name, fn) => {
      const o = await attempt(fn, CALL_TIMEOUT_MS, ctx.now);
      data.calls[name] = o.ok ? { ms: o.ms } : { ms: o.ms, ...(o.timedOut ? { timedOut: true } : { rejected: errInfo(o.error) }) };
      return o.ok ? o.value : undefined;
    };

    data.isOwner = bool(await read('isOwner', () => user.isOwner()));
    data.canEdit = bool(await read('canEdit', () => user.canEdit()));
    const can = {};
    for (const name of ['data.write', 'files.write', 'assets.write', 's1.not-a-capability']) {
      const v = await read(`can(${name})`, () => user.can(name));
      can[name] = v === undefined ? '(no answer)' : short(v);
    }
    data.can = can;

    const id = await read('id', () => user.id());
    const idOk = typeof id === 'string' && id.length > 0;
    data.id = { type: id === null ? 'null' : typeof id, nonEmpty: idOk, length: typeof id === 'string' ? id.length : null };
    if (idOk) ownId = id;

    const me = await read('me', () => user.me());
    if (me && typeof me === 'object') {
      const avatar = me.avatarUrl;
      data.me = {
        nameNonEmpty: typeof me.name === 'string' && me.name.length > 0,
        idEqualsId: me.id === id,
        emailIsNull: me.email === null,
        isOwner: bool(me.isOwner),
        canEdit: bool(me.canEdit),
        avatarScheme: typeof avatar !== 'string' ? typeof avatar : avatar.startsWith('data:') ? 'data' : /^https?:/i.test(avatar) ? 'http' : avatar ? 'other' : 'empty',
        colourPresent: typeof me.color === 'string' && me.color.length > 0,
      };
    } else data.me = me === undefined ? null : { type: typeof me };

    if (idOk) {
      const ps = await read('profiles', () => user.profiles([id]));
      if (ps && typeof ps === 'object') {
        const p = Object.hasOwn(ps, id) ? ps[id] : null;
        data.profiles = {
          keyCount: Object.keys(ps).length,
          ownEntry: !!p,
          nameNonEmpty: !!p && typeof p.name === 'string' && p.name.length > 0,
          isMe: bool(p?.isMe),
          guest: bool(p?.guest),
          emailIsNull: p ? p.email === null : null,
        };
      } else data.profiles = ps === undefined ? null : { type: typeof ps };
    } else data.profiles = { called: false, why: 'no id' };

    if (data.calls.id?.rejected || data.calls.id?.timedOut) {
      return { status: 'fail', summary: `user.id() ${data.calls.id.timedOut ? 'gave no answer in 6 s' : 'rejected'}, although the contract says user reads never reject.`, data };
    }
    if (!idOk) return { status: 'fail', summary: `user.id() resolved ${data.id.type === 'string' ? 'an empty string' : data.id.type}, although the page declares the user capability.`, data };
    const yn = v => (v === true ? 'yes' : v === false ? 'no' : 'unknown');
    const line = `owner ${yn(data.isOwner)}, can edit ${yn(data.canEdit)}, can('data.write') ${String(can['data.write'])}, an id of ${data.id.length} characters, a name in me() ${yn(data.me?.nameNonEmpty)}, in profiles() ${yn(data.profiles?.nameNonEmpty)}`;
    if (data.me?.nameNonEmpty !== true || data.profiles?.nameNonEmpty !== true) {
      return {
        status: 'inconclusive',
        summary: `The viewer id works, but the profile part did not: ${line}. Either the publish did not declare scopes: ['profile'] (lock.json says the declaration has ${JSON.stringify(data.declaredScopes)}; a declared scope is a ceiling, not a guarantee) or the organisation withholds names.`,
        data,
      };
    }
    return { status: 'pass', summary: `The user namespace answered with an id and a profile: ${line}.`, data };
  },
};

// ---- caps.permissions

const permissionsCheck = {
  id: 'caps.permissions',
  title: 'Permission states, read without prompting',
  kind: 'auto',
  what: "Reads permissions.state() with no arguments (it never prompts) and the named states of the declared capabilities, and records them.",
  async run(ctx) {
    const permissions = await ctx.claude('permissions');
    if (!permissions) return { status: 'skipped', summary: "claude.use('permissions') resolved null on this view.", data: { namespace: false } };
    if (typeof permissions.state !== 'function') {
      return { status: 'fail', summary: 'The permissions namespace has no state function.', data: { namespace: true, members: Object.keys(permissions).slice(0, 20) } };
    }
    const all = await attempt(() => permissions.state(), CALL_TIMEOUT_MS, ctx.now);
    const data = { namespace: true, state: null, ms: all.ms };
    if (!all.ok) {
      data.error = all.timedOut ? 'no answer in 6 s' : errInfo(all.error);
      return { status: 'fail', summary: `permissions.state() ${all.timedOut ? 'gave no answer in 6 s' : 'rejected'}.`, data };
    }
    const map = all.value && typeof all.value === 'object' ? all.value : null;
    data.state = map ? Object.fromEntries(Object.entries(map).slice(0, 40).map(([k, v]) => [clip(k, 60), short(v)])) : short(all.value);
    data.named = {};
    for (const name of ['sample', 'db', 'user', 'permissions']) {
      const o = await attempt(() => permissions.state(name), CALL_TIMEOUT_MS, ctx.now);
      data.named[name] = o.ok ? short(o.value) : o.timedOut ? '(no answer in 6 s)' : `(rejected ${errInfo(o.error).code ?? 'no code'})`;
    }
    const listed = map ? Object.entries(data.state).map(([k, v]) => `${k} ${v}`).join(', ') : 'not a map';
    return { status: 'info', summary: `permissions.state() resolved in ${all.ms} ms: ${listed || 'an empty map'}.`, data };
  },
};

// ---- caps.db-roundtrip

const roundtripCheck = {
  id: 'caps.db-roundtrip',
  title: 'db write, read back and delete',
  kind: 'auto',
  what: 'Writes a document of mixed JSON types to ops/s1-probe-<marker>, reads it back from the server, compares it field by field, deletes it and reads again, timing each call.',
  async run(ctx) {
    const db = await ctx.claude('db');
    if (!db) return { status: 'skipped', summary: "claude.use('db') resolved null, so this view has no db.", data: { namespace: false } };
    const path = `ops/s1-probe-${MARKER}`;
    let ref;
    try {
      ref = db.doc(path);
    } catch (e) {
      return { status: 'error', summary: `db.doc('${path}') threw.`, data: { error: errInfo(e) } };
    }
    const body = {
      probe: 's1', marker: MARKER, writtenAt: new Date().toISOString(),
      int: 42, float: 0.1 + 0.2, negative: -7.25, maxSafe: Number.MAX_SAFE_INTEGER,
      yes: true, no: false, nothing: null,
      text: 'colour, naïve café, 中文, emoji 🙂, quote " backslash \\ newline \n end',
      list: [1, 'two', false, null, { k: 'v' }, [3, [4]]],
      nested: { a: { b: { c: [3, 2, 1] } } }, emptyMap: {}, emptyList: [],
    };
    const data = { path, calls: {} };
    const set = await dbCall(() => ref.set(body), ctx.now);
    data.calls.set = brief(set);
    if (!set.ok) {
      if (set.timedOut) data.calls.cleanupDelete = brief(await dbCall(() => ref.delete(), ctx.now));
      return { status: TRANSIENT.has(codeOf(set.error)) || set.timedOut ? 'inconclusive' : 'fail', summary: `set() on ${path} ${set.timedOut ? 'gave no answer in 6 s' : `rejected with ${errInfo(set.error).code ?? 'no code'}`}.`, data };
    }

    const readBack = async label => {
      const g = await dbCall(() => ref.get(), ctx.now);
      data.calls[label] = { ...brief(g), exists: g.ok ? g.value?.exists === true : null, metadata: g.ok ? metaOf(g.value) : null };
      return g;
    };
    let g = await readBack('get');
    if (g.ok && !definitive(metaOf(g.value))) {
      await sleep(1500);
      g = await readBack('getAgain');
    }
    let verdict = null;
    if (g.ok) {
      const { body: got, error } = snapBody(g.value);
      if (error) data.dataError = error;
      if (got) {
        const sentKeys = Object.keys(body);
        const differs = sentKeys.filter(k => canon(body[k]) !== canon(got[k]));
        const extra = Object.keys(got).filter(k => !Object.hasOwn(body, k));
        data.differs = differs.slice(0, 10).map(k => ({ key: k, sent: clip(canon(body[k]), 120), back: clip(canon(got[k]), 120) }));
        data.extraKeys = extra.slice(0, 20);
        verdict = { equal: differs.length === 0, extra: extra.length, definitive: definitive(metaOf(g.value)) };
      }
    }

    data.calls.delete = brief(await dbCall(() => ref.delete(), ctx.now));
    const after = await dbCall(() => ref.get(), ctx.now);
    data.calls.getAfterDelete = { ...brief(after), exists: after.ok ? after.value?.exists === true : null };
    const gone = data.calls.delete.ok && data.calls.getAfterDelete.exists === false;
    const cleanup = gone ? 'deleted' : `not confirmed deleted (delete ${data.calls.delete.ok ? 'resolved' : 'failed'}, then exists ${String(data.calls.getAfterDelete.exists)})`;
    const timing = `set ${data.calls.set.ms} ms, get ${data.calls.get.ms} ms, delete ${data.calls.delete.ms} ms`;

    if (!g.ok) {
      return { status: g.timedOut || TRANSIENT.has(codeOf(g.error)) ? 'inconclusive' : 'fail', summary: `set() resolved but get() ${g.timedOut ? 'gave no answer in 6 s' : 'rejected'}; the document was ${cleanup}.`, data };
    }
    if (!verdict) return { status: 'fail', summary: `set() resolved but get() found no document body; the document was ${cleanup}.`, data };
    if (!verdict.equal) return { status: 'fail', summary: `The body came back different in ${data.differs.length} field(s): ${data.differs.map(d => d.key).join(', ')}; the document was ${cleanup}.`, data };
    if (!verdict.definitive) {
      return { status: 'inconclusive', summary: `The body matched, but the read was not server-definitive (fromCache or hasPendingWrites was not false), so it may be the page's own cache; the document was ${cleanup}.`, data };
    }
    if (verdict.extra) return { status: 'inconclusive', summary: `Every field sent came back equal, but the store added ${verdict.extra} field(s): ${data.extraKeys.join(', ')}; the document was ${cleanup}.`, data };
    return { status: 'pass', summary: `The body of ${Object.keys(body).length} fields came back equal from a server read (${timing}); the document was ${cleanup}.`, data };
  },
};

// ---- caps.db-rules

// [verdict, why] for one rules case: 'as stated', 'wrong', or 'unclear' (no answer, or a transient code).
function judge(expect, set, readBack) {
  const code = set.ok || set.timedOut ? null : codeOf(set.error);
  const unclear = set.timedOut ? 'set() gave no answer in 6 s' : TRANSIENT.has(code) ? `set() rejected with the transient code ${code}` : null;
  if (expect === 'ok') {
    if (set.ok) return readBack === true ? ['as stated', 'written and read back'] : ['unclear', 'set() resolved but the read-back did not show the body'];
    return unclear ? ['unclear', unclear] : ['wrong', `set() rejected with ${code ?? 'no code'}`];
  }
  if (set.ok) return ['wrong', "set() resolved: the write into another viewer's subtree was accepted"];
  if (code === expect) return ['as stated', `set() rejected with ${code}`];
  return unclear ? ['unclear', unclear] : ['wrong', `set() rejected with ${code ?? 'no code'}, not ${expect}`];
}

const rulesCheck = {
  id: 'caps.db-rules',
  title: 'db access rules, as the owner',
  kind: 'auto',
  what: "As the owner, writes the own data/users subtree, another viewer's subtree, board/<own id>, meta/s1-probe and the declared canary s1canary/{self} (own id and another id), records each outcome and error code, and deletes what was written.",
  async run(ctx) {
    const t0 = ctx.now();
    const db = await ctx.claude('db');
    if (!db) return { status: 'skipped', summary: "claude.use('db') resolved null, so this view has no db.", data: { namespace: false } };
    const user = await ctx.claude('user');
    if (!user) return { status: 'skipped', summary: "claude.use('user') resolved null, so the viewer's id is unknown.", data: { namespace: false, of: 'user' } };
    const idO = await attempt(() => user.id(), CALL_TIMEOUT_MS, ctx.now);
    const id = idO.ok ? idO.value : null;
    if (typeof id !== 'string' || !id) return { status: 'skipped', summary: 'user.id() gave no id, so the own subtree cannot be addressed.', data: { idType: idO.ok ? (id === null ? 'null' : typeof id) : 'no answer' } };
    ownId = id;
    const ownerO = await attempt(() => user.isOwner(), CALL_TIMEOUT_MS, ctx.now);
    if (!ownerO.ok || ownerO.value !== true) {
      return { status: 'skipped', summary: 'This check judges the rules as the owner, and isOwner() did not say true for this viewer.', data: { isOwner: ownerO.ok ? bool(ownerO.value) : null } };
    }

    const cases = [
      { name: 'own', path: `data/users/<own id>/s1/probe/p-${MARKER}`, expect: 'ok', build: () => db.collection(`data/users/${id}`).doc('s1').collection('probe').doc(`p-${MARKER}`) },
      { name: 'notMe', path: `data/users/${NOT_ME}/s1`, expect: 'invalid_argument', build: () => db.collection(`data/users/${NOT_ME}`).doc('s1') },
      { name: 'board', path: 'board/<own id>', expect: 'ok', build: () => db.collection('board').doc(id) },
      { name: 'meta', path: 'meta/s1-probe', expect: 'ok', build: () => db.collection('meta').doc('s1-probe') },
      { name: 'canaryOwn', path: `${CANARY}/<own id>`, expect: 'ok', build: () => db.collection(CANARY).doc(id) },
      { name: 'canaryNotMe', path: `${CANARY}/${NOT_ME}`, expect: 'invalid_argument', build: () => db.collection(CANARY).doc(NOT_ME) },
    ];
    const outcomes = {};
    for (const c of cases) {
      const o = { path: c.path, expect: c.expect };
      outcomes[c.name] = o;
      if (ctx.now() - t0 > RULES_BUDGET_MS) {
        o.verdict = 'unclear';
        o.why = 'not attempted: the check ran out of time';
        continue;
      }
      let ref;
      try {
        ref = c.build();
      } catch (e) {
        o.build = errInfo(e);
        o.verdict = 'wrong';
        o.why = 'the ref builder threw';
        continue;
      }
      const set = await dbCall(() => ref.set({ probe: 's1', case: c.name, marker: MARKER, writtenAt: new Date().toISOString() }), ctx.now);
      o.set = brief(set);
      if (set.ok) {
        const g = await dbCall(() => ref.get(), ctx.now);
        const { body } = g.ok ? snapBody(g.value) : { body: null };
        o.get = { ...brief(g), metadata: g.ok ? metaOf(g.value) : null };
        o.readBack = g.ok ? body?.marker === MARKER && body?.case === c.name : null;
      }
      if (set.ok || set.timedOut) o.delete = brief(await dbCall(() => ref.delete(), ctx.now));
      [o.verdict, o.why] = judge(c.expect, set, o.readBack);
    }

    const declared = ctx.lock?.capabilities?.db?.rules;
    const data = {
      marker: MARKER, outcomes, controlled: outcomes.own.verdict === 'as stated',
      declaredRules: Array.isArray(declared) ? jsonCopy(declared, 2000) : 'lock.json lists no declaration',
      canaryDeclared: Array.isArray(declared) && declared.some(r => r?.path === `${CANARY}/{self}`),
      notMeasured: 'Levels below owner (root and meta writes refused, board/{self} for others) need a second participant; the emulator tests them (PLAN.md 7.3).',
    };
    const list = Object.values(outcomes);
    const leftovers = list.filter(o => o.delete && !o.delete.ok).map(o => o.path);
    if (leftovers.length) data.notDeleted = leftovers;
    const tail = `${leftovers.length ? ` Not deleted: ${leftovers.join(', ')}.` : ''} Levels below owner need a second participant and stay with the emulator.`;
    const line = cases.map(c => `${c.name} ${outcomes[c.name].why}`).join('; ');
    const canary = outcomes.canaryNotMe;
    const others = list.filter(o => o !== canary);
    if (others.some(o => o.verdict === 'wrong')) return { status: 'fail', summary: `Not as stated: ${line}.${tail}`, data };
    if (list.some(o => o.verdict === 'unclear')) return { status: 'inconclusive', summary: `Could not tell: ${line}.${tail}`, data };
    if (canary.verdict === 'wrong') {
      return {
        status: 'inconclusive',
        summary: `The owner's write to ${CANARY}/${NOT_ME} was accepted, so the declared canary rule ${CANARY}/{self} did not apply, and as the owner the other outcomes equal the platform's defaults: whether the declared rule set is in effect is not shown (${data.canaryDeclared ? 'lock.json says the canary was declared' : 'lock.json does not list the canary'}). ${line}.${tail}`,
        data,
      };
    }
    return { status: 'pass', summary: `All six as stated, and the canary shows the declared rule set is in effect: ${line}.${tail}`, data };
  },
};

// ---- caps.meta-release: the watch starts in resume(), before any check runs

const watch = {
  started: false, how: null, startedAt: null, deliveries: [], dropped: 0, error: null, dead: false,
  unsubscribe: null, closed: false, listeners: new Set(), signalSeenAt: null, noDb: false,
  subscriptions: 0, resubscribes: [], db: null, log: null, retryTimer: 0,
};
const MAX_DELIVERIES = 500;
const notifyWatch = () => { for (const f of [...watch.listeners]) f(); };

function closeWatch() {
  clearTimeout(watch.retryTimer);
  if (watch.unsubscribe && !watch.closed) {
    watch.closed = true;
    try {
      watch.unsubscribe();
    } catch (e) {
      watch.log?.(`unsubscribing from ${RELEASE_DOC} threw: ${errInfo(e).message}`);
    }
  }
}

function subscribeWatch() {
  const { db, log } = watch;
  const sub = watch.subscriptions++;
  let ref;
  try {
    ref = db.doc(RELEASE_DOC);
  } catch (e) {
    watch.error = errInfo(e);
    watch.dead = true;
    log(`could not build ${RELEASE_DOC}: ${watch.error.message}`);
    notifyWatch();
    return;
  }
  const next = snap => {
    const { body, error } = snapBody(snap);
    const rec = {
      sub,
      at: Date.now(),
      sincePageMs: Date.now() - MODULE_START,
      exists: snap?.exists === true,
      release: short(body?.release),
      docAt: short(body?.at),
      fromCache: bool(snap?.metadata?.fromCache),
      pending: bool(snap?.metadata?.hasPendingWrites),
    };
    if (error) rec.dataError = error;
    if (watch.deliveries.length < MAX_DELIVERIES) watch.deliveries.push(rec);
    else watch.dropped += 1;
    log(`${RELEASE_DOC} delivery: ${rec.exists ? `release ${String(rec.release)}` : 'no document'}${rec.fromCache ? ', from cache' : ''}`);
    notifyWatch();
  };
  const fail = e => {
    const info = errInfo(e);
    watch.error = info;
    log(`the ${RELEASE_DOC} watch stopped: ${info.code ?? 'no code'}`);
    // db.d.ts: a dead bridge ends a listener with 'unavailable', and a fresh onSnapshot is the only recovery.
    if (info.code === 'unavailable' && watch.resubscribes.length < RESUBSCRIBES && !watch.closed) {
      watch.resubscribes.push({ code: info.code, sincePageMs: Date.now() - MODULE_START });
      log(`subscribing to ${RELEASE_DOC} again in ${RESUBSCRIBE_GAP_MS / 1000} s`);
      watch.retryTimer = setTimeout(() => { if (!watch.closed) subscribeWatch(); }, RESUBSCRIBE_GAP_MS);
      return;
    }
    watch.dead = true;
    notifyWatch();
  };
  try {
    watch.unsubscribe = ref.onSnapshot(next, fail);
    log(`watching ${RELEASE_DOC} (${watch.how}${sub ? `, subscription ${sub + 1}` : ''})`);
  } catch (e) {
    fail(e);
  }
}

function startWatch(db, how, log) {
  if (watch.started) return;
  Object.assign(watch, { started: true, how, startedAt: Date.now(), db, log });
  subscribeWatch();
}

// The first s1-v2 delivery shown to be written while this page was open, or null. No clock is compared.
function findFresh() {
  let sawOther = false;
  let firstKey;
  const list = watch.deliveries;
  for (let i = 0; i < list.length; i++) {
    const d = list[i];
    if (d.fromCache !== false) continue; // a cached view could hold any earlier value
    if (d.release !== RELEASE_TARGET) {
      sawOther = true;
      continue;
    }
    const key = String(d.docAt);
    if (i > 0 && sawOther) return { delivery: d, index: i, why: 'it followed a server delivery of another value while the page was open' };
    if (firstKey === undefined) firstKey = key;
    else if (key !== firstKey) return { delivery: d, index: i, why: `its at differs from the ${RELEASE_TARGET} value that was there when this page loaded` };
  }
  return null;
}

function waitFresh(deadline) {
  return new Promise(resolve => {
    let timer = 0;
    const done = f => {
      clearTimeout(timer);
      watch.listeners.delete(probe);
      resolve(f);
    };
    const probe = () => {
      const f = findFresh();
      if (f || watch.dead) done(f);
    };
    timer = setTimeout(() => done(findFresh()), Math.max(0, deadline - Date.now()));
    watch.listeners.add(probe);
    probe();
  });
}

const releaseCheck = {
  id: 'caps.meta-release',
  title: 'A db change reaches the open page after a republish',
  kind: 'republish',
  timeoutMs: RELEASE_TIMEOUT_MS,
  what: `Watches ${RELEASE_DOC} from page start and, after the republish signal, waits up to 90 s from the signal for a delivery saying ${RELEASE_TARGET} that is shown, without comparing clocks, to have been written while this page was open.`,
  async run(ctx) {
    const signal = ctx.republished && typeof ctx.republished.then === 'function' ? await ctx.republished : null;
    if (!watch.signalSeenAt) watch.signalSeenAt = Date.now();
    if (!watch.started) {
      const db = await ctx.claude('db');
      if (!db) return { status: 'skipped', summary: "claude.use('db') resolved null, so nothing could watch meta/release.", data: { namespace: false } };
      startWatch(db, 'late, from the check (resume did not start it)', ctx.log);
    }
    const deadline = watch.signalSeenAt + RELEASE_WAIT_MS;
    const fresh = await waitFresh(deadline);
    closeWatch();
    const list = watch.deliveries;
    const data = {
      watch: { how: watch.how, startedSincePageMs: watch.startedAt ? watch.startedAt - MODULE_START : null, error: watch.error, dead: watch.dead, subscriptions: watch.subscriptions, resubscribes: watch.resubscribes },
      signal: signal ? { source: short(signal.source), at: short(signal.at), to: short(signal.to) } : null,
      signalSeenSincePageMs: watch.signalSeenAt - MODULE_START,
      deadline: { waitFromSignalMs: RELEASE_WAIT_MS, harnessLimitMs: RELEASE_TIMEOUT_MS, waitedUntilSincePageMs: deadline - MODULE_START },
      deliveryCount: list.length + watch.dropped,
      deliveries: list.length > 25 ? [...list.slice(0, 5), ...list.slice(-20)] : list,
      pageStart: new Date(MODULE_START).toISOString(),
      clocks: 'Delivery times are the phone clock; the signal at and the document at come from the machine that wrote them. The verdict compares no clocks.',
    };
    if (!fresh) {
      const stale = list.some(d => d.release === RELEASE_TARGET);
      data.stale = stale;
      if (watch.dead) return { status: 'inconclusive', summary: `The ${RELEASE_DOC} watch stopped with ${watch.error?.code ?? 'no code'}${watch.resubscribes.length ? ` after ${watch.resubscribes.length} new subscriptions` : ''} before a fresh ${RELEASE_TARGET} arrived, so the delivery was not measured.`, data };
      if (stale && !list.some(d => d.release === RELEASE_TARGET && d.fromCache === false)) {
        return { status: 'inconclusive', summary: `${RELEASE_DOC} said ${RELEASE_TARGET} only in deliveries that were not server-definitive (from a cache), so when it was written is not shown.`, data };
      }
      if (stale) return { status: 'inconclusive', summary: `${RELEASE_DOC} said ${RELEASE_TARGET} already when this page loaded, and no later write arrived, so the delivery of the change cannot be timed.`, data };
      return { status: 'fail', summary: `No delivery of ${RELEASE_DOC} saying ${RELEASE_TARGET} arrived within 90 s of the republish signal (${list.length} ${list.length === 1 ? 'delivery' : 'deliveries'} seen).`, data };
    }
    const d = fresh.delivery;
    const signalAt = parseAt(signal?.at);
    const docAt = parseAt(d.docAt);
    data.fresh = { ...d, why: fresh.why, index: fresh.index, wasFirstDelivery: fresh.index === 0 };
    // Same clock (Claude writes meta/release, then the signal): the gap between the two writes.
    data.writeGapMs = signalAt === null || docAt === null ? null : signalAt - docAt;
    data.corroborated = data.writeGapMs === null ? null : data.writeGapMs >= 0 && data.writeGapMs <= 600_000;
    data.latencyFromSignalAtMs = signalAt === null ? null : d.at - signalAt;
    data.latencyFromDocAtMs = docAt === null ? null : d.at - docAt;
    data.deliveredBeforeSignalSeen = d.at <= watch.signalSeenAt;
    data.msFromSignalSeen = d.at - watch.signalSeenAt;
    const L = data.latencyFromDocAtMs ?? (signal?.source === 'db' ? data.latencyFromSignalAtMs : null);
    data.looked = L === null ? 'unknown' : L >= 0 && L <= 10_000 ? 'realtime' : L >= 15_000 && L <= 60_000 ? 'periodic fallback' : 'unclear';
    data.lookedRule = 'realtime when the write-to-delivery time is 0 s to 10 s, periodic fallback when 15 s to 60 s, otherwise unclear; this compares the phone clock with the writer\'s, so it is a hint, not the verdict [our choice]';
    const sec = ms => (Math.abs(ms) / 1000).toFixed(1);
    const L0 = data.latencyFromSignalAtMs;
    const lat = L0 === null ? 'the signal had no readable time' : `${sec(L0)} s ${L0 < 0 ? 'before' : 'after'} the ops/s1-republished time`;
    const gap = data.corroborated === false ? ` Its at is ${sec(data.writeGapMs)} s ${data.writeGapMs < 0 ? 'after' : 'before'} the signal's at, which is unexpected.` : '';
    return { status: 'pass', summary: `${RELEASE_DOC} said ${RELEASE_TARGET} on this open page (${fresh.why}), ${lat} (${signal?.source ?? 'unknown'} signal); it looked ${data.looked}.${gap}`, data };
  },
};

// ---- sample checks (each runs on a tap)

// One sample() call, counted, so the consent check can tell whether it was the first of this page.
function callSample(sample, prompt, options) {
  sampleCalls += 1;
  return sample(prompt, options);
}

async function sampleState(ctx) {
  const permissions = await ctx.claude('permissions');
  if (!permissions || typeof permissions.state !== 'function') return '(no permissions namespace)';
  const o = await attempt(() => permissions.state('sample'), CALL_TIMEOUT_MS, ctx.now);
  return o.ok ? short(o.value) : o.timedOut ? '(no answer in 6 s)' : `(rejected ${errInfo(o.error).code ?? 'no code'})`;
}

const consentCheck = {
  id: 'caps.sample-consent',
  title: 'Asking Claude, with consent',
  kind: 'consent',
  what: "Reads permissions.state('sample'), makes the view's first sample() call on the quick tier, which shows the consent dialog, then reads the state again; it passes when the state went from prompt to granted and the call resolved.",
  async run(ctx) {
    const { sample, skip } = await getSample(ctx);
    if (skip) return skip;
    const pre = show(ctx, 'Reply', 'Waiting for Claude, and for your consent if it asks.');
    const stateBefore = await sampleState(ctx);
    const callsBefore = sampleCalls;
    const t0 = ctx.now();
    try {
      const r = await callSample(sample, 'Reply with the single word: ready', { modelTier: 'quick', cache: false });
      const ms = r0(ctx.now() - t0);
      const text = typeof r?.text === 'string' ? r.text : '';
      if (pre) pre.textContent = text;
      const stateAfter = await sampleState(ctx);
      const data = {
        ms, msMayIncludeConsentDialog: true, stateBefore, stateAfter, sampleCallsBefore: callsBefore,
        saidReady: /\bready\b/i.test(text), chars: text.length, truncated: bool(r?.truncated), modelTierApplied: short(r?.modelTierApplied),
      };
      if (stateBefore === 'prompt' && stateAfter === 'granted' && callsBefore === 0) {
        return { status: 'pass', summary: `sample() resolved in ${ms} ms, including the consent dialog: the state went from prompt to granted, and the reply ${data.saidReady ? 'said' : 'did not say'} the word asked for.`, data };
      }
      const why = callsBefore > 0 ? `${callsBefore} sample call${callsBefore === 1 ? '' : 's'} came first on this page`
        : `the state was ${stateBefore} before the call and ${stateAfter} after it`;
      return { status: 'inconclusive', summary: `sample() resolved in ${ms} ms, but the consent path was not shown: ${why}.`, data };
    } catch (e) {
      const ms = r0(ctx.now() - t0);
      if (pre) pre.textContent = `No reply: ${errInfo(e).code ?? 'no code'}.`;
      const out = sampleFailure(e, ms, 'sample()');
      Object.assign(out.data, { stateBefore, stateAfter: await sampleState(ctx), sampleCallsBefore: callsBefore });
      return out;
    }
  },
};

const limitsCheck = {
  id: 'caps.sample-limits',
  title: 'The sample limits of this view',
  kind: 'auto',
  what: 'Reads sample.limits(), which spends nothing and never prompts, and records the prompt byte cap and whether images and tools are offered.',
  async run(ctx) {
    const { sample, skip } = await getSample(ctx);
    if (skip) return skip;
    if (typeof sample.limits !== 'function') return { status: 'skipped', summary: 'sample.limits is not defined on this runtime.', data: { limits: 'not defined' } };
    const o = await attempt(() => sample.limits(), CALL_TIMEOUT_MS, ctx.now);
    if (!o.ok) {
      const error = o.timedOut ? 'no answer in 6 s' : errInfo(o.error);
      return { status: 'info', summary: `sample.limits() ${o.timedOut ? 'gave no answer in 6 s' : `rejected with ${error.code ?? 'no code'}`}.`, data: { ms: o.ms, error } };
    }
    const l = o.value && typeof o.value === 'object' ? o.value : {};
    const limits = jsonCopy(l, 4000);
    return {
      status: 'info',
      summary: `sample.limits(): ${short(l.maxPromptBytes)} prompt bytes, images ${l.images ? 'offered' : 'not offered'}, tools ${l.tools ? `offered (at most ${short(l.tools.maxCount)})` : 'not offered'}.`,
      data: { ms: o.ms, limits, keys: Object.keys(l).slice(0, 20) },
    };
  },
};

const streamingCheck = {
  id: 'caps.sample-streaming',
  title: 'Streaming through onText',
  kind: 'consent',
  what: 'Asks for about 120 words on the default tier with onText and records each delivery, the time to the first, and how many arrived before the call resolved.',
  async run(ctx) {
    const { sample, skip } = await getSample(ctx);
    if (skip) return skip;
    const pre = show(ctx, 'Reply, as it streams', 'Thinking...');
    const timeline = [];
    let count = 0;
    let afterSettle = 0;
    let broken = 0;
    let prev = '';
    let settled = false;
    let firstMs = null;
    const t0 = ctx.now();
    const onText = update => {
      const t = r0(ctx.now() - t0);
      const text = typeof update?.text === 'string' ? update.text : '';
      const delta = typeof update?.delta === 'string' ? update.delta : null;
      if (settled) afterSettle += 1;
      else count += 1;
      if (firstMs === null) firstMs = t;
      if (delta === null || text !== prev + delta) broken += 1;
      prev = text;
      if (timeline.length < 80) timeline.push([t, delta === null ? -1 : delta.length]);
      if (pre) pre.textContent = text;
    };
    let r;
    try {
      r = await callSample(sample, 'In about 120 words, explain why rain smells. Plain prose, one paragraph.', { modelTier: 'default', cache: false, onText });
    } catch (e) {
      settled = true;
      const out = sampleFailure(e, r0(ctx.now() - t0), 'The streaming call');
      Object.assign(out.data, { deliveriesBeforeSettle: count, firstDeltaMs: firstMs, timeline });
      return out;
    }
    settled = true;
    const ms = r0(ctx.now() - t0);
    const text = typeof r?.text === 'string' ? r.text : '';
    if (pre) pre.textContent = text;
    // A late call after the resolve would break the contract: wait one beat so it can be counted.
    await sleep(500);
    const data = {
      modelTier: 'default', modelTierApplied: short(r?.modelTierApplied), truncated: bool(r?.truncated),
      deliveriesBeforeResolve: count, deliveriesAfterResolve: afterSettle, firstDeltaMs: firstMs, resolveMs: ms,
      textEqualsDeltasSoFar: broken === 0, lastTextEqualsResult: prev === text,
      chars: text.length, words: text.trim() ? text.trim().split(/\s+/).length : 0, timeline,
    };
    const broke = [
      afterSettle !== 0 && `onText fired ${afterSettle} time${afterSettle === 1 ? '' : 's'} after the call resolved (deliveriesAfterResolve)`,
      broken !== 0 && `text was not the previous text plus delta ${broken} time${broken === 1 ? '' : 's'} (textEqualsDeltasSoFar)`,
      prev !== text && "the last onText text differs from the result's text (lastTextEqualsResult)",
    ].filter(Boolean);
    if (broke.length) return { status: 'fail', summary: `onText broke its guarantees: ${broke.join('; ')}.`, data };
    if (count >= 2) return { status: 'pass', summary: `onText fired ${count} times before the call resolved, the first after ${firstMs} ms, each text the previous plus its delta and the last equal to the result; the whole answer took ${ms} ms.`, data };
    return { status: 'fail', summary: `onText fired ${count} time${count === 1 ? '' : 's'} before the call resolved, so the answer did not stream (it took ${ms} ms).`, data };
  },
};

const tiersCheck = {
  id: 'caps.sample-tiers',
  title: 'The three model tiers',
  kind: 'consent',
  what: 'Makes one short call on each of quick, default and complex and records whether each answered, the tier that answered, and the time.',
  async run(ctx) {
    const { sample, skip } = await getSample(ctx);
    if (skip) return skip;
    const pre = show(ctx, 'Replies', '');
    const tiers = {};
    const shown = {}; // the replies, for the screen only
    for (const tier of TIERS) {
      const t0 = ctx.now();
      try {
        const r = await callSample(sample, 'Reply with the single word: ok', { modelTier: tier, cache: false });
        const text = typeof r?.text === 'string' ? r.text : '';
        shown[tier] = clip(text.trim(), 40);
        tiers[tier] = { ok: true, ms: r0(ctx.now() - t0), applied: short(r?.modelTierApplied), truncated: bool(r?.truncated), saidOk: /\bok\b/i.test(text), chars: text.length };
      } catch (e) {
        tiers[tier] = { ok: false, ms: r0(ctx.now() - t0), error: errInfo(e) };
      }
      if (pre) pre.textContent = TIERS.filter(t => tiers[t]).map(t => `${t}: ${tiers[t].ok ? `${shown[t]} (${tiers[t].applied}, ${tiers[t].ms} ms)` : `rejected ${tiers[t].error.code}`}`).join('\n');
    }
    const answered = TIERS.filter(t => tiers[t].ok);
    const refused = TIERS.filter(t => !tiers[t].ok);
    const substituted = answered.filter(t => tiers[t].applied !== t);
    const data = { tiers, answered, refused, substituted };
    const line = TIERS.map(t => `${t} ${tiers[t].ok ? `${tiers[t].ms} ms${tiers[t].applied !== t ? ` (answered by ${tiers[t].applied})` : ''}` : `refused ${tiers[t].error.code ?? 'no code'}`}`).join(', ');
    if (!answered.length) return { status: 'fail', summary: `No tier answered: ${line}.`, data };
    if (refused.length || substituted.length) return { status: 'info', summary: `Not every tier answered as asked: ${line}.`, data };
    return { status: 'pass', summary: `All three tiers answered as asked: ${line}.`, data };
  },
};

const abortCheck = {
  id: 'caps.sample-abort',
  title: 'Stopping a call with an AbortSignal',
  kind: 'consent',
  what: 'Asks for 400 words with onText, aborts at the first delta, and records whether the call rejected with cancelled, how promptly, and whether onText stopped. There is no page-side timer (sample.d.ts).',
  async run(ctx) {
    const { sample, skip } = await getSample(ctx);
    if (skip) return skip;
    const pre = show(ctx, 'Reply, until the stop', 'Thinking...');
    const ctl = new AbortController();
    const t0 = ctx.now();
    let abortedAt = null;
    let reason = null;
    let before = 0;
    let after = 0;
    const stop = why => {
      if (ctl.signal.aborted) return;
      reason = why;
      abortedAt = r0(ctx.now() - t0);
      ctl.abort();
    };
    try {
      const r = await callSample(sample, 'Write about 400 words on the history of the umbrella.', {
        modelTier: 'quick',
        cache: false,
        signal: ctl.signal,
        onText: update => {
          if (ctl.signal.aborted) after += 1;
          else before += 1;
          if (pre) pre.textContent = typeof update?.text === 'string' ? update.text : '';
          stop('first delta');
        },
      });
      const ms = r0(ctx.now() - t0);
      const data = { ms, abortedAt, reason, deltasBeforeAbort: before, deltasAfterAbort: after, chars: typeof r?.text === 'string' ? r.text.length : null };
      if (abortedAt === null) return { status: 'inconclusive', summary: `The call resolved after ${ms} ms with no onText delivery, so nothing was stopped mid-stream.`, data };
      return { status: 'fail', summary: `The call resolved after ${ms} ms although it was aborted at ${abortedAt} ms.`, data };
    } catch (e) {
      const ms = r0(ctx.now() - t0);
      const error = errInfo(e);
      // onText must not fire after the abort: wait one beat so a late call can be counted.
      await sleep(500);
      const data = { ms, abortedAt, reason, rejectAfterAbortMs: abortedAt === null ? null : ms - abortedAt, deltasBeforeAbort: before, deltasAfterAbort: after, partialChars: textLen(e), error };
      if (error.code === 'cancelled' && reason === 'first delta' && before >= 1 && after === 0) {
        return { status: 'pass', summary: `Aborted at the first delta (${abortedAt} ms); the call rejected cancelled ${data.rejectAfterAbortMs} ms later and onText did not fire again.`, data };
      }
      if (error.code === 'cancelled' && after > 0) {
        return { status: 'fail', summary: `The call rejected cancelled, but onText fired ${after} time${after === 1 ? '' : 's'} after the abort.`, data };
      }
      if (error.code === 'cancelled' && abortedAt === null) {
        return { status: 'fail', summary: 'The call rejected cancelled although this page never aborted it.', data };
      }
      return { status: 'fail', summary: `The call rejected with ${error.code ?? 'no code'}${abortedAt === null ? ' before any abort' : ` after the abort at ${abortedAt} ms`}, not with cancelled after the abort.`, data };
    }
  },
};

const toolsCheck = {
  id: 'caps.sample-tools',
  title: 'Page tools in a sample call',
  kind: 'consent',
  what: `Offers one page tool that returns ${PROBE_VALUE} and asks Claude to call it, and records whether execute ran and whether the reply carries the value.`,
  async run(ctx) {
    const { sample, skip } = await getSample(ctx);
    if (skip) return skip;
    let limitsTools = 'limits not defined';
    if (typeof sample.limits === 'function') {
      const l = await attempt(() => sample.limits(), CALL_TIMEOUT_MS, ctx.now);
      limitsTools = l.ok ? (l.value?.tools ? { maxCount: short(l.value.tools.maxCount) } : null) : l.timedOut ? 'no answer in 6 s' : { rejected: errInfo(l.error) };
    }
    const pre = show(ctx, 'Reply', 'Thinking...');
    const t0 = ctx.now();
    let calls = 0;
    let firstCallMs = null;
    const inputs = [];
    const tools = [{
      name: 'read_probe_value',
      description: 'Returns the probe value the user needs.',
      inputSchema: { type: 'object', properties: {} },
      execute: async input => {
        calls += 1;
        if (firstCallMs === null) firstCallMs = r0(ctx.now() - t0);
        if (inputs.length < 5) inputs.push({ type: input === null ? 'null' : typeof input, keys: input && typeof input === 'object' ? Object.keys(input).length : null });
        if (pre) pre.textContent = `The page tool ran (${calls}).`;
        return { value: PROBE_VALUE };
      },
    }];
    try {
      const r = await callSample(sample, 'Call the read_probe_value tool and reply with the value it returns, digits only.', { modelTier: 'quick', tools });
      const ms = r0(ctx.now() - t0);
      const text = typeof r?.text === 'string' ? r.text : '';
      if (pre) pre.textContent = text;
      const hasValue = text.includes(PROBE_VALUE);
      const data = { ms, executeRan: calls > 0, executeCalls: calls, firstCallMs, inputs, chars: text.length, hasValue, truncated: bool(r?.truncated), modelTierApplied: short(r?.modelTierApplied), limitsTools };
      if (calls > 0 && hasValue) return { status: 'pass', summary: `execute ran ${calls} time${calls === 1 ? '' : 's'} and the reply carries ${PROBE_VALUE} (${ms} ms).`, data };
      return { status: 'fail', summary: `execute ${calls > 0 ? `ran ${calls} time${calls === 1 ? '' : 's'}` : 'never ran'} and the reply ${hasValue ? 'carries' : 'does not carry'} ${PROBE_VALUE}.`, data };
    } catch (e) {
      const out = sampleFailure(e, r0(ctx.now() - t0), 'The tools call');
      Object.assign(out.data, { executeRan: calls > 0, executeCalls: calls, limitsTools });
      if (pre) pre.textContent = `No reply: ${out.data.error.code ?? 'no code'}.`;
      return out;
    }
  },
};

// ---- resume: start the meta/release watch before any check runs

async function resume(ctx) {
  if (ctx.republished && typeof ctx.republished.then === 'function') {
    ctx.republished.then(() => { if (!watch.signalSeenAt) watch.signalSeenAt = Date.now(); });
  }
  const db = await ctx.claude('db');
  if (db) startWatch(db, 'from resume, before the checks', ctx.log);
  else {
    watch.noDb = true;
    ctx.log(`db is null, so ${RELEASE_DOC} is not watched`);
  }
  return {};
}

export default {
  id: 'caps',
  title: 'Capabilities: user, permissions, db and sample',
  checks: [userCheck, permissionsCheck, roundtripCheck, rulesCheck, releaseCheck, consentCheck, limitsCheck, streamingCheck, tiersCheck, abortCheck, toolsCheck],
  resume,
};
