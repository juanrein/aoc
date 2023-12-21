import os
import string
import math


def getData():
    heightmap = {c: i for c, i in zip(
        string.ascii_lowercase, range(len(string.ascii_lowercase)))}
    heightmap["S"] = heightmap["a"]
    heightmap["E"] = heightmap["z"]

    fileName = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(fileName) as f:
        lines = f.read().splitlines()

    # lines = [
    #     "Sabqponm",
    #     "abcryxxl",
    #     "accszExk",
    #     "acctuvwj",
    #     "abdefghi"
    # ]
    data = []
    start = None
    for i, line in enumerate(lines):
        row = []
        for j, c in enumerate(line):
            if c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)
            row.append(heightmap[c])

        data.append(row)

    return data, start, end


def isValid(grid, crow, ccol, aval):
    # out of bounds
    if crow < 0 or crow >= len(grid) or ccol < 0 or ccol >= len(grid[0]):
        return False
    cval = grid[crow][ccol]
    # two long leap upwards
    if not (aval <= cval or aval == cval + 1):
        return False

    return True


def makeGraph(grid):
    E = {}
    for arow in range(len(grid)):
        for acol in range(len(grid[arow])):
            moves = [(arow-1, acol), (arow, acol-1),
                     (arow, acol+1), (arow+1, acol)]
            aval = grid[arow][acol]
            allowed = []
            for crow, ccol in moves:
                if isValid(grid, crow, ccol, aval):
                    allowed.append((crow, ccol))
            if len(allowed) > 0:
                E[(arow, acol)] = allowed

    return E


def dijkstra(E, start):
    dist = {}
    Q = []
    for v in E.keys():
        dist[v] = math.inf
        Q.append(v)
    dist[start] = 0

    while len(Q) > 0:
        u = min(Q, key=lambda x: dist[x])
        Q.remove(u)

        for v in Q:
            if v in E[u]:
                alt = dist[u] + 1
                if alt < dist[v]:
                    dist[v] = alt

    return dist


def findStartingPoints(grid):
    startingPoints = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                startingPoints.append((i, j))
    return startingPoints


def solve(grid, start, end):
    E = makeGraph(grid)
    startingPoints = findStartingPoints(grid)
    startingPoints.append(start)
    sols = []
    dist = dijkstra(E, end)
    print(dist)
    for startI in startingPoints:
        if startI in dist:
            sols.append(dist[startI])
    print(sols)
    return min(sols)


def main():
    data, s, e = getData()
    res = solve(data, s, e)
    print(res)


main()
