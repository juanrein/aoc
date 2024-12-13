import os
import re
from collections import Counter, defaultdict, deque
import datetime
from functools import cache


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    return lines


grid = parse_input()

seen = set()


def traverse(si, sj):
    Q = deque()

    Q.appendleft((si, sj))

    seen.add((si, sj))

    seenThisTime = set()
    seenThisTime.add((si, sj))

    c = grid[si][sj]

    perimeter = 0
    area = 0
    while len(Q) > 0:
        i, j = Q.pop()
        connected = 0

        for ni, nj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
            if ni < 0 or nj < 0 or ni >= len(grid) or nj >= len(grid[0]):
                continue
            if grid[ni][nj] == c:
                connected += 1
            if grid[ni][nj] == c and (ni, nj) not in seen:
                seen.add((ni, nj))
                seenThisTime.add((ni, nj))
                Q.appendleft((ni, nj))

        perimeter += 4 - connected
        area += 1

    return perimeter, area, seenThisTime


def part1():
    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) not in seen:
                perimeter, area, _ = traverse(i, j)
                result += perimeter * area

    print(result)


class UnionFind:
    def __init__(self, numOfElements):
        self.parent = self.makeSet(numOfElements)
        self.size = [1]*numOfElements
        self.count = numOfElements

    def makeSet(self, numOfElements):
        return [x for x in range(numOfElements)]

    # Time: O(logn) | Space: O(1)
    def find(self, node):
        while node != self.parent[node]:
            # path compression
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    # Time: O(1) | Space: O(1)
    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        # already in the same set
        if root1 == root2:
            return

        if self.size[root1] > self.size[root2]:
            self.parent[root2] = root1
            self.size[root1] += 1
        else:
            self.parent[root1] = root2
            self.size[root2] += 1

        self.count -= 1


def comp_perimeter(points):
    facets = []
    for i, j in points:
        for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            ni, nj = i+di, j+dj
            if ni >= 0 and nj >= 0 and ni < len(grid) and nj < len(grid[0]) and grid[ni][nj] == grid[i][j]:
                continue
            facets.append((di, dj, i, j))

    uf = UnionFind(len(facets))

    for facetsI in range(len(facets)):
        for facetsI2 in range(len(facets)):
            di,dj,i,j = facets[facetsI]
            di2,dj2,i2,j2 = facets[facetsI2]

            if (di, dj, i, j) == (di2, dj2, i2, j2):
                continue
            if (di, dj) != (di2, dj2):
                continue
            if i == i2+1 and j == j2 or i == i2-1 and j == j2 or i == i2 and j == j2+1 or i == i2 and j == j2-1:
                uf.union(facetsI, facetsI2)

    return uf.count


result = 0
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if (i, j) not in seen:
            _, area, points = traverse(i, j)
            perimeter = comp_perimeter(points)
            result += perimeter * area

print(result)
