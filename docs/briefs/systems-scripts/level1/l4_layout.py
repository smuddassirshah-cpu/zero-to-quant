# Level 1, l4: struct layout. Method A: hand algorithm. Method B: ctypes (x86-64). Method C: clang wasm32 static_assert.
import ctypes as C, subprocess, itertools
T={"u8":(C.c_uint8,1),"u16":(C.c_uint16,2),"u32":(C.c_uint32,4),"i32":(C.c_int32,4),"u64":(C.c_uint64,8),"f64":(C.c_double,8),"i8":(C.c_int8,1)}
def hand(fields):
    off=0; offs=[]; mx=1
    for _,t in fields:
        sz=T[t][1]; off=(off+sz-1)//sz*sz; offs.append(off); off+=sz; mx=max(mx,sz)
    size=(off+mx-1)//mx*mx
    return offs,size
def ct(fields):
    class S(C.Structure): _fields_=[(n,T[t][0]) for n,t in fields]
    return [getattr(S,n).offset for n,_ in fields], C.sizeof(S)
cases={
 "char,double,char":[("a","u8"),("b","f64"),("c","u8")],
 "double,char,char":[("b","f64"),("a","u8"),("c","u8")],
 "int,double,int":[("a","u32"),("b","f64"),("c","u32")],
 "double,int":[("a","f64"),("b","u32")],
 "u16,u8":[("a","u16"),("b","u8")],
 "order_bad":[("type","u8"),("seq","u32"),("side","u8"),("id","u32"),("instr","u16"),("qty","u32"),("price","i32"),("time","u32")],
 "order_sorted":[("seq","u32"),("id","u32"),("qty","u32"),("price","i32"),("time","u32"),("instr","u16"),("type","u8"),("side","u8")],
 "wire_order":[("type","u8"),("side","u8"),("instr","u16"),("seq","u32"),("id","u32"),("qty","u32"),("price","i32"),("time","u32")],
 "u8,u64,u8,u16":[("a","u8"),("b","u64"),("c","u8"),("d","u16")],
 "u8x3,u32":[("a","u8"),("b","u8"),("c","u8"),("d","u32")],
}
for k,f in cases.items():
    a=hand(f); b=ct(f); assert a==b,(k,a,b); print(f"{k:18s} offsets={a[0]} size={a[1]}")
# size_of/best_size on size lists (alignment = size)
def size_of(sizes):
    off=0;mx=1
    for s in sizes: off=(off+s-1)//s*s+s; mx=max(mx,s)
    return (off+mx-1)//mx*mx if sizes else 0
def best(sizes): return size_of(sorted(sizes,reverse=True))
for sz in ([1,8,1],[1,4,1,4,2,4,4,4],[],[1],[2,1],[8,1],[1,1,1,4],[4,1,2,1,8],[1,2,4,8,1,2,4,8],[1,8,1,8,1,8]):
    print(sz,"size",size_of(sz),"best",best(sz))
# method B for size lists via ctypes
for sz in ([1,8,1],[1,4,1,4,2,4,4,4],[2,1],[8,1],[1,1,1,4],[4,1,2,1,8],[1,2,4,8,1,2,4,8],[1,8,1,8,1,8]):
    m={1:C.c_uint8,2:C.c_uint16,4:C.c_uint32,8:C.c_uint64}
    def mk(l):
        class S(C.Structure): _fields_=[(f"f{i}",m[s]) for i,s in enumerate(l)]
        return C.sizeof(S)
    assert mk(sz)==size_of(sz) and mk(sorted(sz,reverse=True))==best(sz)
print("ctypes agrees on size lists")
# straddling: array of 24-byte structs from a 64-byte aligned base, over 8 elements (192 B = 3 lines)
st=[i for i in range(8) if (i*24)//64 != (i*24+23)//64]; print("24-byte straddlers in 8:",st,len(st)/8)
st=[i for i in range(2) if (i*32)//64 != (i*32+31)//64]; print("32-byte straddlers:",st)
# elements per line
print("per line 32:",64/32,"24:",64/24)
print("1e6 orders 32B", 32*10**6/1e6,"MB;24B",24*10**6/1e6,"MB; saving", 1-24/32)
# wasm32 check
src='''#include <stdint.h>
#include <stddef.h>
struct Bad{uint8_t type;uint32_t seq;uint8_t side;uint32_t id;uint16_t instr;uint32_t qty;int32_t price;uint32_t time;};
struct Sorted{uint32_t seq;uint32_t id;uint32_t qty;int32_t price;uint32_t time;uint16_t instr;uint8_t type;uint8_t side;};
struct Wire{uint8_t type;uint8_t side;uint16_t instr;uint32_t seq;uint32_t id;uint32_t qty;int32_t price;uint32_t time;};
struct A{uint8_t a;double b;uint8_t c;}; struct B{double b;uint8_t a;uint8_t c;};
struct E{uint8_t a;uint64_t b;uint8_t c;uint16_t d;};
static_assert(sizeof(Bad)==32&&offsetof(Bad,price)==24&&offsetof(Bad,time)==28,"");
static_assert(sizeof(Sorted)==24&&offsetof(Sorted,instr)==20&&offsetof(Sorted,type)==22,"");
static_assert(sizeof(Wire)==24&&offsetof(Wire,seq)==4&&offsetof(Wire,price)==16&&offsetof(Wire,time)==20,"");
static_assert(sizeof(A)==24&&sizeof(B)==16&&sizeof(E)==24,"");
'''
open("wasmcheck.cpp","w").write(src)
r=subprocess.run(["clang++","--target=wasm32-unknown-unknown","-ffreestanding","-nostdinc++","-fsyntax-only","wasmcheck.cpp"],capture_output=True,text=True); print("wasm32 static_assert:", "OK" if r.returncode==0 else r.stderr)
r=subprocess.run(["g++","-std=c++17","-fsyntax-only","wasmcheck.cpp"],capture_output=True,text=True); print("x86-64 static_assert:", "OK" if r.returncode==0 else r.stderr)
