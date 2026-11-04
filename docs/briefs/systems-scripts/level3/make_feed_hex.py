# Generates feed.hex for homework-3 (E14 data file). Deterministic: own LCG, no random module.
import struct
class Lcg:
    def __init__(self, s): self.s = s
    def next(self, n):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & (2**64 - 1)
        return (self.s >> 33) % n
g = Lcg(2027)
dropped = {17, 18, 90, 150, 151, 152}
frames = []
for seq in range(1, 207):
    r = g.next(100)
    t = ord('A') if r < 70 else (ord('X') if r < 85 else ord('T'))
    side = ord('B') if g.next(2) == 0 else ord('S')
    price = 10000 + g.next(41) - 20
    qty = 10 * (1 + g.next(20))
    frames.append((seq, struct.pack('>BBHIIIiI', t, side, 7, seq, 1000 + seq, qty, price, 36000000 + seq * 5)))
frames = [f for f in frames if f[0] not in dropped]
order = [f for f in frames]
i = [k for k, f in enumerate(order) if f[0] == 40][0]; order[i], order[i + 1] = order[i + 1], order[i]   # 41 arrives before 40
j = [k for k, f in enumerate(order) if f[0] == 100][0]; order.insert(j + 1, order[j])                     # 100 arrives twice
open('feed.hex', 'w').write("\n".join(f[1].hex() for f in order) + "\n")
print(len(order), "lines")
