#include <stdint.h>
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
