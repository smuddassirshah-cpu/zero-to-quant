# Level 1, l1: latency numbers. Method A: floats. Method B: integer picoseconds and Fractions.
from fractions import Fraction as F
ns = {"L1":1,"L2":4,"L3":20,"DRAM":100,"NVMe":100_000,"disk seek":10_000_000,"DC RTT":500_000,"London-NY RTT":60_000_000}
print("== human scale: 1 ns -> 1 s (method A, seconds)")
def hms(s):
    d,r=divmod(s,86400); h,r=divmod(r,3600); m,sec=divmod(r,60); return f"{d:g} d {h:g} h {m:g} min {sec:g} s"
for k,v in ns.items(): print(f"{k:14s} {v:>12,} ns -> {v:>12,} s = {hms(v)} = {v/86400:.2f} days = {v/86400/365:.3f} years")
print("== method B (Fractions, picoseconds)")
for k,v in ns.items():
    ps=F(v)*1000; secs=ps/1000
    print(k, "days", float(secs/86400), "years365", float(secs/86400/365))
print("== ratios")
print("DRAM/L1", ns["DRAM"]/ns["L1"], "NVMe/DRAM", ns["NVMe"]/ns["DRAM"], "disk/NVMe", ns["disk seek"]/ns["NVMe"], "NY/DC", ns["London-NY RTT"]/ns["DC RTT"], "NY/DRAM", ns["London-NY RTT"]/ns["DRAM"])
print("== feed budget")
rate=200_000; budget_ns=1e9/rate; print("budget ns", budget_ns, "DRAM misses", budget_ns/100, "L1 hits", budget_ns/1)
print("Fraction", F(10**9,rate), F(10**9,rate)/100)
print("== light")
c=299_792.458; fib=200_000
for name,km in (("London-New York",5570),("London-Frankfurt",640)):
    print(name, km, "fibre RTT ms", 2*km/fib*1000, "vacuum/air RTT ms", 2*km/c*1000, "diff", 2*km/fib*1000-2*km/c*1000)
    # method B: time = distance / speed in microseconds using integers
    print("  fibre RTT us", F(2*km*10**6, fib), "air RTT us", float(F(2*km*10**6*1000, 299792458)))
print("== cycles at 3 GHz: 1 cycle ns", 1/3, " L1 4 cycles", 4/3, "DRAM 100 ns in cycles", 100*3)
print("== reading 1 MiB: syscalls 4 KiB vs 64 B at 0.2 us")
for chunk in (4096,64): n=2**20//chunk; print(chunk, n, n*0.2, "us")
