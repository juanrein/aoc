import os
import re
from collections import Counter

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    nums = []
    for s in lines:
        matches = re.findall("mul\(\d{1,3},\d{1,3}\)", s)
        for m in matches:
            dot = m.find(",")
            a = m[4:dot]
            b = m[dot+1:len(m)-1]
            nums.append((int(a),int(b)))

    return nums

def part1():
    result = 0
    for a,b in parse_input():
        result += a*b

    print(result)


def parse_input2():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    commands = []
    for s in lines:
        matches = re.findall("mul\(\d{1,3},\d{1,3}\)|don't\(\)|do\(\)", s)
        for m in matches:
            if "mul" in m:
                dot = m.find(",")
                a = m[4:dot]
                b = m[dot+1:len(m)-1]
                commands.append((int(a),int(b)))
            elif "don't" in m:
                commands.append(False)
            elif "do" in m:
                commands.append(True)
            else:
                print(m)

    return commands

def part2():
    result = 0
    run = True

    for command in parse_input2():
        if command is True:
            run = True
        elif command is False:
            run = False
        else:
            if run:
                a,b = command
                result += a * b

    print(result)
