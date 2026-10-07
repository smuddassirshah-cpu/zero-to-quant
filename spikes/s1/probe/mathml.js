// Spike S1 MathML checks: KaTeX 0.19.0 from the CDN through the import map, native MathML layout, the
// 40-formula specimen sheet and the TexSlots sentinel binding of docs/PLAN.md conflict 10.
//
// Decision notes:
// - KaTeX renders with katex.render, which builds MathML nodes with createElementNS: no HTML sink here.
// - mathml.katex measures the import map alone. The other checks take KaTeX through the map, or by its
//   full locked URL when the map failed, so a map failure cannot hide the MathML verdict; each records
//   which path it used in data.via.
// - Layout is judged from bounding boxes, never from feature detection: a numerator's centre at least a
//   quarter em above the denominator's, horizontally centred over it, and a superscript's centre at least
//   a tenth em above its base's. Without native layout the boxes sit side by side on one baseline, so
//   neither margin can be met. Zero-sized boxes give inconclusive, not fail.
// - Formulas render at 1.21em, the size KaTeX's own CSS gives .katex, so the sheet and the web app's
//   screenshot compare at one size. No maths font is set: the browser's MathML default is under test.
// - The TexSlots binding swaps each sentinel <mtext> for an <mn> and also rewrites KaTeX's TeX
//   <annotation>, which repeats the sentinels; the auto check passes only when no sentinel text is left
//   anywhere in the tree. A second copy keeps the digits in <mtext>, for comparison (PLAN.md stage 2).
//   Rewriting the annotation goes beyond the binding ARCHITECTURE.md 5.11 and PLAN.md conflict 10 describe
//   (they swap the <mtext> only): a deviation for the stage report, not settled here.
// - The binding's self-test drives the real slider (value 5, an input event) and expects the literal digits
//   5 and 0.9527: P(X <= 5) for Bin(10, 3/10) is 0.95265101... [verified in Node with exact arithmetic].
// - Left clipping is measured on the formula's content (its descendants' boxes), not on the <math> box,
//   which for display maths is as wide as its container whatever the content does.
// - P(X <= k) for X ~ Bin(10, 0.3) is exact rational arithmetic in BigInt, rounded half up to 4 places;
//   O(n) terms, no floating point.

import { SPECIMEN, INLINE_BEFORE, INLINE_AFTER } from './specimen.js';

const MATHML_NS = 'http://www.w3.org/1998/Math/MathML';
const KATEX_VERSION = '0.19.0';
const KATEX_URL = 'https://cdn.jsdelivr.net/npm/katex@0.19.0/dist/katex.mjs';
const FORMULA_SIZE = '1.21em';
const SLOT_TEX = String.raw`P(X \le \text{ZQSLOTk}) = \text{ZQSLOTp}`;
const SENTINEL = { k: 'ZQSLOTk', p: 'ZQSLOTp' };
const SENTINEL_STEM = 'ZQSLOT';
const BIN_N = 10;
const BIN_P = [3n, 10n]; // p = 3/10 as numerator and denominator
const K_START = 3;
const SPECIMEN_CHOICES = ['All readable and correct', 'Some formulas are wrong or ugly', 'Not usable'];
const FONT_CHOICES = ['They match', 'They look different'];
const MTEXT_CHOICES = ['They look different', 'They look the same'];
const VOICEOVER_CHOICES = ['Reads the current values', 'Reads something else', 'Did not test'];
const SHOT_CHOICES = ['Screenshots sent', 'Not sent'];
const SELF_TEST = { k: '5', p: '0.9527' };
const HTMLDATA_TEX = String.raw`a+\htmlData{term=b}{b^2}`;

// ---- helpers

function errText(e) {
  if (e instanceof Error) return `${e.name}: ${e.message}`;
  return String(e);
}

const clip = (s, n) => (s.length > n ? `${s.slice(0, n)}...` : s);
const round1 = v => Math.round(v * 10) / 10;
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

function el(tag, props = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (v == null) continue;
    if (k === 'text') n.textContent = v;
    else if (k === 'style') Object.assign(n.style, v); // CSSOM, which the page's CSP allows
    else if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, String(v));
  }
  for (const kid of kids) if (kid != null) n.append(kid);
  return n;
}

function box(node) {
  const r = node.getBoundingClientRect();
  return { top: round1(r.top), bottom: round1(r.bottom), left: round1(r.left), right: round1(r.right), w: round1(r.width), h: round1(r.height) };
}

