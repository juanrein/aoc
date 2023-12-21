import os

import copy


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    grid = []
    for line in lines:
        grid.append(list(line))

    return grid


def move_north(grid, i, j):
    while i-1 >= 0 and grid[i-1][j] == ".":
        grid[i-1][j] = "O"
        grid[i][j] = "."
        i-=1

def move_south(grid, i, j):
    while i+1 < len(grid) and grid[i+1][j] == ".":
        grid[i+1][j] = "O"
        grid[i][j] = "."
        i+=1

def move_west(grid, i, j):
    while j-1 >= 0 and grid[i][j-1] == ".":
        grid[i][j-1] = "O"
        grid[i][j] = "."
        j-=1

def move_east(grid, i, j):
    while j+1 < len(grid[0]) and grid[i][j+1] == ".":
        grid[i][j+1] = "O"
        grid[i][j] = "."
        j+=1

def compute_load(grid):
    load = 0
    factor = 1
    for i in range(len(grid)-1, -1, -1):
        load += factor * sum(1 if c == "O" else 0 for c in grid[i])
        factor += 1

    return load

def tilt_north(grid):
    for j in range(len(grid[0])):
        for i in range(len(grid)):
            if grid[i][j] == "O":
                move_north(grid, i, j)

def tilt_south(grid):
    for j in range(len(grid[0])):
        for i in range(len(grid)-1, -1,-1):
            if grid[i][j] == "O":
                move_south(grid, i, j)


def tilt_west(grid):
    for j in range(len(grid[0])):
        for i in range(len(grid)):
            if grid[i][j] == "O":
                move_west(grid, i, j)

def tilt_east(grid):
    for j in range(len(grid[0])-1,-1,-1):
        for i in range(len(grid)):
            if grid[i][j] == "O":
                move_east(grid, i, j)

def part1():
    grid = parse_input()
    tilt_north(grid)
    load = compute_load(grid)
    print(load)





def do_iter(grid):
    tilt_north(grid)

    tilt_west(grid)

    tilt_south(grid)

    tilt_east(grid)


def find_cycle():
    grid = parse_input()

    seen = {}

    cycles = 0

    while str(grid) not in seen:
        seen[str(grid)] = cycles

        do_iter(grid)

        cycles += 1

    return seen[str(grid)], cycles - seen[str(grid)]


def part2():
    offset, cycle = find_cycle()

    grid = parse_input()    

    print(offset, cycle)
    for _ in range(offset):
        do_iter(grid)

    total_cycles = 1000000000 - offset

    remaining_cycles = total_cycles % cycle

    print(remaining_cycles)

    for _ in range(remaining_cycles):
        do_iter(grid)

    print(compute_load(grid))

