import os
from dataclasses import dataclass

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

Workflows = dict[str, list[tuple[str, str] | str]]

def parse_input() -> tuple[Workflows, list[Part]]:
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    workflows = {}
    i = 0
    while lines[i] != "":
        k = lines[i].split("{")[0]
        v = lines[i].split("{")[1].strip("}")
        pairs = v.split(",")
        conds: list[tuple[str, str] | str] = []
        for pair in pairs[0:len(pairs)-1]:
            cond = pair.split(":")
            conds.append((cond[0], cond[1]))            

        conds.append(pairs[len(pairs)-1])

        workflows[k] = conds
        i+=1

    i+=1
    parts = []

    while i < len(lines):
        line = lines[i].strip("{}")
        values = []
        for pair in line.split(","):
            ab = pair.split("=")
            values.append(int(ab[1]))
        
        x,m,a,s = values
        parts.append(Part(x,m,a,s))
        i+=1

    return workflows, parts




def accepted(workflows: Workflows, part: Part):
    current = "in"
    while True:
        for pair in workflows[current]:
            match pair:
                case "A":
                    return True
                case "R":
                    return False
                case (cond, nextValue):
                    s = cond.replace("x", str(part.x)).replace("m", str(part.m)).replace("a", str(part.a)).replace("s", str(part.s))
                    if eval(s):
                        current = nextValue
                        if current == "A":
                            return True
                        elif current == "R":
                            return False
                        break
                case last:
                    current = last
                    if current == "A":
                        return True
                    elif current == "R":
                        return False  

def part1():        
    workflows, parts = parse_input()

    total = 0
    for part in parts:
        if accepted(workflows, part):
            s = part.x + part.m + part.a + part.s
            total += s

    print(total)


workflows,_ = parse_input()

def parse_cond(cond):
    d = {
        "x": 0,
        "m": 1,
        "a": 2,
        "s": 3
    }

    cond = [cond[0], cond[1], int(cond[2:])]

    match cond:
        case [op2, ">", int(op)]:
            valsI = d[op2]
            return valsI, op, True
        case [op2, "<", int(op)]:
            valsI = d[op2]
            return valsI, op, False
        case other:
            raise ValueError(other)


def splitRange(p1, cond):
    valI, value, gt = cond

    fail = [p for p in p1]
    accept = [p for p in p1]

    a,b = accept[valI]

    # x > 10
    if gt:
        accept[valI] = value+1, b
        fail[valI] = a, value+1
    # x < 10
    else:
        accept[valI] = a, value
        fail[valI] = value, b

    return accept, fail


finalRanges = []

def evalTree(workflows, ranges, current):
    if current == "A":
        finalRanges.append(ranges)
        return
    elif current == "R":
        return
    for pair in workflows[current]:
        match pair:
            case (cond, nextValue):
                cond = parse_cond(cond)
                accept, fail = splitRange(ranges, cond)
                evalTree(workflows, accept, nextValue)
                ranges = fail
            case last:
                evalTree(workflows, ranges, last)
                return

def part2():
    evalTree(workflows, ((1,4001), (1,4001), (1,4001), (1,4001)), "in")

    print(167409079868000)

    total2 = 0
    for xmas in finalRanges:
        combs = 1
        for a,b in xmas:
            combs *= (b - a)
        total2 += combs

    print(total2)
