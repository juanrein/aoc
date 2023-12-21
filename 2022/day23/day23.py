from getinput import getInput
import itertools

Point = tuple[int, int]


def move(elves: set[Point], moveds: list[list[Point]], allD: list[Point]):
    # y,x -> [elf1, elf2,...]

    proposals: dict[Point, list[Point]] = {}
    for y, x in elves:
        # all adjacents are empty so no movement
        if all((y+dy, x+dx) not in elves for dy, dx in allD):
            continue
        # consider moving
        for moved in moveds:
            if all((y+dy, x+dx) not in elves for dy, dx in moved):
                dy,dx = moved[1]
                ny,nx = y+dy,x+dx
                if (ny, nx) not in proposals:
                    proposals[(ny, nx)] = []
                proposals[(ny, nx)].append((y, x))
                break

    # if none moved
    if len(proposals) == 0:
        return True

    for (ny, nx), pElves in proposals.items():
        if len(pElves) == 1:
            y, x = pElves[0]
            elves.remove((y, x))
            elves.add((ny, nx))

    return False


def getArea(elves):
    minCol = min([x for y, x in elves])
    maxCol = max([x for y, x in elves])
    minRow = min([y for y, x in elves])
    maxRow = max([y for y, x in elves])

    return minCol, maxCol, minRow, maxRow


def getEmptyTiles(elves):
    minCol, maxCol, minRow, maxRow = getArea(elves)
    totalTiles = (maxCol - minCol + 1) * (maxRow - minRow + 1)
    return totalTiles - len(elves)


def printElves(elves: set[Point]):
    # TODO: needs to handle negative indices
    minCol, maxCol, minRow, maxRow = getArea(elves)
    grid = [["." for _ in range(maxCol+1)] for _ in range(maxRow+1)]

    for y in range(minRow, maxRow+1):
        for x in range(minCol, maxCol+1):
            if (y, x) in elves:
                grid[y][x] = "#"

    for row in grid:
        print("".join(row))


def solve(test):
    elves = getInput(test)
    nswe = [
        [(-1, -1), (-1, 0), (-1, 1)],
        [(1, -1), (1, 0), (1, 1)],
        [(-1, -1), (0, -1), (1, -1)],
        [(-1, 1), (0, 1), (1, 1)]
    ]
    directions = itertools.cycle([[nswe[i%4] for i in range(j,j+4)] for j in range(4)])
    allD = [(-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0),   (1, 1)
            ]
    # printElves(elves)
    for _ in range(10):
        dir = next(directions)
        move(elves, dir, allD)

    empty = getEmptyTiles(elves)
    return empty

def solve2(test):
    elves = getInput(test)
    nswe = [
        [(-1, -1), (-1, 0), (-1, 1)],
        [(1, -1), (1, 0), (1, 1)],
        [(-1, -1), (0, -1), (1, -1)],
        [(-1, 1), (0, 1), (1, 1)]
    ]
    directions = itertools.cycle([[nswe[i%4] for i in range(j,j+4)] for j in range(4)])
    allD = [(-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0),   (1, 1)
            ]
    rounds = 1
    while True:
        dir = next(directions)
        stopped = move(elves, dir, allD)
        if stopped:
            break
        rounds += 1

    return rounds