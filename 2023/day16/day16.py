import os
from collections import deque

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    grid = []
    for line in lines:
        grid.append(list(line))

    return grid

class Direction:
    RIGHT = (0,1)
    LEFT = (0,-1)
    UP = (-1,0)
    DOWN = (1,0)

    
Point = tuple[int, int]
Position = tuple[Point, Point]

def add(a,b):
    a1,a2 = a
    b1,b2 = b
    return a1+b1,a2+b2       

def get_adjacent(grid, pos: Point, dirdir: Point):
    c = grid[pos[0]][pos[1]]

    right = add(pos, Direction.RIGHT)
    left = add(pos, Direction.LEFT)
    up = add(pos, Direction.UP)
    down = add(pos, Direction.DOWN)
    same = add(pos, dirdir)

    match (c, dirdir):
        case (".", _) | ("|", Direction.UP) | ("|", Direction.DOWN) | ("-", Direction.LEFT) | ("-", Direction.RIGHT):
            yield (same, dirdir)

        case ("/", Direction.UP) | ("\\", Direction.DOWN):
            yield (right, Direction.RIGHT)
        case ("/", Direction.RIGHT) | ("\\", Direction.LEFT):
            yield (up, Direction.UP)
        case ("/", Direction.DOWN) | ("\\", Direction.UP):
            yield (left, Direction.LEFT)
        case ("/", Direction.LEFT) | ("\\", Direction.RIGHT):
            yield (down, Direction.DOWN)

        case ("|", Direction.LEFT) | ("|", Direction.RIGHT):
            yield (up, Direction.UP)
            yield (down, Direction.DOWN)

        case ("-", Direction.UP) | ("-", Direction.DOWN):
            yield (left, Direction.LEFT) 
            yield (right, Direction.RIGHT)


def traverse(grid: list[list[str]], start: Position):
    Q: deque[Position] = deque()
    visited = set()

    visited.add(start)
    def valid(move: Position):
        (i,j) = move[0]

        return i < len(grid) and j < len(grid[i]) and i >= 0 and j >= 0

    Q.appendleft(start)
    while len(Q) > 0:
        pos, dir = Q.pop()
        for pos2 in get_adjacent(grid, pos, dir):
            if valid(pos2) and not pos2 in visited:
                visited.add(pos2)
                Q.appendleft(pos2)

    return len({(i,j) for ((i,j),_) in visited})


def part1():
    start = ((0,0), Direction.RIGHT)
    grid = parse_input()
    res = traverse(grid, start)
    print(res)

def part2():
    grid = parse_input()
    leftSide = [((i, 0), Direction.RIGHT) for i in range(len(grid))]
    rightSide = [((i, len(grid[0])-1), Direction.LEFT) for i in range(len(grid))]
    upSide = [((0, j), Direction.DOWN) for j in range(len(grid[0]))]
    downSide = [((len(grid)-1, j), Direction.UP) for j in range(len(grid[0]))]

    startPositions = leftSide + rightSide + upSide + downSide

    bestRes = 0
    for startPos in startPositions:
        res = traverse(grid, startPos)
        bestRes = max(res, bestRes)

    print(bestRes)

part1()
part2()