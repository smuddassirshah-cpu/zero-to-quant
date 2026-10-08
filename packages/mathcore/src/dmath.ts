// Deterministic exp, log, log1p, expm1, tanh, pow, sin and cos (docs/WIDGETS.md 3; docs/PLAN.md conflict 7):
// every seeded number shown or graded must come out with the same bits on every engine. Decision notes:
// - Ported from FreeBSD msun, lib/msun/src at tag release/14.1.0: e_exp.c, e_log.c, e_pow.c, s_log1p.c,
//   s_expm1.c, s_tanh.c, s_sin.c, s_cos.c, k_sin.c, k_cos.c, e_rem_pio2.c and k_rem_pio2.c, Sun's fdlibm with
//   FreeBSD's C99 fixes. The constants and most thresholds and special-value lines were checked against quoted
//   extracts of those files at that tag [sourced]; the rest follows fdlibm as recalled [recalled], and the
//   goldens check all of it. Each constant is the C file's literal, less the trailing zeros Prettier drops,
//   and parses to the hex words its comment gives [measured]; the 2/pi table matches mpmath's bits of 2/pi
//   [measured]. The scaling step follows musl 1.2.5's src/math/scalbn.c, reduced to the exponents used here
//   [recalled].
// - Only IEEE-754 + - * / on doubles, int32 bit operations and a DataView for a double's two words; no Math
//   function. ECMAScript rounds each operation to nearest, ties to even, with no fused multiply-add and no
//   wider intermediate [sourced: ECMA-262, the Number type], so every engine returns the same bits.
// - Departures from the C, each [our choice]: exp(1) returns e correctly rounded, 2.718281828459045, as V8's
//   port does [sourced: V8 12.4.254, src/base/ieee754.cc, exp], where e_exp.c's reduction gives one ulp
//   above; pow(x, 0.5) keeps the general path instead of calling sqrt; the unrolled cases of e_rem_pio2.c for
//   |x| <= 9pi/4 are folded into its medium path, which is accurate on the whole medium range; floating-point
//   exception flags are not raised. pow follows C99 Annex F, so it differs from Math.pow at pow(1, NaN) = 1
//   and pow(-1, +-Infinity) = 1, where ECMAScript returns NaN.
// - Error, a maximum seen and not a bound: over the 10,000 goldens of test/dmath.goldens.txt, 0.73 ulp, and
//   1.45 ulp for tanh; over a sweep of 400,000 inputs to exp, log, log1p, expm1 and tanh against mpmath at
//   40 digits, 0.81 ulp, and 2.03 ulp (2.4e-16 relative) for tanh [measured]. Every function is O(1); sin
//   and cos above 2^20 pi/2 run the Payne-Hanek reduction over at most 20 words.
//
// Licence notice of the ported files, preserved as they require:
// ====================================================
// Copyright (C) 1993 by Sun Microsystems, Inc. All rights reserved.
// (e_exp.c and e_pow.c: Copyright (C) 2004 by Sun Microsystems, Inc. All rights reserved.)
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

function withLowZero(x: number): number {
  view.setFloat64(0, x);
  view.setInt32(4, 0);
  return view.getFloat64(0);
}

// Typed-array and table reads under noUncheckedIndexedAccess; every index is in range by construction.
const at = (a: ArrayLike<number>, i: number): number => a[i] ?? NaN;

const TWO24 = 16777216;
const TWON24 = 5.9604644775390625e-8;
const TWO52 = 4503599627370496;
const TWO53 = 9007199254740992;
const TWO54 = 18014398509481984;
const TWO1023 = words(0x7fe00000, 0);
const TWOM969 = words(0x03600000, 0);
const TWOM1000 = words(0x01700000, 0);

// 2^n for -1991 <= n <= 1023 times x, rounded once: below 2^-1022 it scales into the normal range first, so a
// subnormal result rounds only at the last multiplication (musl's scalbn).
function scalbn(x: number, n: number): number {
  if (n < -1022) {
    x *= TWOM969;
    n += 969;
  }
  return x * words((0x3ff + n) << 20, 0);
}

// floor(v) for 0 <= v < 2^52: adding and removing 2^52 rounds to an integer, then a step down if it rose.
function floorNonNegative(v: number): number {
  const t = v + TWO52 - TWO52;
  return t > v ? t - 1 : t;
}

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
      if (x === 1) return 2.718281828459045;
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

