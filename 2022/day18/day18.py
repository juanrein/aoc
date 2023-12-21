from pathlib import Path
from collections import defaultdict, deque
from itertools import product

def getInput(test):
    if not test:
        with open(Path(__file__).parent.joinpath("input.txt")) as f:
            lines = f.read().splitlines()
    else:
        lines = [
            "2,2,2", #0
            "1,2,2", #1
            "3,2,2", #2
            "2,1,2", #3
            "2,3,2", #4
            "2,2,1", #5
            "2,2,3", #6
            "2,2,4", #7
            "2,2,6", #8
            "1,2,5", #9
            "3,2,5", #10
            "2,1,5", #11
            "2,3,5", #12
        ]
    xyz = []
    for line in lines:
        xyz.append(tuple(map(int,line.split(","))))

    return xyz

def solve(test):
    xyz = getInput(test)

    adjacent = 0
    occupied = set(xyz)
    for x,y,z in xyz:
        neighbors = [
            (x,y,z+1),
            (x,y,z-1),
            (x,y+1,z),
            (x,y-1,z),
            (x+1,y,z),
            (x-1,y,z),
        ]
        for n in neighbors:
            if n in occupied:
                adjacent += 1

    return len(xyz) * 6 - adjacent
 

def bfs(adjacents, start: int, end: int):
    Q = deque()
    Q.append(start)
    visited = set()
    visited.add(start)
    while len(Q) > 0:
        v = Q.popleft()
        if v == end:
            return v
        #doesn't lead anywhere
        if v not in adjacents:
            continue
        for w in adjacents[v]:
            if w not in visited:
                visited.add(w)
                Q.append(w)
    return None

def findAirConnection(xyz, xmin, xmax, ymin, ymax, zmin, zmax):
    """
    Find where air is connected to air or droplet is connected to air
    include one unit of padding
    """
    occupied = set(xyz)
    adjacents = {}
    for x,y,z in product(range(xmin-1, xmax+2), range(ymin-1, ymax+2), range(zmin-1, zmax+2)):
        neighbors = [
            (x,y,z+1),
            (x,y,z-1),
            (x,y+1,z),
            (x,y-1,z),
            (x+1,y,z),
            (x-1,y,z),
        ]
        isEmpty = (x,y,z) not in occupied
        if (x,y,z) not in adjacents:
            adjacents[(x,y,z)] = set()
        for x2,y2,z2 in neighbors:
            #outside the area
            if x2 < xmin-1 or x2 > xmax+1 or y2 < ymin-1 or y2 > ymax+1 or z2 < zmin-1 or z2 > zmax+1:
                continue
            neighborIsEmpty = (x2,y2,z2) not in occupied
            #air to air movement
            if isEmpty and neighborIsEmpty:
                adjacents[(x,y,z)].add((x2,y2,z2))
                if not (x2,y2,z2) in adjacents:
                    adjacents[(x2,y2,z2)] = set()
                adjacents[(x2,y2,z2)].add((x,y,z))
            #droplet to air movement
            elif neighborIsEmpty:
                adjacents[(x,y,z)].add((x2,y2,z2))

    return adjacents


def solve2(test):
    xyz = getInput(test)
    xs = [x for x,_,_ in xyz]
    ys = [y for _,y,_ in xyz]
    zs = [z for _,_,z in xyz]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    zmin, zmax = min(zs), max(zs)

    airConnections = findAirConnection(xyz, xmin, xmax, ymin, ymax, zmin, zmax)
    occupied = set(xyz)
    outsideSides = 0
    cornerPoint = (xmin-1, ymin-1, zmin-1)
    # find which sides of droplets are connected to open air
    for point in airConnections:
        if point not in occupied:
            continue
        for connection in airConnections[point]:
            v = bfs(airConnections, connection, cornerPoint)
            if v is not None:
                outsideSides += 1

    return outsideSides