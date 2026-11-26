#!/usr/bin/env node
/* Blind concept audit, first-python levels 1 to 3, round 1: the test-N sweep (docs/reviews/audit-first-python-1-3.md).
   Every `feedback.byKey.test-N` and `feedback.byKey.error` line of the course's code widgets, with two or three natural codings of the
   mistake it names, submitted through the page's own harness (tools/code-runner.mjs: Pyodide 0.27.7, Python 3.12, wasm32, the page's
   time limits). `expect` is the key the page should give if the line is right: test-N, error, or pass (a wrong program the hidden
   tests do not reject). A line printed DIFF is a routing fact recorded in the audit (finding 2); the script exits 0 when the
   differing lines are exactly the ones the audit lists (KNOWN below), 1 otherwise.
   With --concepts it also runs first-python-L1-3-concepts.py inside the same Pyodide, where its traceback checks are exact.
     node docs/reports/first-python-L1-3-test-line-sweep.mjs --local-cdn <pkgs> [--concepts] */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const appDir = path.resolve(HERE, '..', '..', 'app');
const argv = process.argv.slice(2);
const pkgs = argv[argv.indexOf('--local-cdn') + 1] || process.env.ZQ_LOCAL_CDN;
if (!pkgs) { console.error('give --local-cdn <pkgs>'); process.exit(2); }
// name, src, expect (the key the page gives: test-N, error, pass). @PRE@ = the starter text before its first def.
const CSV = 'with open("prices.csv", "w") as f:\n    f.write("Day,Close\\nMon,101.20\\nTue,102.50\\nWed,99.80\\nThu,100.40\\nFri,101.10\\n")\n\n';
const M = {
  'l1-calculator': {
    9: [{ name: 'no brackets', src: 'print(262.5 - 250 / 250)\n', expect: 'test-1' }],
  },
  'l2-naming-a-value': {
    7: [{ name: 'not stored', src: 'cash = 1000\ncash - 3 * 120\nprint(cash)\n', expect: 'test-1' },
        { name: 'no print', src: 'cash = 1000\ncash = cash - 3 * 120\n', expect: 'test-1' },
        { name: 'printed twice', src: 'cash = 1000\nprint(cash)\ncash = cash - 3 * 120\nprint(cash)\n', expect: 'test-1' }],
    9: [{ name: 'stale value', src: 'price = 182.40\nqty = 25\nvalue = price * qty\nprice = 185.10\nprint(value)\n', expect: 'test-1' }],
  },
  'l3-text': {
    2: [{ name: 'stop 5', src: 'pair = "GBPUSD"\nprint(pair[0:3])\nprint(pair[3:5])\n', expect: 'test-1' }],
    7: [{ name: 'no .2f', src: 'price = 12.5\nprint(f"Price: £{price}")\n', expect: 'test-1' }],
    9: [{ name: 'no .2f', src: 'mon = 37.25\ntue = -8.5\nprint(f"P&L (£): {mon:+}")\nprint(f"P&L (£): {tue:+}")\n', expect: 'test-1' },
        { name: 'no plus', src: 'mon = 37.25\ntue = -8.5\nprint(f"P&L (£): {mon:.2f}")\nprint(f"P&L (£): {tue:.2f}")\n', expect: 'test-1' },
        { name: 'hand-typed plus on Monday only', src: 'mon = 37.25\ntue = -8.5\nprint(f"P&L (£): +{mon:.2f}")\nprint(f"P&L (£): {tue:.2f}")\n', expect: 'pass' }],
  },
  'l4-asking-and-printing': {
    2: [{ name: 'text times 2', src: 'typed = "250"\nqty = typed\nprint(qty * 2)\n', expect: 'test-1' },
        { name: 'text times 2, no qty', src: 'typed = "250"\nprint(typed * 2)\n', expect: 'test-1' }],
    4: [{ name: 'int', src: 'typed = "12.75"\nprice = int(typed)\nprint(price * 4)\n', expect: 'error' }],
    9: [{ name: 'still text', src: 'old_text = "184.20"\nnew_text = "189.35"\nret = (new_text - old_text) / old_text\nprint(f"Return: {ret * 100:.2f}%")\n', expect: 'error' }],
    10: [{ name: 'no slice', src: 'text = "4.5%"\nsavings = 2000\nrate = float(text) / 100\nprint(rate)\nprint(f"Interest: £{savings * rate:.2f}")\n', expect: 'error' }],
  },
  'l5-decisions': {
    9: [{ name: '<=', src: 'def stop_check(price, stop):\n    action = "hold"\n    if price <= stop:\n        action = "sell"\n    return action\n', expect: 'test-2' }],
  },
  'l7-for-each': {
    6: [{ name: 'range(1, n)', src: 'def sum_to(n):\n    total = 0\n    for k in range(1, n):\n        total = total + k\n    return total\n', expect: 'test-1' },
        { name: 'range(n)', src: 'def sum_to(n):\n    total = 0\n    for k in range(n):\n        total = total + k\n    return total\n', expect: 'test-1' }],
    9: [{ name: '>=', src: 'def up_days(returns):\n    count = 0\n    for r in returns:\n        if r >= 0:\n            count = count + 1\n    return count\n', expect: 'test-1' }],
  },
  'l8-many-values': {
    9: [{ name: 'append only on change', src: 'def running_peak(prices):\n    peaks = []\n    if len(prices) > 0:\n        peak = prices[0]\n        for p in prices:\n            if p > peak:\n                peak = p\n                peaks.append(peak)\n    return peaks\n', expect: 'test-1' },
        { name: 'append only on change, from 0', src: 'def running_peak(prices):\n    peaks = []\n    peak = 0\n    for p in prices:\n        if p > peak:\n            peak = p\n            peaks.append(peak)\n    return peaks\n', expect: 'test-1' },
        { name: 'peak starts at 0 (the lesson trap)', src: 'def running_peak(prices):\n    peaks = []\n    peak = 0\n    for p in prices:\n        if p > peak:\n            peak = p\n        peaks.append(peak)\n    return peaks\n', expect: 'pass' }],
  },
  'l9-packaging-steps': {
    3: [{ name: 'prints', src: 'def with_fee(price):\n    print(price + 1.50)\n', expect: 'test-1' }],
    4: [{ name: 'fee per share', src: 'def total_cost(price, shares):\n    return (price + 1.50) * shares\n', expect: 'test-1' },
        { name: 'no fee', src: 'def total_cost(price, shares):\n    return price * shares\n', expect: 'test-1' }],
    8: [{ name: 'still prints', src: 'def daily_gain(p0, p1):\n    print(p1 - p0)\n', expect: 'test-1' },
        { name: 'wrong way round', src: 'def daily_gain(p0, p1):\n    return p0 - p1\n', expect: 'test-1' }],
    10: [{ name: 'divide by new', src: 'def daily_return(p0, p1):\n    return (p1 - p0) / p1\n', expect: 'test-1' },
         { name: 'no brackets', src: 'def daily_return(p0, p1):\n    return p1 - p0 / p0\n', expect: 'test-1' },
         { name: 'times 100', src: 'def daily_return(p0, p1):\n    return (p1 - p0) / p0 * 100\n', expect: 'test-1' }],
  },
  'l10-reading-errors': {
    4: [{ name: 'starter', src: 'closes = [101.20, 102.50]\ncloses = closes.append(99.80)\ncount = len(closes)\n', expect: 'error' },
        { name: 'count is last index', src: 'closes = [101.20, 102.50]\ncloses.append(99.80)\ncount = len(closes) - 1\n', expect: 'test-2' },
        { name: 'count before append', src: 'closes = [101.20, 102.50]\ncount = len(closes)\ncloses.append(99.80)\n', expect: 'test-2' }],
    6: [{ name: 'starter (not converted)', src: 'def with_fee(price_text):\n    return price_text + 1.50\n\nprint(with_fee("101.20"))\n', expect: 'error' },
        { name: 'int', src: 'def with_fee(price_text):\n    return int(price_text) + 1.50\n\nprint(with_fee("101.20"))\n', expect: 'error' },
        { name: 'not converted, print deleted', src: 'def with_fee(price_text):\n    return price_text + 1.50\n', expect: 'test-1' },
        { name: 'joins text to text', src: 'def with_fee(price_text):\n    return price_text + "1.50"\n\nprint(with_fee("101.20"))\n', expect: 'test-1' },
        { name: 'converted, fee forgotten', src: 'def with_fee(price_text):\n    return float(price_text)\n\nprint(with_fee("101.20"))\n', expect: 'test-1' }],
    8: [{ name: 'starter', src: 'def max_drawdown(prices):\n    peak = prices[0]\n    worst = 0.0\n    for i in range(1, len(prices) + 1):\n        price = prices[i]\n        if price > peak:\n            peak = price\n        drop = (peak - price) / peak\n        if drop > worst:\n            worst = drop\n    return worst\n\nprint(max_drawdown([100.00, 110.00, 99.00]))\n', expect: 'error' },
        { name: 'one step early', src: 'def max_drawdown(prices):\n    peak = prices[0]\n    worst = 0.0\n    for i in range(1, len(prices) - 1):\n        price = prices[i]\n        if price > peak:\n            peak = price\n        drop = (peak - price) / peak\n        if drop > worst:\n            worst = drop\n    return worst\n\nprint(max_drawdown([100.00, 110.00, 99.00]))\n', expect: 'test-5' },
        { name: 'range(len - 1)', src: 'def max_drawdown(prices):\n    peak = prices[0]\n    worst = 0.0\n    for i in range(len(prices) - 1):\n        price = prices[i]\n        if price > peak:\n            peak = price\n        drop = (peak - price) / peak\n        if drop > worst:\n            worst = drop\n    return worst\n\nprint(max_drawdown([100.00, 110.00, 99.00]))\n', expect: 'test-5' }],
  },
  'l11-numbers-from-a-file': {
    2: [{ name: 'no float', src: 'def close_from_row(line):\n    return line.split(",")[1]\n\nprint(close_from_row("Tue,102.50\\n"))\n', expect: 'test-1' },
        { name: 'index 0', src: 'def close_from_row(line):\n    return float(line.split(",")[0])\n\nprint(close_from_row("Tue,102.50\\n"))\n', expect: 'error' }],
    3: [{ name: 'no float', src: '@PRE@def read_closes(name):\n    closes = []\n    for line in open(name):\n        closes.append(line)\n    return closes\n\nprint(read_closes("closes.txt"))\n', expect: 'test-1' },
        { name: 'replaced', src: '@PRE@def read_closes(name):\n    closes = []\n    for line in open(name):\n        closes = float(line)\n    return closes\n\nprint(read_closes("closes.txt"))\n', expect: 'test-1' }],
    6: [{ name: 'header kept', src: CSV + 'def read_csv_closes(name):\n    closes = []\n    for line in open(name).readlines():\n        closes.append(float(line.split(",")[1]))\n    return closes\n\nprint(read_csv_closes("prices.csv"))\n', expect: 'error' },
        { name: 'lines[2:]', src: CSV + 'def read_csv_closes(name):\n    closes = []\n    for line in open(name).readlines()[2:]:\n        closes.append(float(line.split(",")[1]))\n    return closes\n\nprint(read_csv_closes("prices.csv"))\n', expect: 'test-1' }],
    8: [{ name: 'first data line', src: CSV + 'def last_close(name):\n    lines = open(name).readlines()\n    return float(lines[1].split(",")[1])\n\nprint(f"Last close: £{last_close(\'prices.csv\'):.2f}")\n', expect: 'test-1' },
        { name: 'index past end, no print yet', src: CSV + 'def last_close(name):\n    lines = open(name).readlines()\n    return float(lines[len(lines)].split(",")[1])\n', expect: 'test-1' },
        { name: 'split on newline, last piece empty', src: CSV + 'def last_close(name):\n    lines = open(name).read().split("\\n")\n    return float(lines[-1].split(",")[1])\n', expect: 'test-1' },
        { name: 'no .2f', src: CSV + 'def last_close(name):\n    lines = open(name).readlines()\n    return float(lines[-1].split(",")[1])\n\nprint(f"Last close: £{last_close(\'prices.csv\')}")\n', expect: 'test-4' },
        { name: 'no print', src: CSV + 'def last_close(name):\n    lines = open(name).readlines()\n    return float(lines[-1].split(",")[1])\n', expect: 'test-4' }],
  },
  'l12-savings-script': {
    2: [{ name: 'simple interest', src: 'def project(balance, rate, years):\n    start = balance\n    for year in range(years):\n        balance = balance + start * rate\n    return balance\n', expect: 'test-1' },
        { name: 'one year too many', src: 'def project(balance, rate, years):\n    for year in range(years + 1):\n        balance = balance * (1 + rate)\n    return balance\n', expect: 'test-1' },
        { name: 'times rate', src: 'def project(balance, rate, years):\n    for year in range(years):\n        balance = balance * rate\n    return balance\n', expect: 'test-1' }],
    3: [{ name: 'deposit first', src: 'def project_saving(balance, rate, years, deposit):\n    for year in range(years):\n        balance = balance + deposit\n        balance = balance * (1 + rate)\n    return balance\n', expect: 'test-1' },
        { name: 'deposits at end', src: 'def project_saving(balance, rate, years, deposit):\n    for year in range(years):\n        balance = balance * (1 + rate)\n    return balance + deposit * years\n', expect: 'test-1' }],
    5: [{ name: 'no newline', src: 'def save_line(name, year, balance):\n    with open(name, "w") as f:\n        f.write(f"Year {year}: £{balance:.2f}")\n\nsave_line("result.txt", 10, 1628.894626777442)\nprint(open("result.txt").read())\n', expect: 'test-1' },
        { name: 'no .2f', src: 'def save_line(name, year, balance):\n    with open(name, "w") as f:\n        f.write(f"Year {year}: £{balance}\\n")\n\nsave_line("result.txt", 10, 1628.894626777442)\nprint(open("result.txt").read())\n', expect: 'test-1' },
        { name: 'append mode instead of w', src: 'def save_line(name, year, balance):\n    with open(name, "a") as f:\n        f.write(f"Year {year}: £{balance:.2f}\\n")\n\nsave_line("result.txt", 10, 1628.894626777442)\nprint(open("result.txt").read())\n', expect: 'pass' }],
    7: [{ name: 'open inside loop', src: 'def save_plan(name, balance, rate, years):\n    for year in range(1, years + 1):\n        balance = balance * (1 + rate)\n        with open(name, "w") as f:\n            f.write(f"Year {year}: £{balance:.2f}\\n")\n\nsave_plan("plan.txt", 2000.00, 0.04, 3)\nprint(open("plan.txt").read())\n', expect: 'test-1' },
        { name: 'range stops early', src: 'def save_plan(name, balance, rate, years):\n    with open(name, "w") as f:\n        for year in range(1, years):\n            balance = balance * (1 + rate)\n            f.write(f"Year {year}: £{balance:.2f}\\n")\n\nsave_plan("plan.txt", 2000.00, 0.04, 3)\nprint(open("plan.txt").read())\n', expect: 'test-1' },
        { name: 'write before growing', src: 'def save_plan(name, balance, rate, years):\n    with open(name, "w") as f:\n        for year in range(1, years + 1):\n            f.write(f"Year {year}: £{balance:.2f}\\n")\n            balance = balance * (1 + rate)\n\nsave_plan("plan.txt", 2000.00, 0.04, 3)\nprint(open("plan.txt").read())\n', expect: 'test-1' },
        { name: 'append mode opened inside the loop', src: 'def save_plan(name, balance, rate, years):\n    for year in range(1, years + 1):\n        balance = balance * (1 + rate)\n        with open(name, "a") as f:\n            f.write(f"Year {year}: £{balance:.2f}\\n")\n\nsave_plan("plan.txt", 2000.00, 0.04, 3)\nprint(open("plan.txt").read())\n', expect: 'pass' }],
    10: [{ name: 'header kept', src: CSV + 'def daily_return(p0, p1):\n    return (p1 - p0) / p0\n\ndef returns_from_file(name):\n    closes = []\n    for line in open(name).readlines():\n        closes.append(float(line.split(",")[1]))\n    returns = []\n    for i in range(1, len(closes)):\n        returns.append(daily_return(closes[i - 1], closes[i]))\n    return returns\n\nfor r in returns_from_file("prices.csv"):\n    print(f"{r:.2%}")\n', expect: 'error' },
         { name: 'loop from 0', src: CSV + 'def daily_return(p0, p1):\n    return (p1 - p0) / p0\n\ndef returns_from_file(name):\n    closes = []\n    for line in open(name).readlines()[1:]:\n        closes.append(float(line.split(",")[1]))\n    returns = []\n    for i in range(len(closes)):\n        returns.append(daily_return(closes[i - 1], closes[i]))\n    return returns\n\nfor r in returns_from_file("prices.csv"):\n    print(f"{r:.2%}")\n', expect: 'test-1' },
         { name: 'swapped', src: CSV + 'def daily_return(p0, p1):\n    return (p1 - p0) / p0\n\ndef returns_from_file(name):\n    closes = []\n    for line in open(name).readlines()[1:]:\n        closes.append(float(line.split(",")[1]))\n    returns = []\n    for i in range(1, len(closes)):\n        returns.append(daily_return(closes[i], closes[i - 1]))\n    return returns\n\nfor r in returns_from_file("prices.csv"):\n    print(f"{r:.2%}")\n', expect: 'test-2' },
         { name: 'plain print', src: CSV + 'def daily_return(p0, p1):\n    return (p1 - p0) / p0\n\ndef returns_from_file(name):\n    closes = []\n    for line in open(name).readlines()[1:]:\n        closes.append(float(line.split(",")[1]))\n    returns = []\n    for i in range(1, len(closes)):\n        returns.append(daily_return(closes[i - 1], closes[i]))\n    return returns\n\nfor r in returns_from_file("prices.csv"):\n    print(r)\n', expect: 'test-7' }],
  },
  'review-3': {
    4: [{ name: 'prints', src: 'def average(prices):\n    print(sum(prices) / len(prices))\n', expect: 'test-1' },
        { name: 'len - 1', src: 'def average(prices):\n    return sum(prices) / (len(prices) - 1)\n', expect: 'test-1' }],
    6: [{ name: 'header kept', src: CSV + 'def average_close(name):\n    closes = []\n    for line in open(name).readlines():\n        closes.append(float(line.split(",")[1]))\n    return sum(closes) / len(closes)\n\nprint(average_close("prices.csv"))\n', expect: 'error' },
        { name: 'divide by line count', src: CSV + 'def average_close(name):\n    lines = open(name).readlines()\n    closes = []\n    for line in lines[1:]:\n        closes.append(float(line.split(",")[1]))\n    return sum(closes) / len(lines)\n\nprint(average_close("prices.csv"))\n', expect: 'test-1' }],
  },
  'homework-1': {
    4: [{ name: 'no times 100', src: 'mon_text = "102.40"\nfri_text = "98.70"\nret = (float(fri_text) - float(mon_text)) / float(mon_text)\nprint(f"Return: {ret:+.2f}%")\n', expect: 'test-1' },
        { name: 'no + in the format', src: 'mon_text = "102.40"\nfri_text = "98.70"\nret = (float(fri_text) - float(mon_text)) / float(mon_text)\nprint(f"Return: {ret * 100:.2f}%")\n', expect: 'pass' }],
    5: [{ name: 'rate 0.25', src: 'price = 63.50\nqty = 40\nfee_text = "0.25%"\nrate = float(fee_text[0:-1])\ntrade = price * qty\nfee = trade * rate\nprint(f"Fee: £{fee:.2f}")\nprint(f"Total: £{trade + fee:.2f}")\n', expect: 'test-1' }],
    6: [{ name: 'no + in either format', src: 'entry_text = "104.50"\nexit_text = "98.20"\nqty_text = "300"\nentry = float(entry_text)\nexit_price = float(exit_text)\nqty = int(qty_text)\npnl = (exit_price - entry) * qty\nret = (exit_price - entry) / entry\nprint(f"P&L (£): {pnl:.2f}")\nprint(f"Return: {ret * 100:.2f}%")\n', expect: 'pass' },
        { name: 'no times 100', src: 'entry_text = "104.50"\nexit_text = "98.20"\nqty_text = "300"\nentry = float(entry_text)\nexit_price = float(exit_text)\nqty = int(qty_text)\npnl = (exit_price - entry) * qty\nret = (exit_price - entry) / entry\nprint(f"P&L (£): {pnl:+.2f}")\nprint(f"Return: {ret:+.2f}%")\n', expect: 'test-1' }],
  },
  'homework-2': {
    0: [{ name: '<= and >=', src: 'def decide(price, stop, target):\n    if price <= stop:\n        action = "sell"\n    elif price >= target:\n        action = "take profit"\n    else:\n        action = "hold"\n    return action\n', expect: 'test-4' }],
    2: [{ name: 'no guard', src: 'def years_to_target(balance, rate, target):\n    years = 0\n    while balance < target:\n        balance = balance * (1 + rate)\n        years = years + 1\n    return years\n', expect: 'test-2' },
        { name: 'rate test first', src: 'def years_to_target(balance, rate, target):\n    years = None\n    if rate > 0:\n        years = 0\n        while balance < target:\n            balance = balance * (1 + rate)\n            years = years + 1\n    return years\n', expect: 'test-5' }],
    3: [{ name: 'compares the day', src: 'def first_breach(pnls, limit):\n    day = None\n    total = 0\n    count = 0\n    for p in pnls:\n        total = total + p\n        count = count + 1\n        if p <= -limit:\n            day = count\n            break\n    return day\n', expect: 'test-4' },
        { name: 'no break', src: 'def first_breach(pnls, limit):\n    day = None\n    total = 0\n    count = 0\n    for p in pnls:\n        total = total + p\n        count = count + 1\n        if total <= -limit:\n            day = count\n    return day\n', expect: 'test-1' }],
    4: [{ name: 'keeps the last gap', src: 'def largest_fall(prices):\n    worst = 0\n    if len(prices) > 0:\n        peak = prices[0]\n        for p in prices:\n            if p > peak:\n                peak = p\n            if peak - p > 0:\n                worst = peak - p\n    return worst\n', expect: 'test-3' },
        { name: 'fall from the final peak only', src: 'def largest_fall(prices):\n    worst = 0\n    if len(prices) > 0:\n        peak = prices[0]\n        for p in prices:\n            if p > peak:\n                peak = p\n                worst = 0\n            if peak - p > worst:\n                worst = peak - p\n    return worst\n', expect: 'test-3' }],
    9: [{ name: 'no float', src: 'def split_bill(prices, people):\n    share = None\n    total = 0\n    for p in prices:\n        total = total + p\n    if people >= 6:\n        total = total * 1.125\n    share = total / people\n    return share\n', expect: 'test-1' },
        { name: 'prints', src: 'def split_bill(prices, people):\n    share = None\n    total = 0\n    for p in prices:\n        total = total + float(p)\n    if people >= 6:\n        total = total * 1.125\n    print(total / people)\n    return share\n', expect: 'test-1' },
        { name: 'missed a price', src: 'def split_bill(prices, people):\n    total = 0\n    for p in prices[1:]:\n        total = total + float(p)\n    if people >= 6:\n        total = total * 1.125\n    return total / people\n', expect: 'test-1' },
        { name: 'always charges', src: 'def split_bill(prices, people):\n    total = 0\n    for p in prices:\n        total = total + float(p)\n    total = total * 1.125\n    return total / people\n', expect: 'test-1' },
        { name: 'int', src: 'def split_bill(prices, people):\n    total = 0\n    for p in prices:\n        total = total + int(p)\n    if people >= 6:\n        total = total * 1.125\n    return total / people\n', expect: 'test-2' },
        { name: '//', src: 'def split_bill(prices, people):\n    total = 0\n    for p in prices:\n        total = total + float(p)\n    if people >= 6:\n        total = total * 1.125\n    return total // people\n', expect: 'test-2' },
        { name: '> 6', src: 'def split_bill(prices, people):\n    total = 0\n    for p in prices:\n        total = total + float(p)\n    if people > 6:\n        total = total * 1.125\n    return total / people\n', expect: 'test-3' },
        { name: 'charge by dishes', src: 'def split_bill(prices, people):\n    total = 0\n    for p in prices:\n        total = total + float(p)\n    if len(prices) >= 6:\n        total = total * 1.125\n    return total / people\n', expect: 'test-4' }],
  },
  'homework-3': {
    0: [{ name: 'one fee', src: 'def pnl(buy, sell, shares):\n    return (sell - buy) * shares - 1.50\n', expect: 'test-1' },
        { name: 'fees per share', src: 'def pnl(buy, sell, shares):\n    return (sell - buy - 3.00) * shares\n', expect: 'test-1' },
        { name: 'wrong way round', src: 'def pnl(buy, sell, shares):\n    return (buy - sell) * shares - 3.00\n', expect: 'test-1' }],
    1: [{ name: 'high and low in any order', src: 'def max_drawdown(prices):\n    return (max(prices) - min(prices)) / max(prices)\n', expect: 'test-1' },
        { name: 'peak never moves', src: 'def max_drawdown(prices):\n    peak = prices[0]\n    worst = 0.0\n    for price in prices:\n        drop = (peak - price) / peak\n        if drop > worst:\n            worst = drop\n    return worst\n', expect: 'test-1' },
        { name: 'one-day falls', src: 'def max_drawdown(prices):\n    worst = 0.0\n    for i in range(1, len(prices)):\n        drop = (prices[i - 1] - prices[i]) / prices[i - 1]\n        if drop > worst:\n            worst = drop\n    return worst\n', expect: 'test-2' }],
    2: [{ name: 'returns the price', src: CSV + 'def best_day(name):\n    lines = open(name).readlines()[1:]\n    best_price = float(lines[0].split(",")[1])\n    for line in lines:\n        price = float(line.split(",")[1])\n        if price > best_price:\n            best_price = price\n    return best_price\n\nprint(best_day("prices.csv"))\n', expect: 'test-1' },
        { name: 'text compare', src: CSV + 'def best_day(name):\n    lines = open(name).readlines()[1:]\n    best = lines[0].split(",")[0]\n    best_price = lines[0].split(",")[1]\n    for line in lines:\n        parts = line.split(",")\n        if parts[1] > best_price:\n            best = parts[0]\n            best_price = parts[1]\n    return best\n\nprint(best_day("prices.csv"))\n', expect: 'test-1' },
        { name: '>=', src: CSV + 'def best_day(name):\n    lines = open(name).readlines()[1:]\n    best = lines[0].split(",")[0]\n    best_price = float(lines[0].split(",")[1])\n    for line in lines:\n        parts = line.split(",")\n        price = float(parts[1])\n        if price >= best_price:\n            best = parts[0]\n            best_price = price\n    return best\n\nprint(best_day("prices.csv"))\n', expect: 'test-4' }],
    3: [{ name: 'no newline', src: 'def log_result(name, ticker, ret):\n    with open(name, "a") as f:\n        f.write(f"{ticker} {ret:.2%}")\n\nlog_result("log.txt", "VOD", 0.012845849802371512)\nprint(open("log.txt").read())\n', expect: 'test-1' },
        { name: 'w mode', src: 'def log_result(name, ticker, ret):\n    with open(name, "w") as f:\n        f.write(f"{ticker} {ret:.2%}\\n")\n\nlog_result("log.txt", "VOD", 0.012845849802371512)\nprint(open("log.txt").read())\n', expect: 'test-2' }],
    8: [{ name: 'no float', src: '@PRE@def contract_cost(fee, rise, years):\n    total = 0\n    for year in range(years):\n        total = total + 12 * fee\n        fee = fee * (1 + rise / 100)\n    return total\n', expect: 'test-1' },
        { name: 'prints, no script print yet', src: '@PRE@def contract_cost(fee, rise, years):\n    fee = float(fee)\n    rise = float(rise)\n    total = 0\n    for year in range(years):\n        total = total + 12 * fee\n        fee = fee * (1 + rise / 100)\n    print(total)\n', expect: 'test-1' },
        { name: 'prints, with the script print line', src: '@PRE@def contract_cost(fee, rise, years):\n    fee = float(fee)\n    rise = float(rise)\n    total = 0\n    for year in range(years):\n        total = total + 12 * fee\n        fee = fee * (1 + rise / 100)\n    print(total)\n\nprint(f"Total: £{contract_cost(form_fee, form_rise, 2):.2f}")\n', expect: 'error' },
        { name: 'raise before paying', src: '@PRE@def contract_cost(fee, rise, years):\n    fee = float(fee)\n    rise = float(rise)\n    total = 0\n    for year in range(years):\n        fee = fee * (1 + rise / 100)\n        total = total + 12 * fee\n    return total\n\nprint(f"Total: £{contract_cost(form_fee, form_rise, 2):.2f}")\n', expect: 'test-1' },
        { name: 'rise // 100', src: '@PRE@def contract_cost(fee, rise, years):\n    fee = float(fee)\n    rise = int(rise)\n    total = 0\n    for year in range(years):\n        total = total + 12 * fee\n        fee = fee * (1 + rise // 100)\n    return total\n\nprint(f"Total: £{contract_cost(form_fee, form_rise, 2):.2f}")\n', expect: 'test-2' },
        { name: 'return inside loop', src: '@PRE@def contract_cost(fee, rise, years):\n    fee = float(fee)\n    rise = float(rise)\n    total = 0\n    for year in range(years):\n        total = total + 12 * fee\n        fee = fee * (1 + rise / 100)\n        return total\n\nprint(f"Total: £{contract_cost(form_fee, form_rise, 2):.2f}")\n', expect: 'test-2' },
        { name: 'int(fee), with the script print line', src: '@PRE@def contract_cost(fee, rise, years):\n    fee = int(fee)\n    rise = float(rise)\n    total = 0\n    for year in range(years):\n        total = total + 12 * fee\n        fee = fee * (1 + rise / 100)\n    return total\n\nprint(f"Total: £{contract_cost(form_fee, form_rise, 2):.2f}")\n', expect: 'error' },
        { name: 'int(fee), no script print yet', src: '@PRE@def contract_cost(fee, rise, years):\n    fee = int(fee)\n    rise = float(rise)\n    total = 0\n    for year in range(years):\n        total = total + 12 * fee\n        fee = fee * (1 + rise / 100)\n    return total\n', expect: 'test-2' },
        { name: 'int(rise)', src: '@PRE@def contract_cost(fee, rise, years):\n    fee = float(fee)\n    rise = int(rise)\n    total = 0\n    for year in range(years):\n        total = total + 12 * fee\n        fee = fee * (1 + rise / 100)\n    return total\n\nprint(f"Total: £{contract_cost(form_fee, form_rise, 2):.2f}")\n', expect: 'test-3' },
        { name: 'right function, no print', src: '@PRE@def contract_cost(fee, rise, years):\n    fee = float(fee)\n    rise = float(rise)\n    total = 0\n    for year in range(years):\n        total = total + 12 * fee\n        fee = fee * (1 + rise / 100)\n    return total\n', expect: 'test-7' },
        { name: 'year loop from 1 pays first year outside', src: '@PRE@def contract_cost(fee, rise, years):\n    fee = float(fee)\n    rise = float(rise)\n    total = 12 * fee\n    for year in range(1, years):\n        fee = fee * (1 + rise / 100)\n        total = total + 12 * fee\n    return total\n\nprint(f"Total: £{contract_cost(form_fee, form_rise, 2):.2f}")\n', expect: 'test-6' }],
  },
};

