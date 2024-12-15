import os
import re
from collections import Counter, defaultdict, deque
import datetime
from functools import cache
import numpy as np
from sympy import symbols, solve
import math
import copy


def parse_input(test):
    file = "testinput.txt" if test else "input.txt"
    with open(os.path.join(os.path.dirname(__file__), file)) as f:
        lines = f.read().splitlines()

    i = 0
    grid = []
    while len(lines[i]) > 0:
        grid.append([c for c in lines[i]])
        i += 1

    i += 1

    commands = ""
    while i < len(lines):
        commands += lines[i]
        i += 1

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "@":
                start = (i, j)
                break

    return grid, commands, start


def move(grid, i, j, di, dj):
    ni, nj = i+di, j+dj
    if grid[ni][nj] == "#":
        return False
    if grid[ni][nj] == "O":
        if move(grid, ni, nj, di, dj):
            grid[ni][nj] = grid[i][j]
            grid[i][j] = "."
            return True
        return False
    if grid[ni][nj] == ".":
        grid[ni][nj] = grid[i][j]
        grid[i][j] = "."
        return True

    raise ValueError("what")


def part1():
    grid, commands, start = parse_input(True)

    dir = {
        "<": (0, -1),
        ">": (0, 1),
        "^": (-1, 0),
        "v": (1, -0)
    }

    posi = start[0]
    posj = start[1]

    for command in commands:
        di, dj = dir[command]
        if move(grid, posi, posj, di, dj):
            posi += di
            posj += dj

    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "O":
                result += i * 100 + j

    print(result)


def move2(grid, si, sj, di, dj):
    gridcopy = copy.deepcopy(grid)

    stack = [(si+di, sj+dj, grid[si][sj])]
    grid[si][sj] = "."
    while len(stack) > 0:
        i, j, c = stack.pop()
        ni,nj = i+di, j+dj
        nc = grid[i][j]
        if nc == "#":
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    grid[i][j] = gridcopy[i][j]

            return False
        grid[i][j] = c
        if nc == "[" and dj == 0:
            stack.append((ni,nj,"["))
            stack.append((ni,nj+1,"]"))
            grid[i][j+1] = "."
        elif nc == "]" and dj == 0:
            stack.append((ni,nj-1, "[")) 
            stack.append((ni,nj, "]"))
            grid[i][j-1] = "."           
        elif nc == "[" or nc == "]":
            stack.append((ni,nj,nc))

    return True

def part2():
    grid, commands, start = parse_input(False)

    dir = {
        "<": (0, -1),
        ">": (0, 1),
        "^": (-1, 0),
        "v": (1, -0)
    }

    grid2 = []

    for i in range(len(grid)):
        row = []
        for j in range(len(grid[i])):
            c = grid[i][j]
            if c == "#":
                row.append("#")
                row.append("#")
            elif c == "O":
                row.append("[")
                row.append("]")
            elif c == ".":
                row.append(".")
                row.append(".")
            elif c == "@":
                row.append("@")
                row.append(".")
            else:
                raise ValueError("no")

        grid2.append(row)

    grid = grid2

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "@":
                start = (i, j)
                break

    posi = start[0]
    posj = start[1]

    for command in commands:
        di, dj = dir[command]
        if move2(grid, posi, posj, di, dj):
            posi += di
            posj += dj

    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "[":
                result += i * 100 + j

    print(result)
