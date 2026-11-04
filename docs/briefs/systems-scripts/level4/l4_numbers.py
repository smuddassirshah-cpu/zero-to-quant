# Level 4 numbers. Method A: floats. Method B: Fractions or enumeration.
from fractions import Fraction as F
print("malloc 50 ns x 3 per message x 200,000/s =", 50e-9*3*200_000*1000,"ms per second;", F(50*3*200_000,10**9)*1000)
print("pool 2 ns x 3 x 200,000 =", 2e-9*3*200_000*1000,"ms per second")
budget=[("NIC to user buffer",1000),("decode",200),("book update",300),("strategy",500),("encode and send",500)]
tot=sum(v for _,v in budget); print("budget total ns",tot, "us",tot/1000)
for name,extra in (("with 4 mallocs at 50 ns",4*50),("with one 5 us stall",5000)): print(name,tot+extra)
print("target 3 us slack", 3000-tot)
print("ring of 4: capacity", 4, "mask", 4-1, "index of counter 5:", 5&3, " 5%4:",5%4)
print("counter wrap: uint32 max+1 -> 0: 2^32 =",2**32, "ops at 10M/s until wrap s =", 2**32/10_000_000)
print("hist buckets: 10 ns -> bucket", 10 .bit_length()-1, "upper", 2**(10 .bit_length()), " 1000 ns -> bucket", 1000 .bit_length()-1, "upper", 2**(1000 .bit_length()))
print("mean of 990x10 + 10x1000:", (990*10+10*1000)/1000, " F:", F(990*10+10*1000,1000))
print("12 per message ... feed handler: 200,000 msgs/s x 24 B =", 200_000*24/1e6,"MB/s;  at 1 M msgs/s", 1_000_000*24/1e6)
print("open-loop vs closed-loop stall: 1 s stall, one request per 10 us -> delayed requests", 1/10e-6)
# open loop latencies after a 1 s stall, 10 s run, 1,000,000 requests at 10 us spacing, service 10 us when not backlogged
N=1_000_000; stall=100_000  # requests intended during the stall
lat=[10.0]*(N-stall)+[1_000_000-10*k for k in range(stall)]  # us: 1 s down to 10 us
import math
def p(v,q10): s=sorted(v); n=len(s); return s[max(1,-(-(q10*n)//1000))-1]
for q in (500,900,990,999): print("open loop p",q/10, p(lat,q))
closed=[10.0]*(N-1)+[1_000_000.0]
for q in (500,990,999,999.9 if False else 1000): print("closed loop p",q/10, p(closed,q))
print("open mean us", sum(lat)/N, "closed mean", sum(closed)/N)
