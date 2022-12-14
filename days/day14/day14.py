import os

def getTestInput():
    return [
        "498,4 -> 498,6 -> 496,6",
        "503,4 -> 502,4 -> 502,9 -> 494,9"
    ]


def getInput():
    fileName = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(fileName) as f:
        lines = f.read().splitlines()
    # lines = getTestInput()
    rows = []

    for line in lines:
        nums = list(
            map(lambda x: list(map(int, x.split(","))), line.split(" -> ")))
        rows.append(nums)

    return rows


def setGrid(grid, xp, yp, x, y):
    if xp == x:
        if yp <= y:
            for i in range(yp, y+1):
                grid[(i, x)] = "#"
        else:
            for i in range(y, yp+1):
                grid[(i, x)] = "#"
    elif yp == y:
        if xp < x:
            for i in range(xp, x+1):
                grid[(y, i)] = "#"
        else:
            for i in range(x, xp+1):
                grid[(y, i)] = "#"

def makeGrid(data):
    grid = {}
    for rockFormation in data:
        for i in range(1, len(rockFormation)):
            xp, yp = rockFormation[i-1]
            x, y = rockFormation[i]
            setGrid(grid, xp, yp, x, y)

    return grid

def printGrid(grid):
    f = open(os.path.join(os.path.dirname(__file__), "test.txt"), mode="w+")
    
    vals = grid.keys()
    minx = min(vals, key=lambda x: x[1])[1]
    maxx = max(vals, key=lambda x: x[1])[1]
    miny = min(vals, key=lambda x: x[0])[0]
    maxy = max(vals, key=lambda x: x[0])[0]
    for i in range(min(0, miny), maxy+1):
        printt = []
        for j in range(minx, maxx+1):
            printt.append(grid.get((i,j), "."))
        f.write("".join(printt) + "\n")

    f.close()

def hasRockUnder(grid, start):
    sy, sx = start
    for (y,x), _ in grid.items():
        if x == sx and y > sy:
            return True
    return False

def intersectsWithFloor(start, maxy):
    sy,_ = start
    return maxy+2 == sy

def dropSand(grid, start, maxy, source):
    sy,sx = start
    # dropped to void
    # if sx not in voidMap or voidMap[sx] > sx:
    #     return False #didn't stop moving
    # if not hasRockUnder(grid, start):
    #     return False
    moves = [(sx, sy+1), (sx-1, sy+1), (sx+1, sy+1)]
    nStart = (None, None)
    for x,y in moves:
        existing = grid.get((y,x), None)
        if not existing and not intersectsWithFloor((y,x), maxy):
            nStart = (y,x)   
            break  
    if nStart[0] is not None:
        return dropSand(grid, nStart, maxy, source)
    grid[start] = "o"
    return True #stopped moving
 

def solve(data):
    start = (0, 500)
    grid = makeGrid(data)
    drops = 0
    maxy = max(grid.keys(), key=lambda x: x[0])[0]
    while True:
        drops += 1
        stopped = dropSand(grid, start, maxy, start)
        if start in grid:
            break
        if not stopped:
            break

    printGrid(grid)
    return drops



def main():
    data = getInput()
    res = solve(data)
    print(res)

main()