const centreY = b => (b.top + b.bottom) / 2;
const centreX = b => (b.left + b.right) / 2;
const hasArea = b => b.w > 0 && b.h > 0;

// Two frames for layout and paint, capped at 250 ms because frames stop in a hidden page.
function settled() {
  return new Promise(resolve => {
    let done = false;
    const finish = () => { if (!done) { done = true; resolve(); } };
    requestAnimationFrame(() => requestAnimationFrame(finish));
    setTimeout(finish, 250);
  });
}

async function fontsSettled() {
  if (document.fonts?.ready) await Promise.race([document.fonts.ready, sleep(2000)]);
  await settled();
}

function fontOf(node) {
  if (!node) return null;
  const s = getComputedStyle(node);
  return { family: clip(s.fontFamily, 160), size: s.fontSize, style: s.fontStyle, weight: s.fontWeight };
}

function mathNodes(root, name) {
  return Array.from(root.getElementsByTagNameNS(MATHML_NS, name));
}

function katexUrl(lock) {
  const m = lock?.modules?.find?.(x => x.specifier === 'katex');
  return typeof m?.url === 'string' ? m.url : KATEX_URL;
}

function resourceTiming(url) {
  const e = performance.getEntriesByName?.(url, 'resource')?.[0];
  if (!e) return null;
  return {
    startMs: Math.round(e.startTime), durationMs: Math.round(e.duration), transferSize: e.transferSize, encodedBodySize: e.encodedBodySize,
    decodedBodySize: e.decodedBodySize, protocol: e.nextHopProtocol || null,
  };
}

// ---- KaTeX, shared by the checks

let katexMemo = null;

function loadKatex(ctx) {
  if (!katexMemo) {
    katexMemo = (async () => {
      const t0 = performance.now();
      let mapError;
      try {
        const mod = await import('katex');
        return { katex: mod.default, via: 'import map', ms: Math.round(performance.now() - t0) };
      } catch (e) {
        mapError = errText(e);
        ctx.log(`import('katex') through the map failed (${mapError}); trying the full locked URL`);
      }
      const url = katexUrl(ctx.lock);
      const mod = await import(url);
      return { katex: mod.default, via: 'full URL', url, mapError, ms: Math.round(performance.now() - t0) };
    })();
    katexMemo.catch(() => { katexMemo = null; }); // a later run tries again
  }
  return katexMemo;
}

async function katexOrSkip(ctx, what) {
  try {
    const k = await loadKatex(ctx);
    return { k };
  } catch (e) {
    return {
      result: {
        status: 'skipped',
        summary: `KaTeX did not load by the import map or by its full URL, so ${what} could not run.`,
        data: { error: errText(e) },
      },
    };
  }
}

const loadInfo = k => ({ via: k.via, version: k.katex?.version ?? null, ...(k.mapError ? { mapError: k.mapError } : {}) });

// ---- the exact binomial distribution function

// P(X <= k) for X ~ Bin(n, num/den) as an exact fraction [numerator, denominator] of BigInts.
export function binomialCdfExact(k, n = BIN_N, num = BIN_P[0], den = BIN_P[1]) {
  const total = den ** BigInt(n);
  if (k < 0) return [0n, total];
  if (k >= n) return [total, total];
  const fail = den - num;
  let c = 1n; // C(n, i), updated in place
  let sum = 0n;
  for (let i = 0; i <= k; i++) {
    if (i > 0) c = (c * BigInt(n - i + 1)) / BigInt(i);
    sum += c * num ** BigInt(i) * fail ** BigInt(n - i);
  }
  return [sum, total];
}

// A non-negative fraction as a decimal string with `places` digits, rounded half up.
export function toFixedExact([num, den], places) {
  const scale = 10n ** BigInt(places);
  const q = (2n * num * scale + den) / (2n * den);
  const whole = q / scale;
  if (places === 0) return whole.toString();
  return `${whole}.${(q % scale).toString().padStart(places, '0')}`;
}

export const slotValues = k => ({ k: String(k), p: toFixedExact(binomialCdfExact(k), 4) });

// ---- the specimen sheet

let sheet = null; // { root, errors } once mathml.specimen has rendered

