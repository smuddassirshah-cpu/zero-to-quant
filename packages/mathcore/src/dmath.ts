// Deterministic exp, log, log1p, expm1 and tanh (docs/WIDGETS.md 3; docs/PLAN.md conflict 7): every seeded
// number shown or graded must come out with the same bits on every engine. Decision notes:
// - Ported from FreeBSD msun, lib/msun/src at tag release/14.1.0: e_exp.c, e_log.c, s_log1p.c, s_expm1.c and
//   s_tanh.c, Sun's fdlibm with FreeBSD's C99 fixes. The constants and most thresholds and special-value lines
//   were checked against quoted extracts of those files at that tag [sourced]; the rest follows fdlibm as
//   recalled [recalled], and the goldens check all of it. Each constant is the C file's literal, less the
//   trailing zeros Prettier drops, and parses to the hex words its comment gives [measured].
// - Only IEEE-754 + - * / on doubles, int32 bit operations and a DataView for a double's two words; no Math
//   function. ECMAScript rounds each operation to nearest, ties to even, with no fused multiply-add and no
//   wider intermediate [sourced: ECMA-262, the Number type], so every engine returns the same bits.
// - Departure from the C [our choice]: floating-point exception flags are not raised.
// - Error over the 10,000 goldens of test/dmath.goldens.txt: at most 0.79 ulp, 1.54 ulp for tanh
//   [measured]. Every function is O(1).
//
// Licence notice of the ported files, preserved as they require:
// ====================================================
// Copyright (C) 1993 by Sun Microsystems, Inc. All rights reserved.
// (e_exp.c: Copyright (C) 2004 by Sun Microsystems, Inc. All rights reserved.)
//
// Developed at SunSoft, a Sun Microsystems, Inc. business.
// Permission to use, copy, modify, and distribute this
// software is freely granted, provided that this notice
// is preserved.
// ====================================================

const view = new DataView(new ArrayBuffer(8));

function high(x: number): number {
  view.setFloat64(0, x);
  return view.getInt32(0);
}

function low(x: number): number {
  view.setFloat64(0, x);
  return view.getUint32(4);
}

function words(hi: number, lo: number): number {
  view.setInt32(0, hi);
  view.setInt32(4, lo);
  return view.getFloat64(0);
}

function withHigh(x: number, hi: number): number {
  view.setFloat64(0, x);
  view.setInt32(0, hi);
  return view.getFloat64(0);
}

const TWO54 = 18014398509481984;
const TWO1023 = words(0x7fe00000, 0);
const TWOM1000 = words(0x01700000, 0);

const LN2_HI = 6.9314718036912381649e-1;
const LN2_LO = 1.90821492927058770002e-10;
const INVLN2 = 1.442695040888963387;
const O_THRESHOLD = 7.09782712893383973096e2;
const U_THRESHOLD = -7.4513321910194110842e2;
const P1 = 1.66666666666666019037e-1;
const P2 = -2.77777777770155933842e-3;
const P3 = 6.61375632143793436117e-5;
const P4 = -1.6533902205465251539e-6;
const P5 = 4.13813679705723846039e-8;

/** e^x, after fdlibm's e_exp.c. */
export function exp(x: number): number {
  let hx = high(x);
  const xsb = hx >>> 31;
  hx &= 0x7fffffff;
  if (hx >= 0x40862e42) {
    if (hx >= 0x7ff00000) return ((hx & 0xfffff) | low(x)) !== 0 ? x + x : xsb === 0 ? x : 0;
    if (x > O_THRESHOLD) return Infinity;
    if (x < U_THRESHOLD) return 0;
  }
  let hi = 0;
  let lo = 0;
  let k = 0;
  if (hx > 0x3fd62e42) {
    if (hx < 0x3ff0a2b2) {
      hi = xsb === 0 ? x - LN2_HI : x + LN2_HI;
      lo = xsb === 0 ? LN2_LO : -LN2_LO;
      k = 1 - xsb - xsb;
    } else {
      k = (INVLN2 * x + (xsb === 0 ? 0.5 : -0.5)) | 0;
      hi = x - k * LN2_HI;
      lo = k * LN2_LO;
    }
    x = hi - lo;
  } else if (hx < 0x3e300000) return 1 + x;
  const t = x * x;
  const c = x - t * (P1 + t * (P2 + t * (P3 + t * (P4 + t * P5))));
  if (k === 0) return 1 - ((x * c) / (c - 2) - x);
  const y = 1 - (lo - (x * c) / (2 - c) - hi);
  if (k < -1021) return y * words((0x3ff + k + 1000) << 20, 0) * TWOM1000;
  return k === 1024 ? y * 2 * TWO1023 : y * words((0x3ff + k) << 20, 0);
}

