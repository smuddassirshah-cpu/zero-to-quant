"""Extend app/content/exams/stage-0.json to topics 0.6 (proof) and 0.7 (getting hired).

The existing parts (gcse, precalc, zetamac, script) are kept as they are, ids and order included. This script inserts the
paper `proof` after `precalc` and appends the checks `proofs-written` and `getting-hired` after the existing checks, so
paper and check positions 0 and 1 are unchanged. It is idempotent: a second run replaces the parts it added.
Route A for every key is below; check_numbers.py recomputes each by a second route.
Run: python3 docs/briefs/exam-stage-0-scripts/build.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'stage-0.json')
NEW_PARTS = ('proof', 'proofs-written', 'getting-hired')


def fb(correct, generic, by_key=None):
    d = {"correct": correct, "generic": generic}
    if by_key:
        d["byKey"] = by_key
    return d


def num(answer, tol, wrong=(), placeholder="a number"):
    w = {"kind": "numeric", "answer": answer, "tol": {"abs": tol}, "placeholder": placeholder}
    if wrong:
        w["wrong"] = [{"id": i, "value": v, "tol": {"abs": t}} for i, v, t in wrong]
    return w


def choice(options):
    return {"kind": "choice", "layout": "stack", "shuffle": True, "options": options}


def opt(id, text, why=None, correct=False):
    o = {"id": id, "text": text}
    if correct:
        o["correct"] = True
    if why:
        o["why"] = why
    return o


def line(id, text, why=None):
    d = {"id": id, "text": text}
    if why:
        d["why"] = why
    return d


def proof(lines, answer, flawed):
    return {"kind": "order", "lines": lines, "answer": answer, "distractors": flawed}


def item(id, d, skills, tags, pace, prose, question, widget, feedback, explain):
    return {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "prose": prose, "question": question,
            "widget": widget, "feedback": feedback, "explain": {"text": explain}}


def flawed_fb(correct, generic, lines, left_out):
    by_key = {ln["id"]: ln["why"] for ln in lines if ln.get("why")}
    by_key["left-out"] = left_out
    return fb(correct, generic, by_key)


def is_prime(n):
    return n > 1 and all(n % p for p in range(2, int(n ** 0.5) + 1))


P = []
ORDER_Q = "Put the proof in order. Leave out the two flawed lines."

# ---------------------------------------------------------------- direct proof
L1 = [line("o1", "Let $n$ be odd, so $n = 2k + 1$ for some integer $k$."),
      line("o2", "Then $n^2 - 1 = 4k^2 + 4k = 4k(k + 1)$."),
      line("o3", "One of $k$ and $k + 1$ is even, so $k(k + 1) = 2m$ for some integer $m$."),
      line("o4", "So $n^2 - 1 = 8m$, which is divisible by 8."),
      line("x1", "Check $n = 3$: $3^2 - 1 = 8$. So the claim holds.", "One example is not a proof for every odd $n$."),
      line("x2", "So $n^2 - 1 = 4k(k + 1)$ is divisible by 8, because 4 divides it.",
           "4 dividing it gives a factor of 4 only. The even product $k(k + 1)$ supplies the other 2.")]
P.append(item("p-direct-proof", 3, ["pv-direct"], ["direct-proof"], 240,
    "Claim: if $n$ is an odd integer, then $n^2 - 1$ is divisible by 8.", ORDER_Q,
    proof(L1, ["o1", "o2", "o3", "o4"], ["x1", "x2"]),
    flawed_fb("From the meaning of odd to a multiple of 8.", "Start from what odd means, then work towards a multiple of 8.", L1,
              "A line that belongs is missing. The proof needs the form of $n$, the factoring, the even product and the conclusion."),
    "A direct proof starts from the hypothesis, $n = 2k + 1$. Factoring gives $4k(k + 1)$, and $k(k + 1)$ is even. "
    "So $n^2 - 1$ is 8 times a whole number."))

k2 = 6
n2 = 2 * k2 + 1
m2 = (n2 ** 2 - 1) // 8
P.append(item("p-direct-step", 2, ["pv-direct"], ["direct-proof"], 60,
    "In the proof above, $n = 2k + 1$ and $n^2 - 1 = 8m$.", "What is $m$ when $n = 13$?",
    num(m2, 0.001, [("gave-whole", n2 ** 2 - 1, 0.001), ("forgot-square", (n2 - 1) / 8, 0.001)]),
    fb("$m = \\tfrac{k(k + 1)}{2}$.", "Find $k$ first, then $4k(k + 1)$, then divide by 8.",
       {"gave-whole": "You gave $n^2 - 1$ itself. Divide it by 8.", "forgot-square": "You used $n - 1$. Square $n$ first."}),
    f"Here $k = {k2}$, so $n^2 - 1 = 4 \\cdot {k2} \\cdot {k2 + 1} = {n2 ** 2 - 1} = 8 \\times {m2}$. So $m = {m2}$."))

# ---------------------------------------------------------------- contrapositive
L3 = [line("c1", "We prove the contrapositive: if $n$ is even, then $5n + 7$ is odd."),
      line("c2", "Suppose $n$ is even, so $n = 2k$ for some integer $k$."),
      line("c3", "Then $5n + 7 = 10k + 7 = 2(5k + 3) + 1$."),
      line("c4", "So $5n + 7$ is odd. The contrapositive holds, so the claim does too."),
      line("x1", "We prove the converse: if $n$ is odd, then $5n + 7$ is even.", "The converse is a different statement. Proving it says nothing about the claim."),
      line("x2", "We prove the inverse: if $5n + 7$ is odd, then $n$ is even.", "The inverse is equivalent to the converse, not to the claim.")]
P.append(item("p-contrapositive-proof", 3, ["pv-indirect"], ["contrapositive"], 180,
    "Claim: for an integer $n$, if $5n + 7$ is even, then $n$ is odd.", ORDER_Q,
    proof(L3, ["c1", "c2", "c3", "c4"], ["x1", "x2"]),
    flawed_fb("Not the conclusion, then not the hypothesis.", "Negate both parts and swap them, then prove that statement directly.", L3,
              "A line that belongs is missing. State the contrapositive, assume its hypothesis, compute, conclude."),
    "The contrapositive of 'if P then Q' is 'if not Q then not P'. It is equivalent to the claim. "
    "Here 'not Q' is '$n$ is even', which gives a formula to work with."))

P.append(item("p-contrapositive-form", 3, ["pv-indirect"], ["contrapositive"], 90,
    "For positive reals $a$ and $b$: if $ab > 9$, then $a > 3$ or $b > 3$.", "Which statement is its contrapositive?",
    choice([opt("a", "If $a \\le 3$ and $b \\le 3$, then $ab \\le 9$.", correct=True),
            opt("b", "If $a > 3$ or $b > 3$, then $ab > 9$.", "You swapped the two parts without negating them. That is the converse."),
            opt("c", "If $a \\le 3$ or $b \\le 3$, then $ab \\le 9$.", "You kept 'or'. The negation of an 'or' is an 'and'."),
            opt("d", "If $ab \\le 9$, then $a \\le 3$ and $b \\le 3$.", "You negated both parts without swapping them. That is the inverse.")]),
    fb("Swap the parts and negate both.", "Write 'if not Q, then not P', and negate the 'or' with care."),
    "The contrapositive is 'if not Q, then not P'. 'Not ($a > 3$ or $b > 3$)' is '$a \\le 3$ and $b \\le 3$'. "
    "'Not $ab > 9$' is '$ab \\le 9$'."))

# ---------------------------------------------------------------- contradiction
log25 = math.log2(5)
L5 = [line("k1", "Suppose, for contradiction, that $\\log_2 5 = \\tfrac{p}{q}$ with $p$ and $q$ positive integers."),
      line("k2", "Then $2^{p/q} = 5$, so $2^p = 5^q$."),
      line("k3", "$2^p$ is even, as $p \\ge 1$. $5^q$ is odd, as a product of odd numbers."),
      line("k4", "An even number cannot equal an odd one. So the assumption is false, and $\\log_2 5$ is irrational."),
      line("x1", f"A calculator shows $\\log_2 5 \\approx {log25:.6f}$, and the digits do not repeat.", "A display shows a few digits. It cannot show that they never repeat."),
      line("x2", "So $p = q\\log_2 5$, which shows that $\\log_2 5$ is rational.", "That restates the assumption. It reaches no contradiction.")]
P.append(item("p-contradiction-proof", 4, ["pv-indirect"], ["contradiction"], 240,
    "Claim: $\\log_2 5$ is irrational.", ORDER_Q,
    proof(L5, ["k1", "k2", "k3", "k4"], ["x1", "x2"]),
    flawed_fb("Assume a fraction, then reach even equals odd.", "Assume the opposite, clear the fraction from the exponent, then compare parities.", L5,
              "A line that belongs is missing. The proof needs the assumption, the equation, the parities and the contradiction."),
    "We assume the opposite and derive something impossible. $2^p = 5^q$ would make an even number equal an odd one."))

primes6 = [p for p in range(2, 18) if is_prime(p)]
N6 = math.prod(primes6) + 1
f6 = next(p for p in range(2, N6) if N6 % p == 0)
P.append(item("p-euclid-number", 3, ["pv-indirect"], ["contradiction"], 150,
    "Euclid's proof that the primes never run out assumes a finite list, multiplies its primes and adds 1.",
    "Take the primes 2, 3, 5, 7, 11, 13 and 17. What is the smallest prime factor of that number?",
    num(f6, 0, [("assumed-prime", N6, 0)]),
    fb("The number is not prime, but its factors are new primes.", "Find the number, then try primes from 19 upwards.",
       {"assumed-prime": f"You took {N6:,} itself as prime. It need not be; any prime factor of it is missing from the list."}),
    f"The number is $2 \\times 3 \\times \\dots \\times 17 + 1 = {N6:,}$. None of the listed primes divides it, since each leaves remainder 1. "
    f"Trying 19 first gives ${N6:,} = 19 \\times {N6 // 19:,}$."))

# ---------------------------------------------------------------- induction
L7 = [line("i1", "Base case: at $n = 4$, $3^4 = 81 > 64 = 4^3$."),
      line("i2", "Inductive step: suppose $3^k > k^3$ for some $k \\ge 4$."),
      line("i3", "Then $3^{k+1} = 3 \\cdot 3^k > 3k^3$."),
      line("i4", "For $k \\ge 4$, $\\left(1 + \\tfrac1k\\right)^3 \\le \\left(\\tfrac54\\right)^3 < 2 < 3$, so $3k^3 > (k + 1)^3$."),
      line("i5", "So $3^{k+1} > (k + 1)^3$. By induction, $3^n > n^3$ for every $n \\ge 4$."),
      line("x1", "Base case: at $n = 1$, $3^1 = 3 > 1$.", "The claim fails at $n = 3$, where both sides are 27. The chain must start at 4."),
      line("x2", "Suppose $3^n > n^3$ for every $n$; then it holds at $k + 1$.", "That assumes what we are proving. The step assumes it for one $k$ only.")]
P.append(item("p-induction-proof", 5, ["pv-induction"], ["induction"], 360,
    "Claim: $3^n > n^3$ for every integer $n \\ge 4$.", ORDER_Q,
    proof(L7, ["i1", "i2", "i3", "i4", "i5"], ["x1", "x2"]),
    flawed_fb("A base case at 4, then a step from $k$ to $k + 1$.", "Check the base case first, then assume the claim for one $k$ and reach $k + 1$.", L7,
              "A line that belongs is missing. The proof needs the base, the hypothesis, two inequalities and the conclusion."),
    "The base case starts the chain at 4, and the step carries it from $k$ to $k + 1$. "
    "The step needs $\\left(1 + \\tfrac1k\\right)^3 < 3$, which holds once $k \\ge 4$."))

N8 = next(N for N in range(1, 50) if all(3 ** n > n ** 3 for n in range(N, 200)))
P.append(item("p-induction-base", 3, ["pv-induction"], ["induction"], 90,
    "Some inequalities hold only from some point on.", "What is the smallest $N$ such that $3^n > n^3$ for every integer $n \\ge N$?",
    num(N8, 0, [("first-true", 1, 0), ("equal-case", 3, 0)]),
    fb("The last failure is at $n = 3$.", "Test $n = 1, 2, 3, 4$, then trust the inductive step from there.",
       {"first-true": "It holds at 1 and 2 but fails at 3. The chain must start after the last failure.",
        "equal-case": "At $n = 3$ both sides are 27, so the strict inequality fails there."}),
    "$3^3 = 27 = 3^3$ fails the strict inequality, and $3^4 = 81 > 64$. The step works from 4 on, so $N = 4$."))

# ---------------------------------------------------------------- counterexample
n9 = next(n for n in range(1, 100) if not is_prime(n * n + n + 17))
v9 = n9 * n9 + n9 + 17
L9 = [line("e1", "The claim is about every positive integer $n$, so one failure refutes it."),
      line("e2", f"Take $n = {n9}$."),
      line("e3", f"Then $n^2 + n + 17 = {n9 * n9} + {n9} + 17 = {v9}$."),
      line("e4", f"${v9} = 17 \\times 17$, so it is not prime. The claim is false."),
      line("x1", f"For $n = 1$ to ${n9 - 1}$ the value is prime, so the claim is true.", "Fifteen cases do not cover every $n$. One failure is enough to refute it."),
      line("x2", "Take $n = 0$, which gives 17.", "0 is not a positive integer, and 17 is prime anyway.")]
P.append(item("p-counterexample-proof", 3, ["pv-logic", "pv-direct"], ["counterexample"], 180,
    "Claim: for every positive integer $n$, $n^2 + n + 17$ is prime.", "Put the disproof in order. Leave out the two flawed lines.",
    proof(L9, ["e1", "e2", "e3", "e4"], ["x1", "x2"]),
    flawed_fb("One value of $n$ where it fails.", "A claim about every $n$ falls to one counterexample. Find it and check it.", L9,
              "A line that belongs is missing. State what refutes the claim, pick $n$, compute, and show the value is not prime."),
    f"A 'for every' claim falls to one counterexample. At $n = {n9}$, $n^2 + n + 17 = {n9} \\cdot {n9 + 1} + 17 = 17^2$."))

n10 = next(n for n in range(1, 200) if not is_prime(2 * n * n + 29))
v10 = 2 * n10 * n10 + 29
P.append(item("p-first-failure", 4, ["pv-logic"], ["counterexample"], 180,
    "Someone claims that $2n^2 + 29$ is prime for every positive integer $n$.", "What is the smallest positive $n$ that refutes the claim?",
    num(n10, 0, [("gave-value", v10, 0)]),
    fb("Look for an $n$ that makes every term share a factor.", "Ask which $n$ makes $2n^2$ a multiple of 29.",
       {"gave-value": f"You gave the value {v10:,}. The question asks for $n$."}),
    f"At $n = {n10}$, $2n^2 + 29 = 29(2 \\cdot {n10} + 1) = 29 \\times {2 * n10 + 1}$. Every $n$ from 1 to {n10 - 1} gives a prime, so {n10} is the first failure."))

# ---------------------------------------------------------------- the earlier levels
P.append(item("p-negate-quantifiers", 3, ["pv-logic"], ["negation"], 120,
    "Statement: every desk has a trader who made a profit on every day.", "Which is its negation?",
    choice([opt("a", "Some desk has, for each of its traders, a day on which that trader made no profit.", correct=True),
            opt("b", "Every desk has a trader who made no profit on some day.", "You negated only the last part. 'Every desk' and 'a trader' must flip too."),
            opt("c", "No desk has a trader who made a profit on any day.", "You turned 'every day' into 'any day'. The negation needs only one bad day per trader."),
            opt("d", "Some desk has a trader who made no profit on some day.", "You kept 'a trader'. The negation must cover every trader of that desk.")]),
    fb("Each quantifier flips, from the outside in.", "Flip 'every' to 'some' and 'some' to 'every', one quantifier at a time."),
    "Negation flips each quantifier in turn. Every desk, a trader and every day become some desk, every trader and some day. "
    "Then the profit statement itself is negated."))

P.append(item("p-onto-function", 2, ["pv-sets"], ["onto-one-to-one"], 90,
    "Each function sends integers to integers.", "Which function is onto but not one-to-one?",
    choice([opt("a", "$f(n) = \\left\\lceil \\tfrac{n}{2} \\right\\rceil$", correct=True),
            opt("b", "$f(n) = 2n$", "It is one-to-one, but odd numbers are never reached, so it is not onto."),
            opt("c", "$f(n) = n + 3$", "It is one-to-one and onto: every $m$ comes from $m - 3$ alone."),
            opt("d", "$f(n) = n^2$", "It misses negative numbers, so it is not onto.")]),
    fb("Every value reached, some reached twice.", "For each function, ask whether every integer is reached, and whether any is reached twice."),
    "$\\left\\lceil \\tfrac{n}{2} \\right\\rceil$ sends both $2m - 1$ and $2m$ to $m$. So every integer is reached, twice, which breaks one-to-one but keeps onto."))

PAPER = {"kind": "paper", "id": "proof", "name": "Reasoning and proof", "minutes": int(math.ceil(1.25 * sum(it["pace"] for it in P) / 60 / 5) * 5),
         "pass": 0.7, "items": P}
CHECKS = [
    {"kind": "check", "id": "proofs-written", "name": "Five proofs written out so a stranger can check every step",
     "detail": "One statement each by direct proof, contrapositive, contradiction, induction and counterexample, in full sentences. "
               "Ask someone to check every step, or check them yourself a week later."},
    {"kind": "check", "id": "getting-hired", "name": "Getting hired (0.7): a target list, a one-page CV and three stories",
     "detail": "A list of the firms you will apply to, with each one's opening date. A one-page CV a stranger can read in a minute. "
               "Three behavioural stories written as situation, task, action and result."},
]

if __name__ == '__main__':
    with open(OUT, encoding='utf8') as f:
        doc = json.load(f)
    parts = [p for p in doc["parts"] if p.get("id") not in NEW_PARTS]
    at = [p.get("id") for p in parts].index("precalc") + 1
    doc["parts"] = parts[:at] + [PAPER] + parts[at:] + CHECKS
    doc["description"] = ("The exit test for From nothing: a GCSE Higher style paper, a precalculus test and a proof paper. "
                          "Then a mental arithmetic score, a script that runs, five written proofs and your 0.7 plan.")
    with open(OUT, 'w', encoding='utf8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write('\n')
    ds = [it["difficulty"] for it in P]
    print("proof paper:", len(P), "items,", PAPER["minutes"], "min, ramp", [ds.count(k) for k in (2, 3, 4, 5)])
    print("parts:", [p.get("id") for p in doc["parts"]])
