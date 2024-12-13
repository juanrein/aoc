import os
import re
from collections import Counter, defaultdict
import datetime


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    start = None
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "^":
                start = (i, j)
    if start is None:
        print("no start pos")

    return lines, start


def part1():
    grid, startPos = parse_input()

    dir = (-1, 0)

    visited = set()

    pos = startPos

    while True:
        i, j = pos
        di, dj = dir

        visited.add(str(pos))

        ni, nj = i+di, j+dj
        if ni < 0 or nj < 0 or ni >= len(grid) or nj >= len(grid[ni]):
            break

        if grid[ni][nj] == "#":
            if dir == (-1, 0):
                dir = (0, 1)
            elif dir == (1, 0):
                dir = (0, -1)
            elif dir == (0, -1):
                dir = (-1, 0)
            elif dir == (0, 1):
                dir = (1, 0)
            else:
                print("mistake")

            di, dj = dir
            pos = i + di, j + dj
        else:
            pos = i+di, j+dj

    print(len(visited))

    return visited


def part2():
    grid, startPos = parse_input()

    loops = 0

    visitedpart1 = part1()

    for blockI in range(len(grid)):
        for blockJ in range(len(grid[blockI])):
            if grid[blockI][blockJ] != "." or str((blockI, blockJ)) not in visitedpart1:
                continue

            dir = (-1, 0)

            visited = set()

            pos = startPos

            while True:
                i, j = pos
                di, dj = dir

                if pos + dir in visited:
                    loops += 1
                    break

                visited.add(pos + dir)

                ni, nj = (i+di, j+dj)
                if ni < 0 or nj < 0 or ni >= len(grid) or nj >= len(grid[ni]):
                    break

                if grid[ni][nj] == "#" or (ni, nj) == (blockI, blockJ):
                    if dir == (-1, 0):
                        dir = (0, 1)
                    elif dir == (1, 0):
                        dir = (0, -1)
                    elif dir == (0, -1):
                        dir = (-1, 0)
                    elif dir == (0, 1):
                        dir = (1, 0)
                    else:
                        print("mistake")
                else:
                    pos = (i + di, j + dj)


    print(loops)


s = datetime.datetime.now()
part2()
e = datetime.datetime.now()

print(e - s)

