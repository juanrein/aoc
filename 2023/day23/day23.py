import os
from collections import deque, defaultdict

# sys.setrecursionlimit(10000)

with open(os.path.join(os.path.dirname(__file__), "testinput.txt")) as f:
    lines = f.read().splitlines()

grid = []
for line in lines:
    grid.append(list(line))

start = (0,1)

N = len(grid)
M = len(grid[0])
end = (N-1, M-2)


def neighbors(grid, pos, part2):
    i,j = pos
    if part2:
        ds = [(i+1, j), (i-1, j), (i, j-1), (i,j+1)]
    else:        
        match grid[i][j]:
            case "v":
                ds = [(i+1, j)]
            case "<":
                ds = [(i,j-1)]
            case ">":
                ds = [(i,j+1)]
            case "^":
                ds = [(i-1, j)]
            case _:
                ds = [(i+1, j), (i-1, j), (i, j-1), (i,j+1)]
            
    accepted = []
    for ni,nj in ds:
        if ni >= 0 and nj >= 0 and ni < N and nj < M and grid[ni][nj] != "#":
            accepted.append((ni,nj))
    return accepted


""" 
def traverse(grid, start, end, part2):
    def traversef(pos, visited, d):
        visited.add(pos)
        if pos == end:
            return d
        
        best = 0
        for nextPos in neighbors(grid, pos, part2):
            if nextPos in visited:
                continue
            d2 = traversef(nextPos, set(visited), d + 1)
            best = max(d2, best)

        return best

    res = traversef(start, set(), 0)

    return res """

""" 
def traverse(grid, start, end, part2):
    Q = deque()
    Q.appendleft((start, set(), 0))
    best = 0
    while len(Q) > 0:
        pos, visited, d = Q.pop()
        visited.add(pos)
        if pos == end:
            best = max(best, d)
            continue

        for nextPos in neighbors(grid, pos, part2):
            if nextPos in visited:
                continue
            Q.appendleft((nextPos, set(visited), d+1))

    return best """

def simplify(grid):
    g = defaultdict(set)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != "#":
                for n in neighbors(grid, (i,j), True):
                    g[(i,j)].add(n)

    gg = defaultdict(set)
    for u in g:
        for v in g[u]:
            w = 1
            prev = u
            current = v
            while len([ve for ve in g[current] if ve != prev]) == 1:
                next = [ve for ve in g[current] if ve != prev][0]
                prev = current
                current = next
                w += 1
            gg[u].add((current, w))

    return gg

def traverse(graph, start, end):
    Q = deque()
    Q.appendleft((start, set(), 0))
    best = 0
    while len(Q) > 0:
        pos, visited, d = Q.pop()
        visited.add(pos)
        if pos == end:
            best = max(best, d)
            continue

        for nextPos,w in graph[pos]:
            if nextPos in visited:
                continue
            Q.appendleft((nextPos, set(visited), d+w))

    return best

graph = simplify(grid)

print(len(graph))
res = traverse(graph, start, end)
    
print(res)
