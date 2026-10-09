// The function table the expression tests compile against: Math's functions, deterministic per engine only,
// which is all a test of the compiler needs.
import type { ExprFunctions } from '@zq/mathcore/expr';

// The Maclaurin series of erf: within 1.12e-15 relative of mpmath's erf at 8,001 points of [-2, 2]
// [measured]. From |x| = 6 it gives +-1, as the correctly rounded erf does from |x| = 5.93 [measured,
// mpmath], so tests that compare erf or Phi with another implementation stay in |x| <= 2 or |x| >= 6. A zero
// keeps its sign.
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
