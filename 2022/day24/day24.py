from getinput import getInput
from collections import deque

Point = tuple[int,int]

def simulateBlizzards(grid: list[list[str]]):
    dirVec = {"v": (1,0),">": (0,1),"<":(0,-1),"^":(-1,0)}
    H = len(grid)
    W = len(grid[0])
    blizzards = set()
    for y in range(H):
        for x in range(W):
            if grid[y][x] in dirVec:
                dy,dx = dirVec[grid[y][x]]
                blizzards.add((y,x,dy,dx))
    initialState = blizzards
    history: list[set[Point]] = []
    while True:
        nextBlizzards = set()
        for y,x,dy,dx in blizzards:
            ny,nx = y+dy,x+dx
            # wrapping but not inside the wall
            if ny == 0:
                ny = H-2
            if ny == H-1:
                ny = 1
            if nx == 0:
                nx = W-2
            if nx == W-1:
                nx = 1
            nextBlizzards.add((ny,nx,dy,dx))

        preserved = set((y,x) for y,x,_,_ in nextBlizzards)
        history.append(preserved)

        if nextBlizzards == initialState:
            return history

        blizzards = nextBlizzards


def printGrid(grid: list[list[str]]):
    for row in grid:
        print("".join(row))

def findPathLength(start: Point, end: Point, history: list[set[Point]], walls: set[Point], initialT: int, W: int, H: int):
    Q = deque()
    #up,down,left,right,wait in place
    moves = [(-1,0),(1,0),(0,-1),(0,1),(0,0)]
    Q.append((start[0],start[1], initialT)) #-1
    best = 100000
    visited = set()
    while len(Q) > 0:
        y,x,t = Q.popleft()
        if (y,x,t) in visited:
            continue
        #can't be better
        if t >= best:
            continue
        visited.add((y,x,t))

        neighbors = []
        for dy,dx in moves:
            yn,xn = y+dy, x+dx
            # if reached target, other moves can't be faster
            if (yn,xn) == end:
                best = min(best, t)
                neighbors = [] # no need to explore others
                break
            # can't be inside wall
            if (yn,xn) in walls:
                continue
            # can't be in blizzard
            if (yn,xn) in history[(t+1) % len(history)]:
                continue

            neighbors.append((yn,xn,t+1))
            
        for n in neighbors:
            Q.append(n)

    return best + 2


def solve(test):
    grid,start,end = getInput(test)

    # each cell can be empty in multiple times in future with different intervals
    # find cells that are never empty
    # if wait too long wind comes
    # maybe possible to find initial heuristic solution

    history = simulateBlizzards(grid)
    W = len(grid[0])
    H = len(grid)

    walls = set()
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "#":
                walls.add((y,x))
    # add wall behind start point so doesn't go out of map
    # probably not neccessary to add wall behind end point
    # as the algorithm should stop at that point
    walls.add((start[0]-1,start[1]))

    res = findPathLength(start, end, history, walls, -1, W, H)
    return res


def solve2(test):
    grid,start,end = getInput(test)

    # each cell can be empty in multiple times in future with different intervals
    # find cells that are never empty
    # if wait too long wind comes
    # maybe possible to find initial heuristic solution

    history = simulateBlizzards(grid)
    W = len(grid[0])
    H = len(grid)

    walls = set()
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "#":
                walls.add((y,x))
    # add wall behind start and end points so doesn't go out of map

    walls.add((start[0]-1,start[1]))
    walls.add((end[0]+1, end[1]))

    t1 = findPathLength(start, end, history, walls, -1, W, H)
    t2 = findPathLength(end, start, history, walls, t1, W, H)
    t3 = findPathLength(start, end, history, walls, t2, W, H)

    print(t1,t2,t3)

    return t3