function renderSheet(katex, mount) {
  const root = el('section', {
    'aria-label': 'MathML specimen sheet: 40 numbered formulas',
    style: { borderTop: '2px solid var(--line-strong)', padding: '8px 0 0' },
  }, el('p', { text: `Specimen: ${SPECIMEN.length} formulas, KaTeX ${katex.version} MathML output.`, style: { fontWeight: '600' } }));
  const errors = [];
  const items = [];
  SPECIMEN.forEach((s, i) => {
    const n = i + 1;
    const host = el('span', { 'data-formula': s.id, style: { fontSize: FORMULA_SIZE } });
    try {
      katex.render(s.tex, host, { output: 'mathml', displayMode: s.display, throwOnError: false, strict: 'ignore' });
    } catch (e) {
      errors.push({ n, id: s.id, thrown: clip(errText(e), 200) });
    }
    const formula = s.display
      ? el('div', { style: { overflowX: 'auto', overflowY: 'hidden', padding: '2px 0' } }, host)
      : el('p', { style: { overflowX: 'auto', overflowY: 'hidden', padding: '2px 0' } }, INLINE_BEFORE, host, INLINE_AFTER);
    root.append(el('div', { style: { padding: '8px 0', borderBottom: '1px solid var(--line)' } },
      el('p', { text: `${n}. ${s.label} (${s.display ? 'display' : 'inline'})`, style: { fontSize: '13px', color: 'var(--ink-muted)' } }),
      formula));
    items.push({ n, s, host, formula });
  });
  mount.append(root);
  return { root, items, errors };
}

// The leftmost edge of a formula's rendered content: its descendants' boxes, the annotation left out.
function contentLeft(math) {
  let min = Infinity;
  for (const node of math.querySelectorAll('*')) {
    if (node.closest('annotation, annotation-xml')) continue;
    const r = node.getBoundingClientRect();
    if (r.width > 0 && r.height > 0 && r.left < min) min = r.left;
  }
  return Number.isFinite(min) ? round1(min) : null;
}

function measureSheet(rendered) {
  const { root, items, errors } = rendered;
  for (const { n, s, host } of items) {
    for (const e of host.querySelectorAll('.katex-error')) {
      errors.push({ n, id: s.id, message: clip(e.getAttribute('title') ?? e.textContent ?? '', 200) });
    }
  }
  const noMath = items.filter(({ host }) => mathNodes(host, 'math').length !== 1).map(({ n }) => n);
  const overflowing = items.filter(({ formula }) => formula.scrollWidth > formula.clientWidth + 1).map(({ n }) => n);
  // Content that starts left of its scroll box overflows where no scroll can reach it.
  const contentLefts = items.map(({ n, host, formula }) => {
    const m = mathNodes(host, 'math')[0];
    return { n, content: m ? contentLeft(m) : null, box: round1(formula.getBoundingClientRect().left) };
  });
  const clippedLeft = contentLefts.filter(c => c.content !== null && c.content < c.box - 1).map(c => c.n);
  const sizes = items.map(({ n, host }) => { const b = box(host); return [n, Math.round(b.w), Math.round(b.h)]; });
  const mathvariant = {};
  for (const node of root.querySelectorAll('[mathvariant]')) {
    const v = node.getAttribute('mathvariant');
    mathvariant[v] = (mathvariant[v] ?? 0) + 1;
  }
  const longInline = items.find(({ s }) => s.id === 'long-inline');
  const firstMath = mathNodes(root, 'math')[0];
  return {
    formulas: items.length,
    mathElements: mathNodes(root, 'math').length,
    errorElements: root.querySelectorAll('.katex-error').length,
    errors,
    noMath,
    overflowing,
    clippedLeft,
    clippedLeftBy: contentLefts.filter(c => clippedLeft.includes(c.n)).map(c => [c.n, round1(c.box - c.content)]),
    longInline: longInline ? { formulaBox: box(longInline.host), lineBox: box(longInline.formula) } : null,
    mathvariant,
    fonts: {
      math: fontOf(firstMath),
      mi: fontOf(mathNodes(root, 'mi')[0]),
      text: fontOf(root.querySelector('p')),
      mathDisplay: firstMath ? getComputedStyle(firstMath).display : null,
    },
    sizes,
  };
}

// ---- the TexSlots binding (conflict 10)

function textNodes(root) {
  const out = [];
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  for (let t = walker.nextNode(); t; t = walker.nextNode()) out.push(t);
  return out;
}

function sentinelCounts(math) {
  let presentation = 0;
  let annotation = 0;
  let attributes = 0;
  for (const t of textNodes(math)) {
    if (!t.data.includes(SENTINEL_STEM)) continue;
    if (t.parentElement?.closest('annotation, annotation-xml')) annotation++;
    else presentation++;
  }
  for (const node of [math, ...math.querySelectorAll('*')]) {
    for (const a of node.attributes) if (a.value.includes(SENTINEL_STEM)) attributes++;
  }
  return { presentation, annotation, attributes };
}

