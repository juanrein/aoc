import os
import re
from collections import Counter, defaultdict
import datetime


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    data = []
    for line in lines:
        parts = line.split(":")
        target = int(parts[0])
        nums = [int(d) for d in parts[1].strip().split(" ")]
        data.append((target, nums))

    return data

def solvable(target, nums, total, i):
    if i >= len(nums):
        return target == total
    if total > target:
        return False
    return solvable(target, nums, total + nums[i], i+1) or solvable(target, nums, total * nums[i], i+1)


def part1():
    result = 0

    for target, nums in parse_input():
        if solvable(target, nums, 0, 0):
            result += target

    print(result)


def solvable2(target, nums, total, i):
    if i >= len(nums):
        return target == total
    if total > target:
        return False
    return solvable2(target, nums, total + nums[i], i+1) or solvable2(target, nums, total * nums[i], i+1) or solvable2(target, nums, int(str(total) + str(nums[i])), i+1)

def part2():
    result = 0

    for target, nums in parse_input():
        if solvable2(target, nums, 0, 0):
            result += target


    print(result)
