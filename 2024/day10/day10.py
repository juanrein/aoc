import os
import re
from collections import Counter, defaultdict, deque
import datetime


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    grid = []
    for line in lines:
        grid.append([int(d) for d in line])

    return grid


def trailheads(grid, i, j, R, C):
    Q = deque()
    visited = set()
    visited.add((i, j))

    Q.appendleft((i, j))
    count = 0
    while len(Q) > 0:
        i, j = Q.pop()
        if grid[i][j] == 9:
            count += 1
            continue
        for ni, nj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if not (ni < R and ni >= 0 and nj < C and nj >= 0):
                continue
            if grid[i][j] + 1 != grid[ni][nj]:
                continue
            if (ni, nj) not in visited:
                visited.add((ni, nj))
                Q.appendleft((ni, nj))

    return count

def part1():
    grid = parse_input()
    R = len(grid)
    C = len(grid[0])

    total = 0

    for i in range(R):
        for j in range(C):
            if grid[i][j] == 0:
                total += trailheads(grid, i, j, R, C)
    print(total)

def trailheads2(grid, i, j, R, C):
    Q = deque()

    Q.appendleft((i, j))
    count = 0
    while len(Q) > 0:
        i, j = Q.pop()
        if grid[i][j] == 9:
            count += 1
            continue
        for ni, nj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if not (ni < R and ni >= 0 and nj < C and nj >= 0):
                continue
            if grid[i][j] + 1 != grid[ni][nj]:
                continue
            Q.appendleft((ni, nj))

    return count

grid = parse_input()
R = len(grid)
C = len(grid[0])

total = 0

for i in range(R):
    for j in range(C):
        if grid[i][j] == 0:
            total += trailheads2(grid, i, j, R, C)
print(total)
