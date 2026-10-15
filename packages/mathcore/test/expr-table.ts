// The function table the expression tests compile against: Math's functions, deterministic per engine only,
// which is all a test of the compiler needs.
import type { ExprFunctions } from '@zq/mathcore/expr';

// The Maclaurin series of erf, against mpmath's erf at 50 digits [measured]:
// - |x| <= 2: within 1.82e-15 relative, over 20,001 even points and 200,000 random doubles of [0, 2] (the
//   series is odd, so [-2, 0] is the same).
// - 2 < |x| < 6: worse as |x| grows, until it is wrong. The relative error first passes 1e-12 at 3.44 and
//   1e-6 at 4.42; the value is negative from 4.955, so erf(5) gives -2.0004 and erf(5.9) -1.34e9.
// - |x| >= 6: +-1, as the correctly rounded erf is from 5.921587195794507, the least double where it rounds
//   to 1.
// So a test that compares erf with another implementation stays in |x| <= 2 or |x| >= 6. Phi takes erf at
// x / sqrt(2): within 6.4e-16 relative on [0, 2.82] and 2.2e-13 on [-2.82, 0), where 1 + erf cancels; beyond
// that it degrades as erf does (Phi(6) is 3.9e-9 out, Phi(-6) four times too large, Phi(8) -4.25e6), and
// from |x| = 8.49 it gives 1 or 0, the 0 below a true Phi that is positive. So a test of Phi stays in
// |x| <= 2.82 or x >= 8.49. A zero keeps its sign.
function erf(x: number): number {
  if (x === 0 || !(Math.abs(x) < 6)) return x === 0 ? x : Math.sign(x);
  let term = x;
  let sum = x;
  for (let n = 1; n < 60; n++) {
    term *= (-x * x) / n;
    sum += term / (2 * n + 1);
  }
  return (2 / Math.sqrt(Math.PI)) * sum;
}

export const MATH: ExprFunctions = {
  sin: (x) => Math.sin(x),
  cos: (x) => Math.cos(x),
  tan: (x) => Math.tan(x),
  asin: (x) => Math.asin(x),
  acos: (x) => Math.acos(x),
  atan: (x) => Math.atan(x),
  sinh: (x) => Math.sinh(x),
  cosh: (x) => Math.cosh(x),
  tanh: (x) => Math.tanh(x),
  exp: (x) => Math.exp(x),
  ln: (x) => Math.log(x),
  log10: (x) => Math.log10(x),
  cbrt: (x) => Math.cbrt(x),
  erf,
  Phi: (x) => (1 + erf(x / Math.SQRT2)) / 2,
  phi: (x) => Math.exp((-x * x) / 2) / Math.sqrt(2 * Math.PI),
  atan2: (y, x) => Math.atan2(y, x),
  pow: (x, y) => Math.pow(x, y),
};
