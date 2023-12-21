import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.read().splitlines()

grid = []
for line in lines:
    grid.append(list(line))

U = (-1,0)
D = (1,0)
L = (0,-1)
R = (0,1)
c_to_dir = {
    "F": [D, R],
    "L": [U, R],
    "7": [D, L],
    "J": [U, L],
    "|": [D, U],
    "-": [L, R],
    ".": [],
    "S": [L, R, D, U]
}

def add(a,b):
    i,j = a
    i2,j2 = b
    return i+i2, j+j2


for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == "S":
            start = (i,j)
            break

def v(p):
    i,j = p
    return i >= 0 and j >= 0 and i < len(grid) and j < len(grid[i])


def adjacent(pos):
    i,j = pos
    if v(pos):
        return list(filter(lambda x: v(x),[add(pos, d) for d in c_to_dir[grid[i][j]]]))
    return []

def common(start, a):
    return start in adjacent(add(start, a))

for c,dirs in c_to_dir.items():
    if all(common(start, a) for a in dirs) and c != ".":
        start_symbol = c

start_dirs = c_to_dir[start_symbol][0]

def move(prev,current):
    return list(filter(lambda n: n != prev, adjacent(current)))[0]

prev = start
current = add(start, start_dirs)
path = [start]
while current != start:
    path.append(current)
    n = move(prev, current)
    prev = current
    current = n

path.append(start)

print("path 1", len(path) // 2)

def det(a,b):
    x1,y1 = a
    x2, y2 = b
    return x1 * y2 - y1 * x2


total = 0

interns = 0
for i in range(1, len(path)):
    interns += det(path[i-1], path[i])

print(abs(len(path) // 2 - interns // 2 - 1))