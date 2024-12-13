import os
import re
from collections import Counter

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    left = []
    right = []
    for line in lines:
        lr = [int(d) for d in re.findall("\d+", line)]
        left.append(lr[0])
        right.append(lr[1])
    
    return left, right

def part1():
    left, right = parse_input()

    lefts = sorted(left)
    rights = sorted(right)

    total = 0
    for l,r in zip(lefts, rights):
        total += abs(l-r)

    print(total)

def part2():
    lefts, rights = parse_input()
    counts = Counter(rights)
    total = 0
    for left in lefts:
        total += counts.get(left, 0) * left

    print(total)
