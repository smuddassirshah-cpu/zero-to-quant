import sympy as sp, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
t=sp.symbols('t',positive=True)
ok=True
def chk(name,cond,info=''):
    global ok; ok&=bool(cond); print('PASS' if cond else 'FAIL',name,info)
# pension
B=sp.Function('B')
sol=sp.dsolve(B(t).diff(t)-sp.Rational(4,100)*B(t)-2000*sp.exp(sp.Rational(2,100)*t),B(t),ics={B(0):0}).rhs
b10=float(sol.subs(t,10))
n=solve_ivp(lambda t,y:0.04*y+2000*np.exp(0.02*t),(0,10),[0],rtol=1e-11,atol=1e-9).y[0,-1]
chk('B(10) cont',abs(b10-27042.19)<0.005 and abs(n-b10)<0.01,(b10,n))
for lab,r,g in [('yearly 4%, cont 2%',np.log(1.04),0.02),('yearly both',np.log(1.04),np.log(1.02))]:
    v=solve_ivp(lambda t,y:r*y+2000*np.exp(g*t),(0,10),[0],rtol=1e-11,atol=1e-9).y[0,-1]
    cf=2000*(np.exp(r*10)-np.exp(g*10))/(r-g); print(' ',lab,round(v,2),round(cf,2))
chk('flat slip',abs(50000*(np.exp(.4)-1)-24591.23)<.005); chk('no-interest',abs(100000*(np.exp(.2)-1)-22140.28)<.005)
# lending
m=sp.symbols('m'); f=-m**2+8*m-12
chk('f>0 on (2,6)',sp.solveset(f>0,m,sp.S.Reals)==sp.Interval.open(2,6))
chk("f'",(f.diff(m).subs(m,2),f.diff(m).subs(m,6))==(4,-4))
r=solve_ivp(lambda t,y:-y**2+8*y-12,(0,20),[2.5],rtol=1e-11,atol=1e-12,dense_output=True)
ys=r.sol(np.linspace(0,20,20001))[0]
chk('monotone, <6, ->6',np.all(np.diff(ys)>=-1e-9) and ys.max()<6+1e-8 and abs(ys[-1]-6)<1e-6,(ys.max(),))
mex=(2+6*sp.Rational(1,7)*sp.exp(4*t))/(1+sp.Rational(1,7)*sp.exp(4*t))
chk('closed form solves ODE',sp.simplify(mex.diff(t)-f.subs(m,mex))==0 and mex.subs(t,0)==sp.Rational(5,2))
chk('6-m = 4/(1+e^{4t}/7) > 0',sp.simplify(6-mex-4/(1+sp.exp(4*t)/7))==0)
# yield gaps
A=sp.Matrix([[-7,2],[-6,1]]); chk('eig',A.eigenvals()=={-1:1,-5:1})
X=sp.exp(A*t)*sp.Matrix([4,2]); X=X.applyfunc(sp.simplify); print(' ',list(X))
zx=sp.solve(X[0],t); zy=sp.solve(X[1],t); print(' ',zx,zy,[float(z) for z in zx+zy])
chk('zeros',len(zx)==1 and len(zy)==1 and abs(float(zx[0])-0.402)<5e-4 and abs(float(zy[0])-0.128)<5e-4)
An=np.array(A,float); r=solve_ivp(lambda t,y:An@y,(0,12),[4,2],rtol=1e-12,atol=1e-14,dense_output=True)
T=np.linspace(0,12,240001); Y=r.sol(T)*np.exp(T)
sc=[int(np.sum(np.diff(np.sign(Y[i]))!=0)) for i in (0,1)]
chk('one sign change each (numeric)',sc==[1,1],(sc,brentq(lambda s:r.sol(s)[0],0,1),brentq(lambda s:r.sol(s)[1],0,1)))
rng=np.random.default_rng(1); worst=0; TT=np.linspace(0,6,6001)
for _ in range(2000):
    y0=rng.normal(size=2); rr=solve_ivp(lambda t,y:An@y,(0,6),y0,rtol=1e-11,atol=1e-15,dense_output=True)
    Z=rr.sol(TT)*np.exp(TT)
    for i in (0,1):
        z=Z[i][np.abs(Z[i])>1e-5]; worst=max(worst,int(np.sum(np.diff(np.sign(z))!=0)))
chk('random starts: <=1 crossing per gap',worst<=1,worst)
# dose
D=sp.Matrix([[-6,0],[6,sp.Rational(-1,2)]]); chk('dose eig',D.eigenvals()=={-6:1,sp.Rational(-1,2):1})
g0=sp.symbols('g0',positive=True); G=sp.exp(D*t)*sp.Matrix([g0,0]); bt=sp.simplify(G[1])
tp=sp.solve(bt.diff(t),t); print('  b(t)=',bt,' peak',tp,float(tp[0]),float(sp.log(12)/5.5))
chk('peak ln12/5.5',abs(float(tp[0])-np.log(12)/5.5)<1e-12)
rd=solve_ivp(lambda t,y:[-6*y[0],6*y[0]-.5*y[1]],(0,24),[100,0],rtol=1e-11,atol=1e-12,dense_output=True)
T=np.linspace(0,24,240001); bb=rd.sol(T)[1]
chk('numeric peak; b rises first',abs(T[bb.argmax()]-np.log(12)/5.5)<2e-4 and bb[100]>bb[0],T[bb.argmax()])
raise SystemExit(0 if ok else 1)
