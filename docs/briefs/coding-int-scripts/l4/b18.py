from lib2 import *
import refs4 as R

N1 = ['narration']
N2 = ['tradeoffs']
N3 = ['product-except-self']


def pes_tests():
    t = [{'call': f"product_except_self({xs!r})", 'expect': e} for xs, e in R.PES_SMALL]
    t.append({'setup': 'xs = [1] * 100000; xs[10] = 2; xs[500] = 3', 'call': 'sum(product_except_self(xs))', 'expect': 599993})
    t.append({'call': "all('/' not in line.split('#')[0] for line in __learner_source__.splitlines())", 'expect': True})
    t.append({'call': "sum(1 for l in __learner_source__.splitlines() if l.strip().startswith('#')) >= 3", 'expect': True})
    return t


def code_console():
    return console('Plan in comments, code below', [
        "# plan: out[i] = left product times right product",
        "for i in range(n): out[i] = left; left *= nums[i]",
        "for i in range(n - 1, -1, -1): out[i] *= right; right *= nums[i]"])


def lesson():
    S = []
    # 1 hook
    S.append(screen(
        'problem', 1, 'Silent or spoken', N1,
        "Reported developer rounds score how you think as well as the code. You practised reasoning aloud in `recruiting` l12 and `mm-games` l12. "
        "New here: the plan, with its trade-offs, written before the code.",
        "Which habit of candidate B earns the most in the interviewer's notes?",
        choice([
            ('a', 'Naming the brute force and its cost before the better idea', None),
            ('b', 'Typing faster than candidate A', "You chose speed. Candidate A typed for ten minutes and the notes show no plan."),
            ('c', 'Reading every line of code aloud as it is typed', "You chose a running commentary. It buries the plan under detail."),
            ('d', 'Starting with the final loops', "You chose to start with the answer. The interviewer cannot see how you reached it."),
        ]),
        hints("Which line of B's talk shows the plan?",
              "The line that says what the slow way costs.", "B names the brute force, says it is quadratic, then offers the better idea.", ["l3", "l4", "l5"]),
        fb("Naming the slow way and its cost shows the plan before any code.", "Not quite right. Look for the line that shows how B chose the method.",
           {'b': "A types for ten minutes and has no plan to show.", 'c': "A line-by-line reading hides the idea.", 'd': "Starting from the answer shows no reasoning."}),
        explain("B says what the slow way costs and why a better one exists. The interviewer hears a plan within two minutes. A's ten silent minutes show only that the code compiles."),
        canvas=console('Two transcripts', [
            "Candidate A types for ten minutes in silence. Then: 'It works, I think.'",
            "Candidate B: 'Each output is the product of the others.'",
            "Candidate B: 'The slow way is a double loop, quadratic.'",
            "Candidate B: 'Better: products to the left, then to the right.'"]), pace=90))
    # 2 restate
    S.append(screen(
        'ladder', 1, 'Say it back', N1,
        "The first sentence of a good answer restates the problem. For `nums = [2, 3, 4, 5]` the entry for the 2 is $3 \\times 4 \\times 5 = 60$.",
        "Which sentence restates `product_except_self`?",
        choice([
            ('a', 'Each output is the product of all the other entries', None),
            ('b', 'Each output is the product of the whole list', "You included the entry itself. For the 2 that gives 120, not 60."),
            ('c', 'Each output is the product of its two neighbours', "You used the neighbours only. The 2 has one neighbour, and the answer uses all three others."),
            ('d', 'Each output is the running product so far', "You described a prefix product. The entry for the 2 needs the numbers after it too."),
        ]),
        hints("What is left out of the product for the 2?",
              "Only the 2 itself.", "The answer for each position multiplies every other entry.", ["l1"]),
        fb("Every other entry, and only the entry itself is left out.", "Not quite right. Check the entry for the 2: it is 60.",
           {'b': "The whole list gives 120. The 2 must be left out.", 'c': "The 2 has one neighbour. The answer uses all three others.", 'd': "A running product ignores the entries to the right."}),
        explain("Every output leaves out only its own entry. For the 2 that is $3 \\times 4 \\times 5 = 60$. One sentence says this."),
        canvas=console('product_except_self([2, 3, 4, 5])', ["The entry for 2 is 3 x 4 x 5 = 60.", "The entry for 3 is 2 x 4 x 5 = 40."]), pace=60))
    # 3 brute force cost
    S.append(screen(
        'ladder', 2, 'Name the brute force', N2,
        "Next, say the slow way and what it costs. For each of $n$ positions it multiplies the other $n - 1$ entries. On `[2, 3, 4, 5]` it gives `[60, 40, 30, 24]`.",
        "At $n = 100{,}000$, how many entries does it multiply in all?",
        numeric(9999900000, 'Entries', '9,999,900,000: 100,000 times 99,999', [('square', 10000000000), ('once', 100000)]),
        hints("How many entries does one position multiply?",
              "$n - 1$, which is 99,999.", "There are 100,000 positions, so $100{,}000 \\times 99{,}999$.", ["l1"]),
        fb("$100{,}000 \\times 99{,}999 = 9{,}999{,}900{,}000$ entries.", "Not quite right. Each position skips its own entry.",
           {'square': "You multiplied $n$ by $n$. Each position skips its own entry, so it is $n - 1$.", 'once': "You counted one pass. The slow way repeats it for every position."}),
        explain("Each of the $n$ positions multiplies $n - 1$ entries, which is $n(n - 1)$. At $n = 100{,}000$ that is nearly ten billion. Say \"quadratic\" and give the number."),
        canvas=console('Brute force on [2, 3, 4, 5]', ["Position 0: 3 x 4 x 5 = 60.", "Position 1: 2 x 4 x 5 = 40.", "Position 2: 2 x 3 x 5 = 30.", "Position 3: 2 x 3 x 4 = 24."]), pace=90))
    # 4 division idea
    S.append(screen(
        'ladder', 2, 'The idea that breaks', N2,
        "A tempting idea: take the product of the whole list and divide by each entry. Now try `[3, 0, 2]`. The right answer is `[0, 6, 0]`.",
        "Why does dividing by each entry fail here?",
        choice([
            ('a', 'The total is 0, so the zero entry cannot be recovered', None),
            ('b', 'The total is too large to store', "You chose overflow. The total of this list is 0."),
            ('c', 'Division is slower than multiplication', "You chose speed. The trouble is wrong answers, not time."),
            ('d', 'Integer division would round the answers', "You chose rounding. Whole-number products divide exactly."),
        ]),
        hints("What is the product of `[3, 0, 2]`?",
              "It is 0.", "For the zero entry the answer should be $3 \\times 2 = 6$, but $0 / 0$ cannot give it.", ["l3"]),
        fb("The total is 0, so no division can recover the 6 for the zero entry.", "Not quite right. Look at the total of `[3, 0, 2]`.",
           {'b': "The total of this list is 0, which is tiny.", 'c': "Both operations are fast. The answers are wrong.", 'd': "The products here are whole numbers and divide exactly."}),
        explain("The total is 0. The entry for the zero should be $3 \\times 2 = 6$, and dividing 0 by 0 cannot give it. The problem says no division for this reason."),
        canvas=console('Dividing the total', ["total = 3 x 0 x 2 = 0", "answer for 3: 0 / 3 = 0", "answer for 0: 0 / 0, undefined (it should be 6)", "answer for 2: 0 / 2 = 0"]), pace=90))
    # 5 code
    ex = [{'call': 'product_except_self([2, 3, 5, 7])', 'expect': [105, 70, 42, 30]}, {'call': 'product_except_self([0, 5])', 'expect': [5, 0]}]
    S.append(screen(
        'problem', 3, 'Plan, then code', N3,
        "Write your plan as comments first, at least three lines, then the code. The tests also check that your code has no division.",
        "Write `product_except_self(nums)` in $O(n)$ time.",
        code('python', R.PES_STARTER, R.PES_SOL, ex, pes_tests(),
             "Check runs 10 hidden tests. Eight check the answers, one checks that no line divides, and one checks for three comment lines."),
        hints("Which product does each position need?",
              "Everything to its left times everything to its right.", "Pass one stores the left product in `out[i]`. Pass two multiplies in the right product, going from the end.", ["l2", "l3"]),
        fb("Two passes: left products, then right products.", "Not quite right. Check the first failing test.",
           tkeys(10, {2: "Test 2: a single zero makes every answer 0 except the zero's own.", 3: "Test 3: two zeros make every answer 0.", 4: "Test 4: the answer for the 0 is 5.",
                      8: "Test 8: 100,000 numbers need a pass, not a double loop.", 9: "Test 9: a line of your code contains a `/`. Use two passes.",
                      10: "Test 10: write at least three comment lines of plan."})),
        explain("Pass one leaves in each place the product of everything to its left. Pass two walks back and multiplies in everything to the right. No division is needed, so zeros are safe."),
        canvas=code_console(), pace=720))
    # 6 trap
    S.append(screen(
        'trap', 2, 'Code first, explain after', N1,
        "A candidate types the two loops in silence and says, \"It works.\" The interviewer asks: why two passes?",
        "What should the candidate have done before typing?",
        choice([
            ('a', 'Written the plan as comments: two passes, no division', None),
            ('b', 'Typed faster, to leave time to explain afterwards', "You treated the explanation as a closing task. The plan is what the interviewer wants first."),
            ('c', 'Explained the code after the tests pass', "You coded first and explained after. Then you cannot say why two passes work."),
            ('d', 'Memorised the standard solution beforehand', "A memorised answer breaks on the first follow-up, such as a stream."),
        ]),
        hints("What does the interviewer want to hear?",
              "The reason for the method, not only the method.", "Writing the plan first forces you to know why two passes work.", ["l1"]),
        fb("A plan in comments comes first, so the code follows from it.", "Not quite right. Choose what the candidate should do before typing.",
           {'b': "Speed does not give a reason for the method.", 'c': "Explaining after the code means you may not know the reason.", 'd': "A memorised answer cannot adapt to a change."}),
        explain("The candidate who codes first often cannot say why the passes work. A plan in comments makes the reason exist before the code. It also gives the interviewer something to follow."),
        canvas=code_console(), pace=90))
    # 7 table matching
    S.append(screen(
        'ladder', 2, 'Which line is being said', N1,
        "Narration follows the code. Each sentence below explains one line of the code on the screen. Give the line number.",
        "Match each sentence to a line.",
        table_w(["What you say", "Line"], [
            ["Each output is the left product times the right product.", ed(1)],
            ["Pass one stores the product of everything to the left.", ed(2)],
            ["Pass two multiplies in the product of everything to the right.", ed(3)]]),
        hints("Which line is a comment, and which two are loops?",
              "The comment is the plan, so it is line 1.", "The first loop runs forwards and builds the left products. The second runs back.", ["l1", "l2", "l3"]),
        fb("Line 1 is the plan, line 2 the left pass and line 3 the right pass.", "Not quite right. Read which direction each loop runs.",
           {'r0c1': "The plan is the comment on line 1.", 'r1c1': "Pass one is the loop that runs forwards, line 2.", 'r2c1': "Pass two is the loop that runs backwards, line 3."}),
        explain("The comment states the plan. The forward loop builds the left products and the backward loop multiplies in the right ones. Each sentence you say should point at one line."),
        canvas=code_console(), pace=90))
    # 8 generalise + order
    S.append(screen(
        'generalise', 2, 'The order of a spoken answer', N1,
        "A spoken answer has a fixed shape.\n\n"
        "```python\n# restate: each output is the product of all the others\n# example: [2, 3, 4, 5] gives [60, 40, 30, 24]\n"
        "# brute force: n * (n - 1) products, quadratic\n# better: left products, then right products, linear\n```",
        "Put the steps of a spoken answer in order. Leave out the step that does not belong.",
        order([
            ('n1', 'Say the problem back in one sentence', None),
            ('n2', 'Give a small example', None),
            ('n3', 'Name the brute force and its cost', None),
            ('n4', 'Name the better idea', None),
            ('n5', 'Write the plan as comments', None),
            ('n6', 'Code it, saying each non-obvious line', None),
            ('d1', 'Stay silent until the code runs', "Silence hides the plan. If the code is wrong, you cannot show where your thinking was right."),
        ], ['n1', 'n2', 'n3', 'n4', 'n5', 'n6'], distractors=['d1']),
        hints("What comes right after the restatement?",
              "An example, so both of you agree on the problem.", "Restate, example, brute force, better idea, comments, then code."),
        fb("Restate, example, brute force, better idea, comments, code.", "Not quite right. The plan comes before the code.",
           {'d1': "You stayed silent. The interviewer then has nothing to follow.", 'left-out': "Six steps belong. Only silence is wrong.", 'n6': "Coding comes last."}),
        explain("The restatement and the example fix the problem. The brute force and the better idea show the choice. The comments make the plan, and the code follows."),
        canvas=code_console(), pace=90))
    # 9 transfer stream
    S.append(screen(
        'transfer', 3, 'What if it is a stream', N2,
        "The interviewer interrupts: \"What if the numbers arrive one at a time?\" The answers are wanted at the end. Say what changes.",
        "Which answer states what changes?",
        choice([
            ('a', 'I must store the numbers, because the right pass needs entries not yet seen', None),
            ('b', 'Nothing changes: two passes work on a stream too', "You assumed the second pass can run as numbers arrive. It runs right to left, so the end must come first."),
            ('c', 'I would divide the total by each entry to answer at once', "You went back to division. It fails on zeros, and the total is unknown until the end."),
            ('d', 'It cannot be done', "You gave up. The question is what changes: the memory and the timing."),
        ]),
        hints("Which pass needs numbers that have not arrived?",
              "The right pass.", "The right product needs every later entry, so keep the numbers and run it at the end.", ["l3"]),
        fb("Store the stream and run the right pass at the end.", "Not quite right. Say which pass is the problem.",
           {'b': "The right pass starts from the last number.", 'c': "Division fails on zeros, and the total is not known yet.", 'd': "It can be done with stored numbers."}),
        explain("The left pass can run as numbers arrive. The right pass needs the last number first, so we must keep the stream. The extra space is then linear, and the answer comes at the end."),
        canvas=code_console(), pace=90))
    # 10 transfer complexity sentence
    S.append(screen(
        'transfer', 2, 'Say the complexity', N2,
        "You finish and the interviewer asks for the cost. Say it in one sentence that names both time and space.",
        "Which sentence is best?",
        choice([
            ('a', 'Linear time, and constant extra space apart from the output', None),
            ('b', 'It is order n, and it uses a little memory', "You gave the time but left the memory vague. Name the space."),
            ('c', 'Quadratic time, because there are two loops', "You counted loops. These two run one after the other, so the cost is $2n$, not $n^2$."),
            ('d', 'Constant time, because there is no nested loop', "Constant time would not read the list. Each pass visits every entry."),
        ]),
        hints("Do the two loops sit inside each other?",
              "No, one runs after the other.", "Two passes of $n$ steps each is $2n$, linear. The only extra space is the output list.", ["l2", "l3"]),
        fb("Linear time, constant extra space apart from the output.", "Not quite right. Count the passes and what they store.",
           {'b': "A vague memory claim gives the interviewer nothing to check.", 'c': "Loops in sequence add, they do not multiply.", 'd': "Reading every entry takes at least linear time."}),
        explain("Two passes of $n$ steps cost $2n$, which is linear. Apart from the output list we keep two running products, which is constant space. Say both in one breath."),
        canvas=code_console(), pace=90))

    quiz = [
        item('q-cost', 2, None, N2, "The brute force of `product_except_self` runs on 50,000 numbers. How many entries does it multiply, as $n(n - 1)$?",
             numeric(2499950000, 'Entries', '2,499,950,000: 50,000 times 49,999', [('square', 2500000000), ('once', 50000)]),
             fb("$50{,}000 \\times 49{,}999 = 2{,}499{,}950{,}000$.", "Not quite right. Each position skips its own entry.",
                {'square': "You used $n^2$. Each position skips its own entry.", 'once': "You counted one pass. The slow way repeats it for every position."}),
             explain("Each of $n$ positions multiplies $n - 1$ entries. At $n = 50{,}000$ that is $50{,}000 \\times 49{,}999 = 2{,}499{,}950{,}000$."), quiz=True),
        item('q-zero', 2, None, N2, "Take `[4, 0, 5]`, whose middle answer is 20. What does dividing the total by the middle entry give?",
             choice([('a', '0 / 0, which is undefined', None),
                     ('b', '20, so division works here', "You ignored the total. It is 0, so no entry can give 20."),
                     ('c', '0, which is also right', "You treated 0 as the answer. The product of the others is 20."),
                     ('d', '9, the sum of the others', "You added the others. The question is about a product.")]),
             fb("The total is 0, so the zero entry gives 0 / 0.", "Not quite right. Find the total first.",
                {'b': "The total is 0, not 20.", 'c': "The answer is the product of the others, 20, not 0.", 'd': "The sum of the others is 9, but the problem asks for the product."}),
             explain("The total of `[4, 0, 5]` is 0. The middle entry would be 0 divided by 0, which has no value. The right answer, 20, needs the product of the others."), quiz=True),
        item('q-pass', 2, None, N3, "After the left pass on `[3, 4, 5]`, what does `out` hold?",
             choice([('a', '`[1, 3, 12]`', None),
                     ('b', '`[20, 15, 12]`', "You wrote the final answer. That needs the right pass too."),
                     ('c', '`[3, 12, 60]`', "You included each entry in its own product. The left product stops before the entry."),
                     ('d', '`[1, 1, 1]`', "You wrote the starting list. The left pass fills it.")]),
             fb("Place 0 has nothing to its left, so 1. Place 1 has 3. Place 2 has 12.", "Not quite right. The left product leaves out the entry itself.",
                {'b': "The final answer comes after the right pass.", 'c': "That includes each entry in its own product.", 'd': "The left pass changes every entry after the first."}),
             explain("Place 0 has nothing to its left, so it holds 1. Place 1 holds 3 and place 2 holds $3 \\times 4 = 12$. The right pass then gives `[20, 15, 12]`."), quiz=True),
        item('q-say', 2, None, N2, "Which sentence states the cost of two separate passes over the list?",
             choice([('a', 'Linear time, with constant extra space beyond the output', None),
                     ('b', 'Quadratic time, because it reads the list twice', "You multiplied the passes. Two passes add: $2n$."),
                     ('c', 'Logarithmic time, because it halves the work', "Nothing halves here. Each pass visits every entry."),
                     ('d', 'It depends', "You avoided a claim. State the cost, then qualify it.")]),
             fb("Two passes add up to linear time.", "Not quite right. Two passes in sequence add.",
                {'b': "Passes in sequence add, they do not multiply.", 'c': "No step halves the list.", 'd': "Give the cost, then qualify it."}),
             explain("Two passes of $n$ steps cost $2n$, which is linear. The only extra memory is two running products."), quiz=True),
    ]
    return {
        "id": "l18-talking-while-coding", "course": "coding-int", "title": "Talking while you code", "minutes": 13,
        "objectives": ["Explain the plan and its trade-offs aloud while writing the code."],
        "skills": ["ci-timed"], "screens": S,
        "summary": summary(
            ["Say the problem back in one sentence, give an example, then name the brute force and its cost.",
             "Name the better idea and write the plan as comments before the code. Then say each non-obvious line.",
             "State the cost in one sentence that names time and space."],
            "Spoken cost", "\\text{time } O(n),\\ \\text{extra space } O(1)",
            "Say both, and say what the output costs separately.",
            "Coding first and explaining after, so you cannot say why it works."),
        "quiz": quiz,
    }
