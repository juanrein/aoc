import os

def parse_input() -> list[list[str]]:
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    grid = []
    for line in lines:
        row = list(line)
        grid.append(row)
    
    return grid


def is_symbol(c: str) -> bool:
    return not c.isdigit() and c != "."

def is_inside(grid, i2, j2):
    return i2 >= 0 and i2 < len(grid) and j2 >= 0 and j2 < len(grid[i2])

def find_num(grid: list[list[str]], i: int, j: int) -> None | tuple[int, int, int]:
    startI = j
    endI = j
    if not grid[i][j].isdigit():
        return None
    
    while startI-1 >= 0 and grid[i][startI-1].isdigit():
        startI -= 1
    while endI + 1 < len(grid[i]) and grid[i][endI+1].isdigit():
        endI += 1

    return i, startI, int("".join(grid[i][startI:endI+1]))
 

def find_adjacent_number_locations(grid: list[list[str]], i: int, j: int) -> list[tuple[int, int, int]]:
    nums = []
    for i2, j2 in [(i-1, j-1), (i-1, j), (i-1, j+1),
                   (i, j-1), (i, j), (i, j+1),
                   (i+1, j-1), (i+1, j), (i+1, j+1)]:
        if is_inside(grid, i2, j2):
            num = find_num(grid, i2, j2)
            if num is not None:
                nums.append(num)

    return nums


def part1():
    grid = parse_input()

    num_locations = {}

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            c = grid[i][j]
            if is_symbol(c):
                locations = find_adjacent_number_locations(grid, i,j)
                for i2, j2, val in locations:
                    k = str(i2) + "," + str(j2)
                    num_locations[k] = val

    result = 0
    for ij, val in num_locations.items():
        result += val

    print(result)

def find_gear(grid: list[list[str]], i: int, j: int) -> None | tuple[int, int]:
    if grid[i][j] != "*":
        return None
    
    nums = find_adjacent_number_locations(grid, i, j)
    
    numsD = {}
    for i2,j2,val in nums:
        k = str(i2) + "," + str(j2)
        numsD[k] = val
    if len(numsD) == 2:
        numsTwo = list(numsD.items())
        return (numsTwo[0][1], numsTwo[1][1])
    
    return None


def part2():
    grid = parse_input()

    result = 0

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            gear = find_gear(grid, i, j)
            if gear is not None:
                result += gear[0] * gear[1]

    print(result)

part2()