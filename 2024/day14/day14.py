import os
import re
from collections import Counter, defaultdict, deque
import datetime
from functools import cache
import numpy as np
from sympy import symbols, solve
import math


def parse_input(test):
    file = "testinput.txt" if test else "input.txt"
    with open(os.path.join(os.path.dirname(__file__), file)) as f:
        lines = f.read().splitlines()

    robots = []
    for line in lines:
        nums = [int(d) for d in re.findall("-?\d+", line)]
        robots.append(nums)

    if test:
        return robots, 11, 7

    return robots, 101, 103


def draw(robots, W, H):
    grid = []
    for i in range(H):
        row = []
        for j in range(W):
            row.append(0)
        grid.append(row)
    for x, y, _, _ in robots:
        grid[y][x] += 1

    for row in grid:
        print("".join(["." if d == 0 else str(d) for d in row]))


def part1():
    robots, W, H = parse_input(False)

    for _ in range(100):
        for i in range(len(robots)):
            x, y, dx, dy = robots[i]
            robots[i][0] = (x+dx) % W
            robots[i][1] = (y+dy) % H

    quadrants = [0, 0, 0, 0]
    for x, y, _, _ in robots:
        if x < W//2 and y < H//2:
            quadrants[0] += 1
        elif x < W//2 and y > H//2:
            quadrants[1] += 1
        elif x > W//2 and y < H//2:
            quadrants[2] += 1
        elif x > W//2 and y > H//2:
            quadrants[3] += 1

    # draw(robots, W, H)
    print(quadrants)
    print(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3])


def part2():
    robots, W, H = parse_input(test = False)

    for time in range(10000):
        for i in range(len(robots)):
            x, y, dx, dy = robots[i]
            robots[i][0] = (x+dx) % W
            robots[i][1] = (y+dy) % H

        points = set()
        for x, y, _, _ in robots:
            points.add((x, y))

        good = True
        closes = 0
        for x, y in points:
            for x2, y2 in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if (x2,y2) in points:
                    closes += 1
                    break
        if closes > len(points) // 2:
            print(time+1)
            draw(robots, W, H)
            break

