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

    a = int(re.findall("\d+", lines[0])[0])
    b = int(re.findall("\d+", lines[1])[0])
    c = int(re.findall("\d+", lines[2])[0])

    program = [int(d) for d in re.findall("\d+", lines[4])]

    return a, b, c, program


def valCombo(arg, a, b, c):
    if 0 <= arg <= 3:
        return arg
    elif arg == 4:
        return a
    elif arg == 5:
        return b
    elif arg == 6:
        return c
    raise ValueError(arg, a, b, c)


def run(program, a, b, c):
    i = 0

    output = []
    while i+1 < len(program):
        command = program[i]
        arg = program[i+1]

        if command == 0:
            val = valCombo(arg, a, b, c)
            # a = a // (2 ** val)
            a = a >> val
            i += 2
        elif command == 1:
            b = b ^ arg
            i += 2
        elif command == 2:
            b = valCombo(arg, a, b, c) % 8
            i += 2
        elif command == 3:
            if a != 0:
                i = arg
            else:
                i += 2
        elif command == 4:
            b = b ^ c
            i += 2
        elif command == 5:
            output.append(valCombo(arg, a, b, c) % 8)
            i += 2
        elif command == 6:
            val = valCombo(arg, a, b, c)
            # b = a // (2 ** val)
            b = a >> val
            i += 2
        elif command == 7:
            val = valCombo(arg, a, b, c)
            # c = a // (2 ** val)
            c = a >> val
            i += 2

    return ",".join(map(str, output))


def part1():
    a, b, c, program = parse_input(False)

    print(run(program, a, b, c))


def printsItself(program):
    def f(a, b, c, i, programI):
        if programI < 0:
            return a
        if i < 0:
            return f(a, b, c, len(program)-2, programI-1)

        command = program[i]
        arg = program[i+1]
        if command == 0 and arg == 3:
            a = a << 3
            return f(a, b, c, i-2, programI)
        elif command == 1:
            b = b ^ arg
            return f(a, b, c, i-2, programI)
        elif command == 2 and arg == 4:
            for ai in range(8):
                f(a+ai, b, c, i-2, programI)
        elif command == 3 and arg == 0:
            return f(a, b, c, i-2, programI)
        elif command == 4 and arg == 0:
            b = b ^ c
            return f(a, b, c, i-2, programI)
        elif command == 5 and arg == 5:
            for bi in range(8):
                if (b + bi) % 8 == program[programI]:
                    return f(a, b+bi, c, i-2, programI)
        elif command == 7 and arg == 5:
            c = a << b
            return f(a, b, c, i-2, programI)
        else:
            print("hups")

    f(0, 0, 0, len(program)-2, len(program)-1)


def run2(a, b, c):
    res = []
    while a != 0:
        b = a % 8
        b = b ^ 1
        c = a >> b
        b = b ^ c
        a = a >> 3
        b = b ^ 6
        res.append(b % 8)

    return ",".join(map(str, res))


def findA(program, programI, A):
    if programI < 0:
        print(A)
        return True
    for ai in range(8):
        a = A << 3 | ai
        res = []
        while a != 0:
            b = a % 8
            b = b ^ 1
            c = a >> b
            b = b ^ c
            a = a >> 3
            b = b ^ 6
            res.append(b % 8)
        if len(res) > 0 and res[0] == program[programI] and findA(program, programI-1, A << 3 | ai):
            return True

    return False


def part2():
    _, _, _, program = parse_input(False)

    expected = ",".join(map(str, program))
    print(expected)

    print(findA(program, len(program)-1, 0))

part2()

# _, b, c, program = parse_input(False)

# a = printsItself(program)
# print(a)

# res = run(program, a, b, c)
# print(",".join(map(str, program)))
# print(res)
