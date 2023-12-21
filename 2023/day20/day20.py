import os

from enum import Enum
from dataclasses import dataclass
from collections import defaultdict, deque
import math

class Type(Enum):
    FlipFlop = 1
    Conjunction = 2
    BroadCaster = 3

@dataclass
class Module:
    name: str
    type: Type
    dest: list[str]
    memory: dict[str, int] | None = None

    state: int = 0

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    configuration = {}

    inputs = defaultdict(set)

    for line in lines:
        parts = line.split(" -> ")
        dest = parts[1].split(", ")

        if line.startswith("%"):
            name = parts[0][1:]
            configuration[name] = Module(name, Type.FlipFlop, dest)
        elif line.startswith("&"):
            name = parts[0][1:]
            configuration[name] = Module(name, Type.Conjunction, dest)
        elif line.startswith("broadcaster"):
            name = "broadcaster"
            configuration[name] = Module(name, Type.BroadCaster, dest)
        else:
            print("missing", line)

        for d in dest:
            inputs[d].add(name)

    for name,m in configuration.items():
        if m.type == Type.Conjunction:
            m.memory = {}
            for source in inputs[name]:
                m.memory[source] = 0

    return configuration


def handle_pulse(module: Module, source: str, pulse: int):
    match module.type:
        case Type.Conjunction:
            if module.memory is None:
                raise ValueError()
            module.memory[source] = pulse
            
            count = sum(module.memory.values())
            # all high send low
            if len(module.memory) == count:
                return [(module.name, d, 0) for d in module.dest]
            return [(module.name, d, 1) for d in module.dest]

        case Type.FlipFlop:
            if pulse == 1:
                return []
            module.state = 1 if module.state == 0 else 0
            return [(module.name, d, module.state) for d in module.dest] 
        case Type.BroadCaster:
            return [(module.name, d, pulse) for d in module.dest]                

seen: dict[str, list] = {
    "mz": [], 
    "sh": [], 
    "jf": [], 
    "bh": []
}

def send(configuration: dict[str, Module], iter_i: int):
    n_low = 0
    n_high = 0
    Q = deque[tuple[str, str, int]]()
    Q.appendleft(("button", "broadcaster", 0))

    while len(Q) > 0:
        source, target, value = Q.pop()
        if target == "mf" and source in seen and value == 1:
            seen[source].append(iter_i)

        if value == 0:
            n_low += 1
        else:
            n_high += 1

        if target not in configuration:
            continue
        m = configuration[target]
        for n in handle_pulse(m, source, value):
            Q.appendleft(n)


    return n_low, n_high


def part1():
    configuration = parse_input()

    total_low = 0
    total_high = 0
    for i in range(1000):
        low, high = send(configuration, i)
        total_low += low
        total_high += high

    print(total_low, total_high)
    print(total_low * total_high)

def part2():
    configuration = parse_input()

    for i in range(1, 100000):
        send(configuration, i)

    print(seen)

    factors = []
    for name, s in seen.items():
        print(name, s[0], s[1] - s[0])
        factors.append(s[1] - s[0])

    answer = math.lcm(*factors)
    print(answer)
