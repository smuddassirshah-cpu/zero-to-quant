"""Build app/content/exams/topic-0.6.json (topic 0.6, Reasoning and proof: the proof course, levels 1 to 3).

Route A for every key: the closed forms below. check_numbers.py recomputes each value by a second route
(brute force, exact fractions, truth tables by enumeration) and asserts it at its path in the written file.
Run from anywhere: python3 docs/briefs/exam-0.6-scripts/build.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-0.6.json')


def fb(correct, generic, by_key=None):
    d = {"correct": correct, "generic": generic}
    if by_key:
        d["byKey"] = by_key
    return d


def num(answer, tol, wrong=(), unit=None, placeholder="a number", label="Answer", accept=None):
    w = {"kind": "numeric", "answer": answer, "tol": {"abs": tol}, "placeholder": placeholder, "label": label}
    if unit:
        w["unit"] = unit
    if accept:
        w["accept"] = accept
    if wrong:
        w["wrong"] = [{"id": i, "value": v, "tol": {"abs": t}} for i, v, t in wrong]
    return w


def choice(options, kind="choice"):
    return {"kind": kind, "layout": "stack", "shuffle": True, "options": options}


def opt(id, text, why=None, correct=False):
    o = {"id": id, "text": text}
    if correct:
        o["correct"] = True
    if why:
        o["why"] = why
    return o


def order(lines, answer, distractors=(), same=None):
    w = {"kind": "order", "lines": [], "answer": answer}
    for ln in lines:
        d = {"id": ln[0], "text": ln[1]}
        if len(ln) > 2:
            d["why"] = ln[2]
        w["lines"].append(d)
    if distractors:
        w["distractors"] = list(distractors)
    if same:
        w["same"] = same
    return w


def item(id, d, skills, tags, pace, title, prose, question, widget, feedback, explain):
    return {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title,
            "prose": prose, "question": question, "widget": widget, "feedback": feedback,
            "explain": {"text": explain}}


def parts(id, d, skills, tags, pace, title, prose, question, ps, explain):
    return {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title,
            "prose": prose, "question": question,
            "parts": [{"question": q, "widget": w, "feedback": f} for q, w, f in ps],
            "explain": {"text": explain}}


def tf(answer, wrong=None):
    c = {"edit": True, "answer": answer, "accept": (["True", "true", "t"] if answer == "T" else ["False", "false", "f"]),
         "placeholder": "T or F"}
    if wrong:
        c["wrong"] = [{"id": wrong, "text": "F" if answer == "T" else "T"}]
    return c


items = []

# ---------------------------------------------------------------- difficulty 2
# A1 L1 (l2): rows of a truth table on five letters
items.append(item(
    "e-five-letter-rows", 2, ["pv-logic"], ["truth-table"], 45, "Rows for five letters",
    "A risk alert depends on five conditions, $P$, $Q$, $R$, $S$ and $T$. Each is either T or F.",
    "How many rows does the alert's full truth table need?",
    num(2 ** 5, 0, [("times", 2 * 5, 0), ("square", 5 ** 2, 0)], placeholder="a whole number", label="Rows"),
    fb("$2^5 = 32$ rows: each new letter doubles the count.",
       "Each letter has two values, and the choices multiply.",
       {"times": "You multiplied 2 by 5 to get 10. Each new letter doubles the rows, so it is $2^5$.",
        "square": "You took $5^2 = 25$. The base is the two truth values, so it is $2^5$."}),
    "One letter gives 2 rows, and each extra letter doubles them. Five letters give $2 \\times 2 \\times 2 \\times 2 \\times 2 = 32$."))

# A2 L1 (l3): a rule whose hypothesis is false is kept
items.append(item(
    "e-vacuous-rule", 2, ["pv-logic"], ["vacuous"], 60, "A rule nobody triggered",
    "Rule: **if a trade is over £2m, it is reported by noon**. Today the desk made one trade, of £500,000, reported at 3pm.",
    "Was the rule kept today?",
    choice([
        opt("kept", "Yes. The trade was not over £2m, so the rule asked nothing of it.", correct=True),
        opt("late", "No. The trade was reported after noon.",
            "You checked the conclusion alone. The rule only binds trades over £2m."),
        opt("no-value", "Neither. With no trade over £2m the rule has no truth value today.",
            "You treated a false hypothesis as leaving the rule undefined. An implication with a false hypothesis is true."),
        opt("converse", "No. A trade reported after noon must have been over £2m.",
            "You read the rule backwards. That is its converse, which the rule does not claim.")]),
    fb("The hypothesis is false, so the implication is true: the rule was kept.",
       "An implication fails only when its hypothesis is true and its conclusion false."),
    "$P \\Rightarrow Q$ is false only on the row where $P$ is T and $Q$ is F. Here $P$, over £2m, is F. "
    "So the rule holds today, vacuously."))

# A3 L2 (l6): elements of a set that holds sets
items.append(item(
    "e-set-elements", 2, ["pv-sets"], ["cardinality"], 45, "Counting elements",
    "Let $X = \\{2, \\{2, 3\\}, \\{3\\}, 2\\}$.",
    "What is $|X|$, the number of elements of $X$?",
    num(3, 0, [("repeat", 4, 0), ("flatten", 2, 0)], placeholder="a whole number", label="Elements"),
    fb("The elements are $2$, $\\{2, 3\\}$ and $\\{3\\}$, so $|X| = 3$.",
       "List the distinct objects between the outer braces. A set inside counts as one object.",
       {"repeat": "You counted the repeated 2 twice, giving 4. Repeats do not add elements.",
        "flatten": "You counted the numbers 2 and 3 inside. $\\{2, 3\\}$ and $\\{3\\}$ are each one element."}),
    "The outer braces hold $2$, $\\{2, 3\\}$, $\\{3\\}$ and $2$ again. The repeat adds nothing. "
    "Each inner set is one element, so $|X| = 3$."))

# A4 L2 (l7): inclusion-exclusion on a bond book
n_union = 22 + 17 - 9
items.append(item(
    "e-callable-floating", 2, ["pv-sets"], ["inclusion-exclusion"], 60, "Callable or floating",
    "A book holds 40 bonds. 22 are callable, 17 pay a floating rate, and 9 are both.",
    "How many bonds are callable or floating, or both?",
    num(n_union, 0, [("added", 22 + 17, 0), ("twice", 22 + 17 - 2 * 9, 0)], placeholder="a whole number", label="Bonds"),
    fb("$|C \\cup F| = 22 + 17 - 9 = 30$.",
       "Add the two counts, then take off the bonds counted twice.",
       {"added": "You added 22 and 17 to get 39. The 9 bonds that are both were counted twice.",
        "twice": "You took off the overlap twice. It was counted twice, so remove it once."}),
    "$|C \\cup F| = |C| + |F| - |C \\cap F|$, since the overlap sits in both counts. "
    "That gives $22 + 17 - 9 = 30$, and $40 - 30 = 10$ bonds are neither."))

# A5 L1 (l4): a witness for an existential claim
items.append(item(
    "e-witness-solve", 2, ["pv-logic"], ["witness"], 45, "Name the witness",
    "Consider $\\exists x \\in \\mathbb{Z},\\ 4x + 7 = -5$.",
    "What is the witness $x$?",
    num(-3, 0, [("sign", 3, 0), ("added", 0.5, 0.01)], placeholder="an integer", label="Witness"),
    fb("$4x = -12$, so $x = -3$, an integer. The claim is true.",
       "Take 7 from both sides, then divide by 4.",
       {"sign": "You lost the sign. $4 \\times 3 + 7 = 19$, not $-5$.",
        "added": "You added 7 instead of taking it away. Also, 0.5 is not in $\\mathbb{Z}$."}),
    "An existential claim needs one value that works. $4(-3) + 7 = -5$, and $-3 \\in \\mathbb{Z}$. So $x = -3$ is the witness."))

# ---------------------------------------------------------------- difficulty 3
# B1 L1 (l5): negating a nested claim
items.append(item(
    "e-negate-desk", 3, ["pv-logic"], ["negation"], 90, "The opposite of a rota rule",
    "Claim: **every desk that trades FX has a trader on call every night**.",
    "Which sentence is its negation?",
    choice([
        opt("right", "Some desk trades FX and has a night with no trader on call.", correct=True),
        opt("all-not", "No desk that trades FX has a trader on call on any night.",
            "You negated every part and kept the quantifiers. Each quantifier must flip."),
        opt("hyp", "Some desk that does not trade FX has a trader on call every night.",
            "You negated the hypothesis. $\\lnot(P \\Rightarrow Q)$ keeps $P$ and negates $Q$."),
        opt("kept-all", "Every desk that trades FX has some night with no trader on call.",
            "You kept the first \"every\". The negation needs only one desk that fails.")]),
    fb("Some FX desk has a night with no one on call. That one desk breaks the claim.",
       "Flip each quantifier in place, and negate the implication as $P$ and not $Q$."),
    "The outer \"every desk\" becomes \"some desk\", which must still trade FX. "
    "Inside, \"every night\" becomes \"some night\" with no one on call. One such desk breaks the claim."))

# B2 L1 (l3, l5): the inverse and the negation of an implication, by truth table
items.append(item(
    "e-converse-table", 3, ["pv-logic"], ["truth-table", "negation"], 120, "The inverse and the negation",
    "The column $P \\Rightarrow Q$ is given. Fill the inverse $\\lnot P \\Rightarrow \\lnot Q$ and the column $P \\land \\lnot Q$.",
    "Fill both columns with T or F.",
    {"kind": "table", "columns": ["$P$", "$Q$", "$P \\Rightarrow Q$", "$\\lnot P \\Rightarrow \\lnot Q$", "$P \\land \\lnot Q$"],
     "rows": [["T", "T", "T", tf("T"), tf("F")],
              ["T", "F", "F", tf("T"), tf("T")],
              ["F", "T", "T", tf("F", "ft-inverse"), tf("F", "imp-not-ft")],
              ["F", "F", "T", tf("T"), tf("F", "imp-not-ff")]]},
    fb("$P \\land \\lnot Q$ is the opposite of $P \\Rightarrow Q$ on every row. The inverse matches the converse instead.",
       "An implication is F only where its hypothesis is T and its conclusion F. An \"and\" is T only where both parts are T.",
       {"ft-inverse": "On the F, T row, $\\lnot P$ is T and $\\lnot Q$ is F, so the inverse is F.",
        "imp-not-ft": "You read it as $P \\Rightarrow \\lnot Q$. An \"and\" is T only when both parts are T.",
        "imp-not-ff": "You read it as $P \\Rightarrow \\lnot Q$. An \"and\" is T only when both parts are T."}),
    "The inverse reads T, T, F, T, the same as the converse, not as $P \\Rightarrow Q$. "
    "$P \\land \\lnot Q$ reads F, T, F, F, the opposite of $P \\Rightarrow Q$ on every row. So it is the negation of the implication."))

# B3 L2 (l8): functions between finite sets
items.append(item(
    "e-functions-count", 3, ["pv-sets"], ["function-count"], 75, "Routing three orders",
    "Each of 3 orders is sent to one of 4 venues. Several orders may go to the same venue.",
    "How many functions from the orders to the venues are there?",
    num(4 ** 3, 0, [("swapped", 3 ** 4, 0), ("product", 3 * 4, 0)], placeholder="a whole number", label="Functions"),
    fb("Each order has 4 choices, so there are $4^3 = 64$ functions.",
       "A function picks one venue for each order. Multiply the choices.",
       {"swapped": "You took $3^4 = 81$. That gives each venue one of 3 orders, which is a function the other way.",
        "product": "You took $3 \\times 4 = 12$. That counts the (order, venue) pairs, not the functions."}),
    "A function gives every order exactly one venue. Order 1, order 2 and order 3 each have 4 choices. "
    "So there are $4 \\times 4 \\times 4 = 64$."))

# B4 L2 (l9): one-to-one functions
items.append(item(
    "e-injection-count", 3, ["pv-sets"], ["one-to-one"], 75, "Three analysts, six sectors",
    "Three analysts are each given one of 6 sectors to cover. No two analysts share a sector.",
    "How many such one-to-one functions are there?",
    num(6 * 5 * 4, 0, [("any", 6 ** 3, 0), ("unordered", math.comb(6, 3), 0)], placeholder="a whole number",
        label="Functions"),
    fb("$6 \\times 5 \\times 4 = 120$: each analyst has one fewer sector left.",
       "The first analyst has 6 choices, the next has one fewer, and so on.",
       {"any": "You took $6^3 = 216$. That lets two analysts share a sector, so it is not one-to-one.",
        "unordered": "You counted the 20 sets of 3 sectors. Which analyst gets which sector matters."}),
    "One-to-one means no sector is used twice. The choices fall from 6 to 5 to 4. That gives $120$ functions."))

# B5 L2 (l9): inverse of a fee schedule
c_inv = (14.5 - 2.5) / 0.8
items.append(item(
    "e-fee-inverse", 3, ["pv-sets"], ["inverse"], 75, "Lots from a bill",
    "A broker charges a fixed £2.50 plus £0.80 a lot: $c(n) = 2.5 + 0.8n$. It is one-to-one, so it has an inverse on its image.",
    "A bill reads £14.50. How many lots were traded?",
    num(round(c_inv, 6), 0.01, [("forward", round(2.5 + 0.8 * 14.5, 6), 0.01), ("added", round((14.5 + 2.5) / 0.8, 6), 0.01)],
        label="Lots", accept="$c^{-1}(14.5) = (14.5 - 2.5) / 0.8 = 15$"),
    fb("$c^{-1}(y) = \\dfrac{y - 2.5}{0.8}$, so $c^{-1}(14.5) = 15$ lots.",
       "Undo the steps in reverse: take off the fixed £2.50, then divide by £0.80.",
       {"forward": "You worked out $c(14.5) = 14.1$. The bill is an output, so apply $c^{-1}$.",
        "added": "You added the £2.50, giving 21.25. Undoing $+2.5$ means taking it away."}),
    "$c$ multiplies by 0.8 and then adds 2.5. The inverse undoes them in reverse: subtract 2.5, then divide by 0.8. "
    "$(14.5 - 2.5) / 0.8 = 12 / 0.8 = 15$."))

# B6 L2 (l9): one-to-one but not onto
items.append(item(
    "e-exp-onto", 3, ["pv-sets"], ["onto"], 90, "Growth factors",
    "A price is multiplied by $g(x) = e^x$ when its natural log rises by $x$. Take $g : \\mathbb{R} \\to \\mathbb{R}$.",
    "Which describes $g$?",
    choice([
        opt("inj", "One-to-one but not onto: no $x$ gives $g(x) = -1$.", correct=True),
        opt("bij", "One-to-one and onto, since $\\ln$ undoes it.",
            "You took $\\ln$ as a full inverse. $\\ln y$ exists only for $y > 0$, so negative targets have no $x$."),
        opt("onto", "Onto but not one-to-one.",
            "You swapped the two tests. $e^a = e^b$ forces $a = b$, so it is one-to-one."),
        opt("neither", "Neither one-to-one nor onto.",
            "You saw that $-1$ is never reached and stopped there. $e^a = e^b$ still forces $a = b$, so $g$ is one-to-one.")]),
    fb("$e^a = e^b$ gives $a = b$, but every output is positive, so $-1$ has no preimage.",
       "Check one-to-one with $g(a) = g(b)$. For onto, find an output of $\\mathbb{R}$ that is never reached."),
    "Taking $\\ln$ of $e^a = e^b$ gives $a = b$, so $g$ is one-to-one. "
    "But $e^x > 0$ for every $x$, so $y = -1$ is never reached. With codomain $(0, \\infty)$ it would be onto."))

# B7 L2 (l7): an element chase with two cases
items.append(item(
    "e-element-chase", 3, ["pv-direct", "pv-sets"], ["element-chase"], 150, "Chasing an element",
    "Claim: $(A \\cup B) \\cap C \\subseteq (A \\cap C) \\cup B$ for all sets $A$, $B$, $C$.",
    "Put the proof in order. Two lines do not belong: move them to Left out.",
    order([
        ("s1", "Let $x \\in (A \\cup B) \\cap C$."),
        ("s2", "Then $x \\in C$, and $x \\in A$ or $x \\in B$."),
        ("s3", "If $x \\in A$, then $x \\in A \\cap C$, since $x \\in C$."),
        ("s4", "If $x \\in B$, then $x$ is in the right side already."),
        ("s5", "In either case $x \\in (A \\cap C) \\cup B$."),
        ("s6", "So every element of the left side is in the right side. $\\blacksquare$"),
        ("d1", "Then $x \\in A$, $x \\in B$ and $x \\in C$.",
         "You turned \"or\" into \"and\". $x \\in A \\cup B$ only says $x$ is in at least one of them."),
        ("d2", "Take $A = \\{1\\}$, $B = \\varnothing$, $C = \\{1\\}$: both sides are $\\{1\\}$.",
         "You kept an example. One case is evidence, not a step of the proof.")],
        ["s1", "s2", "s3", "s4", "s5", "s6"], ["d1", "d2"], [["s3", "s4"]]),
    fb("Pick an element, unpack the definitions, split into the two cases and repack.",
       "Start from an element of the left side, then use the meaning of $\\cup$ and $\\cap$.",
       {"d1": "You kept the line that turns \"or\" into \"and\". Split into cases instead.",
        "d2": "You kept the example. It checks one case and proves nothing for all sets.",
        "left-out": "You left out a line the proof needs."}),
    "Subset means every element of the left side lies in the right. The \"or\" in $A \\cup B$ forces two cases. "
    "The cases may come in either order."))

# B8 L3 (l10): a direct proof with two letters
items.append(item(
    "e-odd-direct", 3, ["pv-direct"], ["direct-proof"], 120, "Odd, odd, odd",
    "Claim: if $m$ and $n$ are odd, then $mn + m + n$ is odd. Write $m = 2a + 1$ and $n = 2b + 1$ for integers $a$ and $b$.",
    "Which line finishes the proof?",
    choice([
        opt("right", "$mn + m + n = 4ab + 4a + 4b + 3 = 2(2ab + 2a + 2b + 1) + 1$, twice an integer plus 1.",
            correct=True),
        opt("same", "Write $m = n = 2k + 1$. Then $mn + m + n = 4k^2 + 8k + 3 = 2(2k^2 + 4k + 1) + 1$, which is odd.",
            "You used one letter for both numbers. That proves only the case $m = n$."),
        opt("example", "With $m = 3$ and $n = 5$: $15 + 3 + 5 = 23$. With $m = 7$ and $n = 9$: $63 + 7 + 9 = 79$. Both are odd.",
            "You checked two cases. The claim is about every pair of odd numbers."),
        opt("gap", "$mn + m + n = 4ab + 4a + 4b + 3$, and 4 is even, so the total is odd.",
            "You stopped before the form $2(\\text{integer}) + 1$. Saying \"4 is even\" does not reach the definition of odd.")]),
    fb("$4ab + 4a + 4b + 3 = 2(2ab + 2a + 2b + 1) + 1$, which is odd by definition.",
       "Expand with separate letters for $m$ and $n$, then write the result as $2(\\text{integer}) + 1$."),
    "Two odd numbers need two letters, $a$ and $b$, or the proof covers only $m = n$. "
    "Expanding gives $4ab + 4a + 4b + 3$. Taking out 2 leaves the form that defines odd."))

# B9 L3 (l11): choosing the contrapositive
items.append(item(
    "e-quarters-contrapositive", 3, ["pv-indirect"], ["contrapositive"], 90, "Average and best quarter",
    "Claim: **if a fund's average return over four quarters is above 3%, then some quarter returned above 3%**. We prove it by contrapositive.",
    "Which statement do we prove?",
    choice([
        opt("contra", "If every quarter returned at most 3%, the average is at most 3%.", correct=True),
        opt("converse", "If some quarter returned above 3%, the average is above 3%.",
            "You swapped hypothesis and conclusion. That is the converse, and it is false: one good quarter is not enough."),
        opt("inverse", "If the average is at most 3%, every quarter returned at most 3%.",
            "You negated both parts but kept their order. That is the inverse, which says something different."),
        opt("negation", "The average is above 3% and every quarter returned at most 3%.",
            "You wrote the negation of the claim. That is what a proof by contradiction assumes.")]),
    fb("$\\lnot Q \\Rightarrow \\lnot P$: no quarter above 3% forces the average to be at most 3%.",
       "Negate the conclusion, then show the negated hypothesis follows."),
    "The contrapositive is easy to prove: four returns each at most 3% sum to at most 12%. "
    "Dividing by 4 gives an average of at most 3%. That proves the claim."))

# B10 L3 (l12): rational plus irrational, by contradiction
items.append(item(
    "e-rational-plus-irrational", 3, ["pv-indirect"], ["contradiction"], 90, "Rational plus irrational",
    "Claim: if $a$ is rational and $b$ is irrational, then $a + b$ is irrational. We prove it by contradiction.",
    "Which argument is a correct proof?",
    choice([
        opt("right", "Suppose $a + b = s$ with $s$ rational. Then $b = s - a$ is a difference of rationals, so rational, a contradiction.",
            correct=True),
        opt("example", "Take $a = 1$ and $b = \\sqrt{2}$. Then $1 + \\sqrt{2}$ is irrational.",
            "You argued from one pair. The proof must cover every rational $a$ and irrational $b$."),
        opt("assumed", "Suppose $a + b$ is irrational. Then $b = (a + b) - a$ is irrational, as required.",
            "You assumed the conclusion. A contradiction proof assumes its opposite, that $a + b$ is rational."),
        opt("reversed", "Suppose $a + b$ is rational. A sum is rational only when both parts are, so $b$ is rational.",
            "You used a false rule: $\\sqrt{2} + (1 - \\sqrt{2}) = 1$ is rational. Write $b = s - a$ instead.")]),
    fb("Assume $a + b$ is rational. Then $b = (a + b) - a$ is rational, against the hypothesis.",
       "Assume the opposite of the conclusion, then solve for $b$."),
    "The opposite of the conclusion is \"$a + b$ is rational\". Rationals are closed under subtraction, so $b = (a + b) - a$ is rational. "
    "That contradicts $b$ being irrational."))

# B11 L3 (l13): a step with no base case
items.append(item(
    "e-step-no-base", 3, ["pv-induction"], ["base-case"], 90, "A step with nothing under it",
    "Claim: $n + 1 < n$ for every whole number $n \\ge 1$. Step: assume $k + 1 < k$. Adding 1 gives $k + 2 < k + 1$.",
    "The step is valid. What does the argument show?",
    choice([
        opt("nothing", "Nothing. The base case fails, since $1 + 1 < 1$ is false, so the chain never starts.", correct=True),
        opt("true", "The claim is true, since the step works for every $k$.",
            "You skipped the base case. A step only carries truth forward from a case that holds."),
        opt("from-two", "The claim fails at $n = 1$ but holds from $n = 2$, since the step carries it on.",
            "You let the step carry truth from a false case. At $n = 2$ the claim reads $3 < 2$, also false."),
        opt("large", "The claim holds for every large enough $n$.",
            "You read the step as eventual truth. With no true case to start from, the step proves nothing.")]),
    fb("The step is sound, but there is no true case for it to start from.",
       "Induction needs both parts. Check the base case."),
    "A valid step says: if case $k$ holds, case $k + 1$ holds. At $n = 1$ the claim reads $2 < 1$, which is false. "
    "So nothing is ever passed along, and the claim is false for every $n$."))

# B12 L3 (l15): a write-up that proves the converse
items.append(item(
    "e-proved-converse", 3, ["pv-writing"], ["checking-proofs"], 90, "Which way round",
    "A write-up reads: \"Claim: if $n^2$ is a multiple of 4, then $n$ is a multiple of 4. "
    "Proof: let $n = 4k$. Then $n^2 = 16k^2 = 4(4k^2)$, a multiple of 4. $\\blacksquare$\"",
    "What is wrong with it?",
    choice([
        opt("converse", "It proves the converse. The claim itself is false: $n = 2$ gives $n^2 = 4$.", correct=True),
        opt("fine", "Nothing. It starts from the definition and reaches a multiple of 4.",
            "You checked each line but not the direction. The proof assumes the conclusion and reaches the hypothesis."),
        opt("letters", "It should write $n^2 = 4k$ and $n = 4m$ with two letters.",
            "You fixed a style point. The fault is which statement was proved, not the letters."),
        opt("induction", "A claim about every $n$ needs induction.",
            "You picked a method by the word \"every\". The claim is false, so no method proves it.")]),
    fb("The proof shows $4 \\mid n \\Rightarrow 4 \\mid n^2$, the converse. $n = 2$ refutes the claim.",
       "Compare what the proof assumes with the claim's hypothesis."),
    "The claim's hypothesis is about $n^2$, but the proof starts from $n = 4k$. So it proves the converse. "
    "A reader who checks the first line against the claim sees it at once, and $n = 2$ refutes the claim."))

# ---------------------------------------------------------------- difficulty 4
# C1 L3 (l14): the first counterexample of a square-free-looking formula
def _is_sq(v):
    return math.isqrt(v) ** 2 == v


counter = next(n for n in range(1, 200) if _is_sq(10 * n * n + 1))
items.append(item(
    "e-prime-formula", 4, ["pv-logic", "pv-direct"], ["counterexample"], 150, "A value that lands on a square",
    "Claim: for every whole number $n \\ge 1$, the number $10n^2 + 1$ is not a perfect square. It gives 11, 41, 91 for $n = 1, 2, 3$.",
    "What is the smallest $n$ that refutes the claim?",
    num(counter, 0, [("value", 10 * counter ** 2 + 1, 0), ("root", math.isqrt(10 * counter ** 2 + 1), 0),
                     ("early", counter - 1, 0)], placeholder="a whole number", label="Smallest n"),
    fb("At $n = 6$ the value is $10 \\times 36 + 1 = 361 = 19^2$, a perfect square. Every $n$ from 1 to 5 gives a non-square.",
       "Work out $10n^2 + 1$ for $n = 4, 5, 6, \\dots$ and ask whether each value is a square.",
       {"value": "361 is the value at the counterexample. The question asks for $n$, which is 6.",
        "root": "19 is the square root of the value. The question asks for $n$, which is 6.",
        "early": "At $n = 5$ the value is 251, which lies between $15^2 = 225$ and $16^2 = 256$. Try one more."}),
    "The values for $n = 1$ to 5 are 11, 41, 91, 161 and 251, and none is a square. "
    "At $n = 6$ the value is $360 + 1 = 361 = 19^2$. One failure refutes the \"for every\"."))

# C2 L3 (l13): where an induction can start
n0 = next(m for m in range(0, 100) if all(2 ** n >= 7 * n for n in range(m, 400)))
items.append(item(
    "e-base-case-seven", 4, ["pv-induction"], ["base-case"], 150, "Where the chain can start",
    "We want to prove $2^n \\ge 7n$ for every whole number $n \\ge n_0$, by induction. "
    "The step is: if $2^k \\ge 7k$ then $2^{k+1} \\ge 14k \\ge 7k + 7$, which needs $k \\ge 1$.",
    "What is the smallest whole number $n_0$ for which the claim holds for every $n \\ge n_0$?",
    num(n0, 0, [("zero", 0, 0), ("five", 5, 0)], placeholder="a whole number", label="Smallest n_0"),
    fb("$2^6 = 64 \\ge 42$, and the step works for every $k \\ge 1$. At $n = 5$, $32 < 35$.",
       "Find the first $n$ from which the inequality holds, then check the step covers every case after it.",
       {"zero": "$2^0 = 1 \\ge 0$ is true, but $n = 1$ gives $2 < 7$. The chain breaks at once.",
        "five": "At $n = 5$, $2^5 = 32$ and $7 \\times 5 = 35$, so the base case fails."}),
    "The inequality fails for $n$ from 1 to 5: at 5, $32 < 35$. At 6, $64 \\ge 42$, and the step holds for $k \\ge 1$. "
    "So $n_0 = 6$; the true case at $n = 0$ does not start a chain."))

# C3 L3 (l12): log base 2 of 3 is irrational
items.append(item(
    "e-log-contradiction", 4, ["pv-indirect"], ["contradiction"], 150, "A logarithm that is not a fraction",
    "Claim: $\\log_2 3$ is irrational. Suppose $\\log_2 3 = \\tfrac{p}{q}$ with $p$ and $q$ positive integers. Then $2^{p/q} = 3$, so $2^p = 3^q$.",
    "Which fact finishes the proof by contradiction?",
    choice([
        opt("parity", "$2^p$ is even, since $p \\ge 1$, but $3^q$ is odd, so they cannot be equal.", correct=True),
        opt("lowest", "$p$ and $q$ then share a factor, against lowest terms.",
            "You copied the $\\sqrt{2}$ template. Nothing here makes $p$ and $q$ share a factor; parity does the work."),
        opt("bigger", "$2^p > 3^q$ for all positive $p$ and $q$.",
            "You compared sizes, as if one side must be bigger. $2^1 < 3^1$ but $2^2 > 3^1$, so size settles nothing."),
        opt("q-zero", "$q$ cannot be 0, so the fraction is undefined.",
            "You named a side condition. $q \\ge 1$ was assumed; it is not the contradiction.")]),
    fb("An even number cannot equal an odd one, so no such $p$ and $q$ exist.",
       "Compare $2^p$ and $3^q$: what is true of every power of 2 that is false of every power of 3?"),
    "Every positive power of 2 is even and every power of 3 is odd. So $2^p = 3^q$ is impossible. "
    "The assumption that $\\log_2 3$ is a fraction must be false."))

# C4 L3 (l15): writing forwards what was found backwards
items.append(item(
    "e-forwards-proof", 4, ["pv-writing", "pv-direct"], ["forwards"], 180, "Write it forwards",
    "Claim: for every real $x > 0$, $x + \\tfrac{1}{x} \\ge 2$. We found the proof by working back from the claim. Now write it forwards.",
    "Put the proof in order. Two lines do not belong: move them to Left out.",
    order([
        ("s1", "Let $x > 0$."),
        ("s2", "$(x - 1)^2 \\ge 0$, since no square is negative."),
        ("s3", "Expanding, $x^2 - 2x + 1 \\ge 0$, so $x^2 + 1 \\ge 2x$."),
        ("s4", "Dividing by $x$, which is positive so the sign is kept, $x + \\tfrac{1}{x} \\ge 2$. $\\blacksquare$"),
        ("d1", "Assume $x + \\tfrac{1}{x} \\ge 2$. Multiplying by $x$ gives $(x - 1)^2 \\ge 0$, which is true.",
         "You kept the backward chain. Starting from the claim and reaching a truth proves nothing."),
        ("d2", "Check $x = 2$: $2 + \\tfrac{1}{2} = 2.5 \\ge 2$.",
         "You kept a check of one value. It is evidence, not a step.")],
        ["s1", "s2", "s3", "s4"], ["d1", "d2"]),
    fb("Start from a fact the reader accepts, a square is never negative, and end at the claim.",
       "A proof runs from accepted facts to the claim, each step with its reason.",
       {"d1": "You kept the line that assumes the claim. Write the chain from the square to the claim instead.",
        "d2": "You kept the check at $x = 2$. It covers one value only.",
        "left-out": "You left out a line the proof needs."}),
    "Working back from the claim is how we found the proof, but it assumes what we want. "
    "The forward version starts from $(x - 1)^2 \\ge 0$. Dividing by $x > 0$ keeps the direction of $\\ge$."))

# C5 L3 (l13): a sum of products by induction
s20 = 20 * 21 * 22 // 3
items.append(parts(
    "e-product-sum", 4, ["pv-induction"], ["induction-sum"], 210, "Products of neighbours",
    "Claim: $1 \\cdot 2 + 2 \\cdot 3 + \\dots + n(n + 1) = \\tfrac{n(n + 1)(n + 2)}{3}$ for every $n \\ge 1$. It holds at $n = 1$: $2 = \\tfrac{1 \\cdot 2 \\cdot 3}{3}$.",
    "Use the formula, then check its step.",
    [("What is $1 \\cdot 2 + 2 \\cdot 3 + \\dots + 20 \\cdot 21$?",
      num(s20, 0, [("no-third", 20 * 21 * 22, 0), ("squares", 20 * 21 * 41 // 6, 0)], placeholder="a whole number",
          label="Sum"),
      fb("$\\tfrac{20 \\times 21 \\times 22}{3} = 3{,}080$.",
         "Put $n = 20$ into $\\tfrac{n(n + 1)(n + 2)}{3}$.",
         {"no-third": "You forgot to divide by 3. $20 \\times 21 \\times 22 = 9{,}240$.",
          "squares": "That is $1^2 + \\dots + 20^2 = 2{,}870$. Each term here is $i(i + 1)$, one more factor than $i^2$."})),
     ("Step: assume the sum to $k$ terms is $\\tfrac{k(k + 1)(k + 2)}{3}$. Which line comes next?",
      choice([
          opt("right", "Add $(k + 1)(k + 2)$: $\\tfrac{k(k + 1)(k + 2)}{3} + (k + 1)(k + 2) = \\tfrac{(k + 1)(k + 2)(k + 3)}{3}$.",
              correct=True),
          opt("old-term", "Add $k(k + 1)$: $\\tfrac{k(k + 1)(k + 2)}{3} + k(k + 1) = \\tfrac{k(k + 1)(k + 5)}{3}$.",
              "You added the $k$th term again. The next term is the $(k + 1)$th, $(k + 1)(k + 2)$."),
          opt("all-n", "Assume the formula for every $n$, so it holds at $n = k + 1$.",
              "You assumed the claim itself. The step may use only case $k$."),
          opt("check", "Check $k = 20$: both sides are 3,080, so the step holds.",
              "You checked one case. The step must work for every $k$.")]),
      fb("Taking out $(k + 1)(k + 2)$ leaves $\\tfrac{k}{3} + 1 = \\tfrac{k + 3}{3}$, the formula at $k + 1$.",
         "Add the next term, $(k + 1)(k + 2)$, and take out the common factor."))],
    "The $(k + 1)$th term is $(k + 1)(k + 2)$. Taking it out as a factor leaves $\\tfrac{k}{3} + 1 = \\tfrac{k + 3}{3}$. "
    "That is the formula with $n = k + 1$, so with the base case it holds for every $n$."))

# ---------------------------------------------------------------- difficulty 5
# E1 L3 (l12, l15): 4m + 3 is not a sum of two squares
items.append(item(
    "e-two-squares", 5, ["pv-indirect", "pv-writing"], ["contradiction", "cases"], 300, "Not a sum of two squares",
    "Claim: no integer of the form $4m + 3$ is a sum of two squares $a^2 + b^2$, for integers $a$ and $b$.",
    "Put the proof in order. Two lines do not belong: move them to Left out.",
    order([
        ("s1", "Suppose $4m + 3 = a^2 + b^2$ for some integers $m$, $a$ and $b$."),
        ("s2", "If $a = 2j$, then $a^2 = 4j^2$, which leaves remainder 0 on division by 4."),
        ("s3", "If $a = 2j + 1$, then $a^2 = 4(j^2 + j) + 1$, which leaves remainder 1."),
        ("s4", "The same holds for $b^2$, so $a^2 + b^2$ leaves remainder 0, 1 or 2."),
        ("s5", "But $4m + 3$ leaves remainder 3: a contradiction. So no such $a$ and $b$ exist. $\\blacksquare$"),
        ("d1", "The same holds for $b^2$, so $a^2 + b^2$ leaves remainder 0 or 1.",
         "You dropped the case where both squares leave 1. Then the sum leaves 2."),
        ("d2", "Check 3, 7, 11 and 15: none is a sum of two squares.",
         "You kept a list of cases. Four checks cannot cover every $m$.")],
        ["s1", "s2", "s3", "s4", "s5"], ["d1", "d2"], [["s2", "s3"]]),
    fb("Each square leaves 0 or 1 on division by 4. A sum of two leaves 0, 1 or 2, never 3.",
       "Work out what a square leaves on division by 4, for even and odd bases.",
       {"d1": "You kept the line that forgets $1 + 1 = 2$. The sum can leave 0, 1 or 2.",
        "d2": "You kept the checks of four numbers. The claim covers every $m$.",
        "left-out": "You left out a line the proof needs."}),
    "Split each base into even and odd: squares leave 0 or 1 on division by 4. Two of them sum to 0, 1 or 2. "
    "None of those is 3, so the assumed equation is impossible."))

# E2 L3 (l13, l15): a written induction, self-marked
items.append({
    "id": "e-weighted-sum", "difficulty": 5, "skills": ["pv-induction", "pv-writing"], "tags": ["written-proof"], "pace": 600,
    "title": "A written induction",
    "kind": "longform",
    "prompt": "Prove that for every whole number $n \\ge 1$,\n\n"
              "$$1 \\cdot 2^1 + 2 \\cdot 2^2 + 3 \\cdot 2^3 + \\dots + n \\cdot 2^n = (n - 1)2^{n + 1} + 2.$$\n\n"
              "Write it so a stranger can check every step. State the method, the base case and what the step assumes. "
              "Then check the formula at $n = 4$ by adding the terms.",
    "model": "We use induction on $n$.\n\n"
             "**Base case.** At $n = 1$ the left side is $1 \\cdot 2 = 2$. The right side is $0 \\cdot 2^2 + 2 = 2$.\n\n"
             "**Step.** Assume, for one fixed $k \\ge 1$, that $1 \\cdot 2^1 + \\dots + k \\cdot 2^k = (k - 1)2^{k + 1} + 2$. "
             "Adding the next term, $(k + 1)2^{k + 1}$, the sum to $k + 1$ terms is\n\n"
             "$$(k - 1)2^{k + 1} + 2 + (k + 1)2^{k + 1} = 2k \\cdot 2^{k + 1} + 2 = k \\cdot 2^{k + 2} + 2.$$\n\n"
             "That is $((k + 1) - 1)2^{(k + 1) + 1} + 2$, the formula with $n = k + 1$.\n\n"
             "**Conclusion.** The base case holds and each case gives the next. So the formula holds for every $n \\ge 1$. $\\blacksquare$\n\n"
             "**Check at $n = 4$.** $2 + 8 + 24 + 64 = 98$, and $3 \\times 2^5 + 2 = 98$.",
    "rubric": [
        {"points": 1, "text": "Names induction on $n$ as the method"},
        {"points": 1, "text": "Base case: both sides equal 2 at $n = 1$"},
        {"points": 2, "text": "States the assumption for one fixed $k$, not for every $n$"},
        {"points": 2, "text": "Adds the next term $(k + 1)2^{k + 1}$ and collects to $2k \\cdot 2^{k + 1} + 2$"},
        {"points": 2, "text": "Rewrites it as $k \\cdot 2^{k + 2} + 2$ and says this is the formula at $k + 1$"},
        {"points": 1, "text": "Concludes for every $n \\ge 1$ from the base case and the step"},
        {"points": 1, "text": "Checks $n = 4$: the terms sum to 98, and $3 \\times 32 + 2 = 98$"}]})

order_d = {2: [], 3: [], 4: [], 5: []}
for it in items:
    order_d[it["difficulty"]].append(it)
exam = {
    "id": "topic-0.6", "topic": "0.6", "name": "Reasoning and proof", "minutes": 60, "pass": 0.7,
    "skills": {"pv-logic": "Statements and logic", "pv-sets": "Sets and functions", "pv-direct": "Direct proof",
               "pv-indirect": "Contrapositive and contradiction", "pv-induction": "Induction",
               "pv-writing": "Writing a proof"},
    "items": order_d[2] + order_d[3] + order_d[4] + order_d[5],
}
with open(OUT, "w", encoding="utf8") as f:
    json.dump(exam, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", os.path.normpath(OUT), len(exam["items"]), "items, pace", sum(i["pace"] for i in exam["items"]), "s")
