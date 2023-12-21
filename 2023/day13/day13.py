import os

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    i = 0
    grids = []
    grid = []
    while i < len(lines):
        if lines[i] == "":
            grids.append(grid)
            grid = []
        else:
            grid.append(list(lines[i]))
        i += 1

    grids.append(grid)
    return grids


def is_reflection_point(startI, grid):
    i = startI
    j = startI+1
    while i >= 0 and j < len(grid):
        if grid[i] != grid[j]:
            return False
        i-=1
        j+=1

    return True

def is_reflection_point2(startI, grid):
    i = startI
    j = startI+1
    smudgeUsed = False
    while i >= 0 and j < len(grid):
        diff = 0
        for a,b in zip(grid[i], grid[j]):
            if a != b:
                diff += 1
            if diff > 1:
                return False
        if diff:
            if smudgeUsed:
                return False
            smudgeUsed = True
        i-=1
        j+=1
    if not smudgeUsed:
        return False
    return True


def find_above_the_horizontal(grid, part2):
    for i in range(0, len(grid)-1):
        if not part2 and is_reflection_point(i, grid):
            return i+1
        if part2 and is_reflection_point2(i, grid):
            return i+1
        
    return -1

def make_horizontal(grid):
    h = []
    for j in range(len(grid[0])):
        r = []
        for i in range(len(grid)):
            r.append(grid[i][j])

        h.append(r)
    
    return h


def find_left_to_vertical(grid, part2):
    return find_above_the_horizontal(make_horizontal(grid), part2)


def part1():
    result = 0

    for grid in parse_input():
        res = find_left_to_vertical(grid, False)
        if res == -1:
            res = 100 * find_above_the_horizontal(grid, False)
        if res == -1:
            raise ValueError(grid)
        print(res)

        result += res

    print("total", result)


result = 0

for grid in parse_input():
    res = find_left_to_vertical(grid, True)
    if res == -1:
        res = 100 * find_above_the_horizontal(grid, True)
    if res == -1 or res == -100:
        raise ValueError(grid)
    print(res)

    print(res)
    result += res

print("total", result)

