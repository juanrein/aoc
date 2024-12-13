import os
import re
from collections import Counter, defaultdict


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    rules = []

    i = 0
    while lines[i] != "":
        rules.append([int(d) for d in lines[i].split("|")])
        i += 1

    updates = []
    for j in range(i+1, len(lines)):
        updates.append([int(d) for d in lines[j].split(",")])

    return rules, updates


def part1():
    rules, updates = parse_input()

    befores = defaultdict(set)

    for lower, higher in rules:
        befores[higher].add(lower)


    result = 0
    for update in updates:
        mistake = False
        for i in range(len(update)):
            for j in range(i+1, len(update)):
                if update[j] in befores[update[i]]:
                    mistake = True
                    break
        if not mistake:
            result += update[len(update)//2]

    print(result)

def sortUpdate(update, rules):
    sortedUpdate = []
    found = set()
    befores = defaultdict(set)

    for lower, higher in rules:
        if lower in update and higher in update:
            befores[higher].add(lower)

    updateLeft = update[:]
    for _ in range(len(update)):
        for i in range(len(updateLeft)):
            if len(befores[updateLeft[i]] - found) == 0:
                sortedUpdate.append(updateLeft[i])
                found.add(updateLeft[i])
                updateLeft.pop(i)
                break
    return sortedUpdate

rules, updates = parse_input()

befores = defaultdict(set)

for lower, higher in rules:
    befores[higher].add(lower)

result = 0
for update in updates:
    mistake = False
    for i in range(len(update)):
        for j in range(i+1, len(update)):
            if update[j] in befores[update[i]]:
                mistake = True
                break
    if mistake:
        sortedupdate = sortUpdate(update, rules)
        result += sortedupdate[len(sortedupdate)//2]

print(result)