// Routing probes: which key a crash gives. In a widget with a stdout test a runtime error keys as test-1; only a SyntaxError keys as error.
const M2 = {
  'l1-calculator': { 9: [{ name: 'NameError', src: 'print((new - old) / old)\n', expect: 'error' }, { name: 'SyntaxError', src: 'print((262.5 - 250 / 250)\n', expect: 'error' }] },
  'l2-naming-a-value': { 3: [{ name: 'NameError (Price/price)', src: 'Price = 12.5\nqty = 4\nprint(price * qty)\n', expect: 'error' }] },
  'l4-asking-and-printing': {
    4: [{ name: 'SyntaxError', src: 'typed = "12.75"\nprice = float(typed\nprint(price * 4)\n', expect: 'error' }],
    7: [{ name: 'starter (TypeError)', src: 'typed_qty = "8"\nprice = 12.5\ntotal = price * typed_qty\nprint(total)\n', expect: 'error' }],
  },
  'review-1': { 6: [{ name: 'TypeError', src: 'price_text = "41.20"\nqty_text = "150"\nvalue = price_text * qty_text\nprint(f"Value: £{value:.2f}")\n', expect: 'error' }] },
  'l12-savings-script': { 10: [{ name: 'SyntaxError', src: CSV + 'def daily_return(p0, p1):\n    return (p1 - p0) / p0\n\ndef returns_from_file(name)\n    return []\n', expect: 'error' }] },
  'homework-3': { 8: [{ name: 'SyntaxError', src: 'def contract_cost(fee, rise, years)\n    return 0\n', expect: 'error' }] },
  'l11-numbers-from-a-file': { 8: [{ name: 'header kept: script print raises', src: CSV + 'def last_close(name):\n    lines = open(name).readlines()\n    return float(lines[0].split(",")[1])\n\nprint(f"Last close: £{last_close(\'prices.csv\'):.2f}")\n', expect: 'error' }] },
  'l10-reading-errors': { 6: [{ name: 'SyntaxError', src: 'def with_fee(price_text)\n    return 1\n', expect: 'error' }] },
  'l6-until-done': {
    6: [{ name: 'block never changes value (runs too long)', src: 'def steps_to_reach(start, target, step):\n    value = start\n    count = 0\n    while value < target:\n        count = count + 1\n    return count\n', expect: 'error' }],
    9: [{ name: 'block never changes balance (runs too long)', src: 'def years_to_double(balance, rate):\n    target = 2 * balance\n    years = 0\n    while balance < target:\n        years = years + 1\n    return years\n', expect: 'error' }],
  },
  'l8-many-values': { 6: [{ name: 'values[0] outside the length check', src: 'def largest(values):\n    best = values[0]\n    for v in values:\n        if v > best:\n            best = v\n    return best\n', expect: 'error' }] },
  'review-2': { 6: [{ name: 'pnls[0] on the empty list', src: 'def worst_day(pnls):\n    worst = pnls[0]\n    for p in pnls:\n        if p < worst:\n            worst = p\n    return worst\n', expect: 'error' }] },
  'homework-2': {
    0: [{ name: 'a branch does not set action', src: 'def decide(price, stop, target):\n    if price < stop:\n        action = "sell"\n    elif price > target:\n        action = "take profit"\n    return action\n', expect: 'error' },
        { name: 'missing colon', src: 'def decide(price, stop, target):\n    if price < stop\n        action = "sell"\n    return action\n', expect: 'error' }],
    2: [{ name: 'no guard (runs too long)', src: 'def years_to_target(balance, rate, target):\n    years = 0\n    while balance < target:\n        balance = balance * (1 + rate)\n        years = years + 1\n    return years\n', expect: 'error' }],
  },
  'l5-decisions': { 7: [{ name: 'missing colon', src: 'def label(change):\n    if change > 0\n        word = "up"\n    return word\n', expect: 'error' },
                        { name: 'no else, word unset at 0', src: 'def label(change):\n    if change > 0:\n        word = "up"\n    elif change < 0:\n        word = "down"\n    return word\n', expect: 'test-3' }] },
};