const LG1 = 6.66666666666673513e-1;
const LG2 = 3.999999999940941908e-1;
const LG3 = 2.857142874366239149e-1;
const LG4 = 2.222219843214978396e-1;
const LG5 = 1.818357216161805012e-1;
const LG6 = 1.531383769920937332e-1;
const LG7 = 1.479819860511658591e-1;

/** The natural logarithm, after fdlibm's e_log.c. */
export function log(x: number): number {
  let hx = high(x);
  const lx = low(x);
  let k = 0;
  if (hx < 0x00100000) {
    if (((hx & 0x7fffffff) | lx) === 0) return -Infinity;
    if (hx < 0) return NaN;
    k -= 54;
    x *= TWO54;
    hx = high(x);
  }
  if (hx >= 0x7ff00000) return x + x;
  if (hx === 0x3ff00000 && lx === 0) return 0;
  k += (hx >> 20) - 1023;
  hx &= 0x000fffff;
  let i = (hx + 0x95f64) & 0x100000;
  x = withHigh(x, hx | (i ^ 0x3ff00000));
  k += i >> 20;
  const f = x - 1;
  if ((0x000fffff & (2 + hx)) < 3) {
    if (f === 0) return k * LN2_HI + k * LN2_LO; // x = 1, with k = 0, returned above
    const r = f * f * (0.5 - 0.3333333333333333 * f);
    return k === 0 ? f - r : k * LN2_HI - (r - k * LN2_LO - f);
  }
  const s = f / (2 + f);
  const z = s * s;
  const w = z * z;
  i = hx - 0x6147a;
  const j = 0x6b851 - hx;
  const r = z * (LG1 + w * (LG3 + w * (LG5 + w * LG7))) + w * (LG2 + w * (LG4 + w * LG6));
  if ((i | j) > 0) {
    const hfsq = 0.5 * f * f;
    return k === 0 ? f - (hfsq - s * (hfsq + r)) : k * LN2_HI - (hfsq - (s * (hfsq + r) + k * LN2_LO) - f);
  }
  return k === 0 ? f - s * (f - r) : k * LN2_HI - (s * (f - r) - k * LN2_LO - f);
}

/** log(1 + x), accurate near x = 0, after fdlibm's s_log1p.c. */
export function log1p(x: number): number {
  const hx = high(x);
  const ax = hx & 0x7fffffff;
  let k = 1;
  let f = 0;
  let c = 0;
  let hu = 0;
  if (hx < 0x3fda827a) {
    if (ax >= 0x3ff00000) return x === -1 ? -Infinity : NaN;
    if (ax < 0x3e200000) return ax < 0x3c900000 ? x : x - x * x * 0.5;
    if (hx > 0 || hx <= (0xbfd2bec4 | 0)) {
      k = 0;
      f = x;
      hu = 1;
    }
  }
  if (hx >= 0x7ff00000) return x + x;
  if (k !== 0) {
    let u = x;
    if (hx < 0x43400000) {
      u = 1 + x;
      hu = high(u);
      k = (hu >> 20) - 1023;
      c = (k > 0 ? 1 - (u - x) : x - (u - 1)) / u;
    } else {
      hu = high(u);
      k = (hu >> 20) - 1023;
    }
    hu &= 0x000fffff;
    if (hu < 0x6a09e) u = withHigh(u, hu | 0x3ff00000);
    else {
      k += 1;
      u = withHigh(u, hu | 0x3fe00000);
      hu = (0x00100000 - hu) >> 2;
    }
    f = u - 1;
  }
  const hfsq = 0.5 * f * f;
  if (hu === 0) {
    // Reached only through the reduction above, which never leaves k = 0 (s_log1p.c's own note).
    if (f === 0) return k * LN2_HI + (c + k * LN2_LO);
    return k * LN2_HI - (hfsq * (1 - 0.6666666666666666 * f) - (k * LN2_LO + c) - f);
  }
  const s = f / (2 + f);
  const z = s * s;
  const r = z * (LG1 + z * (LG2 + z * (LG3 + z * (LG4 + z * (LG5 + z * (LG6 + z * LG7))))));
  return k === 0
    ? f - (hfsq - s * (hfsq + r))
    : k * LN2_HI - (hfsq - (s * (hfsq + r) + (k * LN2_LO + c)) - f);
}

