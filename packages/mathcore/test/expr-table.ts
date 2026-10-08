// The function table the expression tests compile against: Math's functions, deterministic per engine only,
// which is all a test of the compiler needs.
import type { ExprFunctions } from '@zq/mathcore/expr';

// The Maclaurin series of erf, within about 1e-15 for |x| <= 2 [inferred]: tests that compare erf or Phi with
// another implementation stay in that range.
function erf(x: number): number {
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
  sqrt: (x) => Math.sqrt(x),
  cbrt: (x) => Math.cbrt(x),
  erf,
  Phi: (x) => (1 + erf(x / Math.SQRT2)) / 2,
  phi: (x) => Math.exp((-x * x) / 2) / Math.sqrt(2 * Math.PI),
  atan2: (y, x) => Math.atan2(y, x),
  pow: (x, y) => Math.pow(x, y),
};
