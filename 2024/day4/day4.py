import os
import re
from collections import Counter


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    return lines


def search_xmas(grid, i, j):
    pairs = [
        [(i, j), (i, j+1), (i, j+2), (i, j+3)],
        [(i, j), (i, j-1), (i, j-2), (i, j-3)],
        [(i, j), (i+1, j), (i+2, j), (i+3, j)],
        [(i, j), (i-1, j), (i-2, j), (i-3, j)],
        [(i, j), (i+1, j+1), (i+2, j+2), (i+3, j+3)],
        [(i, j), (i-1, j-1), (i-2, j-2), (i-3, j-3)],
        [(i, j), (i+1, j-1), (i+2, j-2), (i+3, j-3)],
        [(i, j), (i-1, j+1), (i-2, j+2), (i-3, j+3)],
    ]

    matches = 0
    for coords in pairs:
        s = ""
        for i2, j2 in coords:
            if i2 >= 0 and j2 >= 0 and i2 < len(grid) and j2 < len(grid[i2]):
                s += grid[i2][j2]
            else:
                break
        if s == "XMAS":
            matches += 1
    return matches


def part1():
    grid = parse_input()
    xmases = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                count = search_xmas(grid, i, j)
                xmases += count

    print(xmases)


def search_xmas2(grid, i, j):
    a = (i-1, j-1), (i, j), (i+1, j+1)
    b = (i-1, j+1), (i, j), (i+1, j-1)

    for points in [a,b]:
        for i2, j2 in points:
            if not (i2 >= 0 and j2 >= 0 and i2 < len(grid) and j2 < len(grid[i2])):
                return False
    mas1 = "".join([grid[i][j] for i,j in a])
    mas2 = "".join([grid[i][j] for i,j in b])
    if (mas1 == "MAS" or mas1 == "SAM") and (mas2 == "MAS" or mas2 == "SAM"):
        return True
    
    return False

grid = parse_input()
xmases = 0
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == "A":
            if search_xmas2(grid, i,j):
                xmases += 1

print(xmases)
