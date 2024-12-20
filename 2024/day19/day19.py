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

    towels = set([s for s in lines[0].split(", ")])

    longestPattern = 0
    for towel in towels:
        longestPattern = max(len(towel), longestPattern)

    return towels, lines[2:], longestPattern


def possible(design, towels, i, maxLength):
    if i >= len(design)-1:
        return True
    for j in range(i+1, min(i+1+maxLength, len(design)+1)):
        if design[i:j] in towels and possible(design, towels, j, maxLength):
            return True
        
    return False

def part1():
    towels, designs, longest = parse_input(False)

    total = 0

    for design in designs:
        if possible(design, towels, 0, longest):
            total += 1

    print(total)

def allways(design, towels, maxLength):
    @cache
    def innerAllways(i):
        if i >= len(design):
            return 1
        ways = 0
        for j in range(i+1, min(i+1+maxLength, len(design)+1)):
            if design[i:j] in towels:
                ways += innerAllways(j) 

        return ways

    return innerAllways(0)

def part2():
    towels, designs, longest = parse_input(False)

    total = 0

    for design in designs:
        subtotal = allways(design, towels, longest)
        total += subtotal

    print(total)

