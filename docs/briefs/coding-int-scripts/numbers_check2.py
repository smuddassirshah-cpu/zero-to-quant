import math, itertools
def rs_a(prices):
    pnl = trades = 0; long_ = False
    for i, p in enumerate(prices):
        if not long_:
            if i >= 1 and p < prices[i-1]: long_, entry, bought = True, p, i
        elif 100*p >= 105*entry or 100*p <= 97*entry or i - bought == 3:
            pnl += p - entry; trades += 1; long_ = False
    if long_: pnl += prices[-1] - entry; trades += 1
    return [pnl, trades]
def rs_ge(prices):   # variant with >= 3 (also correct here), and > 3 (the slip)
    pnl = trades = 0; long_ = False
    for i, p in enumerate(prices):
        if not long_:
            if i >= 1 and p < prices[i-1]: long_, entry, bought = True, p, i
        elif 100*p >= 105*entry or 100*p <= 97*entry or i - bought > 3:
            pnl += p - entry; trades += 1; long_ = False
    if long_: pnl += prices[-1] - entry; trades += 1
    return [pnl, trades]
pr = [100,99,99,99,98,97]
print('correct', rs_a(pr), 'slip >3', rs_ge(pr))
# by hand: buy 99 on day 1; day 4 is three days later: sell 98, pnl -1; day 5: 97 < 98 so buy 97 and sell at the end 97: pnl 0; total -1, 2 trades
print('hand', [98-99 + (97-97), 2])
print('book trade qty', 2+2, 'spread', 100-99)
print(sum(range(1000)), 1000*999//2, math.ceil(math.log2(10**6)), (10**6).bit_length())
print('ratio', (100000*2000)//(2000*10))
