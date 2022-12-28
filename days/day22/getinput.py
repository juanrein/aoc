from pathlib import Path
import re


def addHorizontalJump(line, jumps, y):
    firstDot = line.find(".")
    firstHash = line.find("#")
    lastDot = line.rfind(".")
    lastHash = line.rfind("#")

    if firstDot != -1 and firstHash != -1:
        start = min(firstDot, firstHash)
    elif firstDot != -1:
        start = firstDot
    elif firstHash != -1:
        start = firstHash
    else:
        raise ValueError(line, firstDot, firstHash)

    if lastDot != -1 and lastHash != -1:
        end = max(lastDot, lastHash)
    elif lastDot != -1:
        end = lastDot
    elif lastHash != -1:
        end = lastHash
    else:
        raise ValueError(lastDot, lastHash)

    # horizontal jumps
    jumps[(y, start-1)] = (y, end)
    jumps[(y, end+1)] = (y, start)


def addVerticalJumps(jumps, nCols, nRows, grid):
    # vertical jumps
    columnMins = []
    columnMaxes = []
    for x in range(nCols):
        for y in range(nRows):
            if grid[y][x] != " ":
                columnMins.append(y-1)
                break
        for y in reversed(range(nRows)):
            if grid[y][x] != " ":
                columnMaxes.append(y+1)
                break

    assert len(columnMins) == len(columnMaxes)
    for x in range(nCols):
        ymin = columnMins[x]
        ymax = columnMaxes[x]
        jumps[(ymin, x)] = (ymax-1, x)
        jumps[(ymax, x)] = (ymin+1, x)


def getPart2Jumps(test):
    if test:
        sides = [
            [(3, x, "top") for x in range(0, 4)],
            [(3, x, "top") for x in range(4, 8)],
            [(-1, x, "top") for x in range(8, 12)],
            [(7, x, "top") for x in range(12, 16)],

            [(8, x, "bottom") for x in range(0, 4)],
            [(8, x, "bottom") for x in range(4, 8)],
            [(12, x, "bottom") for x in range(8, 12)],
            [(12, x, "bottom") for x in range(12, 16)],

            [(y, 7, "left") for y in range(0, 4)],
            [(y, -1, "left") for y in range(4, 8)],
            [(y, 7, "left") for y in range(8, 12)],

            [(y, 12, "right") for y in range(0, 4)],
            [(y, 12, "right") for y in range(4, 8)],
            [(y, 16, "right") for y in range(8, 12)],
        ]
        # True = reversed
        connections = [(0, 2, True), (1, 8, False), (13, 11, True),
                       (10, 5, True), (6, 4, True), (9, 7, True), (12, 3, True)]
    else:
        sides = [
            [(99, x, "top") for x in range(0, 50)],
            [(-1, x, "top") for x in range(50, 100)],
            [(-1, x, "top") for x in range(100, 150)],

            [(200, x, "bottom") for x in range(0, 50)],
            [(150, x, "bottom") for x in range(50, 100)],
            [(50, x, "bottom") for x in range(100, 150)],

            [(y, 49, "left") for y in range(0, 50)],
            [(y, 49, "left") for y in range(50, 100)],
            [(y, -1, "left") for y in range(100, 150)],
            [(y, -1, "left") for y in range(150, 200)],

            [(y, 150, "right") for y in range(0, 50)],
            [(y, 100, "right") for y in range(50, 100)],
            [(y, 100, "right") for y in range(100, 150)],
            [(y, 50, "right") for y in range(150, 200)],
        ]
        # True = reversed
        connections = [(0, 7, False), (13, 4, False), (1, 9, False),
                       (11, 5, False), (6, 8, True), (2, 3, False), (10, 12, True)]
    # when jumped then need to change the position from wall by one to the actual area
    sidemapping = {"top": (1, 0), "bottom": (-1, 0),
                   "left": (0, 1), "right": (0, -1)}
    jumps = {}
    # 0 = right, 1 = down, 2 = left, 3 = up
    facingMapping = {"top": 1, "bottom": 3, "left": 0, "right": 2}
    for i, j, rev in connections:
        if rev:
            sidesJ = reversed(sides[j])
        else:
            sidesJ = sides[j]
        for (y1, x1, side1), (y2, x2, side2) in zip(sides[i], sidesJ):
            dy1, dx1 = sidemapping[side1]
            dy2, dx2 = sidemapping[side2]
            facing1 = facingMapping[side1]
            facing2 = facingMapping[side2]
            jumps[(y1, x1)] = (y2+dy2, x2+dx2, facing2)
            jumps[(y2, x2)] = (y1+dy1, x1+dx1, facing1)

    # print(jumps[(3, 0)])
    # print(jumps[(-1, 11)])
    # print(jumps[(-1,50)])
    return jumps


def buildGrid(mapLines, part2, test):
    nCols = max(len(line) for line in mapLines)
    nRows = len(mapLines)
    grid = [[" " for _ in range(nCols)] for _ in range(nRows)]
    jumps = {}

    for y, line in enumerate(mapLines):
        if not part2:
            addHorizontalJump(line, jumps, y)

        for x, val in enumerate(line):
            grid[y][x] = val

    if not part2:
        addVerticalJumps(jumps, nCols, nRows, grid)
    else:
        jumps = getPart2Jumps(test)

    return grid, jumps


def startPosition(grid: list[list[str]]):
    for i, point in enumerate(grid[0]):
        if point == ".":
            return (0, i)

    raise ValueError("missing start position")


def getInput(test, part2):
    if test:
        with open(Path(__file__).parent.joinpath("testinput.txt")) as f:
            lines = f.read().splitlines()
    else:
        with open(Path(__file__).parent.joinpath("input.txt")) as f:
            lines = f.read().splitlines()
    # add R to beginning to make input full (letter, number) list
    commandLine = "R" + lines[-1]
    # print(commandLine)
    moves = []
    for a, b in re.findall("(L|R)(\d+)", commandLine):
        moves.append((a, int(b)))

    mapLines = lines[:len(lines)-2]

    grid, jumps = buildGrid(mapLines, part2, test)

    start = startPosition(grid)
    return moves, grid, jumps, start

# getPart2Jumps(False)