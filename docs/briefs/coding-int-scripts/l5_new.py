"""Problem 5.2 replacement: hamming_total(nums)."""
import random, json
import numpy as np
from harness import *
random.seed(52)
REP = {}
HT_REF = '''
def hamming_total(nums):
    total = 0
    for bit in range(32):
        ones = sum((v >> bit) & 1 for v in nums)
        total += ones * (len(nums) - ones)
    return total
'''
HT_START = '''
def hamming_total(nums):
    return 0
'''
HT_SLOW = '''
def hamming_total(nums):
    total = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            total += bin(nums[i] ^ nums[j]).count("1")
    return total
'''
def ht_brute(nums):
    return sum(bin(nums[i] ^ nums[j]).count('1') for i in range(len(nums)) for j in range(i + 1, len(nums)))
def ht_np(nums):      # independent: numpy pairwise xor and a lookup popcount
    a = np.array(nums, dtype=np.int64)
    if len(a) < 2: return 0
    x = (a[:, None] ^ a[None, :])
    pc = np.zeros(x.shape, dtype=np.int64)
    for b in range(32): pc += (x >> b) & 1
    return int(pc.sum() // 2)
ns = {}; exec(HT_REF, ns); ref = ns['hamming_total']
for _ in range(3000):
    nums = [random.randint(0, 2 ** random.choice([3, 8, 20, 31]) - 1) for _ in range(random.randint(0, 12))]
    assert ref(nums) == ht_brute(nums)
for _ in range(20):
    nums = [random.randint(0, 2 ** 30) for _ in range(300)]
    assert ref(nums) == ht_np(nums) == ht_brute(nums)
smalls = [[], [7], [3, 3], [1, 2], [5, 9, 12], [0, 255], [7, 7, 7, 0]]
HT_TESTS = [dict(call=f'hamming_total({n})', expect=ht_brute(n)) for n in smalls]
# closed form for range(2^16): every one of 16 bit columns has 32768 ones and 32768 zeros
assert sum(1 for _ in [0]) == 1
assert ref(list(range(256))) == ht_brute(list(range(256))) == 8 * 128 * 128
big = 16 * 32768 * 32768
assert ref(list(range(65536))) == big == 17179869184
HT_TESTS.append(dict(setup='xs = list(range(65536))', call='hamming_total(xs)', expect=big))
check_py('hamming_total', HT_REF, HT_START, HT_TESTS)
REP['ht'] = md_tests(HT_TESTS)
r = run_py(HT_SLOW, HT_TESTS)
print('slow double loop:', [ok for ok, _ in r])
assert all(ok for ok, _ in r[:7]) and not r[7][0] and 'timeout' in r[7][1]
print('expected', [t['expect'] for t in HT_TESTS])
print('starter fails', sum(1 for ok, _ in run_py(HT_START, HT_TESTS) if not ok))
json.dump(REP, open('l5_tests.json', 'w'))
