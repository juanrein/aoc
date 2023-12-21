import os
from collections import defaultdict
import re
from itertools import cycle
import math

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    return [[int(d) for d in line.split()] for line in lines]


def part1():
    result = 0

    for line in parse_input():
        nums = line
        nextVal = 0
        while True:
            differences = []

            nextVal += nums[-1]

            n_zeros = 0
            for i in range(1, len(nums)):
                d = nums[i] - nums[i-1]
                differences.append(d)
                if d == 0:
                    n_zeros += 1
                
            if n_zeros == len(differences):
                break

            nums = differences

        result += nextVal

    print(result)


result = 0

for line in parse_input():
    nums = line
    nextVals = []
    while True:
        differences = []

        nextVals.append(nums[0])

        n_zeros = 0
        for i in range(1, len(nums)):
            d = nums[i] - nums[i-1]
            differences.append(d)
            if d == 0:
                n_zeros += 1
            
        if n_zeros == len(differences):
            break

        nums = differences

    current = 0

    for i in range(len(nextVals)-1, -1, -1):
        current = nextVals[i] - current

    result += current

print(result)