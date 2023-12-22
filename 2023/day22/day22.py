import os

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    bricks = []
    for line in lines:
        a,b = line.split("~")
        x,y,z = [int(i) for i in a.split(",")]
        x2,y2,z2 = [int(i) for i in b.split(",")]

        d = abs(x-x2)
        d2 = abs(y-y2)
        d3 = abs(z-z2)

        # print(line, d,d2,d3)
        # only expand to one dim, or one cube
        assert sum(1 if dd > 0 else 0 for dd in [d,d2,d3]) in [0,1]

        if d > 0:
            expand_dim = 0
            expand_amount = d
        elif d2 > 0:
            expand_dim = 1
            expand_amount = d2
        elif d3 > 0:
            expand_dim = 2
            expand_amount = d3
        else:
            expand_dim = 0
            expand_amount = 0

        bricks.append((x,y,z, expand_dim, expand_amount + 1))

    bricks.sort(key=lambda x: x[2])

    return bricks


def touching(occupied, coords):
    res = any((pos in occupied) for pos in coords)
    return res

def get_coords(start, expand_dim, expand_amount):
    points = []
    i,j,k = start

    for d in range(start[expand_dim], start[expand_dim] + expand_amount):
        if expand_dim == 0:
            points.append((d, j,k))
        elif expand_dim == 1:
            points.append((i, d,k))
        elif expand_dim == 2:
            points.append((i, j,d))
        
    return points


def add(occupiedMap, coords, id):
    for c in coords:
        occupiedMap[c] = id

def simulate_to_end():
    bricks = parse_input()

    occupied = {}

    cubes = 0
    for id, (i,j,k, expand_dim, expand_amount) in enumerate(bricks):
        cubes += len(get_coords((i,j,k), expand_dim, expand_amount))
        while k-1 > 0 and not touching(occupied, get_coords((i,j,k-1), expand_dim, expand_amount)):
            k -= 1
        coords = get_coords((i,j,k), expand_dim, expand_amount)
        add(occupied, coords, id)

    # print(cubes, len(occupied))
    # print(occupied)

    return occupied

def part1():
    occupied = simulate_to_end()

    supporters = {id: set() for id in occupied.values()}
    supportedBy = {id: set() for id in occupied.values()}

    import string

    for point, id in occupied.items():
        i,j,k = point
        id2 = occupied.get((i,j,k+1))
        if id2 is not None and id != id2:
            supporters[id].add(id2)
            supportedBy[id2].add(id)

    # print(supportedBy)
    total = 0
    for k,v in supporters.items():
        # print(string.ascii_letters[k], [string.ascii_letters[i] for i in v])

        if all(len(supportedBy[supported]) > 1 for supported in v):
            # print("voi poistaa", string.ascii_letters[k])
            total += 1

    print(total)

def part2():
    occupied = simulate_to_end()

    supporterToSupporteds = {id: set() for id in occupied.values()}
    supportedToSupporters = {id: set() for id in occupied.values()}

    for point, id in occupied.items():
        i,j,k = point
        id2 = occupied.get((i,j,k+1))
        if id2 is not None and id != id2:
            supporterToSupporteds[id].add(id2)
            supportedToSupporters[id2].add(id)

    # print(supportedBy)

    def traverse(current, collapsed):
        supported = supporterToSupporteds[current]

        collapsed.add(current)

        collapsedSupported = []
        for s in supported:
            if len(supportedToSupporters[s] - collapsed) == 0:
                collapsedSupported.append(s)

        for s in collapsedSupported:
            traverse(s, collapsed)

    total = 0

    for id in supporterToSupporteds:
        collapsed = set()
        traverse(id, collapsed)
        count = len(collapsed)
        total += count - 1
            

    print(total)
