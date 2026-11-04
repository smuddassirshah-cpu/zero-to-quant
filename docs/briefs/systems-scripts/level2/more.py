import sys; sys.path.insert(0,'.')
from interleave import *
def inc(var,k=1): return [(('load','r',var),),(('addi','r',k),),(('store',var,'r'),)]
xr=lambda st:[st['var'].get('x',0)]; xb=lambda V,R:[V.get('x',0)]
# position: +100 and -300 from 500
pr=lambda st:[st['var'].get('pos')]; pb=lambda V,R:[V.get('pos')]
report("position 500, +100 and -300",[inc('pos',100),inc('pos',-300)],{'pos':500},pr,pb,expect_total=20)
# atomic flag check-then-act: both enter?
chk=lambda: [(('load','r','flag'),('ge','r',1,'seen')),(('storeif_enter',),)]
# model: step1: seen = (flag>=1); step2: if not seen: flag=1, entered +=1 (as reg)
# implement with existing micro-ops: ge sets seen=(flag>=1); use 'setif' needs flag true... invert: use ('empty','e','flag') -> e = (flag==0); ('setif','e','in',1); ('storei' guarded?) 
t=[(('empty','e','flag'),),(('setif','e','in',1),('storeif','e','flag','one',-1))]
# storeif sets var = reg - k: reg 'one' = 0 -> var = 0 - (-1) = 1. register 'one' defaults 0.
fr=lambda st:[st['reg'][0].get('in',0)+st['reg'][1].get('in',0)]; fb=lambda V,R:[R[0].get('in',0)+R[1].get('in',0)]
report("atomic flag test then set: how many enter",[t,t],{'flag':0},fr,fb,expect_total=6)
# atomic x = x + 1 as load then store (2 steps)
two=[(('load','r','x'),('addi','r',1)),(('store','x','r'),)]
report("atomic x = x + 1 as separate load and store (2 steps)",[two,two],{'x':0},xr,xb,expect_total=6)
# cv with mutex: consumer lock;check;wait(+unlock) ; producer lock;push;unlock;notify
cons=[(('lock','m'),),(('empty','e','q'),),(('waitif','e'),('unlock','m'))]
prod=[(('lock','m'),),(('fetchadd','q',1),),(('unlock','m'),),(('notify',),)]
nr=lambda st:[]; nb=lambda V,R:[]
report("condition variable with the mutex held across check and wait",[cons,prod],{'q':0},nr,nb)
