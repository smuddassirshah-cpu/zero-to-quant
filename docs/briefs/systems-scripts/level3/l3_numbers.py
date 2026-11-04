# Level 3 numbers. Method A: formula. Method B: simulation or exact fractions.
import random
from fractions import Fraction as F
print("== l11: syscall counts reading 1 MiB")
for chunk in (64,4096,65536):
    n=2**20//chunk; print(f"chunk {chunk:6d} B -> {n:6d} syscalls x 0.2 us = {n*0.2:9.1f} us ; ratio vs 64 KiB {n/16:.0f}")
print("context switch wake per message: 2 switches x 2 us =",2*2,"us ; at 100,000 msg/s CPU share =",100_000*4e-6)
print("thread per message 15 us at 200,000/s =",200_000*15e-6,"core-seconds per second")
print("== l12: partial reads 100 bytes of 24-byte frames:", divmod(100,24), " 1000 bytes:",divmod(1000,24), " 23 bytes:",divmod(23,24), "48:",divmod(48,24))
print("kernel path 10 us vs 5 us budget; bypass 1 us -> budget share", 1/5)
print("== l13: TCP handshake, RTT 60 ms")
rtt=60; print("UDP first data at server (ms):",rtt/2,"; TCP SYN, SYN-ACK, ACK+data:",1.5*rtt,"; ratio",1.5*rtt/(rtt/2))
# method B: event times
t=0; syn_arrives=t+30; synack_arrives_client=syn_arrives+30; data_arrives=synack_arrives_client+30; print("event-time method:", data_arrives)
print("HOL: msgs queued behind one loss, 100,000 msg/s")
for name,delay in (("fast retransmit ~1 RTT 0.5 ms",0.0005),("RTO 200 ms",0.2)): print(f"  {name}: {100_000*delay:g} messages delayed")
print("multicast vs unicast, 50 subscribers, 1,000 msg/s, 100 B:")
uni=50*1000*100; mc=1000*100; print("  unicast B/s",uni,"=",uni*8/1e6,"Mbit/s; multicast",mc,"B/s =",mc*8/1e6,"Mbit/s; ratio",uni/mc)
print("== A/B arbitration: loss 1% each, 1,000,000 messages")
N=10**6; p=F(1,100)
print("  single feed lost:",N*p,"; both lost (independent):",N*p*p)
random.seed(7); a=sum(random.random()<0.01 for _ in range(N)); 
random.seed(7); lostA=[random.random()<0.01 for _ in range(N)]; random.seed(8); lostB=[random.random()<0.01 for _ in range(N)]
print("  simulation: A lost",sum(lostA),"B lost",sum(lostB),"both",sum(x and y for x,y in zip(lostA,lostB)))
# exact: probability both lost = 1e-4; expected 100; std = sqrt(N p q)
import math; print("  std of both-lost count ~", math.sqrt(N*1e-4*(1-1e-4)))
print("== l14: frames per 1500-byte datagram (MTU payload ~1472 for UDP over Ethernet): 1472//24 =",1472//24,"remainder",1472%24)
print("   bandwidth: 200,000 msgs/s x 24 B =",200_000*24,"B/s =",200_000*24*8/1e6,"Mbit/s")
