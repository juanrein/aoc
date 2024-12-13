import os
import re
from collections import Counter, defaultdict, deque
import datetime
from functools import cache
import numpy as np
from sympy import symbols, solve

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    slots = []
    for i in range(0, len(lines), 4):
        a = tuple([int(d) for d in re.findall("\d+", lines[i])])
        b = tuple([int(d) for d in re.findall("\d+", lines[i+1])])
        prize = tuple([int(d) for d in re.findall("\d+", lines[i+2])])

        slots.append((a, b, prize))

    return slots

def solve1(ax,ay,bx,by,prizex,prizey):
    for a in range(100):
        for b in range(100):
            (posx,posy) = (a*ax+b*bx, a*ay+b*by)
            if posx > prizex or posy > prizey:
                break
            if posx == prizex and posy == prizey:
                return a,b
            
    return None
                

def part1():  
    result = 0

    for (ax,ay),(bx,by),(prizex, prizey) in parse_input():
        solution = solve1(ax,ay,bx,by,prizex,prizey)
        print(solution)
        if solution is not None:
            a,b = solution
            result += a * 3 + b

    print(result)

def part2():
    result = 0

    big = 10000000000000

    for (ax,ay),(bx,by),(prizex, prizey) in parse_input():
        a,b = symbols("a, b")

        prizex = prizex + big
        prizey = prizey + big

        solution = solve([ax*a+bx*b-prizex, a*ay+b*by-prizey], [a,b], dict=True)
        if solution:
            if len(solution) > 1:
                print(len(solution))
            # only integer solutions allowed
            ints = "<class 'sympy.core.numbers.Integer'>"
            if ints == str(type(solution[0][a])) and ints == str(type(solution[0][b])):
                av = int(solution[0][a])
                bv = int(solution[0][b])

                result += 3 * av + bv

    print(result)
