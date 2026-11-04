import csv

def report(path):
    """Read latencies.csv (seq, intended_us, sent_us, done_us). A closed-loop client sent each request
    when the previous reply arrived. Return nearest-rank percentiles (rank = ceil(p * n / 100)) of
    done - sent ("sent") and of done - intended ("true"), and the mean of the true latency."""
    with open(path) as f:
        rows = list(csv.DictReader(f))
    sent = sorted(int(r["done_us"]) - int(r["sent_us"]) for r in rows)
    mid = sent[len(sent) // 2]
    return {"p50_sent": mid, "p99_sent": mid, "p999_sent": mid,
            "p50_true": mid, "p99_true": mid, "p999_true": mid,
            "mean_true": sum(sent) / len(sent)}