const annotationText = v => SLOT_TEX.replace(String.raw`\text{${SENTINEL.k}}`, v.k).replace(String.raw`\text{${SENTINEL.p}}`, v.p);

// Renders SLOT_TEX once; mode 'mn' swaps each sentinel <mtext> for an <mn>, mode 'mtext' keeps the
// <mtext> and writes the digits into it. Returns the bound nodes and the raw counts.
function bindSlots(katex, host, mode) {
  katex.render(SLOT_TEX, host, { output: 'mathml', displayMode: true, throwOnError: true, strict: 'ignore' });
  const math = mathNodes(host, 'math')[0];
  if (!math) throw new Error('KaTeX produced no <math> element');
  const before = sentinelCounts(math);
  const found = { k: 0, p: 0 };
  const slots = { k: [], p: [] };
  let replaced = 0;
  for (const t of mathNodes(math, 'mtext')) {
    const key = t.textContent === SENTINEL.k ? 'k' : t.textContent === SENTINEL.p ? 'p' : null;
    if (!key) continue;
    found[key]++;
    if (mode === 'mn') {
      const mn = document.createElementNS(MATHML_NS, 'mn');
      t.replaceWith(mn);
      slots[key].push(mn);
      replaced++;
    } else {
      slots[key].push(t);
    }
  }
  const annotations = mathNodes(math, 'annotation');
  const set = k => {
    const v = slotValues(k);
    for (const node of slots.k) node.textContent = v.k;
    for (const node of slots.p) node.textContent = v.p;
    for (const a of annotations) a.textContent = annotationText(v);
    return v;
  };
  return { math, slots, found, replaced, before, annotations: annotations.length, set };
}

function slotWidget(katex, mount, idSuffix) {
  const live = el('div', { style: { fontSize: FORMULA_SIZE, overflowX: 'auto' } });
  const plain = el('div', { style: { fontSize: FORMULA_SIZE, overflowX: 'auto' } });
  const id = `mathml-slot-k-${idSuffix}`;
  const slider = el('input', { type: 'range', id, min: '0', max: '10', step: '1', value: String(K_START), style: { width: '100%', minHeight: '44px' } });
  const wrap = el('div', { style: { display: 'grid', gap: '6px' } },
    el('p', { text: 'Live slots: digits in the swapped <mn>, X ~ Bin(10, 0.3).', style: { fontSize: '13px', color: 'var(--ink-muted)' } }),
    live,
    el('p', { text: 'For comparison: the same digits left in the sentinel’s <mtext>.', style: { fontSize: '13px', color: 'var(--ink-muted)' } }),
    plain,
    el('label', { for: id, text: 'Move k from 0 to 10', style: { fontWeight: '600' } }),
    slider);
  mount.append(wrap);
  const a = bindSlots(katex, live, 'mn');
  const b = bindSlots(katex, plain, 'mtext');
  const update = k => { b.set(k); return a.set(k); };
  update(K_START);
  slider.addEventListener('input', () => update(Number(slider.value)));
  return { live: a, plain: b, slider, update };
}

function slotEvidence(w) {
  const { live, plain } = w;
  const mns = [...live.slots.k, ...live.slots.p];
  const wellFormed = mns.every(n => n.isConnected && n.namespaceURI === MATHML_NS && n.localName === 'mn' && live.math.contains(n));
  const after = sentinelCounts(live.math);
  const sentinelMtext = mathNodes(live.math, 'mtext').filter(t => t.textContent.includes(SENTINEL_STEM)).length;
  // Self-test through the slider: value 5 and an input event must show the literal 5 and 0.9527 in both
  // copies; then the slider's value is restored the same way.
  const start = w.slider.value;
  const read = b => ({ k: b.slots.k.map(n => n.textContent), p: b.slots.p.map(n => n.textContent) });
  w.slider.value = SELF_TEST.k;
  w.slider.dispatchEvent(new Event('input', { bubbles: true }));
  const shown = read(live);
  const comparisonShown = read(plain);
  w.slider.value = start;
  w.slider.dispatchEvent(new Event('input', { bubbles: true }));
  const restored = live.slots.k.every(n => n.textContent === start);
  return {
    found: live.found,
    replaced: live.replaced,
    mnElements: mathNodes(live.math, 'mn').length,
    wellFormed,
    sentinelsBefore: live.before,
    sentinelsAfter: after,
    sentinelMtextLeft: sentinelMtext,
    annotationsRewritten: live.annotations,
    comparisonFound: plain.found,
    comparisonSentinelsAfter: sentinelCounts(plain.math),
    selfTest: { expected: SELF_TEST, shown, comparisonShown, restoredTo: start, restored },
    fonts: {
      mnK: fontOf(live.slots.k[0]),
      mnP: fontOf(live.slots.p[0]),
      mtextK: fontOf(plain.slots.k[0]),
      mi: fontOf(mathNodes(live.math, 'mi')[0]),
      mo: fontOf(mathNodes(live.math, 'mo')[0]),
    },
  };
}

