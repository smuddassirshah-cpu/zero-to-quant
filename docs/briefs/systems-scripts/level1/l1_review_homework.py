# Review and homework numbers for level 1. Each is computed by method A here and checked by method B inline.
import sys; sys.path.insert(0,'.'); sys.path.insert(0,'../cpp')
from l2_cache import simA, simB
from problems_l1 import tr, size_of, best, mp
D=8
# R: stride 4 over 64 doubles in a big cache
ad=[D*i for i in range(0,64,4)]; print("stride4 over 64 doubles:",len(ad),"accesses",simA(ad,1<<20,1<<20),"misses (A)",simB(ad,1<<20,1<<20),"(B); lines touched", len({a//64 for a in ad}))
# R: stride 3 over 96 doubles
ad=[D*i for i in range(0,96,3)]; print("stride3 over 96:",len(ad),simA(ad,1<<20,1<<20),simB(ad,1<<20,1<<20), len({a//64 for a in ad}))
# R: translate
t=[5,2,-1,8]; print("translate 0x3B10",tr(t,0x3B10), 8*4096+0xB10, "fault 0x2000:",tr(t,0x2000),"0x3B10 hex",hex(tr(t,0x3B10)))
# R: struct u8,u16,u8,u32,u8
s=[1,2,1,4,1]; print("struct",s,size_of(s),"best",best(s))
# R: history TTTN x4
h="TTTN"*4; print(h,mp(h)); h="TTTTTTTN"*2; print(h,mp(h))
# R: 8x8 col-major etc already. 
# R: 512-entry matrix? L1 32 KiB holds 512 lines; array of 100,000 doubles sum: lines
print("100,000 doubles lines", -(-100000//8), "misses at 100 ns ms", -(-100000//8)*100e-6)
# R: homework: cost model row vs col N=1000: misses * 100 ns
print("N=1000 row ms", 125000*100e-6, "col ms", 1000000*100e-6)
# R: one million orders 32B vs 24B per 64B line; orders scanned in 1 pass: lines
print("lines 32B", 10**6*32/64, "24B", 10**6*24/64, "misses ratio", 24/32)
# HW: Order book of 1000 levels each {double price; uint32 qty; char side}: size
print("level struct double,u32,u8 :", size_of([8,4,1]), "best", best([8,4,1]), "per line", 64//size_of([8,4,1]))
# HW: page walk
print("walk 4 reads 100ns=",4*100,"ns; fraction of 1 us fault", 1000/400)
# HW: how many 4 KiB pages for 3 GiB reserve at start; faults ms
for gib in (1,3): print(gib,"GiB faults",gib*2**30//4096,"ms",gib*2**30//4096/1000)
# HW: 2 MiB pages: pages needed for 3 GiB
print("2MiB pages for 3 GiB", 3*2**30//(2*2**20), "TLB reach 64*2MiB MiB", 64*2)
# TLB reach for 1536 entries 4 KiB: 
print("1536*4KiB MiB", 1536*4096/2**20)
