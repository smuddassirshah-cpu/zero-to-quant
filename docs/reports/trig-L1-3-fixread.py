import math, numpy as np
from fractions import Fraction
D=math.degrees; R=math.radians
# homework-3
u=np.array([3,4.]);v=np.array([5,-12.])
c=u@v/(np.linalg.norm(u)*np.linalg.norm(v)); c2=float(Fraction(3*5+4*-12,5*13))
print('cos',c,c2,D(math.acos(c)), D(math.atan2(u[0]*v[1]-u[1]*v[0],u@v)), 'acute',D(math.acos(-c)))
# de-meaned two-day: always +-1
ud=u-u.mean();vd=v-v.mean();print('2-day demeaned cos',ud@vd/np.linalg.norm(ud)/np.linalg.norm(vd), np.corrcoef(u,v)[0,1])
rng=np.random.default_rng(1); mx=0
for n in (3,10,250,5000):
  for _ in range(200):
    x=rng.normal(0.3,1,n); y=0.4*x+rng.normal(-0.2,1,n)
    a=x-x.mean(); b=y-y.mean()
    mx=max(mx,abs(a@b/np.linalg.norm(a)/np.linalg.norm(b)-np.corrcoef(x,y)[0,1]))
print('max |cos demeaned - corr|',mx)
# raw cosine != correlation in general
x=rng.normal(5,1,5000); y=rng.normal(5,1,5000); print('raw cos indep with mean',x@y/np.linalg.norm(x)/np.linalg.norm(y), np.corrcoef(x,y)[0,1])
# homework-1
s2=.25**2+.2**2-2*.25*.2*math.cos(R(120)); s2b=.25**2+.2**2+2*.5*.25*.2
print('vol',math.sqrt(s2),math.sqrt(s2b),'per pound',math.sqrt(s2)/2, '90:',math.hypot(.25,.2))
C=D(math.acos((.0625+.04-.09)/.1)); print('C',C,180-C)
# simulate £1 each
z=rng.multivariate_normal([0,0],[[.0625,.025],[.025,.04]],2_000_000); print('sim sd of sum',z.sum(1).std(), 'sd of half-half',(z.sum(1)/2).std())
# lake
AB=math.sqrt(60**2+45**2-2*60*45*math.cos(R(55))); print('AB',AB)
sA=45*0.8192/50.27; A=D(math.asin(sA)); print('sinA',sA,A,180-A,180-A+55)
A2=D(math.atan2(45*math.sin(R(55)),60-45*math.cos(R(55)))); print('A exact via coords',A2)
sB=60*0.8192/50.27; B=D(math.asin(sB)); print('B',B,180-B,180-B+55,'true B',180-55-A2)
# ambiguous-case rule test over random SSA: a,b,A -> second solution valid iff A+(180-B)<180
bad=0
for _ in range(200000):
    Aa=rng.uniform(1,179); a=rng.uniform(.1,5); b=rng.uniform(.1,5)
    s=b*math.sin(R(Aa))/a
    if s>=1: continue
    Bx=D(math.asin(s))
    for Bc,rule in ((Bx,Aa+Bx<180),(180-Bx,Aa+180-Bx<180)):
        Cc=180-Aa-Bc
        valid = Cc>0
        if valid:
            c_=a*math.sin(R(Cc))/math.sin(R(Aa))
            # verify triangle truly has sides a,b and angle A via cosine rule
            ok=abs(a*a-(b*b+c_*c_-2*b*c_*math.cos(R(Aa))))<1e-9
            valid=ok
        if valid!=rule: bad+=1
print('SSA rule mismatches',bad)
# others
print('tan35',math.tan(R(35)),'tan15',math.tan(R(15)),12*math.tan(R(15)),12*.26795,12*.2679,12/.26795,12*math.sin(R(15)),12/math.cos(R(15)))
print('pi/2',math.pi/2,'cos120',math.cos(R(120)),'sin 0.8',D(math.asin(.8)), 6000**2+8000**2==10000**2)
print('l5 5,6,7 with 120: c2',25+36-2*30*math.cos(R(120)))
# assertions (exit non-zero if any content number is off)
assert abs(D(math.acos(c))-120.51)<0.005 and abs(c+0.5077)<5e-5
assert mx<1e-12
assert abs(math.sqrt(s2)-0.3905)<5e-5 and abs(math.sqrt(s2)/2-0.195)<5e-4
assert abs(A-47.2)<0.05 and abs(180-A-132.8)<0.05 and 180-A+55>180
# obtuse candidate at B passes the angle-sum test yet is not the lake's B
assert 180-B+55<180 and abs((180-55-A2)-B)<0.1
assert bad==0
assert round(12*.26795,2)==3.22 and round(12*.2679,2)==3.21 and abs(math.tan(R(15))-.26795)<5e-6
assert round(math.pi/2,2)==1.57
print('fixread OK')
