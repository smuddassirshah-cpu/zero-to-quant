"""Trap of l3 screen 7: a window that shrinks but never drops a front index that has left it."""
from collections import deque
def buggy(nums, limit):
    hi, lo = deque(), deque()
    left = best = 0
    for right, x in enumerate(nums):
        while hi and nums[hi[-1]] <= x: hi.pop()
        hi.append(right)
        while lo and nums[lo[-1]] >= x: lo.pop()
        lo.append(right)
        while left <= right and nums[hi[0]] - nums[lo[0]] > limit:
            left += 1
        best = max(best, right - left + 1)
    return best
def correct(nums, limit):
    hi, lo = deque(), deque()
    left = best = 0
    for right, x in enumerate(nums):
        while hi and nums[hi[-1]] <= x: hi.pop()
        hi.append(right)
        while lo and nums[lo[-1]] >= x: lo.pop()
        lo.append(right)
        while nums[hi[0]] - nums[lo[0]] > limit:
            left += 1
            if hi[0] < left: hi.popleft()
            if lo[0] < left: lo.popleft()
        best = max(best, right - left + 1)
    return best
def strict_ok(nums, limit):      # keeps equal values (pops only strictly smaller) and drops the front by index: still correct
    hi, lo = deque(), deque()
    left = best = 0
    for right, x in enumerate(nums):
        while hi and nums[hi[-1]] < x: hi.pop()
        hi.append(right)
        while lo and nums[lo[-1]] > x: lo.pop()
        lo.append(right)
        while nums[hi[0]] - nums[lo[0]] > limit:
            left += 1
            if hi[0] < left: hi.popleft()
            if lo[0] < left: lo.popleft()
        best = max(best, right - left + 1)
    return best
def brute(nums, limit):
    return max([j - i for i in range(len(nums) + 1) for j in range(i + 1, len(nums) + 1) if max(nums[i:j]) - min(nums[i:j]) <= limit], default=0)
a = [4, 2, 2, 2, 4, 4, 2, 2]
print('buggy', buggy(a, 0), 'correct', correct(a, 0), 'strict (keeps equals, drops by index)', strict_ok(a, 0), 'brute', brute(a, 0))
import random
for _ in range(3000):
    n = [random.randint(0, 5) for _ in range(random.randint(1, 12))]; l = random.randint(0, 4)
    assert correct(n, l) == strict_ok(n, l) == brute(n, l)
print('correct and strict versions agree with brute on 3000 random cases')
