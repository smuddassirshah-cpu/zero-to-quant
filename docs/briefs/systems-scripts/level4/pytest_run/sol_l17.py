import csv

def nearest_rank(values, permille):
    s = sorted(values)
    rank = max(1, -(-permille * len(s) // 1000))      # ceil(permille * n / 1000) in integers
    return s[rank - 1]

def report(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    sent = [int(r["done_us"]) - int(r["sent_us"]) for r in rows]
    true = [int(r["done_us"]) - int(r["intended_us"]) for r in rows]
    return {
        "p50_sent": nearest_rank(sent, 500), "p99_sent": nearest_rank(sent, 990), "p999_sent": nearest_rank(sent, 999),
        "p50_true": nearest_rank(true, 500), "p99_true": nearest_rank(true, 990), "p999_true": nearest_rank(true, 999),
        "mean_true": sum(true) / len(true),
    }