// ---- the checks

const katexCheck = {
  id: 'mathml.katex',
  title: 'KaTeX 0.19.0 through the import map',
  kind: 'auto',
  what: "Imports KaTeX with import('katex') through the page's import map, then checks that its version is 0.19.0 and that renderToString returns MathML.",
  async run(ctx) {
    const url = katexUrl(ctx.lock);
    const t0 = ctx.now();
    let mod;
    try {
      mod = await import('katex');
    } catch (e) {
      const ms = Math.round(ctx.now() - t0);
      const fallback = {};
      try {
        const k = await loadKatex(ctx);
        Object.assign(fallback, { ok: true, version: k.katex?.version ?? null, via: k.via });
      } catch (e2) {
        Object.assign(fallback, { ok: false, error: errText(e2) });
      }
      return {
        status: 'fail',
        summary: `import('katex') through the import map failed after ${ms} ms: ${clip(errText(e), 140)}.`,
        data: { error: errText(e), ms, url, fullUrl: fallback, timing: resourceTiming(url) },
      };
    }
    const ms = Math.round(ctx.now() - t0);
    const katex = mod.default;
    if (!katexMemo) katexMemo = Promise.resolve({ katex, via: 'import map', ms });
    const version = katex?.version ?? null;
    let out = '';
    let renderError = null;
    const r0 = ctx.now();
    try {
      out = katex.renderToString(String.raw`\frac{1}{2}`, { output: 'mathml', throwOnError: true });
    } catch (e) {
      renderError = errText(e);
    }
    const renderMs = Math.round((ctx.now() - r0) * 10) / 10;
    const rendered = typeof out === 'string' && out.includes('<math') && out.includes('<mfrac>') && !out.includes('katex-error');
    // timing.startMs before checkStartMs means an earlier import had already fetched the file.
    const data = { version, ms, checkStartMs: Math.round(t0), renderMs, outputChars: out.length, rendered, url, timing: resourceTiming(url), ...(renderError ? { renderError } : {}) };
    if (version !== KATEX_VERSION) {
      return { status: 'fail', summary: `KaTeX loaded through the map in ${ms} ms but reports version ${version}, not ${KATEX_VERSION}.`, data };
    }
    if (!rendered) {
      return { status: 'fail', summary: `KaTeX ${version} loaded in ${ms} ms but renderToString did not return MathML.`, data };
    }
    return { status: 'pass', summary: `KaTeX ${version} loaded through the import map in ${ms} ms and rendered MathML in ${renderMs} ms.`, data };
  },
};

