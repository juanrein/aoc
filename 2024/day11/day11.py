import os
import re
from collections import Counter, defaultdict, deque
import datetime
from functools import cache

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    return [int(d) for d in lines[0].split(" ")]


nums = parse_input()


@cache
def count(num, t):
    if t <= 0:
        return 1
    if num == 0:
        return count(1, t-1)
    s = str(num)
    if len(s) % 2 == 0:
        slh = len(s)//2
        return count(int(s[:slh]), t-1) + count(int(s[slh:]), t-1)
    return count(num*2024, t-1)


total = 0
for num in nums:
    total += count(num, 75)

print(total)
