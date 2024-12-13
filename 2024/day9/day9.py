import os
import re
from collections import Counter, defaultdict
import datetime


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    return [int(d) for d in lines[0]]


def part1():
    blocks = []

    data = parse_input()

    id = 0
    file = True

    for d in data:
        if file:
            for _ in range(d):
                blocks.append(id)
            id += 1
        else:
            for _ in range(d):
                blocks.append(".")

        file = not file

    i = 0
    j = len(blocks)-1

    while i < j:
        while j >= 0 and blocks[j] == ".":
            j -= 1
        while i < len(blocks) and blocks[i] != ".":
            i += 1

        blocks[i] = blocks[j]
        blocks[j] = "."

    i = 0
    j = len(blocks)-1
    while j >= 0 and blocks[j] == ".":
        j -= 1
    while i < len(blocks) and blocks[i] != ".":
        i += 1

    blocks[i] = blocks[j]
    blocks[j] = "."

    checksum = 0

    id = 0

    for d in blocks:
        if d != ".":
            checksum += d * id
            id += 1

    print(checksum)

def part2():
    data = parse_input()

    blocks = []
    id = 0
    file = True

    for d in data:
        if file:
            blocks.append((d, id))
            id += 1
        else:
            blocks.append((d, "."))

        file = not file

    blockToMove = id-1

    while blockToMove >= 0:
        blockI = len(blocks)-1
        # find next movable block
        while blockI >= 0 and blocks[blockI][1] != blockToMove:
            blockI -= 1
        
        count, num = blocks[blockI]

        # find space
        spaceI = 0
        while spaceI < blockI: 
            while spaceI < blockI and blocks[spaceI][1] != ".":
                spaceI += 1

            if blocks[spaceI][1] != ".":
                spaceI += 1
                continue
            count2 = blocks[spaceI][0]
            if count2 >= count:
                remain = count2 - count
                blocks[blockI] = (count, ".")
                blocks[spaceI] = (count, num)
                if remain > 0:
                    blocks.insert(spaceI+1, (remain, "."))
                break
            spaceI += 1

        blockToMove -= 1

    checksum = 0
    position = 0
    for i in range(len(blocks)):
        count, num = blocks[i]
        for _ in range(count):
            if num != ".":
                checksum += position * num

            position += 1
        
    print(checksum)