const layoutCheck = {
  id: 'mathml.native-layout',
  title: 'MathML laid out natively',
  kind: 'auto',
  what: 'Renders 1/2 and x squared as MathML and measures their boxes: the numerator must sit above and over the denominator, and the superscript above its base.',
  async run(ctx) {
    const { k, result } = await katexOrSkip(ctx, 'the layout check');
    if (result) return result;
    const { katex } = k;
    ctx.mount.replaceChildren();
    const fracHost = el('span');
    const supHost = el('span');
    const wrap = el('div', { style: { fontSize: '24px', display: 'flex', gap: '32px', alignItems: 'center' } }, fracHost, supHost);
    ctx.mount.append(wrap);
    katex.render(String.raw`\frac{1}{2}`, fracHost, { output: 'mathml', displayMode: true, throwOnError: true });
    katex.render(String.raw`x^{2}`, supHost, { output: 'mathml', displayMode: true, throwOnError: true });
    await fontsSettled();
    const mfrac = mathNodes(fracHost, 'mfrac')[0];
    const msup = mathNodes(supHost, 'msup')[0];
    if (!mfrac || mfrac.children.length !== 2 || !msup || msup.children.length !== 2) {
      return { status: 'error', summary: 'KaTeX did not produce the expected mfrac and msup elements.', data: { error: 'unexpected MathML structure', ...loadInfo(k) } };
    }
    const em = parseFloat(getComputedStyle(wrap).fontSize) || 24;
    const num = box(mfrac.children[0]);
    const den = box(mfrac.children[1]);
    const base = box(msup.children[0]);
    const sup = box(msup.children[1]);
    const fracLift = round1(centreY(den) - centreY(num));
    const fracOffsetX = round1(Math.abs(centreX(num) - centreX(den)));
    const supLift = round1(centreY(base) - centreY(sup));
    const criteria = {
      numeratorAbove: fracLift >= 0.25 * em && num.top < den.top && num.bottom < den.bottom,
      numeratorOverDenominator: fracOffsetX < 0.5 * Math.max(num.w, den.w),
      superscriptRaised: supLift >= 0.1 * em && sup.bottom < base.bottom,
      superscriptRight: sup.left >= base.left + 0.5 * base.w,
    };
    const math = mathNodes(fracHost, 'math')[0];
    const data = {
      ...loadInfo(k),
      em,
      boxes: { numerator: num, denominator: den, base, superscript: sup },
      fracLift,
      fracOffsetX,
      supLift,
      criteria,
      mathmlElementClass: typeof window.MathMLElement === 'function',
      nodeClass: Object.prototype.toString.call(mfrac),
      mathDisplay: math ? getComputedStyle(math).display : null,
      fontSizes: { numerator: getComputedStyle(mfrac.children[0]).fontSize, base: getComputedStyle(msup.children[0]).fontSize, superscript: getComputedStyle(msup.children[1]).fontSize },
      fontFamily: fontOf(math)?.family ?? null,
    };
    if (![num, den, base, sup].every(hasArea)) {
      return { status: 'inconclusive', summary: 'At least one MathML box has no size, so the layout cannot be judged from boxes.', data };
    }
    if (Object.values(criteria).every(Boolean)) {
      return { status: 'pass', summary: `The browser lays MathML out: the numerator sits ${fracLift} px above the denominator and the superscript ${supLift} px above its base.`, data };
    }
    const failed = Object.entries(criteria).filter(([, v]) => !v).map(([key]) => key);
    return { status: 'fail', summary: `MathML is not laid out natively: ${failed.join(', ')} did not hold.`, data };
  },
};

const specimenCheck = {
  id: 'mathml.specimen',
  title: 'Specimen sheet of 40 formulas',
  kind: 'auto',
  what: "Renders the 40 numbered formulas below with KaTeX's MathML output and counts KaTeX's error elements; it passes when all 40 render without error.",
  async run(ctx) {
    const { k, result } = await katexOrSkip(ctx, 'the specimen sheet');
    if (result) return result;
    ctx.mount.replaceChildren();
    sheet = null;
    const t0 = ctx.now();
    const rendered = renderSheet(k.katex, ctx.mount);
    const renderMs = Math.round(ctx.now() - t0);
    await fontsSettled();
    const m = measureSheet(rendered);
    sheet = { root: rendered.root, errors: m.errors.length };
    const data = { ...loadInfo(k), renderMs, ...m };
    const ok = SPECIMEN.length === 40 && m.formulas === 40 && m.mathElements === 40 && m.errorElements === 0 && m.errors.length === 0 && m.noMath.length === 0;
    if (ok) {
      return { status: 'pass', summary: `All 40 formulas rendered as MathML without a KaTeX error in ${renderMs} ms; ${m.overflowing.length} scroll sideways, ${m.clippedLeft.length} start left of their scroll box${m.clippedLeft.length ? ` (numbers ${m.clippedLeft.join(', ')})` : ''}.`, data };
    }
    const bad = [...new Set([...m.errors.map(e => e.n), ...m.noMath])].sort((x, y) => x - y);
    return { status: 'fail', summary: `${bad.length} of ${m.formulas} formulas did not render cleanly: numbers ${bad.join(', ') || 'none'}; ${m.mathElements} <math> elements.`, data };
  },
};

