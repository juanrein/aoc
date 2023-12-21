import os
import heapq

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    grid = []
    for line in lines:
        grid.append(list(map(int, line)))    

    return grid


def moves(i,j, di, dj, least, most):
    # starting pos
    if di == 0 and dj == 0:
        return [
            (i+1, j, 1, 0),
            (i, j+1, 0, 1)
        ]
    # vertical
    if di != 0:
        needMore = abs(di) < least
        noMore = abs(di) >= most
        d = -1 if di < 0 else 1

        if noMore:
            return [
                (i, j+1, 0, 1), # turn
                (i, j-1, 0, -1), # turn
            ]          

        if needMore:
            return [
                (i+d, j, di+d, 0) # continue
            ]

        return [
            (i, j+1, 0, 1), # turn
            (i, j-1, 0, -1), # turn
            (i+d, j, di+d, 0), # continue
        ]
    
    # horizontal
    needMore = abs(dj) < least
    noMore = abs(dj) >= most
    d = -1 if dj < 0 else 1

    if noMore:
        return [
            (i+1, j, 1, 0), # turn
            (i-1, j, -1, 0), # turn
        ]          

    if needMore:
        return [
            (i, j+d, 0, dj+d) # continue
        ]
        
    return [
        (i+1, j, 1, 0), # turn
        (i-1, j, -1, 0), # turn
        (i, j+d, 0, dj+d), # continue
    ]



def traverse(grid, pos: tuple[int, int, int, int], target: tuple[int, int], least, most) -> int | None:
    visited = set()

    Q = []
    Q.append((0,) + pos)

    def valid(move):
        i2, j2, di2, dj2 = move
        return i2 >= 0 and i2 < len(grid) and j2 >= 0 and j2 < len(grid[i2]) 

    while len(Q) > 0:
        heat_loss, i,j,di,dj = heapq.heappop(Q)

        if (i,j) == target and (di >= least or dj >= least):
            return heat_loss
        if (i,j,di,dj) in visited:
            continue

        visited.add((i,j,di,dj))

        for move in moves(i,j, di, dj, least, most):
            i2, j2, di2, dj2 = move
            if valid(move):
                move_heat_loss = grid[i2][j2]
                hl = heat_loss + move_heat_loss

                heapq.heappush(Q, (hl, i2,j2, di2, dj2))

    raise ValueError("err")


def part1():
    grid = parse_input()

    pos = (0,0, 0,0)
    target = (len(grid)-1, len(grid[0])-1)
    hl = traverse(grid, pos, target, 1, 3)

    print("best", hl)


def part2():
    grid = parse_input()

    pos = (0,0, 0,0)
    target = (len(grid)-1, len(grid[0])-1)
    hl = traverse(grid, pos, target, 4, 10)

    print("best", hl)

part1()
part2()