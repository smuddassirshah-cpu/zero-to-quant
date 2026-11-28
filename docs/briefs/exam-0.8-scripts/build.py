"""Build app/content/exams/topic-0.8.json (topic 0.8, AI from nothing: ai-basics levels 1 to 4 and ai-use levels 1 to 3).

Route A for every key: plain floats and loops below. check_numbers.py recomputes each value by a second route (exact
Fractions, brute-force enumeration, Counter tables, Decimal money) and asserts it at its path in the written file.
Run from anywhere: python3 docs/briefs/exam-0.8-scripts/build.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-0.8.json')


def r(x, n=6):
    return round(x, n)


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


def item(id, d, skills, tags, pace, title, prose, question, widget, feedback, explain):
    it = {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title}
    if prose:
        it["prose"] = prose
    it.update({"question": question, "widget": widget, "feedback": feedback, "explain": {"text": explain}})
    return it


def parts(id, d, skills, tags, pace, title, prose, question, ps, explain):
    return {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title,
            "prose": prose, "question": question,
            "parts": [{"question": q, "widget": w, "feedback": f} for q, w, f in ps],
            "explain": {"text": explain}}


def mse(w, b, xs, ys):
    return sum((w * x + b - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


items = []

# ================================================================ difficulty 2
# M1 (ai-basics l2): a column known only after the event
items.append(item(
    "e-auction-leak", 2, ["ab-models"], ["leak"], 60, "The closing auction",
    "At 3 pm a desk wants a model that says whether today's closing auction will trade over 2 million shares. "
    "Its table of past days holds that label and four other columns.",
    "Which column must the model not use as a feature?",
    choice([
        opt("close", "Today's closing price", correct=True),
        opt("by3", "Shares traded by 3 pm",
            "You dropped the strongest clue. It is known at 3 pm, so it is a fair feature."),
        opt("yday", "Yesterday's auction size",
            "You left out a fact from yesterday. It is known by 3 pm, so the model may use it."),
        opt("day", "The day of the week",
            "You removed the day. It is known in advance, so it may be a feature even if it helps little.")]),
    fb("The closing price is set by the auction itself, so it is not known at 3 pm.",
       "Ask of each column: is it known at 3 pm, when the model is asked?"),
    "A feature must be known when the model is asked. Today's closing price comes out of the auction the model is meant to predict. "
    "A model trained with it would look good on past days and fail at 3 pm."))

# N1 (l6): MSE of a line on three points
xs1, ys1 = [1, 2, 4], [4, 4, 12]
e1 = [3 * x - 1 - y for x, y in zip(xs1, ys1)]
mse1 = sum(e * e for e in e1) / 3
items.append(item(
    "e-mse-three-points", 2, ["ab-nudge"], ["mse"], 75, "Three points, one line",
    "The line $y = 3x - 1$ is tested on three points: (1, 4), (2, 4) and (4, 12).",
    "What is its mean squared error?",
    num(r(mse1), 0, [("sum", r(mse1 * 3), 0), ("raw", r(sum(e1) / 3, 4), 0.001), ("n-minus-1", r(mse1 * 3 / 2), 0)],
        label="MSE"),
    fb("The errors $-2$, 1 and $-1$ square to 4, 1 and 1. The mean is $6 / 3 = 2$.",
       "Find each prediction, take prediction minus actual, square, then average.",
       {"sum": "You stopped at the sum of the squares, 6. Divide by the 3 points.",
        "raw": "You averaged the raw errors, $-2/3$. Square each error before you take the mean.",
        "n-minus-1": "You divided 6 by 2, giving 3. The mean divides by all 3 points."}),
    "The predictions are 2, 5 and 11, so the errors are $-2$, 1 and $-1$. Squared, they add to 6. "
    "Over 3 points the MSE is 2."))

# U1 (l9): a weighted sum with four inputs
w4, b4, x4 = [1.5, -0.5, 2, -1], -1.5, [1, 0, 1, 1]
s4 = sum(a * b for a, b in zip(w4, x4)) + b4
items.append(item(
    "e-four-input-sum", 2, ["ab-neuron"], ["weighted-sum"], 60, "Four inputs",
    "Four inputs feed one neuron. Their weights are 1.5, $-0.5$, 2 and $-1$, in order, and the bias is $-1.5$. The inputs arrive as (1, 0, 1, 1).",
    "Before the threshold, what does the neuron add up to?",
    num(s4, 0, [("no-bias", s4 - b4, 0), ("zero-input", s4 - 0.5, 0)], label="Sum"),
    fb("$1.5 + 2 - 1 - 1.5 = 1$.",
       "Multiply each input by its weight, add them, then add the bias.",
       {"no-bias": "You left out the bias. $1.5 + 2 - 1 = 2.5$, and the bias $-1.5$ brings it to 1.",
        "zero-input": "You added the weight $-0.5$ of an input that is 0, giving 0.5. An input of 0 adds nothing."}),
    "The input that is 0 adds nothing. $1.5 + 2 - 1 = 2.5$, and the bias brings it to 1."))

# L1 (l15): pick by running totals
items.append(item(
    "e-pick-buy", 2, ["ab-language"], ["sampling"], 60, "A draw of 0.52",
    "A next-move row has chances hold 0.45, buy 0.3 and sell 0.25, in that order. A draw gives $u = 0.52$.",
    "Which move does the picker write, using the rule of the lessons?",
    choice([
        opt("buy", "buy", correct=True),
        opt("hold", "hold", "You took the move with the biggest chance. The draw picks by running totals, and 0.52 is past hold's 0.45."),
        opt("sell", "sell", "You walked past buy because 0.52 is above its chance, 0.3. Compare $u$ with the running total, 0.75, not the chance.")]),
    fb("The running totals are 0.45, 0.75 and 1, and 0.75 is the first above 0.52.",
       "Add the chances in order and find the first running total above $u$."),
    "The running totals are 0.45, 0.75 and 1. The first above 0.52 is 0.75, which belongs to buy. "
    "Over many draws buy comes up 30% of the time, as its chance says."))

# K1 (ai-use l1): a base model continues a pattern
items.append(item(
    "e-base-qa", 2, ["au-making"], ["base-model"], 60, "A list of questions",
    "A base model, pretrained and never fine-tuned, is given this text: "
    "\"Q: What is a bond? A: A loan to a firm or a government. Q: What is a share?\"",
    "What does it most likely write next?",
    choice([
        opt("pattern", "\"A:\" and a likely answer, perhaps then another question", correct=True),
        opt("friendly", "A friendly reply that opens \"Great question\"",
            "You expected an assistant. A base model never saw example chats, so it does not reply in that style."),
        opt("nothing", "Nothing, since no request was made",
            "You looked for a request. A base model goes on from any text it is given."),
        opt("check", "A check that the first answer is true",
            "You credited it with checking. Pretraining teaches it to continue text, not to judge it.")]),
    fb("The text so far is questions, each followed by \"A:\" and an answer, so that is the likely next text.",
       "Ask what usually comes next in text shaped like this."),
    "Pretraining teaches a base model to continue text. Here each question is followed by \"A:\" and an answer. "
    "So it likely writes an answer, from the pattern, not because it was asked."))

# H1 (ai-use l4): an invented paper
items.append(item(
    "e-invented-paper", 2, ["au-limits"], ["hallucination"], 60, "A paper that does not exist",
    "A chatbot with no search tool is asked for a paper on market crashes. It gives a title, two authors and a journal, "
    "in a sure tone. No such paper exists.",
    "What is this called, and why does it happen?",
    choice([
        opt("halluc", "A hallucination: it wrote likely text, and nothing checked it", correct=True),
        opt("lie", "A lie: the chatbot chose to mislead you",
            "You gave it a motive. It predicts likely tokens and has no aim to deceive."),
        opt("bug", "A bug: a well-built chatbot never does this",
            "You blamed a fault. Fluent invention follows from predicting likely text, even in a well-built model."),
        opt("search", "A search slip: it found the wrong paper online",
            "You assumed it searched. It has no search tool, so it wrote the title token by token.")]),
    fb("Titles and authors have a familiar shape, and the model writes text of that shape.",
       "Think about what the model does at each step: it writes a likely next token."),
    "Titles, authors and journals have a familiar shape. The model writes tokens that fit that shape, and nothing in that step checks the paper is real. "
    "Fluent, sure text is what it was trained to produce."))

# ================================================================ difficulty 3
# M2 (l3, l4): accuracy of a model that always says no
n_pay, n_fraud = 2000, 60
acc_lazy = (n_pay - n_fraud) / n_pay
items.append(item(
    "e-always-no", 3, ["ab-models"], ["accuracy"], 75, "A lazy fraud model",
    "A card firm keeps back 2,000 test payments, and 60 of them are fraud. A lazy model says \"not fraud\" for every payment.",
    "What is its accuracy on the test payments? Give a percentage.",
    num(acc_lazy, 0.0005, [("flipped", n_fraud / n_pay, 0.0005), ("half", 0.5, 0.0005)], unit="%", label="Accuracy",
        accept="1,940 / 2,000 = 97%"),
    fb("It is right on all 1,940 genuine payments: $1940 / 2000 = 97\\%$. Yet it catches no fraud.",
       "Accuracy is the number right over the number of payments.",
       {"flipped": "You gave the share of fraud, 3%. Accuracy counts every right answer, and it is right on the 1,940 genuine payments.",
        "half": "You assumed two labels give 50%. Count the payments it gets right: every genuine one, 1,940."}),
    "Accuracy is right answers over all answers: $1940 / 2000 = 97\\%$. The model learned nothing, yet scores well because fraud is rare. "
    "So compare a score with what this lazy rule gets."))

# N2 (l7): one round of nudging, by hand
xs2, ys2 = [0, 1, 2], [1, 3, 4]
m_start = mse(1, 1, xs2, ys2)
m_wu, m_wd = mse(1.5, 1, xs2, ys2), mse(0.5, 1, xs2, ys2)
m_bu, m_bd = mse(1.5, 1.5, xs2, ys2), mse(1.5, 0.5, xs2, ys2)
assert m_wu < m_start and m_wu < m_wd and m_bu > m_wu and m_bd > m_wu
items.append(parts(
    "e-round-by-hand", 3, ["ab-nudge"], ["nudge-round"], 240, "One round with step 0.5",
    "Points (0, 1), (1, 3) and (2, 4). The line starts at $w = 1$, $b = 1$, and one round of the nudge rule uses step 0.5.",
    "Work through the round.",
    [("What is the MSE at the start? Give a decimal to 4 places.",
      num(r(m_start, 4), 0.0005, [("sum", r(m_start * 3), 0.0005)], label="MSE", accept="2/3, about 0.6667"),
      fb("The errors are 0, $-1$ and $-1$, so the MSE is $2/3 \\approx 0.6667$.",
         "Predict with $y = x + 1$, take the errors, square and average.",
         {"sum": "You stopped at the sum of the squares, 2. Divide by the 3 points."})),
     ("$w = 1.5$ and $w = 0.5$ are tried with $b = 1$. What is $w$ after the $w$ nudge?",
      num(1.5, 0, [("stay", 1, 0), ("down", 0.5, 0)], label="w"),
      fb(f"$w = 1.5$ gives MSE {r(m_wu, 4)}, lower than {r(m_start, 4)}, and $w = 0.5$ gives {r(m_wd, 4)}.",
         "Work out the MSE at each trial and keep the lower one if it beats the start.",
         {"stay": f"You kept $w = 1$. At $w = 1.5$ the errors are 0, $-0.5$ and 0, an MSE of {r(m_wu, 4)}, which is lower.",
          "down": f"You went the wrong way. $w = 0.5$ gives MSE {r(m_wd, 4)}, higher than the start."})),
     ("From that $w$, $b = 1.5$ and $b = 0.5$ are tried. What is $b$ after the round?",
      num(1, 0, [("better-trial", 1.5, 0), ("down", 0.5, 0)], label="b"),
      fb(f"Both trials raise the MSE above {r(m_wu, 4)}, so $b$ stays at 1.",
         "Compare each trial with the MSE after the $w$ nudge, not with each other.",
         {"better-trial": f"You kept the better of the two trials. $b = 1.5$ gives {r(m_bu, 4)}, which is above the {r(m_wu, 4)} you already have.",
          "down": f"You moved $b$ down. $b = 0.5$ gives {r(m_bd, 4)}, higher than {r(m_wu, 4)}."}))],
    f"At $w = 1.5$ the MSE drops to {r(m_wu, 4)}, so $w$ moves. Both $b$ trials then score higher, {r(m_bu, 4)} and {r(m_bd, 4)}, so $b$ stays at 1. "
    "A trial is kept only when it lowers the error, not when it is the better of two."))

# N3 (l5, l6): two forecasts with the same MSE
eA, eB = [1, 1, 1, 1, 4], [2, 2, 2, 2, 2]
items.append(item(
    "e-mse-tie", 3, ["ab-nudge"], ["mse"], 75, "Steady or spiky",
    "Two forecasts of a share's daily volume, in thousands, over five days. Forecast A misses by 1, 1, 1, 1 and 4. "
    "Forecast B misses by 2 every day.",
    "Which forecast has the lower mean squared error?",
    choice([
        opt("tie", "Neither: both have MSE 4", correct=True),
        opt("sum", "A, since its misses add to 8 against B's 10",
            "You added the misses without squaring. Squared, A's 4 counts 16, and both totals are 20."),
        opt("most", "A, since four of its five misses are only 1",
            "You counted the small misses. Squaring makes the one miss of 4 count 16, so A's total is 20, the same as B's."),
        opt("worst", "B, since its worst miss is only 2",
            "You judged by the worst miss alone. The MSE averages every squared miss, and both average 4.")]),
    fb("A's squares add to $1 + 1 + 1 + 1 + 16 = 20$ and B's to $5 \\times 4 = 20$, so both MSEs are 4.",
       "Square each miss, add, and divide by the 5 days."),
    "A's squares are 1, 1, 1, 1 and 16, which add to 20. B's are five 4s, also 20. "
    "Over five days both MSEs are 4: squaring makes A's one big miss cost as much as B's steady ones."))

# U2 (l9, l10): a risk alarm by hand
wA, bA = [1.5, -2, 1], -1


def sum3(x):
    return sum(a * b for a, b in zip(wA, x)) + bA


pats = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
fire_n = sum(1 for p in pats if sum3(p) > 0)
items.append(parts(
    "e-alarm-neuron", 3, ["ab-neuron"], ["neuron-output"], 210, "A risk alarm",
    "A desk's risk alarm is one neuron. Its inputs are a loss today, a hedge in place and a large position, each 1 for yes. "
    "The weights are 1.5, $-2$ and 1, in that order, and the bias is $-1$. It fires when its sum is greater than 0.",
    "Work out the alarm by hand.",
    [("What is the weighted sum for a large position with no loss and no hedge, (0, 0, 1)?",
      num(sum3((0, 0, 1)), 0, [("no-bias", 1, 0), ("bias-only", -1, 0)], label="Sum"),
      fb("$1 - 1 = 0$.", "Add the weights of the inputs that are 1, then the bias.",
         {"no-bias": "You left out the bias. The large position adds 1 and the bias $-1$ takes it to 0.",
          "bias-only": "You used the bias alone. The large position is 1, so its weight 1 is added: $1 - 1 = 0$."})),
     ("What does the alarm output for (0, 0, 1)?",
      num(0, 0, [("zero-fires", 1, 0)], label="Output"),
      fb("A sum of exactly 0 is not greater than 0, so the output is 0.", "Apply the threshold: fire only when the sum is greater than 0.",
         {"zero-fires": "You let a sum of 0 fire. The neuron fires only when its sum is greater than 0."})),
     ("For how many of the eight input patterns does the alarm fire?",
      num(fire_n, 0, [("with-zero", fire_n + 1, 0), ("half", 4, 0)], label="Patterns"),
      fb("Only (1, 0, 0) and (1, 0, 1) fire, with sums 0.5 and 1.5.", "Work out all eight sums and count those above 0.",
         {"with-zero": "You counted (0, 0, 1), whose sum is exactly 0. It does not fire.",
          "half": "You guessed half of the eight. Only a loss with no hedge lifts the sum above 0, which is 2 patterns."}))],
    "With a large position alone the sum is $1 - 1 = 0$, which does not fire. Only a loss with no hedge lifts the sum above 0: 0.5 alone, 1.5 with a large position. "
    "Any pattern with the hedge is pulled down by its weight of $-2$."))

# U3 (l11): a neuron for "neither"
items.append(item(
    "e-neither-neuron", 3, ["ab-neuron"], ["and-or"], 90, "Neither input",
    "A neuron with two inputs should fire only on (0, 0): \"neither\". Each option gives $(w_1, w_2, b)$, and the neuron fires when its sum is greater than 0.",
    "Which one computes \"neither\"?",
    choice([
        opt("nor", "$(-2, -2, 1)$", correct=True),
        opt("nand", "$(-2, -2, 3)$", "You built NAND. Its sums are 3, 1, 1 and $-1$, so three corners fire."),
        opt("or", "$(2, 2, -1)$", "You built OR. It fires on the three corners \"neither\" must not."),
        opt("never", "$(-2, -2, -1)$", "You made every sum negative: $-1$, $-3$, $-3$ and $-5$. Nothing fires, not even (0, 0).")]),
    fb("The sums are 1, $-1$, $-1$ and $-3$, so only (0, 0) fires.",
       "Work out the sum at all four corners for each option."),
    "At (0, 0) the sum is the bias alone, so the bias must be above 0. Each input of 1 must pull the sum to 0 or below, so each weight is negative and at least as large as the bias. "
    "$(-2, -2, 1)$ gives 1, $-1$, $-1$ and $-3$."))

# L2 (l13, l14): a row whose last word starts no pair
log = "sell sell buy hold sell buy buy sell".split()
pairs_log = list(zip(log, log[1:]))
row_sell = [b for a, b in pairs_log if a == "sell"]
p_buy = row_sell.count("buy") / len(row_sell)
items.append(item(
    "e-sell-row", 3, ["ab-language"], ["next-word"], 90, "After sell",
    "A trader's message log reads `sell sell buy hold sell buy buy sell`.",
    "What is the chance that \"buy\" comes straight after \"sell\"? Give a fraction.",
    num(r(p_buy, 4), 0.0005, [("all-sells", 0.5, 0.0005), ("all-pairs", r(2 / 7, 4), 0.0005), ("words", 0.25, 0.0005)],
        placeholder="fraction or decimal", label="Chance", accept="2/3, or 0.6667"),
    fb("Three pairs start with \"sell\": one goes on to \"sell\" and two to \"buy\". So the chance is $2/3$.",
       "Divide the count of \"sell buy\" by the number of pairs that start with \"sell\".",
       {"all-sells": "You divided by the 4 times \"sell\" appears. The last one ends the log and starts no pair, so the row total is 3.",
        "all-pairs": "You divided by all 7 pairs. Divide by the row total, the 3 pairs that start with \"sell\".",
        "words": "You divided by the 8 words. The chance of the next word divides by the row total, 3."}),
    "The log has 7 pairs, and 3 of them start with \"sell\". Two of those go on to \"buy\", so the chance is $2/3$. "
    "The final \"sell\" has no word after it, so it adds nothing to the row."))

# L3 (l16): temperature 1/2 on a row of three
ch3 = [0.5, 0.3, 0.2]
sq = [c * c for c in ch3]
cold = sq[0] / sum(sq)
rt = [math.sqrt(c) for c in ch3]
hot = rt[0] / sum(rt)
items.append(item(
    "e-cold-three", 3, ["ab-language"], ["temperature"], 90, "A colder row",
    "A row has chances 0.5, 0.3 and 0.2 for rise, flat and fall.",
    "What is rise's chance at temperature $\\tfrac12$? Give a decimal to 3 places.",
    num(r(cold, 3), 0.0005, [("no-rescale", 0.25, 0.0005), ("roots", r(hot, 3), 0.0005), ("same", 0.5, 0.0005)],
        label="Chance", accept="0.25 / 0.38, about 0.658"),
    fb(f"The squares are 0.25, 0.09 and 0.04, which add to 0.38, so rise gets $0.25 / 0.38 \\approx {r(cold, 3)}$.",
       "Square each chance, then divide each square by their total.",
       {"no-rescale": "You squared but did not rescale. The squares add to 0.38, so divide 0.25 by 0.38.",
        "roots": f"You took square roots, which is temperature 2 and gives {r(hot, 3)}. Temperature $\\tfrac12$ squares.",
        "same": "You left the chance alone, which is temperature 1. Temperature $\\tfrac12$ squares each chance and rescales."}),
    f"Temperature $\\tfrac12$ squares each chance: 0.25, 0.09 and 0.04, which add to 0.38. Dividing by 0.38 makes them add to 1 again. "
    f"Rise goes from 0.5 to {r(cold, 3)}, so the top word gains."))

# K2 (ai-use l1): training examples from two documents
docs_n = [12, 30]
n_ex = sum(n - 1 for n in docs_n)
items.append(item(
    "e-examples-two-docs", 3, ["au-making"], ["pretraining"], 75, "Labels from the text",
    "Pretraining reads two separate documents, of 12 and 30 tokens. At each place, the tokens so far are the input and the next token is the label.",
    "How many (input, label) training examples do the two documents give?",
    num(n_ex, 0, [("every-token", sum(docs_n), 0), ("joined", sum(docs_n) - 1, 0)], label="Examples"),
    fb("Each document gives one fewer example than it has tokens: $11 + 29 = 40$.",
       "Count the tokens that have a token before them in the same document.",
       {"every-token": "You gave every token an example. The first token of a document has nothing before it to be its input.",
        "joined": "You joined the two into one text of 42 tokens. They are separate, so each loses one: $11 + 29$."}),
    "In each document every token but the first is a label once. That gives 11 and 29 examples, 40 in all. "
    "The labels come from the text itself, so no person marks anything."))

# K3 (ai-use l3, l4): raters who reward the look of a source
items.append(item(
    "e-raters-citations", 3, ["au-making", "au-limits"], ["human-feedback"], 90, "Rewarded for citing",
    "A raters' guide says: \"Prefer the reply that cites a source.\" The raters have no time to check the sources. "
    "The assistant is trained on a great many of their rankings.",
    "What does it most likely learn?",
    choice([
        opt("cite", "To add sources to its replies, whether or not they are real", correct=True),
        opt("real", "To cite only real sources, since raters prefer cited replies",
            "You assumed the rankings rewarded real sources. Raters could not check, so a made-up source scored as well as a real one."),
        opt("tone", "Nothing, since rankings change only the tone of replies",
            "You limited feedback training to tone. It makes any kind of reply raters preferred more likely, citations included."),
        opt("stop", "To stop citing sources, since no one checks them",
            "You reversed the guide. Cited replies were preferred, so citing becomes more likely, not less.")]),
    fb("Raters rewarded the look of a source, so cited replies become more likely, invented or not.",
       "Ask what the raters could see and reward."),
    "Training from human feedback makes the preferred kind of reply more likely. Raters preferred the look of a source, not a checked one. "
    "So the model learns to cite, and a likely-looking invented citation counts as a cited reply."))

# H2 (ai-use l1, l4): what makes a fluent wrong answer more likely
items.append(item(
    "e-wrong-more-likely", 3, ["au-limits"], ["hallucination"], 90, "Where it goes wrong",
    "A chatbot with no search tool is asked several questions.",
    "Select all that apply: which make a fluent wrong answer more likely?",
    choice([
        opt("rare", "A fact about a small firm that is rarely written about", correct=True),
        opt("late", "An event after its training text was gathered", correct=True),
        opt("premise", "A question built on something false, such as why a fund closed when it never did", correct=True),
        opt("polite", "A request that is written politely",
            "You linked politeness to truth. The tone of a request does not change which facts the model saw."),
        opt("common", "A fact repeated in millions of documents",
            "You treated a widely written fact as risky. Many examples make the likely answer and the true one agree.")],
        kind="multi"),
    fb("Rare facts, later events and false premises all leave the likely answer apart from the true one.",
       "Ask when the most likely text and the true answer come apart."),
    "The model writes what is likely given the text it saw. Rare facts and later events leave little to make the true answer likely, "
    "and a false premise invites a likely-sounding reason. A fact written everywhere is the safe case."))

# A1 (ai-use l5): which part of a request is missing
items.append(item(
    "e-missing-part", 3, ["au-asking"], ["request-parts"], 60, "Action list",
    "A request reads: \"You are helping a fund's client team. Using the meeting notes pasted below, list the actions agreed. "
    "Give a table with columns for the action, the owner and the date.\"",
    "Which of the four parts of a clear request is missing?",
    choice([
        opt("example", "An example: one sample row of the table", correct=True),
        opt("task", "The task: what to do", "You missed \"list the actions agreed\", which is the task."),
        opt("context", "The context: who it is for and what to use", "You missed the client team and the pasted notes, which are the context."),
        opt("format", "The format: the shape of the answer", "You missed the table with three columns, which is the format.")]),
    fb("It has the task, the context and the format, but no sample row.",
       "Find the task, the context, the format and an example in the request, one at a time."),
    "\"List the actions agreed\" is the task, and the client team with the pasted notes is the context. The three-column table is the format. "
    "Only an example, one sample row, is missing."))

# A2 (ai-use l5, l7): a request whose answers can be checked fast
items.append(item(
    "e-quote-the-line", 3, ["au-asking", "au-checking"], ["checkable-request"], 90, "Fees in a loan agreement",
    "An analyst has pasted a 40-page loan agreement into a chatbot. She wants the fees it charges, and she must check each one before a client call.",
    "Which request gives answers she can check fastest?",
    choice([
        opt("quote", "List each fee in the agreement below. Quote the sentence and clause it comes from, or say \"not found\".", correct=True),
        opt("usual", "What fees does a loan agreement like this one usually charge its borrowers?",
            "You asked about agreements in general. The reply would be likely text, not this agreement's fees."),
        opt("paragraph", "Read the agreement below carefully and describe all of its fees in one paragraph.",
            "You asked for a summary with no way to trace each fee. She would have to search all 40 pages for each one."),
        opt("memory", "You have read many loan agreements, so list this one's fees from what you know.",
            "You asked it to recall instead of reading the pasted text. The fees should come from the agreement in front of it.")]),
    fb("A quote and a clause number let her find each fee at once, and \"not found\" lets it say it does not know.",
       "Pick the request whose answer points to where each fee is written."),
    "A quoted sentence and a clause number let her find each fee in seconds. \"Not found\" gives the model a way to say it does not know instead of guessing. "
    "Using the pasted agreement means the answer can come from the text, not from a likely guess."))

# C1 (ai-use l6): compound interest check
bal = 15000 * 1.045 ** 3
items.append(item(
    "e-compound-check", 3, ["au-checking"], ["recompute"], 90, "Three years at 4.5%",
    "A chatbot says £15,000 saved at 4.5% a year, compounded yearly, is worth £17,025 after 3 years.",
    "What is it really worth after 3 years? Give the balance to the nearest penny.",
    num(r(bal, 2), 0.005, [("simple", 17025, 0.005), ("four-years", r(15000 * 1.045 ** 4, 2), 0.005)], unit="£",
        label="Balance", accept="15000 × 1.045^3 = £17,117.49"),
    fb("$15000 \\times 1.045^3 = £17{,}117.49$. The chatbot used simple interest.",
       "Multiply by 1.045 once for each year.",
       {"simple": "You kept the chatbot's simple interest: $15000 \\times (1 + 3 \\times 0.045) = £17{,}025$. Each year's 4.5% is on a bigger balance.",
        "four-years": f"You compounded for 4 years, giving £{r(15000 * 1.045 ** 4, 2):,.2f}. The money is saved for 3."}),
    "Simple interest adds $3 \\times 4.5\\% = 13.5\\%$, which gives the chatbot's £17,025. Compounding adds each year's 4.5% to a bigger balance: "
    "$15000 \\times 1.045^3 = £17{,}117.49$. The estimate \"a little over 13.5%\" already says £17,025 is too low."))

# R1 (ai-use l9): rows that point to one person
rows = [("Rates", "30 to 39"), ("Rates", "30 to 39"), ("FX", "20 to 29"), ("FX", "30 to 39"), ("Credit", "40 to 49"),
        ("Rates", "20 to 29"), ("FX", "20 to 29")]
uniq = sum(1 for x in rows if rows.count(x) == 1)
distinct = len(set(rows))
items.append(item(
    "e-unique-rows", 3, ["au-risks"], ["re-identify"], 75, "A survey with no names",
    "Before pasting a staff survey into a chatbot, a team deletes the names. Its 7 rows still show each person's desk and age band.\n\n"
    "| Row | Desk | Age band |\n|---:|---|---|\n" + "".join(f"| {k + 1} | {a} | {b} |\n" for k, (a, b) in enumerate(rows)),
    "How many rows match only one person in the survey, and so could identify them?",
    num(uniq, 0, [("all", len(rows), 0), ("none", 0, 0), ("distinct", distinct, 0)], label="Rows"),
    fb("FX 30 to 39, Credit 40 to 49 and Rates 20 to 29 each occur once.",
       "Count the desk and age band pairs that appear in just one row.",
       {"all": "You counted every row. Rows that share their pair with another row point to two people, not one.",
        "none": "You trusted the missing names. A pair that only one row has still points to one person.",
        "distinct": "You counted the different pairs, 5. Two of them are shared by two rows each, so only 3 rows stand alone."}),
    "A combination that only one row has points to one person, even with no name. FX 30 to 39, Credit 40 to 49 and Rates 20 to 29 each occur once. "
    "The other four rows share their pair with someone, so 3 rows could identify a person."))

# G1 (ai-use l12): a summariser scored by shared words
items.append(item(
    "e-summary-reward", 3, ["au-alignment"], ["measured-meant"], 75, "Scored by shared words",
    "A note summariser is trained to raise a score that counts the words its summary shares with the original note. "
    "Its makers wanted short summaries a busy reader can trust.",
    "What is it likely to learn?",
    choice([
        opt("copy", "To copy long stretches of the note, since copied words raise the score", correct=True),
        opt("meant", "To write short, faithful summaries, since that was the aim",
            "You credited it with the makers' aim. It is trained on the score, which rewards shared words, not brevity."),
        opt("fresh", "To reword everything, since fresh wording reads better",
            "You reversed the score. New wording shares fewer words with the note, so it lowers the score."),
        opt("fine", "Nothing harmful, since the score is close to the aim",
            "You treated the gap as harmless. Training pushes on exactly what is measured, so it goes where the gap is.")]),
    fb("Copied words raise the measured score, though they defeat the short summary that was meant.",
       "Separate what was measured from what was meant."),
    "This is an alignment gap: what was measured is not what was meant. Copying raises the count of shared words, so training pushes that way. "
    "The makers wanted brevity and trust, which the score never measured."))

# ================================================================ difficulty 4
# M3 (l3, l4): choose a threshold, then test it
sx, sy = [1, 2, 2, 3, 4, 5, 5, 6], [0, 0, 1, 0, 1, 1, 0, 1]
tx, ty = [1, 3, 4, 6, 5], [0, 1, 1, 1, 0]


def right(xs, ys, t):
    return sum(1 for x, y in zip(xs, ys) if (x >= t) == (y == 1))


scores = {t: right(sx, sy, t) for t in range(8)}
t_best = max(scores, key=lambda t: (scores[t], -t))
assert list(scores.values()).count(scores[t_best]) == 1
test_best = max(right(tx, ty, t) for t in range(8))
items.append(parts(
    "e-signal-days", 4, ["ab-models"], ["threshold", "test-score"], 270, "Choosing and testing a cut-off",
    "A desk tests the rule **say up when the signal is at least $t$** on eight past days. "
    "The signals were 1, 2, 2, 3, 4, 5, 5 and 6, and the share went up (1) or not (0) on those days: 0, 0, 1, 0, 1, 1, 0, 1.",
    "Choose the cut-off, then score it honestly.",
    [("Which whole-number $t$ from 0 to 7 gets the most training days right?",
      num(t_best, 0, [("middle", 3, 0)], label="t"),
      fb(f"$t = 4$ gets {scores[4]} of 8 right, and every other $t$ gets 5 or fewer.",
         "Count the days each $t$ gets right, from 0 to 7.",
         {"middle": f"You took a middle value. $t = 3$ gets {scores[3]} right; $t = 4$ gets {scores[4]}."})),
     ("What is that threshold's accuracy on the eight training days? Give a percentage.",
      num(scores[t_best] / 8, 0.0005, [("five", 5 / 8, 0.0005)], unit="%", label="Accuracy", accept="6 / 8 = 75%"),
      fb("$6 / 8 = 75\\%$.", "Divide the days right by the 8 days.",
         {"five": "You used 5 right, the score of the other thresholds. $t = 4$ gets 6 of 8."})),
     ("Five more days were kept back: signals 1, 3, 4, 6 and 5, and the share went up on 0, 1, 1, 1, 0. Using $t = 4$ from part 1, what is its test score? Give a percentage.",
      num(right(tx, ty, 4) / 5, 0.0005, [("train", 0.75, 0.0005)], unit="%", label="Test score", accept="3 / 5 = 60%"),
      fb("It is right on the days with signals 1, 4 and 6, and wrong on 3 and 5: $3/5 = 60\\%$.",
         "Apply $t = 4$ to each kept-back day and count the days it gets right.",
         {"train": "You reported the training score. Score the five kept-back days: 3 of 5 are right."})),
     ("Which figure should the desk report for how the rule will do on new days?",
      choice([
          opt("test", "60%, the score on the kept-back days", correct=True),
          opt("train", "75%, the score on the days that chose $t$",
              "You reported the training score. Those days chose $t$, so they flatter it."),
          opt("avg", "67.5%, the average of the two scores",
              "You averaged in the training score, which is not a test."),
          opt("best", "80%, the best score any $t$ gets on the kept-back days",
              "You let the kept-back days choose $t$. Then they no longer test it.")]),
      fb("Only the kept-back days played no part in choosing $t$.", "Ask which days had no say in the choice."))],
    "On the training days $t = 4$ gets 6 of 8, and every other $t$ gets 5 or fewer. On the kept-back days it gets 3 of 5, 60%. "
    "Only the 60% comes from days that played no part in the choice."))

# U4 (l11, l12): two layers that compute "both the same"


def fire(ws, xs, b):
    return 1 if sum(w * x for w, x in zip(ws, xs)) + b > 0 else 0


def same_net(x1, x2):
    h1 = fire([2, 2], [x1, x2], -3)
    h2 = fire([-2, -2], [x1, x2], 1)
    return fire([2, 2], [h1, h2], -1)


assert [same_net(a, b) for a in (0, 1) for b in (0, 1)] == [1, 0, 0, 1]
items.append(parts(
    "e-same-network", 4, ["ab-neuron"], ["two-layers"], 240, "A network for \"both the same\"",
    "A two-layer network has three neurons, each firing when its sum is greater than 0. "
    "Neuron $h_1$ has weights 2 and 2 with bias $-3$. Neuron $h_2$ has weights $-2$ and $-2$ with bias 1. "
    "The output neuron takes $h_1$ and $h_2$ as its inputs, with weights 2 and 2 and bias $-1$.",
    "Follow the network by hand.",
    [("What is $h_2$'s sum for input (0, 0)?",
      num(1, 0, [("weights", -3, 0)], label="Sum"),
      fb("Both inputs are 0, so the sum is the bias, 1.", "Inputs of 0 add nothing; add the bias.",
         {"weights": "You added the weights $-2$ and $-2$, but both inputs are 0. Only the bias, 1, is left."})),
     ("What does the network output for input (1, 0)?",
      num(same_net(1, 0), 0, [("one", 1, 0)], label="Output"),
      fb("$h_1$ sums to $-1$ and $h_2$ to $-1$, so both give 0. The output neuron then sums to $-1$ and gives 0.",
         "Work out $h_1$ and $h_2$ first, then feed their outputs to the output neuron.",
         {"one": "You may have fed $x_1$ and $x_2$ to the output neuron. It takes $h_1$ and $h_2$, which are both 0 at (1, 0)."})),
     ("Which function does the network compute?",
      choice([
          opt("same", "\"Both the same\": it fires on (0, 0) and (1, 1)", correct=True),
          opt("xor", "XOR: it fires on (0, 1) and (1, 0)", "You read it as XOR. It fires exactly where XOR does not."),
          opt("and", "AND: it fires on (1, 1) only", "You followed $h_1$ only. $h_2$ fires on (0, 0), and the output neuron passes either on."),
          opt("or", "OR: it fires unless both inputs are 0", "You named the output neuron's own rule. Its inputs are $h_1$ and $h_2$, not $x_1$ and $x_2$.")]),
      fb("$h_1$ is AND, $h_2$ is \"neither\", and the output is OR of the two.", "Work out all four inputs, then name the pattern."))],
    "$h_1$ is AND and $h_2$ is \"neither\", and the output neuron is OR of the two. So the network fires when both inputs are 1 or both are 0. "
    "No single neuron can do this: like XOR, it needs two lines."))

# L4 (l13 to l15, ai-use l4): build a bigram table from a log and sample from it
dtext = "buy the dip . sell the rip . buy the rip .".split()
dpairs = list(zip(dtext, dtext[1:]))


def row_of(word):
    nexts = [b for a, b in dpairs if a == word]
    order = []
    for n in nexts:
        if n not in order:
            order.append(n)
    return [(n, nexts.count(n), len(nexts)) for n in order]


def pick_row(word, u):
    run = 0
    row = row_of(word)
    for n, c, tot in row:
        run += c / tot
        if u < run:
            return n
    return row[-1][0]


us_d = [0.4, 0.5, 0.2, 0.7]
wd, out_d = "sell", ["sell"]
for u in us_d:
    wd = pick_row(wd, u)
    out_d.append(wd)
gen = " ".join(out_d)
assert gen == "sell the rip . buy"
path5 = ["sell", "the", "dip", ".", "buy", "the"]
p5 = 1.0
for a, b in zip(path5, path5[1:]):
    p5 *= dict((n, c / t) for n, c, t in row_of(a))[b]
the_total = len([1 for a, b in dpairs if a == "the"])
items.append(parts(
    "e-desk-bigram", 4, ["ab-language", "au-limits"], ["bigram", "sampling"], 300, "A table from a desk log",
    "A desk log of 12 words, counting each full stop as a word: `buy the dip . sell the rip . buy the rip .`. "
    "Build its next-word table, keeping the next words of each row in the order they first appear.",
    "Build the table, sample from it, and score a sentence.",
    [("How many pairs start with \"the\"?",
      num(the_total, 0, [("dip-rip", 2, 0)], label="Pairs"),
      fb("\"the dip\", \"the rip\" and \"the rip\": 3 pairs.", "List every pair whose first word is \"the\".",
         {"dip-rip": "You counted the different next words, dip and rip. \"the rip\" happens twice, so the row total is 3."})),
     ("What is the chance of \"rip\" after \"the\"? Give a fraction.",
      num(r(2 / 3, 4), 0.0005, [("words", r(2 / 12, 4), 0.0005), ("half", 0.5, 0.0005)], placeholder="fraction or decimal",
          label="Chance", accept="2/3, or 0.6667"),
      fb("Two of the 3 pairs that start with \"the\" go on to \"rip\": $2/3$.", "Divide the count by the row total.",
         {"words": "You divided by the 12 words. Divide by the 3 pairs that start with \"the\".",
          "half": "You split the row evenly between dip and rip. \"rip\" follows \"the\" twice, so it gets $2/3$."})),
     ("Start at \"sell\" and draw $u = 0.4$, then 0.5, 0.2 and 0.7. Each pick is the first word whose running total is above $u$. Which words are written?",
      choice([
          opt("right", "sell the rip . buy", correct=True),
          opt("dip", "sell the dip . buy", "You took dip for $u = 0.5$. Dip's running total is only $\\tfrac13$, so 0.5 walks on to rip."),
          opt("sell", "sell the rip . sell",
              "You put buy before sell in the row for \".\". Sell follows \".\" first in the log, so 0.7 lands in buy's half."),
          opt("rip", "sell the rip . rip", "You wrote a pair the log never has. \".\" is followed only by sell and buy.")]),
      fb("sell → the (its only word), the → rip ($0.5 > \\tfrac13$), rip → \".\", then \".\" → buy ($0.7 > \\tfrac12$).",
         "Take each row in turn and walk its running totals.")),
     ("The log never says \"sell the dip\". Starting at \"sell\", what is the chance the next five words are \"the dip . buy the\"? Give a fraction.",
      num(r(p5, 4), 0.0005, [("not-in-text", 0, 0), ("one-step", r(1 / 3, 4), 0.0005)], placeholder="fraction or decimal",
          label="Chance", accept="1 × 1/3 × 1 × 1/2 × 1 = 1/6, or 0.1667"),
      fb("$1 \\times \\tfrac13 \\times 1 \\times \\tfrac12 \\times 1 = \\tfrac16$.", "Multiply the chance of each pair along the way.",
         {"not-in-text": "You gave it chance 0 because the log never says it. Every pair in it is in the log, so the table can write it.",
          "one-step": "You kept only the $\\tfrac13$ of \"the dip\". The step from \".\" to buy has chance $\\tfrac12$ too."}))],
    "Each row divides counts by its row total, and a run of words multiplies its pairs' chances: $1 \\times \\tfrac13 \\times 1 \\times \\tfrac12 \\times 1 = \\tfrac16$. "
    "Every pair is in the log but the whole run is not, which is how a fluent model writes what nobody said."))

# C3 (ai-use l6, l7): a pension reply with two sums and a source
pot = 250 * 36
grown = 9000 * 1.04 ** 10
items.append(parts(
    "e-pension-reply", 4, ["au-checking", "au-limits"], ["recompute", "source-check"], 300, "A pension reply",
    "A chatbot's reply about a pension has three lines. The reply and its source are invented. "
    "Line 1: \"Paying in £250 a month for 3 years adds £7,500.\" "
    "Line 2: \"A pot of £9,000 left to grow at 4% a year, compounded, for 10 years becomes £12,600.\" "
    "Line 3: \"Fees average 0.75% a year, says the 2023 Pension Costs Review, page 14.\"",
    "Check each line before you use it.",
    [("Recompute line 1. What do 3 years of £250 a month add, in pounds?",
      num(pot, 0, [("chatbot", 7500, 0), ("one-year", 3000, 0)], unit="£", label="Paid in"),
      fb("$250 \\times 36 = £9{,}000$. The chatbot's £7,500 is 30 months.", "Count the months in 3 years.",
         {"chatbot": "You kept the chatbot's figure. Three years is 36 months, and $250 \\times 36 = £9{,}000$.",
          "one-year": "You counted one year of payments. Three years is 36 payments."})),
     ("Recompute line 2. What does £9,000 become after 10 years at 4% a year, compounded? Give it to the nearest penny.",
      num(r(grown, 2), 0.005, [("simple", 12600, 0.005)], unit="£", label="Pot", accept="9000 × 1.04^10 = £13,322.20"),
      fb("$9000 \\times 1.04^{10} = £13{,}322.20$. The £12,600 is simple interest.",
         "Multiply by 1.04 once for each of the 10 years.",
         {"simple": "You kept simple interest: $9000 \\times 1.4$. Each year's 4% is on a bigger pot, which gives £13,322.20."})),
     ("You find the review and read page 14. It is about pension transfers and gives no figure for fees. What follows for line 3?",
      choice([
          opt("unsupported", "The 0.75% is unsupported: the source is real but does not say it", correct=True),
          opt("supported", "It is supported, since the review is real",
              "You checked only that the source exists. It must also say the claim at the part cited."),
          opt("fake", "The review must be fake, so the figure is false",
              "You concluded too much. The review exists; it just does not hold the figure, which may still be true or false."),
          opt("ask", "It is supported if the chatbot gives 0.75% again",
              "You asked for agreement instead of a source. A repeat is likely text again, not a check.")]),
      fb("A source checks a claim only when it is found, read at the cited part, and says the claim.",
         "Ask whether the page you read says the claim."))],
    "Line 1 is 36 payments of £250, £9,000, not £7,500. Line 2 compounds to £13,322.20, while £12,600 is simple interest. "
    "Line 3 cites a real review that does not say it, so the figure is unsupported until you find it somewhere you can read."))

# R2 (ai-use l10): the fewest shortlisted to close a gap
gE, nE, nF = 117, 180, 200
rateE = gE / nE
kmin = next(k for k in range(nF + 1) if abs(rateE - k / nF) < 0.05)
items.append(item(
    "e-fewest-shortlisted", 4, ["au-risks"], ["bias-gap"], 150, "Closing the gap",
    "A firm retrains its CV screener. It now shortlists 117 of 180 applicants from Group E. Group F has 200 applicants. "
    "Both groups meet the job's stated requirements at the same rate. The firm and the numbers are invented.",
    "The firm's rule is that the two shortlist rates must be less than 5 percentage points apart. What is the fewest Group F applicants the screener must shortlist?",
    num(kmin, 0, [("at-five", kmin - 1, 0), ("equal", 130, 0), ("same-count", 117, 0)], label="Applicants"),
    fb("Group E's rate is $117 / 180 = 65\\%$. Group F needs more than 60%, and 121 of 200 is 60.5%.",
       "Find Group E's rate, then the smallest count whose rate is less than 5 points below it.",
       {"at-five": "You allowed a gap of exactly 5 points. 120 of 200 is 60%, which is 5 points below 65%, not less.",
        "equal": "You matched the rates exactly, 65% of 200. The rule only needs the gap under 5 points.",
        "same-count": "You matched the count, 117. Group F is larger, so 117 of 200 is only 58.5%, 6.5 points below."}),
    "Group E's rate is $117 / 180 = 65\\%$. Group F must be above 60%, and 120 of 200 is exactly 60%, which is 5 points apart. "
    "So the fewest is 121, a rate of 60.5%."))

# G2 (ai-use l12): scored by days in profit
A_tot = 19 * 0.5 - 15
B_tot = 12 * 1 - 8 * 0.5
items.append(parts(
    "e-profit-days", 4, ["au-alignment"], ["measured-meant"], 210, "Scored by winning days",
    "Two trading bots are scored by how many days end in profit. Over 20 days, bot A makes £0.5k on 19 days and loses £15k on one. "
    "Bot B makes £1k on 12 days and loses £0.5k on the other 8. The bots and figures are invented.",
    "Compare the score with the money.",
    [("What is bot A's total profit over the 20 days, in £ thousands?",
      num(A_tot, 0.005, [("gains-only", 9.5, 0.005), ("sign", -A_tot, 0.005)], label="£ thousands"),
      fb("$19 \\times 0.5 - 15 = -5.5$: a loss of £5.5k.", "Add the 19 gains and take off the one loss.",
         {"gains-only": "You added the 19 gains, £9.5k, and left out the £15k loss.",
          "sign": "You dropped the sign. Gains of £9.5k less a £15k loss is $-5.5$, a loss."})),
     ("What is bot B's total profit over the 20 days, in £ thousands?",
      num(B_tot, 0.005, [("gains-only", 12, 0.005), ("one-loss", 11.5, 0.005)], label="£ thousands"),
      fb("$12 \\times 1 - 8 \\times 0.5 = 8$.", "Add the 12 gains and take off the 8 losses.",
         {"gains-only": "You added the 12 gains and left out the 8 losses of £0.5k.",
          "one-loss": "You took off one loss of £0.5k. B lost on 8 days, £4k in all."})),
     ("The firm keeps the bot with the higher score. What happens, and what does it show?",
      choice([
          opt("gap", "It keeps A: winning days were measured, money made was meant", correct=True),
          opt("b", "It keeps B, since B made more money",
              "You judged by what was meant. The score counts winning days, where A has 19 and B has 12."),
          opt("fine", "It keeps A, which is right since A wins more often",
              "You took the measure for the aim. Winning often while losing £5.5k in all is not what the firm wanted."),
          opt("tie", "Neither, since the two scores tie",
              "You compared money with days. The scores are 19 and 12, which do not tie.")]),
      fb("A scores 19 to B's 12, yet A lost £5.5k and B made £8k.", "Compare the scores, then the money."))],
    "A scores 19 and B scores 12, so the score keeps A. Yet A lost £5.5k and B made £8k. "
    "The score measured how often a bot wins, not what the firm meant: money made."))

# ================================================================ difficulty 5
# U5 (l10, l11): a bias for "at least two of three"
wts = [2, 3, 4]
pat3 = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
must_fire = [sum(w * x for w, x in zip(wts, p)) for p in pat3 if sum(p) >= 2]
must_not = [sum(w * x for w, x in zip(wts, p)) for p in pat3 if sum(p) < 2]
good_b = [b for b in range(-20, 21) if all(s + b > 0 for s in must_fire) and all(s + b <= 0 for s in must_not)]
assert good_b == [-4]
items.append(parts(
    "e-two-of-three", 5, ["ab-neuron"], ["neuron-design"], 300, "At least two of three",
    "A neuron has weights 2, 3 and 4 on three inputs, each 0 or 1. It fires when its sum is greater than 0. "
    "You want it to fire when **at least two** inputs are 1.",
    "Find the bias.",
    [("What is the smallest sum, before the bias, of a pattern that must fire?",
      num(min(must_fire), 0, [("all-three", 9, 0), ("smallest-single", 2, 0)], label="Sum"),
      fb("The pairs give 5, 6 and 7, and all three give 9. The smallest is $2 + 3 = 5$.",
         "List the weight sums of the patterns with two or three inputs on.",
         {"all-three": "You took all three inputs. Two are enough, and the two smallest weights give 5.",
          "smallest-single": "You took a single input. One input on must not fire; the smallest pair gives 5."})),
     ("What is the largest sum, before the bias, of a pattern that must not fire?",
      num(max(must_not), 0, [("none-on", 0, 0), ("pair", 5, 0)], label="Sum"),
      fb("The single inputs give 2, 3 and 4, and none gives 0. The largest is 4.",
         "List the weight sums of the patterns with at most one input on.",
         {"none-on": "You took the pattern with no input on. The single inputs are larger, up to 4.",
          "pair": "You took a pair. A pair must fire; the patterns that must not are the singles, up to 4."})),
     ("Which whole-number bias makes the neuron compute \"at least two\"?",
      num(good_b[0], 0, [("zero-fires", -5, 0), ("too-high", -3, 0), ("sign", 4, 0)], label="Bias"),
      fb("$5 + b > 0$ needs $b > -5$, and $4 + b \\le 0$ needs $b \\le -4$. Only $-4$ is whole.",
         "Use part 1 to make every pair fire and part 2 to keep every single quiet.",
         {"zero-fires": "You allowed $-5$. Then (1, 1, 0) sums to exactly 0, which does not fire.",
          "too-high": "You allowed $-3$. Then the single input of weight 4 sums to 1, which fires.",
          "sign": "You dropped the sign. A bias of 4 makes every pattern fire; the bias must pull the sums down, to $-4$."})),
     ("Which describes every bias that works, whole or not?",
      choice([
          opt("range", "Greater than $-5$ and at most $-4$", correct=True),
          opt("both", "From $-5$ to $-4$, both ends included",
              "You let $-5$ in. At $-5$, (1, 1, 0) sums to exactly 0, which does not fire."),
          opt("below", "Any bias of $-4$ or less",
              "You kept the singles quiet but forgot the pairs. Below $-5$, (1, 1, 0) no longer fires."),
          opt("open", "Greater than $-9$ and less than $-2$",
              "You used the extreme sums, 9 and 2. The tight limits are the smallest pair, 5, and the largest single, 4.")]),
      fb("$b > -5$ from the smallest pair and $b \\le -4$ from the largest single.", "Combine the limits from parts 1 and 2."))],
    "The pairs sum to 5, 6 and 7 and all three to 9, so the bias must lift 5 above 0: $b > -5$. The single inputs sum to 2, 3 and 4, so 4 must stay at or below 0: $b \\le -4$. "
    "The gap is one unit wide, and $-4$ is the only whole number in it."))

# N4 (l7, l8): fit a line by nudging with a halving step (the topic's exit script)
MSE_SRC = ("def mse(w, b, xs, ys):\n    total = 0\n    for i in range(len(xs)):\n        e = w * xs[i] + b - ys[i]\n"
           "        total = total + e * e\n    return total / len(xs)\n")
FIT_SOL = MSE_SRC + (
    "\ndef fit_halving(xs, ys):\n    w, b = 0.0, 0.0\n    for step in [1, 0.5, 0.25, 0.125]:\n        while True:\n"
    "            old = (w, b)\n            best = mse(w, b, xs, ys)\n"
    "            up, down = mse(w + step, b, xs, ys), mse(w - step, b, xs, ys)\n"
    "            if up < best and up <= down:\n                w, best = w + step, up\n"
    "            elif down < best:\n                w, best = w - step, down\n"
    "            up, down = mse(w, b + step, xs, ys), mse(w, b - step, xs, ys)\n"
    "            if up < best and up <= down:\n                b, best = b + step, up\n"
    "            elif down < best:\n                b, best = b - step, down\n"
    "            if (w, b) == old:\n                break\n"
    "    return (w, b, round(mse(w, b, xs, ys), 6))\n")
FIT_STARTER = MSE_SRC + (
    "\ndef fit_halving(xs, ys):\n    # steps 1, 0.5, 0.25 and 0.125 in turn\n"
    "    # at each step: nudge w, then b from the new w, until a round changes nothing\n"
    "    return (0.0, 0.0, 0.0)\n")
FIT_NO_HALF = FIT_SOL.replace("[1, 0.5, 0.25, 0.125]", "[1]")
FIT_LE = FIT_SOL.replace("if up < best and up <= down:", "if up <= best and up <= down:")
FIT_OLD_W = FIT_SOL.replace("            old = (w, b)\n            best = mse(w, b, xs, ys)\n",
                            "            old = (w, b)\n            w0 = w\n            best = mse(w, b, xs, ys)\n").replace(
    "            up, down = mse(w, b + step, xs, ys), mse(w, b - step, xs, ys)\n",
    "            best = mse(w0, b, xs, ys)\n            up, down = mse(w0, b + step, xs, ys), mse(w0, b - step, xs, ys)\n")
FIT_W_ONLY = FIT_SOL.replace("            if (w, b) == old:\n", "            if w == old[0]:\n")
assert FIT_NO_HALF != FIT_SOL and FIT_LE != FIT_SOL and FIT_OLD_W != FIT_SOL and FIT_W_ONLY != FIT_SOL

ns_fit = {}
exec(FIT_SOL, ns_fit)
fit_cases = [
    ([0, 1, 2, 3], [1, 3, 5, 7]),
    ([0, 1, 2, 3, 4], [0.5, 1.25, 2, 2.75, 3.5]),
    ([1, 3, 4], [0, 5, 7]),
    ([-2, -1, 0, 1, 2], [5.5, 3.5, 1.5, -0.5, -2.5]),
    ([0, 0], [1, 4]),
    ([1, 2, 3, 4], [10, 9, 11, 12]),
    ([2, 4, 6], [3, 4, 7]),
]
fit_tests = []
for xs, ys in fit_cases:
    got = ns_fit["fit_halving"](xs, ys)
    fit_tests.append({"call": f"list(fit_halving({xs}, {ys}))", "expect": repr([float(got[0]), float(got[1]), float(got[2])]),
                      "compare": "isclose"})
items.append({
    "id": "e-fit-halving", "difficulty": 5, "skills": ["ab-nudge"], "tags": ["nudge-script"], "pace": 600,
    "title": "Nudging with a shrinking step",
    "prose": "`mse(w, b, xs, ys)` is written for you. One round of the nudge rule tries $w$ + step and $w$ − step and keeps the lower if it lowers the MSE "
             "(+ step on a tie). Then it does the same for $b$, starting from the new $w$.",
    "question": "Write `fit_halving(xs, ys)`. Start at $w = 0$, $b = 0$ with step 1, and do rounds until a round changes nothing. "
                "Then halve the step and go on, through steps 0.5, 0.25 and 0.125. When a round at step 0.125 changes nothing, return `(w, b, error)`, "
                "with the error rounded to 6 places.",
    "widget": {
        "kind": "code", "language": "python",
        "starter": FIT_STARTER,
        "solution": FIT_SOL,
        "examples": [{"call": "list(fit_halving([0, 1, 2, 3], [1, 3, 5, 7]))", "expect": fit_tests[0]["expect"], "compare": "isclose"},
                     {"call": "list(fit_halving([0, 2], [1, 2]))",
                      "expect": repr([float(v) for v in ns_fit["fit_halving"]([0, 2], [1, 2])]), "compare": "isclose"}],
        "tests": fit_tests,
        "how": f"Submit runs {len(fit_tests)} hidden tests. Each answer is accepted when it is equal up to a tiny rounding difference.",
        "mutants": [
            {"source": FIT_NO_HALF, "test": 2, "symptom": "Stops after step 1, so it never tries the finer steps."},
            {"source": FIT_OLD_W, "test": 3, "symptom": "Scores the b trials on the old w, so rounds can undo each other for ever.", "timeout": True},
            {"source": FIT_LE, "test": 5, "symptom": "A tie moves the line, so on points that all have x = 0 the loop never settles.", "timeout": True},
            {"source": FIT_W_ONLY, "test": 3, "symptom": "Stops a step when w settles, even if b is still moving."},
        ],
    },
    "feedback": fb("The line settles at each step in turn, and the halving steps reach slopes a step of 1 cannot.",
                   "Read the first failing test.",
                   {"test-2": "On these points step 1 settles at a line that the finer steps still improve. Check the step halves after each settle.",
                    "test-3": "Nudge $b$ from the new $w$, and compare each $b$ trial with the error after the $w$ nudge. End a step only when neither $w$ nor $b$ moved in a round.",
                    "test-5": "Both points have $x = 0$, so changing $w$ never changes the error. Keep a nudge only when it lowers the error, and stop a step only when neither $w$ nor $b$ moved."}),
    "explain": {"text": "Each step runs the nudge rule until a whole round changes nothing, then the step halves. "
                        "The steps 1, 0.5, 0.25 and 0.125 add up exactly in a computer, so no rounding of $w$ or $b$ is needed. "
                        "A finer step finds lines that a coarse one jumps over."}})

# L5 (l13 to l15): a letter table with start and end marks, sampled into a name
NAME_SOL = ("def sample_name(names, us):\n    counts = {}\n    for name in names:\n        marked = '.' + name + '.'\n"
            "        for i in range(len(marked) - 1):\n            row = counts.setdefault(marked[i], {})\n"
            "            row[marked[i + 1]] = row.get(marked[i + 1], 0) + 1\n"
            "    letter, out = '.', ''\n    for u in us:\n        row = counts[letter]\n        total = sum(row.values())\n"
            "        running = 0\n        for nxt in sorted(row):\n            running = running + row[nxt]\n"
            "            if running > u * total:\n                break\n        if nxt == '.':\n            break\n"
            "        out += nxt\n        letter = nxt\n    return out\n")
NAME_STARTER = ("def sample_name(names, us):\n    # 1. count the pairs of '.' + name + '.' for every name\n"
                "    # 2. from '.', pick each next letter with one u; stop when '.' is picked\n    return ''\n")
NAME_FIRST_SEEN = NAME_SOL.replace("for nxt in sorted(row):", "for nxt in row:")
NAME_GE = NAME_SOL.replace("if running > u * total:", "if running >= u * total:")
NAME_NO_END = NAME_SOL.replace("marked = '.' + name + '.'", "marked = '.' + name")
NAME_KEEP_DOT = NAME_SOL.replace("        if nxt == '.':\n            break\n        out += nxt\n",
                                 "        out += nxt\n        if nxt == '.':\n            break\n")
assert len({NAME_SOL, NAME_FIRST_SEEN, NAME_GE, NAME_NO_END, NAME_KEEP_DOT}) == 5
ns_name = {}
exec(NAME_SOL, ns_name)
name_cases = [
    (["ab", "b"], [0.3, 0.6, 0.9]),
    (["ann", "bob", "ada"], [0.1, 0.3, 0.7, 0.95]),
    (["zoe", "amy"], [0.3, 0.3, 0.9]),
    (["ab", "ba"], [0.5, 0.5, 0.5]),
    (["kai", "kim", "ken", "kit"], [0.6, 0.3, 0.1, 0.2]),
    (["anna", "anne", "annie"], [0.2, 0.4, 0.1, 0.9, 0.05, 0.99]),
    (["eve", "eva", "ewan"], [0.9, 0.1, 0.4]),
    (["max", "mia", "mo"], [0.5, 0.1, 0.8, 0.3, 0.5]),
]
name_tests = []
for names, us in name_cases:
    got = ns_name["sample_name"](names, us)
    name_tests.append({"call": f"sample_name({names!r}, {us!r})", "expect": repr(got), "compare": "equal"})
items.append({
    "id": "e-sample-name", "difficulty": 5, "skills": ["ab-language"], "tags": ["bigram", "sampling"], "pace": 600,
    "title": "A name from a letter table",
    "prose": "`names` is a list of names in lower case. Build a next-letter table with a start and an end mark: \"ann\" becomes `.ann.` "
             "and gives the pairs `.a`, `an`, `nn` and `n.`. In each row, list the next letters in alphabetical order, with \".\" first.",
    "question": "Write `sample_name(names, us)`. Start at \".\" and, for each `u` in `us`, pick the first next letter whose running total of chances is above `u`. "
                "Stop when \".\" is picked and return the letters written as one string, without the marks. If `us` runs out first, return the letters so far.",
    "widget": {
        "kind": "code", "language": "python",
        "starter": NAME_STARTER,
        "solution": NAME_SOL,
        "examples": [{"call": "sample_name(['ab', 'b'], [0.3, 0.6, 0.9])", "expect": name_tests[0]["expect"], "compare": "equal"},
                     {"call": "sample_name(['ann'], [0.5, 0.5, 0.5, 0.5])",
                      "expect": repr(ns_name["sample_name"](["ann"], [0.5, 0.5, 0.5, 0.5])), "compare": "equal"}],
        "tests": name_tests,
        "how": f"Submit runs {len(name_tests)} hidden tests. Each result must equal the expected text exactly.",
        "mutants": [
            {"source": NAME_FIRST_SEEN, "test": 2, "symptom": "Keeps the next letters in the order first met, not alphabetical."},
            {"source": NAME_GE, "test": 4, "symptom": "Picks a letter whose running total equals u, not one above it."},
            {"source": NAME_NO_END, "test": 1, "symptom": "Leaves out the end mark, so a last letter has no row and no name can stop."},
            {"source": NAME_KEEP_DOT, "test": 1, "symptom": "Writes the end mark into the name."},
        ],
    },
    "feedback": fb("The table and the picks match the rule: alphabetical rows, the first running total above $u$, and a stop at \".\".",
                   "Read the first failing test.",
                   {"test-1": "Mark both ends of each name, and stop without writing \".\" when it is picked.",
                    "test-2": "List each row's next letters in alphabetical order, with \".\" first, not in the order you first meet them.",
                    "test-4": "A running total equal to $u$ is not above it, so walk on to the next letter."}),
    "explain": {"text": "The start mark gives the first row the first letters of the names, and the end mark lets a name stop. "
                        "Each pick walks the running totals of one row, exactly as for words in l15. "
                        "`makemore` builds names from the same kind of table, then swaps it for a network."}})

order_d = {2: [], 3: [], 4: [], 5: []}
for it in items:
    order_d[it["difficulty"]].append(it)
exam = {
    "id": "topic-0.8", "topic": "0.8", "name": "AI from nothing", "minutes": 90, "pass": 0.7,
    "skills": {"ab-models": "Models from data", "ab-nudge": "Error and learning by nudging", "ab-neuron": "Neurons and layers",
               "ab-language": "Language by counting", "au-making": "How a chatbot is made", "au-limits": "Why chatbots make things up",
               "au-asking": "Asking well", "au-checking": "Checking answers and sources", "au-risks": "Privacy, bias and misuse",
               "au-alignment": "What alignment means"},
    "items": order_d[2] + order_d[3] + order_d[4] + order_d[5],
}
with open(OUT, "w", encoding="utf8") as f:
    json.dump(exam, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", os.path.normpath(OUT), len(exam["items"]), "items, pace", sum(i["pace"] for i in exam["items"]), "s",
      {k: len(v) for k, v in order_d.items()})