const specimenVerdict = {
  id: 'mathml.specimen-verdict',
  title: 'Your verdict on the specimen sheet',
  kind: 'manual',
  what: "You compare the specimen sheet with the screenshot of the web app's KaTeX rendering and say whether every formula is readable and correctly set.",
  async run(ctx) {
    ctx.mount.replaceChildren();
    let where = 'specimen card';
    let sheetErrors = sheet?.errors ?? null;
    if (sheet?.root?.isConnected) {
      const target = sheet.root;
      ctx.mount.append(el('button', { type: 'button', class: 'btn', text: 'Show the sheet', onclick: () => target.scrollIntoView({ block: 'start' }) }));
    } else {
      const { k, result } = await katexOrSkip(ctx, 'the sheet for the verdict');
      if (result) return result;
      where = 'this card';
      const rendered = renderSheet(k.katex, ctx.mount);
      await fontsSettled();
      sheetErrors = measureSheet(rendered).errors.length;
      ctx.log('the specimen card had no sheet, so the sheet was rendered in this card');
    }
    const answer = await ctx.ask('Compare the sheet with the screenshot Claude sent of the web app (KaTeX HTML output). Is every formula readable and correctly set?', SPECIMEN_CHOICES);
    let note = null;
    if (answer !== SPECIMEN_CHOICES[0]) note = await ctx.note('Which formulas, by number, and what is wrong?');
    const screenshots = await ctx.ask('Take screenshots of the whole sheet on this phone, in light and in dark mode, and send them to Claude. Done?', SHOT_CHOICES);
    const data = { answer, note, screenshots, sheet: where, sheetErrors };
    const shots = ` Screenshots: ${screenshots === SHOT_CHOICES[0] ? 'sent' : 'not sent'}.`;
    if (answer === SPECIMEN_CHOICES[0]) return { status: 'pass', summary: `The owner judged every formula readable and correctly set.${shots}`, data };
    return { status: 'fail', summary: `The owner answered "${answer}".${shots}`, data };
  },
};

const texslotsCheck = {
  id: 'mathml.texslots',
  title: 'TexSlots sentinels swapped for <mn>',
  kind: 'auto',
  what: 'Renders a formula with two sentinel \\text{} slots, swaps each sentinel <mtext> for an <mn> made with createElementNS and checks that no sentinel text is left; the slider then drives the digits.',
  async run(ctx) {
    const { k, result } = await katexOrSkip(ctx, 'the TexSlots binding');
    if (result) return result;
    ctx.mount.replaceChildren();
    const w = slotWidget(k.katex, ctx.mount, 'auto');
    const e = slotEvidence(w);
    const data = { ...loadInfo(k), ...e };
    const t = e.selfTest;
    const selfTestOk = t.shown.k.join() === SELF_TEST.k && t.shown.p.join() === SELF_TEST.p
      && t.comparisonShown.k.join() === SELF_TEST.k && t.comparisonShown.p.join() === SELF_TEST.p && t.restored;
    const ok = e.found.k === 1 && e.found.p === 1 && e.replaced === 2 && e.wellFormed
      && e.sentinelsAfter.presentation === 0 && e.sentinelsAfter.annotation === 0 && e.sentinelsAfter.attributes === 0
      && e.sentinelMtextLeft === 0 && selfTestOk;
    if (ok) {
      const note = e.sentinelsBefore.annotation ? ", after the TeX annotation, which repeated them, was rewritten" : '';
      return { status: 'pass', summary: `Both sentinels became <mn> elements and no sentinel text is left${note}; moving the slider to 5 showed 5 and 0.9527 in both copies.`, data };
    }
    return {
      status: 'fail',
      summary: `The binding did not complete: found k ${e.found.k}, p ${e.found.p}; replaced ${e.replaced}; sentinel text left ${e.sentinelsAfter.presentation} shown, ${e.sentinelsAfter.annotation} in the annotation; self-test ${selfTestOk ? 'passed' : 'failed'}.`,
      data,
    };
  },
};

