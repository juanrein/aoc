import os
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    grid = []
    for line in lines:
        grid.append(list(line))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                return grid, (i,j)


def neighbors(grid, i,j):
    n = []
    for ni,nj in [(i-1, j), (i+1,j), (i,j-1), (i,j+1)]:
        if ni >= 0 and nj >= 0 and ni < len(grid) and nj < len(grid[i]) and grid[ni][nj] != "#":
            n.append((ni,nj))
    return n

def move(grid, positions):
    nextPositions = set()
    for i,j in positions:
        for ni,nj in neighbors(grid, i,j):
            nextPositions.add((ni,nj))

    return nextPositions

def part1():    
    grid, start = parse_input()

    positions = set[tuple[int,int]]()
    positions.add(start)

    for _ in range(64):
        positions = move(grid, positions)

    print(len(positions))

def neighbors2(grid, i,j):
    n = []
    N = len(grid)
    M = len(grid[i % N])
    for ni,nj in [(i-1, j), (i+1,j), (i,j-1), (i,j+1)]:
        if grid[ni % N][nj % M] != "#":
            n.append((ni,nj))
    return n

def move2(grid, positions):
    nextPositions = set()
    for i,j in positions:
        for ni,nj in neighbors2(grid, i,j):
            nextPositions.add((ni,nj))

    return nextPositions



def draw_positions(grid, positions):
    imin = min(positions, key=lambda x: x[0])[0]
    imax = max(positions, key=lambda x: x[0])[0]
    jmin = min(positions, key=lambda x: x[1])[1]
    jmax = max(positions, key=lambda x: x[1])[1]

    N = len(grid)
    M = len(grid[0])
    for i in range(imin, imax+1):
        row = []
        for j in range(jmin, jmax+1):
            if (i,j) in positions:
                row.append("O")
            else:
                row.append(grid[i % N][j % M])
        print("".join(row))

def plot(data, data2 = None):
    fix,ax = plt.subplots()
    ax.plot(range(1, len(data)+1), data, c="blue")
    if data2:
        ax.plot(range(1, len(data2)+1), data2, c="red")
        
    plt.show()

def diff(arr):
    return [arr[i] - arr[i-1] for i in range(1, len(arr))]

def fit_quadratic(seq):
    twoa = diff(diff(seq))

    u1 = seq[0]
    u2 = seq[1]

    a = twoa[0] // 2
    b = u2 - u1 - 3 * a
    c = u1 - a - b

    return a,b,c


# a,b,c = fit_quadratic(moves)
# f = lambda x: a * x**2 + b * x + c


grid, start = parse_input()

positions = set[tuple[int,int]]()
positions.add((start[0], start[1]))

limit = len(grid) * 2 + 65
moves = []

for i in range(limit):
    positions = move2(grid, positions)
    moves.append(len(positions))
    # if i == 64:
    #    draw_positions(grid, positions)

# print(a,b,c)
# y = [f(x) for x in range(1, len(moves)+1)]

# plot(moves, y)

# plot(diff(diff(moves)))

# plot(moves)
print(len(grid))
x = [65, 65 + len(grid), 65 + len(grid) * 2]
y = [moves[64], moves[64 + len(grid)], moves[64 + len(grid) * 2]]


print(x, y)

n_steps = 26501365

a,b,c = np.polyfit(list(range(1, len(moves)+1)), moves, 2)
print(a * n_steps ** 2 + b * n_steps + c)

# plot([a * x ** 2 + b * x + c for x in range(1,limit+1)], moves)

a,b,c = np.polyfit(x, y, 2)

val = n_steps // len(grid)

print(a * val ** 2 + b * val + c)

a,b,c = fit_quadratic(y)

print(a * val ** 2 + b * val + c)

goal = 26501365
def f(n):
    a0 = 3778
    a1 = 33833
    a2 = 93864

    b0 = a0
    b1 = a1-a0
    b2 = a2-a1
    return b0 + b1*n + (n*(n-1)//2)*(b2-b1)

print(f(goal//len(grid)))
