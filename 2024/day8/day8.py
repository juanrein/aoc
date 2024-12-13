import os
import re
from collections import Counter, defaultdict
import datetime


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    antennas = defaultdict(list)

    cs = set()

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            c = lines[i][j]
            cs.add(c)
            if c != ".":
                antennas[c].append((i, j))

    return antennas, lines


antennas, lines = parse_input()

result = set()

R = len(lines)
C = len(lines[0])

for c, positions in antennas.items():
    for i in range(len(positions)):
        for j in range(len(positions)):
            if i == j:
                continue
            i2, j2 = positions[i]
            i3, j3 = positions[j]

            multiplier = 1
            while True:
                ni, nj = i2 + multiplier * (i3-i2), j2 + multiplier*(j3-j2)
                if ni < R and ni >= 0 and nj < C and nj >= 0:
                    result.add((ni, nj))
                else:
                    break
                multiplier += 1

            multiplier = 1
            while True:
                ni2, nj2 = i3 + multiplier * (i2-i3), j3 + multiplier * (j2-j3)
                if ni2 < R and ni2 >= 0 and nj2 < C and nj2 >= 0:
                    result.add((ni2, nj2))
                else:
                    break
                multiplier += 1

print(len(result))
