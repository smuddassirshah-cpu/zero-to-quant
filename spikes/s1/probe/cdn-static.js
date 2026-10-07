// Spike S1 probe: a module with static bare imports, all resolved through the page's import map.
// Decision notes:
// - Two signal bindings are measured apart: a component that reads count.value (re-rendered through
//   Preact's queue) and a signal passed straight as a text child (patched in place, decision 2's pattern).
//   Both depend on @preact/signals hooking the same preact instance the page resolved, so a second
//   copy of preact behind the map would show here as a missed update.
// - zod/mini is checked on one valid and one invalid object, comparing the exact issue code and path.
// - Where each bare specifier went is read with this module's own import.meta.resolve(), so the caller can
//   compare it with the locked URL: a module that runs is not proof that it is the locked one.

import { h, render } from 'preact';
import { useState } from 'preact/hooks';
import { signal } from '@preact/signals';
import * as z from 'zod/mini';

const errText = (e) => {
  if (e == null) return String(e);
  const s = typeof e === 'object' && 'message' in e ? `${e.name || 'Error'}: ${e.message}` : String(e);
  return s.slice(0, 300);
};
const r1 = (v) => Math.round(v * 10) / 10;

// Polls until test() holds or ms pass: a few microtask turns first, then 10 ms timer steps.
async function waitFor(test, ms, now) {
  const end = now() + ms;
  for (let i = 0; i < 6; i++) {
    if (test()) return true;
    await Promise.resolve();
  }
  while (now() < end) {
    if (test()) return true;
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
  return test();
}

// { supported, url } per specifier from this module's resolution, or { supported, url: null, error }.
function resolveAll(specifiers) {
  const out = {};
  for (const spec of specifiers) {
    if (typeof import.meta.resolve !== 'function') out[spec] = { supported: false, url: null };
    else {
      try {
        out[spec] = { supported: true, url: import.meta.resolve(spec) };
      } catch (e) {
        out[spec] = { supported: true, url: null, error: errText(e) };
      }
    }
  }
  return out;
}

export async function run(mount, now = () => performance.now(), specifiers = []) {
  const phases = {};
  const out = { ok: false, phases, render: null, update: null, zod: null, error: null, phase: null, resolved: resolveAll(specifiers) };
  const host = document.createElement('div');
  mount.appendChild(host);
  const count = signal(1);
  const text = (k) => host.querySelector(`[data-k="${k}"]`)?.textContent ?? null;

  function Counter() {
    const [label] = useState('component');
    return h('span', { 'data-k': 'comp' }, `${label} ${count.value}`);
  }
  function Bound() {
    return h('span', { 'data-k': 'bound' }, count);
  }

  try {
    out.phase = 'render';
    let t = now();
    render(h('div', null, h(Counter, null), ' ', h(Bound, null)), host);
    phases.renderMs = r1(now() - t);
    out.render = { comp: text('comp'), bound: text('bound') };
    const renderOk = out.render.comp === 'component 1' && out.render.bound === '1';

    out.phase = 'update';
    t = now();
    count.value = 2;
    const compOk = await waitFor(() => text('comp') === 'component 2', 2000, now);
    const compMs = r1(now() - t);
    const boundOk = await waitFor(() => text('bound') === '2', 2000, now);
    phases.updateMs = r1(now() - t);
    out.update = { comp: text('comp'), bound: text('bound'), compOk, boundOk, compMs };

    out.phase = 'zod';
    t = now();
    const schema = z.object({ a: z.number(), b: z.string() });
    const good = z.safeParse(schema, { a: 1, b: 'x' });
    const bad = z.safeParse(schema, { a: '1', b: 'x' });
    phases.zodMs = r1(now() - t);
    const issue = bad.success ? null : (bad.error?.issues?.[0] ?? null);
    out.zod = {
      validSuccess: good.success,
      validData: good.success ? { a: good.data.a, b: good.data.b } : null,
      invalidSuccess: bad.success,
      invalidCode: issue?.code ?? null,
      invalidPath: Array.isArray(issue?.path) ? issue.path.map(String) : null,
    };
    const zodOk = good.success === true && good.data?.a === 1 && good.data?.b === 'x'
      && bad.success === false && out.zod.invalidCode === 'invalid_type' && out.zod.invalidPath?.[0] === 'a';

    out.phase = 'done';
    out.ok = renderOk && compOk && boundOk && zodOk;
    out.parts = { renderOk, compOk, boundOk, zodOk };
  } catch (e) {
    out.error = errText(e);
  } finally {
    try {
      render(null, host);
    } catch (e) {
      out.cleanupError = errText(e);
    }
    host.remove();
  }
  return out;
}
