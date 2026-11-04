# Generates latencies.csv for l17 (E14 data file): a closed-loop client sending 10,000 requests a second.
# Deterministic: own LCG. Run: python3 -I make_latencies_csv.py   (writes latencies.csv next to this file)
class Lcg:
    def __init__(self, s): self.s = s
    def next(self, n):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & (2**64 - 1)
        return (self.s >> 33) % n
g = Lcg(11)
rows = []
done_prev = 0
for seq in range(2000):
    intended = seq * 100                      # one request every 100 us
    sent = max(intended, done_prev)           # closed loop: wait for the previous reply
    service = 30 + g.next(21)                 # 30..50 us
    if g.next(100) == 0: service += 200       # 1% slow replies
    if seq == 1000: service += 50000          # one 50 ms stall
    done = sent + service
    rows.append((seq, intended, sent, done)); done_prev = done
with open('latencies.csv', 'w') as f:
    f.write("seq,intended_us,sent_us,done_us\n")
    for r in rows: f.write("%d,%d,%d,%d\n" % r)
