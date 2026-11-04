#include <cstdint>
#include <cstdio>
#include <vector>
struct R { std::vector<int> b; uint32_t mask,head,tail; R(uint32_t cap,uint32_t start):b(cap),mask(cap-1),head(start),tail(start){}
 bool push(int v){ if(tail-head==b.size()) return false; b[tail&mask]=v; ++tail; return true;}
 bool pop(int&o){ if(head==tail) return false; o=b[head&mask]; ++head; return true;} };
int main(){ R r(4,4294967294u); int o; int in[]={1,2,3,4,5}; for(int v:in) std::printf("push %d -> %d tail=%u size=%u\n",v,(int)r.push(v),r.tail,r.tail-r.head);
 while(r.pop(o)) std::printf("pop %d head=%u\n",o,r.head);
 // non power of two capacity 3 with mask: breaks
 R q(3,4294967294u); std::printf("cap3 mask=%u indices:",q.mask); for(uint32_t t=4294967294u;t<4294967294u+4;t++) std::printf(" %u",t&q.mask); std::printf("\n"); }
