import os
import re

def getTestInput():
    return [
        "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
        "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
        "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
        "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
        "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
        "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
        "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
        "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
        "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
        "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
        "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
        "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
        "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
        "Sensor at x=20, y=1: closest beacon is at x=15, y=3"
    ]
    # return [
    #     "Sensor at x=0, y=0: closest beacon is at x=3, y=0",
    #     "Sensor at x=3, y=-2: closest beacon is at x=3, y=0"
    # ]


def getInput():
    fileName = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(fileName) as f:
        lines = f.read().splitlines()
    pat = re.compile(
        "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    # lines = getTestInput()

    data = []
    for line in lines:
        m = pat.match(line)
        data.append((int(m.group(1)), int(m.group(2)),
                    int(m.group(3)), int(m.group(4))))
    return data


def distance(sx, sy, bx, by):
    return abs(bx-sx) + abs(by-sy)

def occupies(sx, sy, bx, by, row):
    d = distance(sx, sy, bx, by)
    rowd = abs(sy - row)
    if rowd > d:
        return None
    return sx - (d - rowd), sx + (d - rowd)


def nonPossibleInRow(data, row):
    res = 0
    beaconsInRow = set()
    sensorsInRow = set()
    pairs = []
    for sx, sy, bx, by in data:
        ab = occupies(sx, sy, bx, by, row)

        if by == row:
            beaconsInRow.add(bx)
        if sy == row:
            sensorsInRow.add(sy)
        if ab is not None:
            a, b = ab
            # print(ab)
            pairs.append(ab)
            res += b-a+1

    X = set()
    for a,b in pairs:
        for i in range(a,b+1):
            X.add(i)

    return len(X) - len(beaconsInRow) - len(sensorsInRow)


def findHole(pairs, maxV):
    current = 0
    # pairs = sorted(pairs, key=lambda x: x[0])
    pairs.sort(key=lambda x: x[0])
    for a,b in pairs:
        if a <= current <= b:
            current = b

    if current >= maxV:
        return None

    return current+1

def findLocation(data):
    maxV = 4000000
    # maxV = 20
    for row in range(0, maxV+1):
        pairs = []
        for sx, sy, bx, by in data:
            cd = occupies(sx, sy, bx, by, row)
            if cd is not None:
                pairs.append(cd)
        hole = findHole(pairs, maxV)
        if hole:
            return hole, row

def solve(data):
    # res = nonPossibleInRow(data, 2000000)
    # return res
    x,y = findLocation(data)
    print(x,y)
    tuning_freq = x * 4000000 + y
    return tuning_freq

def main():
    data = getInput()
    res = solve(data)
    print(res)


main()
