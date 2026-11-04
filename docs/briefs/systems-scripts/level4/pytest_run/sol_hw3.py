import struct

def summarise(path):
    seen, rows = set(), []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        kind, side, instrument, seq, order_id, qty, price, time = struct.unpack(">BBHIIIiI", bytes.fromhex(line))
        if seq in seen:
            continue                      # a duplicate from the second feed
        seen.add(seq)
        rows.append((kind, qty, price))
    trades = [(q, p) for k, q, p in rows if k == ord("T")]
    return {
        "unique": len(seen),
        "missing": sorted(set(range(1, max(seen) + 1)) - seen),
        "trades": len(trades),
        "vwap": sum(q * p for q, p in trades) / sum(q for q, _ in trades),
    }