const BP1 = 1.5;
const DP_H1 = 5.84962487220764160156e-1;
const DP_L1 = 1.35003920212974897128e-8;
const THRD = 3.3333333333333331e-1;
const L1 = 5.99999999999994648725e-1;
const L2 = 4.28571428578550184252e-1;
const L3 = 3.33333329818377432918e-1;
const L4 = 2.72728123808534006489e-1;
const L5 = 2.30660745775561754067e-1;
const L6 = 2.06975017800338417784e-1;
const LG2_F = 6.93147180559945286227e-1;
const LG2_H = 6.93147182464599609375e-1;
const LG2_L = -1.90465429995776804525e-9;
const OVT = 8.008566259537294e-17;
const CP = 9.61796693925975554329e-1;
const CP_H = 9.61796700954437255859e-1;
const CP_L = -7.02846165095275826516e-9;
const IVLN2 = 1.442695040888963387;
const IVLN2_H = 1.44269502162933349609;
const IVLN2_L = 1.92596299112661746887e-8;

/** x^y with the special values of C99 Annex F, after fdlibm's e_pow.c. */
export function pow(x: number, y: number): number {
  const hx = high(x);
  const lx = low(x);
  const hy = high(y);
  const ly = low(y);
  let ix = hx & 0x7fffffff;
  const iy = hy & 0x7fffffff;
  if ((iy | ly) === 0) return 1;
  if (hx === 0x3ff00000 && lx === 0) return 1;
  if (
    ix > 0x7ff00000 ||
    (ix === 0x7ff00000 && lx !== 0) ||
    iy > 0x7ff00000 ||
    (iy === 0x7ff00000 && ly !== 0)
  ) {
    return x + y;
  }
  // yisint: 0 when y is not an integer, 1 when it is odd, 2 when it is even; only needed for x < 0.
  let yisint = 0;
  if (hx < 0) {
    if (iy >= 0x43400000) yisint = 2;
    else if (iy >= 0x3ff00000) {
      const k = (iy >> 20) - 0x3ff;
      if (k > 20) {
        const j = ly >>> (52 - k);
        if ((j << (52 - k)) >>> 0 === ly) yisint = 2 - (j & 1);
      } else if (ly === 0) {
        const j = iy >> (20 - k);
        if (j << (20 - k) === iy) yisint = 2 - (j & 1);
      }
    }
  }
  if (ly === 0) {
    if (iy === 0x7ff00000) {
      if (((ix - 0x3ff00000) | lx) === 0) return 1;
      if (ix >= 0x3ff00000) return hy >= 0 ? y : 0;
      return hy < 0 ? -y : 0;
    }
    if (iy === 0x3ff00000) return hy < 0 ? 1 / x : x;
    if (hy === 0x40000000) return x * x;
  }
  let ax = hx < 0 ? -x : x;
  if (lx === 0 && (ix === 0x7ff00000 || ix === 0 || ix === 0x3ff00000)) {
    let z = hy < 0 ? 1 / ax : ax;
    if (hx < 0) {
      if (((ix - 0x3ff00000) | yisint) === 0) z = NaN;
      else if (yisint === 1) z = -z;
    }
    return z;
  }
  let n = (hx >>> 31) - 1;
  if ((n | yisint) === 0) return NaN;
  const s = (n | (yisint - 1)) === 0 ? -1 : 1;
  // log2(|x|) as t1 + t2, t1 with its low word cleared.
  let t1: number;
  let t2: number;
  if (iy > 0x41e00000) {
    if (iy > 0x43f00000) {
      if (ix <= 0x3fefffff) return hy < 0 ? Infinity : 0;
      return hy > 0 ? Infinity : 0;
    }
    if (ix < 0x3fefffff) return hy < 0 ? s * Infinity : s * 0;
    if (ix > 0x3ff00000) return hy > 0 ? s * Infinity : s * 0;
    const t = ax - 1;
    const w = t * t * (0.5 - t * (THRD - t * 0.25));
    const u = IVLN2_H * t;
    const v = t * IVLN2_L - w * IVLN2;
    t1 = withLowZero(u + v);
    t2 = v - (t1 - u);
  } else {
    n = 0;
    if (ix < 0x00100000) {
      ax *= TWO53;
      n -= 53;
      ix = high(ax);
    }
    n += (ix >> 20) - 0x3ff;
    const j = ix & 0x000fffff;
    ix = j | 0x3ff00000;
    let k = 0;
    if (j > 0x3988e) {
      if (j < 0xbb67a) k = 1;
      else {
        n += 1;
        ix -= 0x00100000;
      }
    }
    ax = withHigh(ax, ix);
    const bp = k === 0 ? 1 : BP1;
    let u = ax - bp;
    let v = 1 / (ax + bp);
    const ss = u * v;
    const sH = withLowZero(ss);
    let tH = words(((ix >> 1) | 0x20000000) + 0x00080000 + (k << 18), 0);
    let tL = ax - (tH - bp);
    const sL = v * (u - sH * tH - sH * tL);
    let s2 = ss * ss;
    let r = s2 * s2 * (L1 + s2 * (L2 + s2 * (L3 + s2 * (L4 + s2 * (L5 + s2 * L6)))));
    r += sL * (sH + ss);
    s2 = sH * sH;
    tH = withLowZero(3 + s2 + r);
    tL = r - (tH - 3 - s2);
    u = sH * tH;
    v = sL * tH + tL * ss;
    const pH = withLowZero(u + v);
    const pL = v - (pH - u);
    const zH = CP_H * pH;
    const zL = CP_L * pH + pL * CP + (k === 0 ? 0 : DP_L1);
    const dpH = k === 0 ? 0 : DP_H1;
    t1 = withLowZero(zH + zL + dpH + n);
    t2 = zL - (t1 - n - dpH - zH);
  }
  // y * log2(|x|) as pH + pL, then 2^(pH + pL).
  const y1 = withLowZero(y);
  const pL = (y - y1) * t1 + y * t2;
  let pH = y1 * t1;
  let z = pL + pH;
  let j = high(z);
  const i = low(z);
  if (j >= 0x40900000) {
    if (((j - 0x40900000) | i) !== 0 || pL + OVT > z - pH) return s * Infinity;
  } else if ((j & 0x7fffffff) >= 0x4090cc00) {
    if (((j - 0xc090cc00) | i) !== 0 || pL <= z - pH) return s * 0;
  }
  const iz = j & 0x7fffffff;
  n = 0;
  if (iz > 0x3fe00000) {
    n = j + (0x00100000 >> ((iz >> 20) - 0x3ff + 1));
    const k = ((n & 0x7fffffff) >> 20) - 0x3ff;
    pH -= words(n & ~(0x000fffff >> k), 0);
    n = ((n & 0x000fffff) | 0x00100000) >> (20 - k);
    if (j < 0) n = -n;
  }
  const t = withLowZero(pL + pH);
  const u = t * LG2_H;
  const v = (pL - (t - pH)) * LG2_F + t * LG2_L;
  z = u + v;
  const w = v - (z - u);
  const tt = z * z;
  const c = z - tt * (P1 + tt * (P2 + tt * (P3 + tt * (P4 + tt * P5))));
  const r = (z * c) / (c - 2) - (w + z * w);
  z = 1 - (r - z);
  j = high(z) + (n << 20);
  return s * (j >> 20 <= 0 ? scalbn(z, n) : withHigh(z, j));
}

