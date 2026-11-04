# Level 2 round-figure costs (assumptions, not measurements). Method A: floats. Method B: Fractions of nanoseconds.
from fractions import Fraction as F
print("thread per message: 15 us x 200,000/s =", 15e-6*200_000, "cores;", F(15,10**6)*200_000)
print("stack 8 MiB x 1,000 threads =", 8*1000/1024, "GiB virtual;", F(8*1000,1024))
print("partial sums: 1..4 =",sum(range(1,5)),"5..8 =",sum(range(5,9)),"total",sum(range(1,9)))
n=4*1_000_000
print("4 threads x 1,000,000 increments, total", n)
for name,ns in (("mutex uncontended 25 ns",25),("atomic uncontended 5 ns",5),("atomic contended 60 ns",60),("mutex contended with sleep 5,000 ns",5000),("per-thread local 1 ns",1)):
    print(f"  all serialised at {name}: {n*ns/1e9:.4f} s ; as Fraction {F(n*ns,10**9)}")
print("per-thread local counters in parallel: 1,000,000 x 1 ns =", 1_000_000*1/1e9*1000,"ms plus merge of 4 adds")
print("ratio contended atomic vs local: ",(n*60)/(1_000_000*1))
print("false sharing: 60 ns vs 1 ns per increment ->",60/1)
print("wake from sleep 5 us vs spin 0.1 us ->", 5/0.1, "x ; spin burns 1 core =", 1.0)
print("lock-order graph 3-lock ring paths A->B,B->C,C->A cycle length 3")
