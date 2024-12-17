import os
import re
from collections import Counter, defaultdict, deque
import datetime
from functools import cache
import numpy as np
from sympy import symbols, solve
import math
import copy
import heapq
import networkx as nx


def parse_input(test):
    file = "testinput.txt" if test else "input.txt"
    with open(os.path.join(os.path.dirname(__file__), file)) as f:
        lines = f.read().splitlines()

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "S":
                start = (i, j)
            if lines[i][j] == "E":
                end = (i, j)

    g = defaultdict(set)
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "#":
                continue
            for i2, j2 in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                if i2 >= 0 and j2 >= 0 and i2 < len(lines) and j2 < len(lines[0]) and lines[i2][j2] != "#":
                    for di2, dj2 in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                        g[(i, j, di2, dj2)].add((i2, j2))

    return g, start, end, lines


def shortest_path(g, start, end):
    dist = defaultdict(int)

    Q = []
    heapq.heappush(Q, (0, start))

    for k, v in g.items():
        dist[k] = math.inf

    dist[start] = 0

    while len(Q) > 0:
        _, u = heapq.heappop(Q)

        i, j, di, dj = u
        for i2, j2 in g[u]:
            di2, dj2 = i2 - i, j2 - j
            v = (i2, j2, di2, dj2)

            d = round(math.sqrt((di2-di)**2 + (dj2-dj)**2))
            score = d * 1000 + 1
            alt = dist[u] + score

            if alt < dist[v]:
                dist[v] = alt
                heapq.heappush(Q, (alt, v))

    result = math.inf
    for k, v in dist.items():
        i, j, di, dj = k
        if (i, j) == end:
            result = min(result, v)

    return result


def part1():
    g, start, end, _ = parse_input(False)

    si, sj = start
    result = shortest_path(g, (si, sj, 0, 1), end)

    print(result)

def part2():
    G = nx.Graph()
    g, start, end, lines = parse_input(False)
    si, sj = start

    for k, v in g.items():
        G.add_node(k)

    for (i, j, di, dj), v in g.items():
        for i2, j2 in v:
            di2, dj2 = i2 - i, j2 - j
            d = round(math.sqrt((di2-di)**2 + (dj2-dj)**2))
            score = d * 1000 + 1
            G.add_edge((i, j, di, dj), (i2, j2, di2, dj2), weight=score)

    ei, ej = end
    steps = set()
    for di, dj in [(-1,0)]: # [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        paths = nx.all_shortest_paths(
            G, (si, sj, 0, 1), (ei, ej, di, dj), weight="weight")

        for path in paths:
            for i, j, _, _ in path:
                steps.add((i, j))


    for i in range(len(lines)):
        s = ""
        for j in range(len(lines[i])):
            if (i, j) in steps:
                s += "O"
            else:
                s += lines[i][j]
        print(s)
    print(len(steps))

part2()