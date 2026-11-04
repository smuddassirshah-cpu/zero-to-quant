# Level 1, l3: virtual memory. Method A: shifts and masks. Method B: divmod and hex strings.
def tr_A(table,v,ps=4096):
    p=v>>12; o=v&0xFFF
    if p>=len(table) or table[p]<0: return -1
    return (table[p]<<12)|o
def tr_B(table,v,ps=4096):
    p,o=divmod(v,ps)
    if p>=len(table) or table[p]<0: return -1
    return table[p]*ps+o
tests=[([7,-1,9],0x2A7C),([7,-1,9],0x2A7C-0x2000),([7,-1,9],0x1000),([7,-1,9],0x5000),([7,-1,9],0),([7,-1,9],4095),([7,-1,9],0x2000),([7,-1,9],0x2FFF),([3],4096),([3,5],4096+17),([],0)]
for t,v in tests:
    a=tr_A(t,v); b=tr_B(t,v); assert a==b; print(t,hex(v),v,"->",a,hex(a) if a>=0 else "fault")
# x86-64 4-level split
v=0x00007F3A1C2D5E48
A=[(v>>s)&0x1FF for s in (39,30,21,12)]; off_A=v&0xFFF
b=bin(v)[2:].zfill(64)[-48:]  # 48 bits
B=[int(b[i:i+9],2) for i in (0,9,18,27)]; off_B=int(b[36:],2)
assert A==B and off_A==off_B
print("v",hex(v),"idx",A,"offset",off_A,hex(off_A), "page number", hex(v>>12))
print("bits: 9*4+12 =",9*4+12)
# toy: 16-bit addresses, 1 KiB pages? keep 4 KiB; 
print("TLB reach 64*4KiB", 64*4096//1024,"KiB; 64*2MiB", 64*2,"MiB")
print("pages in 64 MiB (4 KiB):", 64*2**20//4096, " hit prob", 64/(64*2**20//4096), " %", 100*64/(64*2**20//4096))
print("pages in 64 MiB (2 MiB):", 64*2**20//(2*2**20))
print("1 GiB faults", 2**30//4096, "x1us =", 2**30//4096*1e-6*1000,"ms; with 2 MiB pages", 2**30//(2*2**20))
print("worst walk 4 reads x100ns", 4*100)
# fault 1 GiB check B
print((1<<30)/ (1<<12))