// Lines that differ from `expect`, each one recorded in the audit (finding 2: a runtime error or a timeout keys as test-N, not error:
// in script mode it fails test 1; in function mode it fails the test whose call raised or ran too long).
const KNOWN = new Set([
  'l1-calculator[9] NameError', 'l2-naming-a-value[3] NameError (Price/price)', 'l4-asking-and-printing[4] int',
  'l4-asking-and-printing[7] starter (TypeError)', 'l4-asking-and-printing[9] still text', 'l4-asking-and-printing[10] no slice',
  'review-1[6] TypeError', 'l12-savings-script[10] header kept', 'l11-numbers-from-a-file[8] header kept: script print raises',
  'homework-3[8] prints, with the script print line', 'homework-3[8] int(fee), with the script print line',
  'l6-until-done[6] block never changes value (runs too long)', 'l6-until-done[9] block never changes balance (runs too long)',
  'l8-many-values[6] values[0] outside the length check', 'review-2[6] pnls[0] on the empty list',
  'homework-2[0] a branch does not set action', 'homework-2[2] no guard (runs too long)',
]);
const { makeRunner } = await import(pathToFileURL(path.join(appDir, 'tools/code-runner.mjs')).href);
const runner = makeRunner({ pkgs, root: appDir, jobs: 3 });
const dir = path.join(appDir, 'content/courses/first-python');
const jobs = [];
let unexpected = 0, differing = 0;
for (const set of [M, M2]) for (const [file, items] of Object.entries(set)) {
  const d = JSON.parse(fs.readFileSync(path.join(dir, file + '.json'), 'utf8'));
  const list = d.screens || d.items;
  for (const [idx, muts] of Object.entries(items)) {
    const spec = list[+idx].widget;
    const PRE = spec.starter.split('def ')[0];
    for (const m of muts) jobs.push(runner.grade(spec, m.src.replace('@PRE@', PRE), 'tests').then((r) => {
      const key = r.ok ? 'pass' : r.key;
      const first = r.rows && r.rows.find((x) => !x.ok);
      const got = first ? String(first.error || JSON.stringify(first.actual)).split('\n').pop().slice(0, 90) : '';
      const id = `${file}[${idx}] ${m.name}`, ok = key === m.expect;
      if (!ok) { differing++; if (!KNOWN.has(id)) unexpected++; }
      return `${ok ? 'ok  ' : 'DIFF'} ${id}: expect ${m.expect} got ${key} | ${got}`;
    }));
  }
}
const out = await Promise.all(jobs);
console.log(out.join('\n'));
console.log(`mutants ${out.length}, differing ${differing} (recorded in the audit: ${differing - unexpected}), unexpected ${unexpected}`);
await runner.close();
let rc = unexpected ? 1 : 0;
if (argv.includes('--concepts')) {
  const index = path.join(pkgs, 'pyodide-0.27.7', 'package');
  const { loadPyodide } = await import(pathToFileURL(path.join(index, 'pyodide.mjs')).href);
  const py = await loadPyodide({ indexURL: index + '/', stdout: (s) => console.log(s), stderr: (s) => console.log(s) });
  py.FS.mkdirTree('/zq/content');
  for (const f of fs.readdirSync(dir)) if (f.endsWith('.json')) py.FS.writeFile('/zq/content/' + f, fs.readFileSync(path.join(dir, f), 'utf8'));
  py.FS.writeFile('/zq/concepts.py', fs.readFileSync(path.join(HERE, 'first-python-L1-3-concepts.py'), 'utf8'));
  const code = py.runPython(`
import os, runpy, sys
os.environ['ZQ_FP_CONTENT'] = '/zq/content'
sys.setrecursionlimit(3000)
try:
    runpy.run_path('/zq/concepts.py', run_name='__main__'); rc = 0
except SystemExit as e:
    rc = e.code or 0
rc`);
  console.log(`concepts script inside Pyodide: exit ${code}`);
  rc = rc || code;
}
process.exit(rc);
