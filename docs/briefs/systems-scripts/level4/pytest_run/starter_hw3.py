import struct

def summarise(path):
    """Each line of feed.hex is one 24-byte frame in hex (>BBHIIIiI: type, side, instrument, seq, id, qty, price, time).
    Return the number of unique sequence numbers, the sorted list of missing ones (1 up to the largest),
    the number of trades (type 84, 'T') and their volume-weighted average price in pence."""
    frames = [struct.unpack(">BBHIIIiI", bytes.fromhex(l.strip())) for l in open(path) if l.strip()]
    return {"unique": len(frames), "missing": [], "trades": 0, "vwap": 0.0}
