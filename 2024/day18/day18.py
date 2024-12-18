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

    points = []
    for line in lines:
        x = line.split(",")
        points.append((int(x[0]), int(x[1])))

    if test:
        return points, 0, 6

    return points, 0, 70



def bfs(grid, start, end):
    Q = deque()
    visited = set()

    visited.add(start)
    Q.appendleft(start)

    prev = {}

    while len(Q) > 0:
        i, j = Q.pop()

        if (i,j) == end:
            current = i,j
            path = []

            while current != start:
                path.append(current)
                current = prev[current]
            path.append(start)
            return path

        for i2, j2 in [(i-1, j), (i+1, j), (i, j+1), (i, j-1)]:
            if i2 < 0 or j2 < 0 or i2 >= len(grid) or j2 >= len(grid[0]):
                continue
            if (i2, j2) in visited:
                continue
            if grid[i2][j2] != ".":
                continue

            visited.add((i2,j2))
            Q.appendleft((i2,j2))
            prev[(i2,j2)] = (i,j)


def part1():
    points, low, high = parse_input(False)

    grid = [["." for j in range(high+1)] for i in range(high+1)]
    for x, y in points[:1024]:
        grid[y][x] = "#"

    path = bfs(grid, (low, low), (high, high))

    for y,x in path:
        grid[y][x] = "O"

    print("\n".join(map(lambda x: "".join(x), grid)))

    print(len(path)-1)


def part2():
    points, low, high = parse_input(False)

    grid = [["." for j in range(high+1)] for i in range(high+1)]
    for i in range(len(points)):
        x,y = points[i]
        grid[y][x] = "#"

        path = bfs(grid, (low, low), (high, high))

        if not path:
            print(points[i])
            break
