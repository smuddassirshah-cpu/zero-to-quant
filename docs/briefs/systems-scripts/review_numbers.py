# Review and homework numbers for levels 1 to 4. Each value is computed by method A (formula) and method B (Fractions, bytes or enumeration).
from fractions import Fraction as F
import struct, math, ctypes as C
def chk(name,a,b,tol=1e-9):
    ok = abs(float(a)-float(b))<=tol*max(1,abs(float(a)))
    print(f"{'OK ' if ok else 'BAD'} {name}: A={a} B={b}"); assert ok
# ---- level 1
walk=30; pages=65536; hit=F(64,pages); cost=100+(1-hit)*walk
chk("HW1 TLB hit rate 4KiB (256 MiB)",64/65536,hit); chk("HW1 per-read cost ns 4KiB",100+(1-64/65536)*30,cost)
pages2=256*2**20//(2*2**20); hit2=F(min(64,pages2),pages2); cost2=100+(1-hit2)*walk
print("   2MiB pages",pages2,"hit",float(hit2),"cost",float(cost2),"saving %",float((cost-cost2)/cost*100))
chk("R6 2 GiB pages",2**31/4096,524288); chk("R6 ms",524288*1e-6*1000,F(524288,1000))
chk("R2 DRAM miss share of 5 us budget %",100/5000*100,F(100,5000)*100)
# ---- level 2
chk("L2 R2 1.5 cores",15e-6*100_000,F(15,10**6)*100000)
chk("L2 H7 shared",8*500_000*60/1e9,F(8*500_000*60,10**9)); chk("L2 H7 ratio",(8*500_000*60)/(500_000*1),480)
chk("L2 l6 sum 1M atomic ms",1_000_000*60/1e6,F(1_000_000*60,10**6)); chk("L2 l6 local ms",250_000*1/1e6,F(250_000,10**6)); chk("ratio",60e6/250e3,240)
chk("L2 924",math.comb(12,6),math.factorial(12)//math.factorial(6)**2); chk("1680",math.factorial(9)//6**3,1680); chk("20",math.comb(6,3),20)
chk("3! orders",math.factorial(3),6)
# ---- level 3
chk("L3 R1 calls",4*2**20/4096,1024); chk("L3 R1 us",1024*0.2,F(1024*2,10))
chk("L3 R1b 8 MiB 4K calls",8*2**20/4096,2048); chk("us",2048*0.2,409.6); chk("64K calls",8*2**20/65536,128); chk("us",128*0.2,25.6)
def feed(chunks,fs=24):
    left=0;frames=0
    for c in chunks: left+=c; frames+=left//fs; left%=fs
    return frames,left
print("   R3 chunks [50,50,50]:",feed([50,50,50]),"; l12 drill [100,50,24,23,1]:",feed([100,50,24,23,1]))
assert feed([50,50,50])==(6,6) and feed([100,50,24,23,1])==(8,6)
# method B: total bytes divmod
print("   B:",divmod(150,24),divmod(198,24))
chk("R5 TCP 40ms RTT first data",1.5*40,60); chk("UDP",0.5*40,20)
chk("R7 BE 0x0100",int.from_bytes(bytes([0,0,1,0]),'big'),256); chk("LE",int.from_bytes(bytes([0,0,1,0]),'little'),65536)
chk("R8 -100 last byte",struct.pack('>i',-100)[3],(2**32-100)&0xFF); print("   bytes",struct.pack('>i',-100).hex())
chk("R9 both lost 2%",1e6*0.02*0.02,F(1,50)**2*10**6); chk("single",1e6*0.02,20000)
chk("H2 RTT 80 TCP",1.5*80,120); chk("UDP",0.5*80,40); chk("held back 50,000/s x 1ms",50_000*0.001,50); chk("200ms",50_000*0.2,10000)
chk("H2 unicast",20*2000*150,6_000_000); chk("mc",2000*150,300_000)
m=(ord('T'),ord('S'),12,300,99,1000,-5,43_200_000)
packed=struct.pack('>BBHIIIiI',*m); print("   HW3 H4 frame",packed.hex(' '))
B=[m[0],m[1]]+[ (12>>8)&255,12&255]
chk("H4 last bytes seq/id/qty/price/time", [packed[7],packed[11],packed[15],packed[19],packed[23]][0], 300&255)
print("   last bytes (decimal): instr",packed[3],"seq",packed[7],"id",packed[11],"qty",packed[15],"price",packed[19],"time",packed[23], " time hex",hex(43_200_000), "12:00:00 check", 12*3600*1000)
chk("H5 100k/s at 10us",1/10e-6,100000); chk("1M/s at 1us",1/1e-6,1_000_000); chk("cores 200k at 10us",200_000*10e-6,F(200000*10,10**6))
chk("L3 batch 61 frames calls/s",200_000/61,F(200000,61)); print("   3278.69 ->",200000/61)
chk("L3 l11 4% core",200_000*0.2e-6,F(200000*2,10**7)) 
# ---- level 4
chk("L4 R3 40 ms",4*50*200_000/1e9*1000,F(4*50*200000,10**9)*1000)
chk("pool 25x",30/1.2,25)
chk("R4 ring size",20-13,7); chk("slot",20&7,4)
chk("R6 mean",(990*10+10*1000)/1000,F(199,10))
chk("R8 budget",1000+200+300+500+500,2500); chk("R8+4 allocs",2500+4*50,2700); chk("slack",3000-2500,500)
chk("R9 1472//24",1472//24,61); chk("remainder",1472%24,8)
chk("H2 pool 1500",1000*1.5,1500); chk("bytes 24",1500*24,36000); chk("32 B",1500*32,48000); print("   KiB",36000/1024,48000/1024)
chk("H2 ring 1ms",200_000*0.001,200); chk("pow2 256",2**math.ceil(math.log2(200)),256); chk("bytes",256*24,6144)
chk("5ms at 1M",1_000_000*0.005,5000); chk("pow2",2**math.ceil(math.log2(5000)),8192); chk("bytes",8192*24,196608); print("   KiB",196608/1024)
chk("wrap s",2**32/10_000_000,429.4967296); print("   =",divmod(429.4967296,60))
# pooled percentile
def p(v,permille): s=sorted(v); n=len(s); return s[max(1,-(-permille*n//1000))-1]
A=[10]*1000; Bv=[10]*970+[1000]*30; pool=A+Bv
print("   pooled p99",p(pool,990),"A p99",p(A,990),"B p99",p(Bv,990),"avg of p99s",(p(A,990)+p(Bv,990))/2)
print("   11 outliers of 1000 pooled? 20 slow B:",p([10]*1000+[10]*980+[1000]*20,990))
# struct with flags
class S(C.Structure): _fields_=[("t",C.c_uint8),("s",C.c_uint8),("i",C.c_uint16),("q",C.c_uint32),("id",C.c_uint32),("qty",C.c_uint32),("px",C.c_int32),("tm",C.c_uint32),("fl",C.c_uint16)]
print("   host struct with u16 flags size",C.sizeof(S),"offset flags",S.fl.offset)
# Handler size via compile
import subprocess,re,os