const S1 = -1.66666666666666324348e-1;
const S2 = 8.33333333332248946124e-3;
const S3 = -1.98412698298579493134e-4;
const S4 = 2.75573137070700676789e-6;
const S5 = -2.50507602534068634195e-8;
const S6 = 1.58969099521155010221e-10;
const C1 = 4.16666666666666019037e-2;
const C2 = -1.38888888888741095749e-3;
const C3 = 2.48015872894767294178e-5;
const C4 = -2.75573143513906633035e-7;
const C5 = 2.0875723212981748279e-9;
const C6 = -1.13596475577881948265e-11;

// sin(x + y) for |x + y| <= pi/4, y the tail of x (k_sin.c; tail false means y is zero).
function kernelSin(x: number, y: number, tail: boolean): number {
  const z = x * x;
  const w = z * z;
  const r = S2 + z * (S3 + z * S4) + z * w * (S5 + z * S6);
  const v = z * x;
  return tail ? x - (z * (0.5 * y - v * r) - y - v * S1) : x + v * (S1 + z * r);
}

// cos(x + y) for |x + y| <= pi/4 (k_cos.c).
function kernelCos(x: number, y: number): number {
  const z = x * x;
  const w = z * z;
  const r = z * (C1 + z * (C2 + z * C3)) + w * w * (C4 + z * (C5 + z * C6));
  const hz = 0.5 * z;
  const v = 1 - hz;
  return v + (1 - v - hz + (z * r - x * y));
}

const INVPIO2 = 6.36619772367581382433e-1;
const PIO2_1 = 1.57079632673412561417;
const PIO2_1T = 6.07710050650619224932e-11;
const PIO2_2 = 6.0771005063039659766e-11;
const PIO2_2T = 2.02226624879595063154e-21;
const PIO2_3 = 2.0222662487111664558e-21;
const PIO2_3T = 8.47842766036889956997e-32;
const TOINT = 6755399441055744;