const texslotsVerdict = {
  id: 'mathml.texslots-verdict',
  title: 'Your verdict on the live slots',
  kind: 'manual',
  what: "You move the slider, judge whether the live digits match the formula's maths font and whether they differ from the <mtext> copy, check with VoiceOver that the formula reads its current values, and send screenshots.",
  async run(ctx) {
    const { k, result } = await katexOrSkip(ctx, 'the live slots');
    if (result) return result;
    ctx.mount.replaceChildren();
    const w = slotWidget(k.katex, ctx.mount, 'verdict');
    const e = slotEvidence(w);
    // Counted from here, after the self-test's own input events.
    const moves = { count: 0, values: new Set() };
    const onMove = () => { moves.count += 1; moves.values.add(w.slider.value); };
    w.slider.addEventListener('input', onMove);
    let font;
    let atFont;
    let mtext;
    let voiceOver;
    let screenshots;
    try {
      font = await ctx.ask('Move the slider. Do the changing digits match the maths font of the surrounding formula?', FONT_CHOICES);
      atFont = { sliderMoves: moves.count, kValuesSeen: [...moves.values].slice(0, 11) };
      mtext = await ctx.ask('Do the digits in the first line (<mn>) look different from the digits in the comparison line (<mtext>)?', MTEXT_CHOICES);
      voiceOver = await ctx.ask('Turn on VoiceOver and move to the formula. Does it read the current values?', VOICEOVER_CHOICES);
      screenshots = await ctx.ask('Take screenshots of these live slots, in light and in dark mode, and send them to Claude. Done?', SHOT_CHOICES);
    } finally {
      w.slider.removeEventListener('input', onMove);
    }
    const data = {
      font, mtextComparison: mtext, voiceOver, screenshots, ...atFont, kAtAnswer: Number(w.slider.value), ...loadInfo(k),
      binding: { found: e.found, replaced: e.replaced, sentinelsAfter: e.sentinelsAfter }, fonts: e.fonts,
    };
    const extra = ` The <mn> digits ${mtext === MTEXT_CHOICES[0] ? 'look different from' : 'look the same as'} the <mtext> copy; screenshots ${screenshots === SHOT_CHOICES[0] ? 'sent' : 'not sent'}.`;
    if (atFont.sliderMoves === 0) {
      return { status: 'inconclusive', summary: `The font answer came before the slider was moved, so the changing digits were not judged.${extra}`, data };
    }
    if (font === FONT_CHOICES[0] && voiceOver === VOICEOVER_CHOICES[0]) {
      return { status: 'pass', summary: `The live digits match the maths font over ${atFont.kValuesSeen.length} values of k, and VoiceOver reads the current values.${extra}`, data };
    }
    if (font !== FONT_CHOICES[0] || voiceOver === VOICEOVER_CHOICES[1]) {
      return { status: 'fail', summary: `Font: "${font}"; VoiceOver: "${voiceOver}".${extra}`, data };
    }
    return { status: 'inconclusive', summary: `The live digits match the maths font; VoiceOver was not tested.${extra}`, data };
  },
};

const htmlDataCheck = {
  id: 'mathml.htmldata',
  title: '\\htmlData term anchors in the MathML output',
  kind: 'auto',
  what: "Renders a+\\htmlData{term=b}{b^2} with trust on, with KaTeX's MathML output and, as the control, its HTML output, and records whether any element carries data-term (ARCHITECTURE.md 14 item 20).",
  async run(ctx) {
    const { k, result } = await katexOrSkip(ctx, 'the htmlData check');
    if (result) return result;
    const render = output => {
      const host = document.createElement('span'); // detached: counted, never shown
      try {
        k.katex.render(HTMLDATA_TEX, host, { output, trust: true, strict: 'ignore', throwOnError: true });
      } catch (e) {
        return { error: errText(e) };
      }
      const marked = host.querySelectorAll('[data-term]');
      return { elements: host.querySelectorAll('*').length, withDataTerm: marked.length, value: marked[0]?.getAttribute('data-term') ?? null, onMathml: [...marked].some(n => n.namespaceURI === MATHML_NS) };
    };
    const mathml = render('mathml');
    const html = render('html');
    const data = { ...loadInfo(k), tex: HTMLDATA_TEX, mathml, html };
    if (mathml.error || html.error) {
      return { status: 'error', summary: `KaTeX threw while rendering the \\htmlData formula: ${mathml.error ?? html.error}.`, data: { ...data, error: mathml.error ?? html.error } };
    }
    if (html.withDataTerm === 0) {
      return { status: 'inconclusive', summary: 'The control (HTML output) has no data-term either, so KaTeX did not honour \\htmlData here and the MathML reading says nothing.', data };
    }
    if (mathml.withDataTerm > 0) {
      return { status: 'pass', summary: `\\htmlData term anchors survive in KaTeX ${data.version}'s MathML output (${mathml.withDataTerm} element with data-term="${mathml.value}").`, data };
    }
    return {
      status: 'fail',
      summary: `KaTeX ${data.version}'s MathML output drops \\htmlData: no element carries data-term, while the HTML output does. The fallback of ARCHITECTURE.md 14 item 20 applies: live-formula in the Artifact highlights a term from its term list.`,
      data,
    };
  },
};

export default {
  id: 'mathml',
  title: 'Maths as MathML',
  checks: [katexCheck, layoutCheck, specimenCheck, specimenVerdict, texslotsCheck, texslotsVerdict, htmlDataCheck],
};
