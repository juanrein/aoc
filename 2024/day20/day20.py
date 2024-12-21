import os
import re
from collections import Counter, defaultdict, deque
import datetime
from functools import cache
import numpy as np
from sympy import symbols, solve
import math
import copy
import heapq
import networkx as nx


def parse_input(test):
    file = "testinput.txt" if test else "input.txt"
    with open(os.path.join(os.path.dirname(__file__), file)) as f:
        lines = f.read().splitlines()

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "S":
                start = (i, j)
            if lines[i][j] == "E":
                end = (i, j)
    return lines, start, end


def draw(grid):
    print("\n".join(["".join(row) for row in grid]))


def traverse(grid, start, end, removed):
    Q = deque()
    visited = set()
    visited.add(start)
    Q.appendleft(start)
    prev = {}

    while len(Q) > 0:
        cur = Q.pop()
        if cur == end:
            path = []
            while cur in prev:
                path.append(cur)
                cur = prev[cur]
            path.append(cur)
            return path

        i, j = cur
        for i2, j2 in [(i-1, j), (i+1, j), (i, j+1), (i, j-1)]:
            if i2 < 0 or j2 < 0 or i2 >= len(grid) or j2 >= len(grid[0]):
                continue
            if (i2, j2) in visited:
                continue

            if grid[i2][j2] == "#" and (i2, j2) not in removed:
                continue
            visited.add((i2, j2))
            Q.appendleft((i2, j2))
            prev[(i2, j2)] = (i, j)


def part1():
    grid, start, end = parse_input(False)

    removable = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != "#":
                continue
            removable.add(((i, j),))
            """ for i2, j2 in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                if i2 < 0 or j2 < 0 or i2 >= len(grid) or j2 >= len(grid[0]):
                    continue
                if grid[i2][j2] == "#":
                    if ((i2, j2), (i, j)) not in removable:
                        removable.add(((i, j), (i2, j2))) """

    shortestLegitPath = traverse(grid, start, end, ())

    savings = defaultdict(int)
    total = 0
    for removed in removable:
        path = traverse(grid, start, end, removed)
        if len(shortestLegitPath) > len(path):
            savings[len(shortestLegitPath) - len(path)] += 1
            # print("saved", len(shortestLegitPath) - len(path))

        if len(shortestLegitPath) - len(path) >= 100:
            total += 1

    print(total)


def distance(i, j, i2, j2):
    return abs(i-i2) + abs(j-j2)

def part2():
    grid, start, end = parse_input(False)

    pathThroughMaze = traverse(grid, start, end, ())
    pathThroughMaze = list(reversed(pathThroughMaze))

    total = 0
    for pathI in range(len(pathThroughMaze)):
        for pathJ in range(pathI+1, len(pathThroughMaze)):
            i, j = pathThroughMaze[pathI]
            i2, j2 = pathThroughMaze[pathJ]
            d = distance(i, j, i2, j2)
            if 1 < d <= 20:
                savings = pathJ-pathI - d
                if savings >= 100:
                    total += 1

    print(total)
