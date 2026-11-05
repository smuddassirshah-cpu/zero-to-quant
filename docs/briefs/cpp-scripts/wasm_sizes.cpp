// Layout facts for l21, checked as static_asserts on a wasm32 target (no headers needed).
struct Plain { int x; };
struct OneVirtual { int x; virtual void f(); };
struct Two { int x; virtual void f(); virtual void g(); };
struct D : OneVirtual { int y; void f() override; };
struct NoData { virtual ~NoData(); };
struct Empty {};
static_assert(sizeof(void*) == 4, "wasm32 pointers are 4 bytes");
static_assert(sizeof(Plain) == 4, "");
static_assert(sizeof(OneVirtual) == 8, "vptr 4 + int 4");
static_assert(sizeof(Two) == 8, "a second virtual adds no per-object bytes");
static_assert(sizeof(D) == 12, "vptr 4 + x 4 + y 4");
static_assert(sizeof(NoData) == 4, "just the vptr");
static_assert(sizeof(Empty) == 1, "");
struct Quote { virtual double mid() const; double bid, ask; };
struct PlainQuote { double bid, ask; };
static_assert(sizeof(PlainQuote) == 16, "");
static_assert(sizeof(Quote) == 24, "wasm32: vptr 4, 4 padding, then two 8-byte doubles; desktop: vptr 8 and no padding");
static_assert(alignof(double) == 8, "");
