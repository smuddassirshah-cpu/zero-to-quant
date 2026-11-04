# Level 2: every interleaving of small thread programs, two independent ways.
# Method A: recursive enumeration of schedules over mutable dict state.
# Method B: dynamic programming over immutable states counting paths (memoised), different interpreter code.
# IR: a thread is a list of steps; a step is a tuple of micro-ops executed together.
import sys, itertools
from collections import Counter
from functools import lru_cache
sys.setrecursionlimit(10000)
# micro-ops: ('load',reg,var) ('addi',reg,k) ('store',var,reg) ('storei',var,k) ('fetchadd',var,k)
#            ('lock',L) ('unlock',L) ('ge',reg,k,flag) ('storeif',flag,var,reg,k) ('setif',flag,reg,k)
#            ('empty',flag,var) ('waitif',flag) ('notify',) ('popif',var,flagempty,reg)
def enabled_A(st,tid,prog):
    pc=st['pc'][tid]
    if pc>=len(prog[tid]) or st['asleep'][tid]: return False
    for m in prog[tid][pc]:
        if m[0]=='lock' and st['locks'].get(m[1]) is not None: return False
    return True
def step_A(st,tid,prog):
    pc=st['pc'][tid]; reg=st['reg'][tid]
    for m in prog[tid][pc]:
        k=m[0]
        if k=='load': reg[m[1]]=st['var'].get(m[2],0)
        elif k=='addi': reg[m[1]]=reg.get(m[1],0)+m[2]
        elif k=='store': st['var'][m[1]]=reg.get(m[2],0)
        elif k=='storei': st['var'][m[1]]=m[2]
        elif k=='fetchadd': st['var'][m[1]]=st['var'].get(m[1],0)+m[2]
        elif k=='lock': st['locks'][m[1]]=tid
        elif k=='unlock': st['locks'][m[1]]=None
        elif k=='ge': reg[m[3]]=reg.get(m[1],0)>=m[2]
        elif k=='storeif':
            if reg.get(m[1]): st['var'][m[2]]=reg.get(m[3],0)-m[4]
        elif k=='setif':
            if reg.get(m[1]): reg[m[2]]=m[3]
        elif k=='empty': reg[m[1]]=(st['var'].get(m[2],0)==0)
        elif k=='waitif':
            if reg.get(m[1]):
                st['asleep'][tid]=True
        elif k=='notify':
            for t in range(len(prog)):
                if st['asleep'][t]:
                    st['asleep'][t]=False
        elif k=='popif':
            reg[m[3]]=1 if st['var'].get(m[1],0)>0 else 0
        else: raise ValueError(k)
    st['pc'][tid]=pc+1
def clone(st): return dict(pc=list(st['pc']),var=dict(st['var']),reg=[dict(r) for r in st['reg']],locks=dict(st['locks']),asleep=list(st['asleep']))
def enumerate_A(prog,var0,outcome):
    res=Counter(); n=[0]
    def rec(st):
        ts=[t for t in range(len(prog)) if enabled_A(st,t,prog)]
        if not ts:
            done=all(st['pc'][t]>=len(prog[t]) for t in range(len(prog))) and not any(st['asleep'])
            if done: res[('done',)+tuple(outcome(st))]+=1
            else: res[('stuck',)+tuple(outcome(st))]+=1
            n[0]+=1; return
        for t in ts:
            s2=clone(st); step_A(s2,t,prog); rec(s2)
    rec(dict(pc=[0]*len(prog),var=dict(var0),reg=[{} for _ in prog],locks={},asleep=[False]*len(prog)))
    return res
# ---- method B: tuple state, DP
def enumerate_B(prog,var0,outcome_names,outcome_fn):
    T=len(prog)
    def freeze(d): return tuple(sorted(d.items()))
    @lru_cache(maxsize=None)
    def go(pcs,var,regs,locks,asleep):
        V=dict(var); R=[dict(r) for r in regs]; L=dict(locks)
        moves=[]
        for t in range(T):
            if pcs[t]>=len(prog[t]) or asleep[t]: continue
            if any(m[0]=='lock' and L.get(m[1]) is not None for m in prog[t][pcs[t]]): continue
            moves.append(t)
        if not moves:
            fin=all(pcs[t]>=len(prog[t]) for t in range(T)) and not any(asleep)
            return Counter({(('done' if fin else 'stuck'),)+tuple(outcome_fn(V,R)):1})
        tot=Counter()
        for t in moves:
            V2=dict(V); R2=[dict(r) for r in R]; L2=dict(L); A2=list(asleep)
            for m in prog[t][pcs[t]]:
                op=m[0]
                if op=='load': R2[t][m[1]]=V2.get(m[2],0)
                elif op=='addi': R2[t][m[1]]=R2[t].get(m[1],0)+m[2]
                elif op=='store': V2[m[1]]=R2[t].get(m[2],0)
                elif op=='storei': V2[m[1]]=m[2]
                elif op=='fetchadd': V2[m[1]]=V2.get(m[1],0)+m[2]
                elif op=='lock': L2[m[1]]=t
                elif op=='unlock': L2[m[1]]=None
                elif op=='ge': R2[t][m[3]]=(R2[t].get(m[1],0)>=m[2])
                elif op=='storeif':
                    if R2[t].get(m[1]): V2[m[2]]=R2[t].get(m[3],0)-m[4]
                elif op=='setif':
                    if R2[t].get(m[1]): R2[t][m[2]]=m[3]
                elif op=='empty': R2[t][m[1]]=(V2.get(m[2],0)==0)
                elif op=='waitif':
                    if R2[t].get(m[1]): A2[t]=True
                elif op=='notify':
                    A2=[False]*T
                elif op=='popif': R2[t][m[3]]=1 if V2.get(m[1],0)>0 else 0
            pcs2=list(pcs); pcs2[t]+=1
            tot+=go(tuple(pcs2),freeze(V2),tuple(freeze(r) for r in R2),freeze(L2),tuple(A2))
        return tot
    return go(tuple([0]*T),freeze(var0),tuple(freeze({}) for _ in range(T)),freeze({}),tuple([False]*T))
