import os
import math
from collections import deque

def parse_input(part2):
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    grid = []
    galaxyId = 1

    for line in lines:
        row = []
        for c in line:
            if c == "#":
                row.append(galaxyId)
                galaxyId += 1
            else:
                row.append(c)

        grid.append(row)

    if not part2:
        result = []

        # multiply empty rows
        for row in grid:
            if all(c == "." for c in row):
                result.append(row)
                result.append(row[:])
            else:
                result.append(row)

        expandableCols = []
        for j in range(len(grid[0])):
            if all(grid[i][j] == "." for i in range(len(grid))):
                expandableCols.append(j)

        res = []
        for i in range(len(result)):
            row = []
            for j in range(len(result[i])):
                if j in expandableCols:
                    row.append(".")
                    row.append(".")
                else:
                    row.append(result[i][j])
        
            res.append(row)
    else:
        res = grid

    galaxyPos = []
    for i in range(len(res)):
        for j in range(len(res[i])):
            if res[i][j] != ".":
                galaxyPos.append((i,j))
    return res, galaxyPos


def find_distances(grid, start):
    """
    bfs
    """
    Q = deque()

    si, sj = start
    visited = [[False for _ in range(len(grid[i]))] for i in range(len(grid))]
    distances = [[math.inf for _ in range(len(grid[i]))] for i in range(len(grid))]
    distances[si][sj] = 0
    visited[si][sj] = True
    Q.appendleft(start)

    while len(Q) > 0:
        i,j = Q.pop()
        for i2, j2 in [(i-1, j), (i, j-1), (i, j+1), (i+1, j)]:
            if i2 >= 0 and j2 >= 0 and i2 < len(grid) and j2 < len(grid[i2]):
                if not visited[i2][j2]:
                    visited[i2][j2] = True
                    Q.appendleft((i2, j2))
                    distances[i2][j2] = distances[i][j] + 1

    ds = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != "." and grid[i][j] > grid[si][sj]:
                ds.append(distances[i][j])

    return ds

def part1():
    grid, galaxyPos = parse_input(part2 = False)

    sum_of_lengths = 0

    for pos in galaxyPos:
        distances = find_distances(grid, pos)
        for d in distances:
            sum_of_lengths += d

    print(sum_of_lengths)

def manhattan_distance(i,j, i2, j2):
    return abs(i-i2) + abs(j - j2)



def expand(a, expandableCols, expandableRows, factor):
    ai, aj = a

    ni = 0
    nj = 0
    for i in range(ai):
        if i in expandableRows:
            ni += factor
        else:
            ni += 1
    for j in range(aj):
        if j in expandableCols:
            nj += factor
        else:
            nj += 1

    return ni,nj

def compute_distance(a,b, expandableCols, expandableRows, factor):
    ai, aj = expand(a, expandableCols, expandableRows, factor)
    bi, bj = expand(b, expandableCols, expandableRows, factor)

    return manhattan_distance(ai, aj, bi, bj)

def part2():
    grid, galaxyPos = parse_input(part2 = True)

    expandableCols = []
    for j in range(len(grid[0])):
        if all(grid[i][j] == "." for i in range(len(grid))):
            expandableCols.append(j)

    expandableRows = []

    for i,row in enumerate(grid):
        if all(c == "." for c in row):
            expandableRows.append(i)

    result = 0
    for i in range(len(galaxyPos)):
        for j in range(i+1, len(galaxyPos)):
            d = compute_distance(galaxyPos[i], galaxyPos[j], expandableCols, expandableRows, 1000000)
            result += d

    print(result)

part1()
part2()