// x - n pi/2 as head + tail, written to these two; returns n (n mod 8 above 2^20 pi/2), of which the callers
// use n mod 4. |x| > pi/4 and finite.
let head = 0;
let tail = 0;

function remPio2(x: number): number {
  const ix = high(x) & 0x7fffffff;
  if (ix >= 0x413921fb) return remPio2Large(x, ix);
  const fn = x * INVPIO2 + TOINT - TOINT;
  let r = x - fn * PIO2_1;
  let w = fn * PIO2_1T;
  const e = ix >> 20;
  head = r - w;
  if (e - ((high(head) >> 20) & 0x7ff) > 16) {
    let t = r;
    w = fn * PIO2_2;
    r = t - w;
    w = fn * PIO2_2T - (t - r - w);
    head = r - w;
    if (e - ((high(head) >> 20) & 0x7ff) > 49) {
      t = r;
      w = fn * PIO2_3;
      r = t - w;
      w = fn * PIO2_3T - (t - r - w);
      head = r - w;
    }
  }
  tail = r - head - w;
  return fn | 0;
}

// The bits of 2/pi in 24-bit words, and pi/2 in 24-bit pieces (k_rem_pio2.c).
const IPIO2: readonly number[] = [
  0xa2f983, 0x6e4e44, 0x1529fc, 0x2757d1, 0xf534dd, 0xc0db62, 0x95993c, 0x439041, 0xfe5163, 0xabdebb,
  0xc561b7, 0x246e3a, 0x424dd2, 0xe00649, 0x2eea09, 0xd1921c, 0xfe1deb, 0x1cb129, 0xa73ee8, 0x8235f5,
  0x2ebb44, 0x84e99c, 0x7026b4, 0x5f7e41, 0x3991d6, 0x398353, 0x39f49c, 0x845f8b, 0xbdf928, 0x3b1ff8,
  0x97ffde, 0x05980f, 0xef2f11, 0x8b5a0a, 0x6d1f6d, 0x367ecf, 0x27cb09, 0xb74f46, 0x3f669e, 0x5fea2d,
  0x7527ba, 0xc7ebe5, 0xf17b3d, 0x0739f7, 0x8a5292, 0xea6bfb, 0x5fb11f, 0x8d5d08, 0x560330, 0x46fc7b,
  0x6babf0, 0xcfbc20, 0x9af436, 0x1da9e3, 0x91615e, 0xe61b08, 0x659985, 0x5f14a0, 0x68408d, 0xffd880,
  0x4d7327, 0x310606, 0x1556ca, 0x73a8c9, 0x60e27b, 0xc08c6b,
];
const PIO2: readonly number[] = [
  1.57079625129699707031, 7.54978941586159635335e-8, 5.39030252995776476554e-15, 3.28200341580791294123e-22,
  1.27065575308067607349e-29, 1.22933308981111328932e-36, 2.73370053816464559624e-44,
  2.16741683877804819444e-51,
];
const JK = 4; // init_jk[1]: double precision
const tx = new Float64Array(3);
const f = new Float64Array(20);
const q = new Float64Array(20);
const fq = new Float64Array(20);
const iq = new Int32Array(20);

