"""rl_ops_l3.py: the rl course's level-3 gridworld and Q-learning helpers, shared with the AI strand.

The 4 by 5 grid of rl levels 2 and 3: cells are named 'r<row>c<col>' with rows 1 to 4 from the top and columns 1 to 5,
r2c3 is a wall, r1c5 pays +1 and r2c5 pays -1 (both end the episode), and every move costs 0.04. The moves are
U, R, D and L. With slip s the intended move happens with chance 1 - 2s and each side move with chance s; a move into
the edge or the wall leaves the agent where it is. Q is a dict {(cell, action): value}.

Conventions, all as in rl l11 and homework 3 (the course's numbers depend on them):
  * q_update masks the bootstrap at an end cell: the target is just the reward there.
  * Greedy ties go to the first best action in the order U, R, D, L.
  * An episode starts at rng.choice of the open cells unless a start is given. Each step draws rng.random() for the
    exploring test, then rng.choice(actions) if exploring, then (only when slip > 0) one rng.random() for the slip.
  * run_episode takes a max_steps cap, so an agent whose greedy policy loops still ends its episode.

Pure Python, no imports beyond random. Another grid can reuse run_episode and q_update by passing an env object with
the four members Gridworld has: actions, starts, is_end(s) and step(s, a, rng).
"""
import random

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
ACTIONS = 'URDL'
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]
OPEN = [s for s in CELLS if s not in TERMINAL]


def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t


def reward(t):
    """Reward for entering cell t: its payoff (+1, -1 or 0) plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP


def transition(s, a, slip=0.0):
    """{next cell: chance} for action a in s: the intended move 1 - 2*slip, each side move slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out


def sample_next(s, a, slip, rng):
    """One draw of the next cell. With slip 0 it is move(s, a) and uses no random number; otherwise one rng.random()."""
    if not slip:
        return move(s, a)
    u, acc, t = rng.random(), 0.0, s
    for t, p in transition(s, a, slip).items():
        acc += p
        if u < acc:
            break
    return t


def q_update(Q, s, a, r, s2, alpha, gamma, terminal, actions=ACTIONS):
    """One Q-learning update of Q[(s, a)], in place; return the new value.
    The target is r when `terminal` is true (s2 is an end cell), else r + gamma * max Q(s2, .)."""
    target = r if terminal else r + gamma * max(Q[(s2, b)] for b in actions)
    Q[(s, a)] += alpha * (target - Q[(s, a)])
    return Q[(s, a)]


def greedy_action(Q, s, actions=ACTIONS):
    """The first best action in s, in the order of `actions` (U, R, D, L here)."""
    return max(actions, key=lambda b: Q[(s, b)])


def greedy_policy(Q, cells=OPEN, actions=ACTIONS):
    """{cell: first best action} for every open cell (or the cells given)."""
    return {s: greedy_action(Q, s, actions) for s in cells}


class Gridworld:
    """The level-3 grid as an environment. slip is 0.0 (deterministic) or, in the course, 0.1."""
    actions = ACTIONS
    starts = OPEN

    def __init__(self, slip=0.0):
        self.slip = slip

    def is_end(self, s):
        return s in TERMINAL

    def step(self, s, a, rng):
        """Take action a in s. Return (next cell, reward, done)."""
        t = sample_next(s, a, self.slip, rng)
        return t, reward(t), t in TERMINAL


def run_episode(env, Q, start, alpha, gamma, eps, rng, max_steps=None, learn=True):
    """One episode from `start`, epsilon-greedy on Q, updating Q after every step when `learn` is true.
    It ends at an end cell or after max_steps steps (None: no cap), so a looping agent still stops.
    Return (steps, total reward, reached): reached is False when the cap ended the episode."""
    s, steps, total = start, 0, 0.0
    while not env.is_end(s):
        if max_steps is not None and steps >= max_steps:
            return steps, total, False
        if rng.random() < eps:
            a = rng.choice(env.actions)
        else:
            a = greedy_action(Q, s, env.actions)
        t, r, done = env.step(s, a, rng)
        if learn:
            q_update(Q, s, a, r, t, alpha, gamma, done, env.actions)
        total += r
        steps += 1
        s = t
    return steps, total, True


def q_learning(episodes, alpha, eps, seed, gamma=0.9, slip=0.0, max_steps=None):
    """Tabular Q-learning on the level-3 grid from all-zero Q; each episode starts at rng.choice(OPEN).
    Return Q. With slip 0 and max_steps None it is exactly rl l11's q_learning."""
    env, rng = Gridworld(slip), random.Random(seed)
    Q = {(s, a): 0.0 for s in CELLS for a in ACTIONS}
    for _ in range(episodes):
        run_episode(env, Q, rng.choice(env.starts), alpha, gamma, eps, rng, max_steps)
    return Q
