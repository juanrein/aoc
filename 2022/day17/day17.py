from pathlib import Path
from itertools import cycle
from dataclasses import dataclass


@dataclass
class Cycler:
    items: list
    i: int = 0

    def next(self):
        current = self.items[self.i]
        self.i = (self.i + 1) % len(self.items)
        return current


def getrock(x: int, y: int, shape: int):
    if shape == 0:
        return [(x, y), (x+1, y), (x+2, y), (x+3, y)]
    elif shape == 1:
        return [
            (x+1, y+2),
            (x, y+1), (x+1, y+1), (x+2, y+1),
            (x+1, y)]
    elif shape == 2:
        return [
            (x+2, y+2),
            (x+2, y+1),
            (x, y), (x+1, y), (x+2, y),
        ]
    elif shape == 3:
        return [
            (x, y+3),
            (x, y+2),
            (x, y+1),
            (x, y),
        ]
    elif shape == 4:
        return [
            (x, y+1), (x+1, y+1),
            (x, y), (x+1, y),
        ]


def intersects(rock: list[tuple[int, int]], occupied: set[tuple[int, int]]):
    return any((point in occupied) for point in rock) or any(x < 0 or x > 6 for x, _ in rock)


def move(winds: Cycler, rock: list[tuple[int, int]], occupied: set[tuple[int, int]]):
    startI = winds.i
    while True:
        dx = winds.next()
        rockToSide = [(x+dx, y) for x, y in rock]
        if not intersects(rockToSide, occupied):
            rock = rockToSide
        rockDown = [(x, y-1) for x, y in rock]
        if not intersects(rockDown, occupied):
            rock = rockDown
        else:
            break
    endI = winds.i
    return rock, (startI, endI)


def handle(occupied: set[tuple[int, int]], shape: int, winds: Cycler, maxys: list[int], x: int, y: int):
    rock = getrock(x, y, shape)
    rock, (startI, endI) = move(winds, rock, occupied)
    for p in rock:
        occupied.add(p)

    for ax, ay in rock:
        if maxys[ax] < ay:
            maxys[ax] = ay
    endHeight = max([y for _,y in rock])
    endX = min([x for x,_ in rock])
    return startI, endI, y, endHeight, endX


def printObjects(occupied: set[tuple[int, int]]):
    my = max(occupied, key=lambda x: x[1])[1]
    grid = [["." for _ in range(7)] for _ in range(my+1)]
    for x, y in occupied:
        grid[y][x] = "#"

    for row in reversed(grid):
        print("".join(row))



def solve(nRocks: int, test: bool, verbose: bool):
    with open(Path(__file__).parent.joinpath("input.txt")) as f:
        line = f.read().strip()
    if test:
        line = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    winds = Cycler(list(map(lambda x: -1 if x == "<" else 1, line)))
    shapes = Cycler(list(range(5)))

    maxys = [0, 0, 0, 0, 0, 0, 0]
    points = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)}

    plots = []
    prevMinMax = tuple([0 for _ in range(7)])
    for iterI in range(nRocks):
        if verbose:
            printObjects(points)
        shape = shapes.next()
        y = max(maxys) + 4
        x = 2
        startI, endI, startY, endY, endX = handle(points, shape, winds, maxys, x, y)

        maxysmin = min(maxys)
        maxysmax = max(maxys)
        currentMinMax = tuple(
            [(maxy - maxysmin)//(maxysmax - maxysmin) for maxy in maxys])
        plots.append([iterI, startI, endI, startY, endY, prevMinMax, currentMinMax, endX, maxysmax])
        prevMinMax = currentMinMax

    return max(maxys), plots