const Q1 = -3.33333333333331316428e-2;
const Q2 = 1.58730158725481460165e-3;
const Q3 = -7.93650757867487942473e-5;
const Q4 = 4.00821782732936239552e-6;
const Q5 = -2.01099218183624371326e-7;

/** e^x - 1, accurate near x = 0, after fdlibm's s_expm1.c. */
export function expm1(x: number): number {
  let hx = high(x);
  const neg = hx < 0;
  hx &= 0x7fffffff;
  if (hx >= 0x4043687a) {
    if (hx >= 0x40862e42) {
      if (hx >= 0x7ff00000) return ((hx & 0xfffff) | low(x)) !== 0 ? x + x : neg ? -1 : x;
      if (x > O_THRESHOLD) return Infinity;
    }
    if (neg) return -1;
  }
  let k = 0;
  let c = 0;
  if (hx > 0x3fd62e42) {
    let hi: number;
    let lo: number;
    if (hx < 0x3ff0a2b2) {
      hi = neg ? x + LN2_HI : x - LN2_HI;
      lo = neg ? -LN2_LO : LN2_LO;
      k = neg ? -1 : 1;
    } else {
      k = (INVLN2 * x + (neg ? -0.5 : 0.5)) | 0;
      hi = x - k * LN2_HI;
      lo = k * LN2_LO;
    }
    x = hi - lo;
    c = hi - x - lo;
  } else if (hx < 0x3c900000) return x;
  const hfx = 0.5 * x;
  const hxs = x * hfx;
  const r1 = 1 + hxs * (Q1 + hxs * (Q2 + hxs * (Q3 + hxs * (Q4 + hxs * Q5))));
  const t = 3 - r1 * hfx;
  let e = hxs * ((r1 - t) / (6 - x * t));
  if (k === 0) return x - (x * e - hxs);
  e = x * (e - c) - c - hxs;
  if (k === -1) return 0.5 * (x - e) - 0.5;
  if (k === 1) return x < -0.25 ? -2 * (e - (x + 0.5)) : 1 + 2 * (x - e);
  if (k <= -2 || k > 56) {
    const y = 1 - (e - x);
    return (k === 1024 ? y * 2 * TWO1023 : y * words((0x3ff + k) << 20, 0)) - 1;
  }
  const twopk = words((0x3ff + k) << 20, 0);
  if (k < 20) return (words(0x3ff00000 - (0x200000 >> k), 0) - (e - x)) * twopk;
  return (x - (e + words((0x3ff - k) << 20, 0)) + 1) * twopk;
}

/** The hyperbolic tangent, after fdlibm's s_tanh.c. */
export function tanh(x: number): number {
  const jx = high(x);
  const ix = jx & 0x7fffffff;
  if (ix >= 0x7ff00000) return jx >= 0 ? 1 / x + 1 : 1 / x - 1;
  let z = 1;
  if (ix < 0x40360000) {
    if (ix < 0x3e300000) return x;
    const ax = jx < 0 ? -x : x;
    if (ix >= 0x3ff00000) z = 1 - 2 / (expm1(2 * ax) + 2);
    else {
      const t = expm1(-2 * ax);
      z = -t / (t + 2);
    }
  }
  return jx >= 0 ? z : -z;
}
