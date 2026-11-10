from fractions import Fraction as F
from math import comb, log
from itertools import product, combinations
import random
# d4 vs d6
pay=sum(1 for f in range(1,5) for s in range(1,7) if not f>s)
print('d4 pay', F(pay,24)*12, 'sgtf',F(sum(1 for f in range(1,5) for s in range(1,7) if s>f),24)*12)
# tetra
n=1
while 1-F(15,16)**n<=F(9,10): n+=1
print('tetra n',n, float(1-F(15,16)**36), float(1-F(15,16)**35), float(1-F(15,16)**15), float(1-F(15,16)**11), log(.1)/log(15/16))
print('adding', min(k for k in range(1,99) if F(k,16)>F(9,10)))
# breach
for k in range(3,9): print('breach',k, float(1-F(comb(11,k),comb(15,k))), float(F(comb(11,k),comb(15,k))))
print('adding',min(k for k in range(1,99) if F(4*k,15)>F(9,10)),'replace',min(k for k in range(1,99) if 1-F(11,15)**k>F(9,10)))
print(comb(11,6),comb(15,6))
# sim breach
random.seed(1); N=200000; c=0
for _ in range(N):
    s=random.sample(range(15),6); c+= any(x<4 for x in s)
print('sim6',c/N)
# ace king
T=comb(52,5); print(T, T-comb(48,5), T-comb(44,5), 2*(T-comb(48,5))-(T-comb(44,5)), T-2*comb(48,5)+comb(44,5))
print(0.100179*T, 0.341158**2*T, (T-comb(48,5))**2/T, 260360/T)
# short deck
deck=[(r,s) for r in range(5) for s in range(4)]
from collections import Counter
cl=Counter()
for h in combinations(deck,4):
    cl[tuple(sorted(Counter(r for r,_ in h).values()))]+=1
print(cl)
# dealer calls
p1=F(4,10); p2=F(6,10)*F(4,9); p3=F(6,10)*F(5,9)*F(4,8)
print('dealer',p2/(p2+p3), float(p2/(p2+p3)), float(p2/(p1+p2+p3)), float(p3/(p2+p3)), .24/.384, p1+p2+p3)
# enumerate orders
from itertools import permutations
cnt=Counter()
for perm in permutations(range(10),3):
    first=next((i for i,x in enumerate(perm) if x<4),None)
    cnt[first]+=1
print(cnt, F(cnt[1],cnt[1]+cnt[2]))
# bad ticks
e=F(2,100); a=e*F(95,100); g=(1-e)*F(4,100)
print('bt', float(a+g), float(a/(a+g)), float(e+F(4,100)))
ab=a*F(70,100); gb=g*F(1,100)
print(float(ab/(ab+gb)), float(ab/gb), float(gb/(ab+gb)), gb*10**6, ab*10**6, float(gb/ab), 33.9/34.9, 33.93/34.93, 1e6*.04*.01, 980000*.04)
print('product',float(a/(a+g))*0.7, 'skipped', float(e*F(7,10)/(e*F(7,10)+(1-e)*F(1,100))))
# three loans
t=F(1,4)*F(28,100)**3+F(3,4)*F(4,100)**3; print(float(t), float(t/F(1,1000)), float(F(1,1000)/t), float(t-F(1,1000)), (0.28**3+0.04**3)/0.001)
# desks
st=list(product([0,1],repeat=3))
A=[s for s in st if s[0]==s[1]]; B=[s for s in st if s[0]==s[2]]; C=[s for s in st if s[1]==s[2]]
def P(*ev): return F(len(set.intersection(*[set(e) for e in ev])),8)
print('desks',P(A),P(B),P(C),P(A,B),P(A,C),P(B,C),P(A,B,C), float(1-F(3,4)**8), float(1-F(7,8)**8), float(F(3,4)**8))
# others
print(180/456, .06/.51, 3/17, 9/17, 54/71, 16/46, 16/31, 153.4/248, 4*.65**3*.35, .65**3*.35, 1-.65**4, .3/.475)