def report(name,prog,var0,outA,outB_fn,expect_total=None):
    A=enumerate_A(prog,var0,outA)
    B=enumerate_B(prog,var0,None,outB_fn)
    assert A==B,(name,A,B)
    total=sum(A.values())
    print(f"== {name}: {total} complete schedules")
    for k,v in sorted(A.items(),key=lambda kv:str(kv[0])): print("   ",k,v)
    if expect_total: assert total==expect_total,(total,expect_total)
    return A
def inc(var,k=1): return [(('load','r',var),),(('addi','r',k),),(('store',var,'r'),)]
if __name__=="__main__":
    xr=lambda st:[st['var'].get('x',0)]
    xb=lambda V,R:[V.get('x',0)]
    report("counter 2 threads",[inc('x'),inc('x')],{'x':0},xr,xb,expect_total=20)   # 6!/(3!3!)
    report("counter 3 threads",[inc('x'),inc('x'),inc('x')],{'x':0},xr,xb,expect_total=1680) # 9!/(3!)^3
    tr=lambda st:[st['var'].get('total',0)]; tb=lambda V,R:[V.get('total',0)]
    report("partial sums 10 and 26",[inc('total',10),inc('total',26)],{'total':0},tr,tb,expect_total=20)
    atm=lambda g: [(( 'load','r','bal'),('ge','r',80,'ok')),(('storeif','ok','bal','r',80),('setif','ok','got',80))]
    ar=lambda st:[st['var'].get('bal'),st['reg'][0].get('got',0)+st['reg'][1].get('got',0)]
    ab=lambda V,R:[V.get('bal'),R[0].get('got',0)+R[1].get('got',0)]
    report("ATM 2 withdrawals of 80 from 100",[atm(1),atm(2)],{'bal':100},ar,ab,expect_total=6)
    mu=[(('lock','m'),),(('load','r','x'),),(('addi','r',1),),(('store','x','r'),),(('unlock','m'),)]
    report("mutex counter 2 threads",[mu,mu],{'x':0},xr,xb)
    af=[(('fetchadd','x',1),)]
    report("atomic counter 2 threads",[af,af],{'x':0},xr,xb,expect_total=2)
    report("atomic counter 3 threads",[af,af,af],{'x':0},xr,xb,expect_total=6)
    pubw=[(('storei','data',42),),(('storei','ready',1),)]; pubr=[(('load','r1','ready'),),(('load','r2','data'),)]
    pr=lambda st:[st['reg'][1]['r1'],st['reg'][1]['r2']]; pb=lambda V,R:[R[1]['r1'],R[1]['r2']]
    report("publication, data then ready (SC)",[pubw,pubr],{},pr,pb,expect_total=6)
    pubw2=[(('storei','ready',1),),(('storei','data',42),)]
    report("publication, ready then data (SC, wrong order)",[pubw2,pubr],{},pr,pb,expect_total=6)
    sb1=[(('storei','x',1),),(('load','r1','y'),)]; sb2=[(('storei','y',1),),(('load','r2','x'),)]
    sr=lambda st:[st['reg'][0]['r1'],st['reg'][1]['r2']]; sbf=lambda V,R:[R[0]['r1'],R[1]['r2']]
    report("store buffering (SC)",[sb1,sb2],{},sr,sbf,expect_total=6)
    # deadlock
    nr=lambda st:[]; nb=lambda V,R:[]
    t1=[(('lock','A'),),(('lock','B'),),(('unlock','B'),),(('unlock','A'),)]
    t2=[(('lock','B'),),(('lock','A'),),(('unlock','A'),),(('unlock','B'),)]
    report("two locks, opposite order",[t1,t2],{},nr,nb)
    t2s=[(('lock','A'),),(('lock','B'),),(('unlock','B'),),(('unlock','A'),)]
    report("two locks, same order",[t1,t2s],{},nr,nb)
    c1=[(('lock','A'),),(('lock','B'),),(('unlock','B'),),(('unlock','A'),)]
    c2=[(('lock','B'),),(('lock','C'),),(('unlock','C'),),(('unlock','B'),)]
    c3=[(('lock','C'),),(('lock','A'),),(('unlock','A'),),(('unlock','C'),)]
    report("three locks in a ring",[c1,c2,c3],{},nr,nb)
    c3f=[(('lock','A'),),(('lock','C'),),(('unlock','C'),),(('unlock','A'),)]
    report("three locks, ring broken by ordering",[c1,c2,c3f],{},nr,nb)
    # lost wakeup: consumer checks, waits; producer pushes then notifies
    cons=[(('empty','e','q'),),(('waitif','e'),)]
    prod=[(('fetchadd','q',1),),(('notify',),)]
    cr=lambda st:[st['reg'][0].get('got',0)]; cb=lambda V,R:[R[0].get('got',0)]
    report("lost wakeup: check, then wait, no lock",[cons,prod],{'q':0},cr,cb,expect_total=6)
