def split_brute(nums):
    return sum(1 for i in range(1, len(nums)) if sum(nums[:i]) == sum(nums[i:]))


for n in ([4, 1, 3, 2, 2], [2, 3, 5, 0, 5], [1, 2, 3, 0, 3], [5, -5] * 3, [3, 1, 2], [0, 0, 0, 0], [6, -2, 4, 0, 0, 1, 3]):
    print(n, split_brute(n))
print(split_brute([0] * 6), split_brute([5, -5, 5, -5]))
# big: [0]*200000 -> 199999; [5,-5]*100000: total 0; left sums 5,0,5,0..; zero when left==0 -> after even count: indices 2,4,...,199998 -> 99999 cuts
n = 100000
print('alt cuts', n - 1)


def ds(x):
    return sum(int(c) for c in str(x))


def dsp_brute(nums):
    ans = -1
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if ds(nums[i]) == ds(nums[j]):
                ans = max(ans, nums[i] + nums[j])
    return ans


print(dsp_brute([18, 43, 36, 13, 7]), dsp_brute([51, 71, 17, 42]), dsp_brute([39, 93, 12, 48, 84]))
print(180000 * 179999 // 2)
