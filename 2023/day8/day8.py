import os
from collections import defaultdict
import re
from itertools import cycle
import math

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    moves = lines[0]
    
    grid = defaultdict(list)
    for i in range(2, len(lines)):
        m = re.fullmatch("(?P<src>\w+) = \((?P<left>\w+), (?P<right>\w+)\)", lines[i])
        if m:
            src = m.group("src")
            left = m.group("left")
            right = m.group("right")

        grid[src].append(left)
        grid[src].append(right)

    return moves, grid

def part1():
    moves, grid = parse_input()

    nextMove = cycle(moves)

    current = "AAA"

    totalMoves = 0
    while True:
        move = next(nextMove)

        match move:
            case "L":
                current = grid[current][0]
                totalMoves += 1
            case "R":
                current = grid[current][1]
                totalMoves += 1

        if current == "ZZZ":
            break

    print(totalMoves)
        


def part2():
    moves, grid = parse_input()

    nextMove = cycle(moves)

    currentNodes = []
    for n in grid:
        if n[2] == "A":
            currentNodes.append(n)

    totalMoves = 0

    print(currentNodes)

    cycles = []

    for c in currentNodes:
        current = c

        totalMoves = 0
        while True:
            move = next(nextMove)

            match move:
                case "L":
                    current = grid[current][0]
                    totalMoves += 1
                case "R":
                    current = grid[current][1]
                    totalMoves += 1

            if current[2] == "Z":
                break

        print(totalMoves)

        cycles.append(totalMoves)

        
    print(cycles)
    print(math.lcm(*cycles))