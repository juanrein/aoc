import os
import re
from collections import Counter

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    grid = []
    for line in lines:
        nums = [int(d) for d in line.split(" ")]
        grid.append(nums)

    return grid

def is_save(nums):
    i = 0
    dir = None
    while i + 1 < len(nums):
        if nums[i] < nums[i+1]:
            if dir is None:
                dir = 1
            elif dir == -1:
                return False
            d = abs(nums[i] - nums[i+1])
            if not (1 <= d <= 3):
                return False
        elif nums[i] > nums[i+1]:
            if dir is None:
                dir = -1
            elif dir == 1:
                return False
            d = abs(nums[i] - nums[i+1])
            if not (1 <= d <= 3):
                return False
        else:
            return False
        i+=1

    return True


def part1():
    saves = 0

    for nums in parse_input():
        if is_save(nums):
            saves += 1

    print(saves)

def part2():
    saves = 0
    for nums in parse_input():
        if is_save(nums):
            saves += 1
        else:
            for i in range(len(nums)):       
                if is_save(nums[:i] + nums[i+1:]):
                    saves += 1
                    break
    print(saves)
        