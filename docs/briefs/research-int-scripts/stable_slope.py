"""research-int l18 and E8 drill: a slope on a large offset. Method A: exact Fractions. Method B: centred float64 and naive float64 sums."""
from fractions import Fraction as F
import numpy as np
from chk import two, done
xs = [1e9+1, 1e9+2, 1e9+3]; ys = [1.0, 3.0, 2.0]; n = 3
ex = (n*sum(F(a)*F(b) for a, b in zip(xs, ys))-sum(F(a) for a in xs)*sum(F(b) for b in ys))/(n*sum(F(a)**2 for a in xs)-sum(F(a) for a in xs)**2)
mx, my = sum(xs)/n, sum(ys)/n
cen = sum((a-mx)*(b-my) for a, b in zip(xs, ys))/sum((a-mx)**2 for a in xs)
naive = None
two("exact slope is 1/2", float(ex), 0.5, 1e-15); two("centred float64 slope", cen, 0.5, 1e-9); two("numpy polyfit slope", float(np.polyfit(np.array(xs)-1e9, ys, 1)[0]), 0.5, 1e-9)
den_ = n*sum(a*a for a in xs)-sum(xs)**2; num_ = n*sum(a*b for a, b in zip(xs, ys))-sum(xs)*sum(ys)
print("     naive float64: numerator", num_, " denominator", den_, " (zero denominator over a non-zero numerator gives inf in numpy, never 0.5)")
with np.errstate(all="ignore"): two("naive numpy slope is inf or NaN, never 0.5", float(not np.isfinite(np.float64(num_)/np.float64(den_))), 1.0)
two("intercept exact", float(F(sum(F(b) for b in ys), n)-ex*F(sum(F(a) for a in xs), n)), -499999999.0, 1e-6)
done()
