import os
from collections import deque


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


def find_connections(grid, i, j):
    def is_possible(move):
        i2, j2 = move
        return i2 >= 0 and i2 < len(grid) and j2 >= 0 and j2 < len(grid[i])
    
    def moves(m):
        return list(filter(is_possible, m))
    
    up = (i-1, j)
    down = (i+1, j)
    left = (i, j-1)
    right = (i, j+1)
    match grid[i][j]:
        case "|":
            return moves([up, down])
        case "-":
            return moves([left, right])
        case "L":
            return moves([up, right])
        case "J":
            return moves([left, up])
        case "7":
            return moves([left, down])
        case "F":
            return moves([down, right])
        case "S":
            return moves([down, up, left, right])
        case _:
            return []            
        
def dfs(grid, si, sj):
    S = [(si, sj)]
    visited = [[False for _ in range(len(grid[si]))] for _ in range(len(grid))]

    while len(S) > 0:
        (i,j) = S.pop()
        if not visited[i][j]:
            visited[i][j] = True
            for ni, nj in find_connections(grid, i, j):
                S.append((ni,nj))
        elif grid[i][j] == "S":
            return visited

def follow_until_meet(grid, s, p1, p2):
    steps = 0
    visited = [[False for _ in range(len(grid[i]))] for i in range(len(grid))]

    visited[p1[0]][p1[1]] = True
    visited[p2[0]][p2[1]] = True
    visited[s[0]][s[1]] = True

    while True:
        p1 = list(filter(lambda x: not visited[x[0]][x[1]], find_connections(grid, p1[0], p1[1])))[0]
        p2 = list(filter(lambda x: not visited[x[0]][x[1]], find_connections(grid, p2[0], p2[1])))[0]
        visited[p1[0]][p1[1]] = True
        visited[p2[0]][p2[1]] = True

        if p1 == p2:
            return steps
        steps += 1

def part1():
    grid, starting_point = parse_input()

    (i,j) = starting_point

    visited = dfs(grid, i, j)

    paths = []
    if i-1 >= 0 and visited[i-1][j] and starting_point in find_connections(grid, i-1, j):
        paths.append((i-1, j))
    if i+1 < len(grid) and visited[i+1][j] and starting_point in find_connections(grid, i+1, j):
        paths.append((i+1, j))
    if j+1 < len(grid[i]) and visited[i][j+1] and starting_point in find_connections(grid, i, j+1):
        paths.append((i, j+1))
    if j-1 >= 0 and visited[i][j-1] and starting_point in find_connections(grid, i, j-1):
        paths.append((i, j-1))

    p1 = paths[0]
    p2 = paths[1]

    steps = 2 + follow_until_meet(grid, starting_point, p1, p2)
    print(steps)

def start_con(grid, starting_point):
    paths = []
    (i,j) = starting_point
    visited = dfs(grid, i, j)
    
    if i-1 >= 0 and visited[i-1][j] and starting_point in find_connections(grid, i-1, j):
        paths.append((i-1, j))
    if i+1 < len(grid) and visited[i+1][j] and starting_point in find_connections(grid, i+1, j):
        paths.append((i+1, j))
    if j+1 < len(grid[i]) and visited[i][j+1] and starting_point in find_connections(grid, i, j+1):
        paths.append((i, j+1))
    if j-1 >= 0 and visited[i][j-1] and starting_point in find_connections(grid, i, j-1):
        paths.append((i, j-1))

    p1 = paths[0]
    p2 = paths[1]

    p1i,p1j = p1

    # TODO: figure out how to decide between p1 and p2
    return p1

def where_to_look(starting_point, p1):
    i,j = starting_point
    i2, j2 = p1

    if i < i2:
        return [(i, j-1), (i+1, j-1)]
    if i2 < i:
        return [(i, j+1)]
    if j < j2:
        return [(i+1, j)]
    if j2 < j:
        return [(i-1, j)]

def get_con(i,j, starting_point, grid, visited):
    if (i,j) == starting_point:
        return start_con(grid, starting_point)
    else:
        for ni, nj in find_connections(grid, i, j):
            if not visited[ni][nj]:
                return ni, nj

def find_path(grid, starting_point):
    visited = [[False for _ in range(len(grid[i]))] for i in range(len(grid))]

    path = [starting_point]
    visited[starting_point[0]][starting_point[1]]= True
    
    current = get_con(starting_point[0], starting_point[1], starting_point, grid, visited)
    while True:
        i,j = current
        path.append(current)
        if not visited[i][j]:
            visited[i][j] = True
            ninj = get_con(i, j, starting_point, grid, visited)
            if ninj is None:
                return path
            ni,nj = ninj

            current = (ni,nj)
        elif grid[i][j] == "S":
            return path



def add_right_side(grid, starting_point):
    outside = [[False for _ in range(len(grid[i]))] for i in range(len(grid))]

    visited = [[False for _ in range(len(grid[i]))] for i in range(len(grid))]

    current = starting_point
    while True:
        i,j = current
        if not visited[i][j]:
            visited[i][j] = True
            ninj = get_con(i, j, starting_point, grid, visited)
            if ninj is None:
                return outside, visited
            ni,nj = ninj
            for outsideI, outsideJ in where_to_look((i,j), (ni,nj)):
                if outsideI >= 0 and outsideJ >= 0 and outsideI < len(outside) and outsideJ < len(outside[i]):
                    outside[outsideI][outsideJ] = True

            current = (ni,nj)
        elif grid[i][j] == "S":
            return outside, visited


def connect_outside(starting_point, grid, outside, loop_nodes, visited):
    Q = deque()

    visited[starting_point[0]][starting_point[1]] = True

    Q.appendleft(starting_point)

    while len(Q) > 0:
        (i,j) = Q.pop()
        outside[i][j] = True
        # moves = [(i-1, j), (i+1, j), (i, j-1), (i,j+1)]
        moves = [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]
        for i2,j2 in moves:
            if i2 >= 0 and j2 >= 0 and i2 < len(grid) and j2 < len(grid[i2]) and not visited[i2][j2] and not loop_nodes[i2][j2]:
                visited[i2][j2] = True
                Q.appendleft((i2, j2))

def print_table(grid, loop_nodes, outside):
    for i in range(len(grid)):
        resr = []
        for j in range(len(grid[i])):
            if not outside[i][j] and not loop_nodes[i][j]:
                resr.append("I")
            if outside[i][j]:
                resr.append("O")
            elif loop_nodes[i][j]:
                resr.append("#")

        print("".join(resr))

def part2():
    grid, starting_point = parse_input()

    outside, loop_nodes = add_right_side(grid, starting_point)

    for i in range(len(outside)):
        for j in range(len(outside[i])):
            if loop_nodes[i][j]:
                outside[i][j] = False

    visited = [[False for _ in range(len(grid[i]))] for i in range(len(grid))]
    for i in range(len(outside)):
        for j in range(len(outside[i])):
            if outside[i][j]:
                connect_outside((i,j), grid, outside, loop_nodes, visited)

    # print_table(grid, loop_nodes, outside)

    count = 0
    loop = 0
    other = 0
    for i in range(len(outside)):
        for j in range(len(outside[i])):
            if not outside[i][j] and not loop_nodes[i][j]:
                count += 1
            elif loop_nodes[i][j]:
                loop += 1
            else:
                other += 1

    print(count, loop, other)

part1()
part2()