import os
from functools import lru_cache

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    res = []
    for line in lines:
        ab = line.split()
        x = ab[0], list(map(int, ab[1].split(",")))
        res.append(x)

    return res

def is_valid(springs, broken):
    groups = []
    currentGroup = 0

    for i in range(len(springs)):
        if springs[i] == "#":
            currentGroup += 1
        elif currentGroup > 0:
            groups.append(currentGroup)
            currentGroup = 0

    if currentGroup > 0:
        groups.append(currentGroup)

    return groups == broken

def arrangements(springs: str, broken: list[int]) -> int:
    unknowns = set()
    result = 0
    for i,c in enumerate(springs):
        if c == "?":
            unknowns.add(i)

    for i in range(2**len(unknowns)):
        choices = bin(i)[2:].rjust(len(unknowns), "0")
        choicesI = 0
        possible = ""
        for j in range(len(springs)):
            if j in unknowns:
                possible += ("#" if choices[choicesI] == "0" else ".")
                choicesI += 1
            else:
                possible += springs[j]
        
        valid = is_valid(possible, broken)
        if valid:
            result += 1

    return result

def part1():
    data = parse_input()

    result = 0

    for springs, brokens in data:
        count = arrangements(springs, brokens)
        # print(springs, count)
        result += count

    print("total", result)

def multiply(springs, brokens):
    s = "?".join(springs for _ in range(5))
    b = brokens * 5

    return s, b

@lru_cache()
def arrangements2(springs: str, broken: tuple[int, ...], current: int) -> int:
    if len(springs) == 0:
        if current > 0:
            if len(broken) == 1 and broken[0] == current:
                return 1
        if len(broken) > 0:
            return 0
        return 1
    
    match springs[0]:
        case "?":
            return arrangements2("#" + springs[1:], broken, current) + arrangements2("." + springs[1:], broken, current)
        case ".":
            if current > 0:
                if len(broken) == 0:
                    return 0
                if current != broken[0]:
                    return 0
                return arrangements2(springs[1:], broken[1:], 0)
            return arrangements2(springs[1:], broken, 0)
        case "#":
            if len(broken) == 0:
                return 0
            if broken[0] < current+1:
                return 0
            return arrangements2(springs[1:], broken, current+1)
        case _:
            raise ValueError()


def part2():
    data = parse_input()

    result = 0

    for springs, brokens in data:
        springs, brokens = multiply(springs, brokens)
        count = arrangements2(springs, tuple(brokens), 0)
        # print(springs, count)
        result += count

    print("total", result)

part2()