from getinput import getInput


Point = tuple[int,int]

def turn(facing, direction):
    assert direction == "R" or direction == "L"
    if direction == "R": #clockwise
        return (facing + 1) % 4
    return (facing - 1) % 4

def takeSteps(grid: list[list[str]], jumps: dict[Point,Point], pos: Point, facing: int, amount: int):
    if facing == 0:
        dy = 0
        dx = 1
    elif facing == 1:
        dy = 1
        dx = 0
    elif facing == 2:
        dy = 0
        dx = -1
    elif facing == 3:
        dy = -1
        dx = 0

    y,x = pos
    for _ in range(amount):
        # print(y,x, facing)
        ny,nx = y+dy, x+dx

        if (ny,nx) in jumps:
            jy,jx = jumps[(ny,nx)]
            if grid[jy][jx] != "#":
                y,x = jy,jx
        else:
            if grid[ny][nx] == ".":
                y,x = ny,nx
        
    return (y,x)


def getFinalPos(moves: list[tuple[str, int]], grid: list[list[str]], jumps: dict[Point, Point], start: Point):
    pos = start
    # 0 = right, 1 = down, 2 = left, 3 = up
    facing = 3
    for direction, amount in moves:
        facing = turn(facing, direction)
        pos = takeSteps(grid, jumps, pos, facing, amount)
    # return (5,7,0)
    return pos[0], pos[1], facing

def solve(test):
    moves, grid, jumps, start = getInput(test, False)
    finalRowI, finalColI, finalFacing = getFinalPos(moves, grid, jumps, start)

    print(finalRowI, finalColI, finalFacing)
    password = 1000 * (finalRowI+1) + 4 * (finalColI+1) + finalFacing

    return password

def takeSteps2(grid: list[list[str]], jumps: dict[Point, tuple[int,int,int]], pos: Point, facing: int, amount: int):
    facingToDyDx = {
        0: (0,1),
        1: (1,0),
        2: (0,-1),
        3: (-1,0)
    }

    y,x = pos
    for _ in range(amount):
        # print(y,x, facing)
        dy,dx = facingToDyDx[facing]
        ny,nx = y+dy, x+dx

        if (ny,nx) in jumps:
            jy,jx,jFacing = jumps[(ny,nx)]
            if grid[jy][jx] != "#":
                y,x = jy,jx
                facing = jFacing
        else:
            if grid[ny][nx] == ".":
                y,x = ny,nx
        
    return (y,x), facing


def getFinalPos2(moves: list[tuple[str,int]], grid: list[list[str]], jumps: dict[Point, tuple[int,int,int]], start: Point):
    pos = start
    # 0 = right, 1 = down, 2 = left, 3 = up
    #added R to input so the facing gets changed to 0
    facing = 3
    for direction, amount in moves:
        facing = turn(facing, direction)
        pos,facing = takeSteps2(grid, jumps, pos, facing, amount)
    # return (5,7,0)
    return pos[0], pos[1], facing

def solve2(test):
    moves, grid, jumps, start = getInput(test, True)
    finalRowI, finalColI, finalFacing = getFinalPos2(moves, grid, jumps, start)

    print((finalRowI+1), (finalColI+1), finalFacing)
    password = 1000 * (finalRowI+1) + 4 * (finalColI+1) + finalFacing

    return password
