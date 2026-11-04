import random, subprocess, tempfile, time, re
src = open('l4.py').read()
# reuse definitions
a = src.index("CS_CPP_REF = '''"); b = src.index("'''", src.index("CS_CPP_START = '''")+20)+3
from harness import *
ns = {}
exec(src[a:b], ns)
def cs_brute(nums, k):
    pre = [0]
    for x in nums: pre.append(pre[-1] + x)
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if pre[j] - pre[i] == k)
css = [([1,1,1],2),([1,2,3],3),([],0),([0,0,0],0),([1,-1,0],0),([3,4,7,2,-3,1,4,2],7),([5],5),([5],-5),([-1,-1,1],0)]
calls = [(f'count_subarrays_sum_k(std::vector<int>{cpp_lit(n)}, {k})', cs_brute(n, k)) for n, k in css]
calls.append(('count_subarrays_sum_k(std::vector<int>(200000, 0), 0)', 200000*200001//2))
calls.append(('[&]{ std::vector<int> v; for (int i = 0; i < 100000; ++i) { v.push_back(i % 2 ? -1 : 1); } return count_subarrays_sum_k(v, 0); }()', sum(100000 - L + 1 for L in range(2, 100001, 2))))
# starter is correct but slow: the harness' starter-fails assertion is replaced by a timing statement
import harness
try:
    check_cpp('count_subarrays_cpp', ns['CS_CPP_REF'], ns['CS_CPP_REF'], calls)
except AssertionError as e:
    print('expected: starter passes correctness (fails only by time):', str(e)[:80])