// Payne-Hanek reduction for |x| >= 2^20 pi/2 (e_rem_pio2.c's large case and __kernel_rem_pio2 with prec 1).
function remPio2Large(x: number, ix: number): number {
  const e0 = (ix >> 20) - 1046;
  let z = words(ix - (e0 << 20), low(x));
  for (let i = 0; i < 2; i++) {
    tx[i] = z | 0;
    z = (z - at(tx, i)) * TWO24;
  }
  tx[2] = z;
  let nx = 3;
  while (at(tx, nx - 1) === 0) nx--;
  const jx = nx - 1;
  const jv = ((e0 - 3) / 24) | 0; // e0 >= -3 here, so the C's clamp at 0 never applies
  let q0 = e0 - 24 * (jv + 1);
  for (let i = 0, j = jv - jx; i <= jx + JK; i++, j++) f[i] = j < 0 ? 0 : at(IPIO2, j);
  const product = (i: number): number => {
    let fw = 0;
    for (let j = 0; j <= jx; j++) fw += at(tx, j) * at(f, jx + i - j);
    return fw;
  };
  for (let i = 0; i <= JK; i++) q[i] = product(i);
  let jz = JK;
  let n: number;
  let ih: number;
  for (;;) {
    // Distil q[] into 24-bit integers iq[], most significant last.
    z = at(q, jz);
    for (let i = 0, j = jz; j > 0; i++, j--) {
      const fw = (TWON24 * z) | 0;
      iq[i] = z - TWO24 * fw;
      z = at(q, j - 1) + fw;
    }
    z = scalbn(z, q0);
    z -= 8 * floorNonNegative(z * 0.125);
    n = z | 0;
    z -= n;
    ih = 0;
    if (q0 > 0) {
      const i = at(iq, jz - 1) >> (24 - q0);
      n += i;
      iq[jz - 1] = at(iq, jz - 1) - (i << (24 - q0));
      ih = at(iq, jz - 1) >> (23 - q0);
    } else if (q0 === 0) ih = at(iq, jz - 1) >> 23;
    else if (z >= 0.5) ih = 2;
    if (ih > 0) {
      // The fraction is above 1/2: take 1 - fraction, and n + 1.
      n += 1;
      let carry = 0;
      for (let i = 0; i < jz; i++) {
        const j = at(iq, i);
        if (carry !== 0) iq[i] = 0xffffff - j;
        else if (j !== 0) {
          carry = 1;
          iq[i] = 0x1000000 - j;
        }
      }
      if (q0 === 1) iq[jz - 1] = at(iq, jz - 1) & 0x7fffff;
      else if (q0 === 2) iq[jz - 1] = at(iq, jz - 1) & 0x3fffff;
      if (ih === 2) {
        z = 1 - z;
        if (carry !== 0) z -= scalbn(1, q0);
      }
    }
    if (z !== 0) break;
    let j = 0;
    for (let i = jz - 1; i >= JK; i--) j |= at(iq, i);
    if (j !== 0) break;
    // Every word so far is zero: bring in more of 2/pi and distil again.
    let k = 1;
    while (iq[JK - k] === 0) k++;
    for (let i = jz + 1; i <= jz + k; i++) {
      f[jx + i] = at(IPIO2, jv + i);
      q[i] = product(i);
    }
    jz += k;
  }
  if (z === 0) {
    jz -= 1;
    q0 -= 24;
    while (iq[jz] === 0) {
      jz--;
      q0 -= 24;
    }
  } else {
    z = scalbn(z, -q0);
    if (z >= TWO24) {
      const fw = (TWON24 * z) | 0;
      iq[jz] = z - TWO24 * fw;
      jz += 1;
      q0 += 24;
      iq[jz] = fw;
    } else iq[jz] = z;
  }
  let fw = scalbn(1, q0);
  for (let i = jz; i >= 0; i--) {
    q[i] = fw * at(iq, i);
    fw *= TWON24;
  }
  for (let i = jz; i >= 0; i--) {
    fw = 0;
    for (let k = 0; k <= JK && k <= jz - i; k++) fw += at(PIO2, k) * at(q, i + k);
    fq[jz - i] = fw;
  }
  fw = 0;
  for (let i = jz; i >= 0; i--) fw += at(fq, i);
  const sum = fw;
  fw = at(fq, 0) - fw;
  for (let i = 1; i <= jz; i++) fw += at(fq, i);
  const neg = x < 0 !== (ih !== 0);
  head = neg ? -sum : sum;
  tail = neg ? -fw : fw;
  return x < 0 ? -n & 7 : n & 7;
}

/** The sine, after fdlibm's s_sin.c. */
export function sin(x: number): number {
  const ix = high(x) & 0x7fffffff;
  if (ix <= 0x3fe921fb) return ix < 0x3e500000 ? x : kernelSin(x, 0, false);
  if (ix >= 0x7ff00000) return x - x;
  switch (remPio2(x) & 3) {
    case 0:
      return kernelSin(head, tail, true);
    case 1:
      return kernelCos(head, tail);
    case 2:
      return -kernelSin(head, tail, true);
    default:
      return -kernelCos(head, tail);
  }
}

/** The cosine, after fdlibm's s_cos.c. */
export function cos(x: number): number {
  const ix = high(x) & 0x7fffffff;
  if (ix <= 0x3fe921fb) return ix < 0x3e46a09e ? 1 : kernelCos(x, 0);
  if (ix >= 0x7ff00000) return x - x;
  switch (remPio2(x) & 3) {
    case 0:
      return kernelCos(head, tail);
    case 1:
      return -kernelSin(head, tail, true);
    case 2:
      return -kernelCos(head, tail);
    default:
      return kernelSin(head, tail, true);
  }
}
