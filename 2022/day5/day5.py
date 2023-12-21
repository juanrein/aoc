import os
import re

fileName = os.path.join(os.path.dirname(__file__), "input.txt")
with open(fileName) as f:
    lines = f.read().splitlines()


fileI = 0
stackRows = []
while lines[fileI] != "":
    line = lines[fileI]
    stackRow = []
    for j in range(0, len(line), 4):
        if line[j] == "[":
            stackRow.append(line[j+1])
        elif line[j+1].isdigit():
            stackRow.append(line[j+1])
        else:
            stackRow.append("")
    stackRows.append(stackRow)
    fileI += 1
    
stackRows.pop()

stacks = [[] for _ in range(len(stackRows[0]))]

for i in range(len(stackRows)):
    for j in range(len(stackRows[i])):
        elem = stackRows[i][j]
        if elem != "":
            stacks[j].append(elem)

for i in range(len(stacks)):
    stacks[i] = list(reversed(stacks[i]))

def makeMove(count, fromI, toI):
    move = []
    current = 0
    while current < count:
        move.append(stacks[fromI].pop())
        current += 1
    for i in reversed(range(len(move))):
        stacks[toI].append(move[i])

command = re.compile(r"move (\d+) from (\d+) to (\d+)")
while fileI < len(lines):
    match = command.match(lines[fileI])
    if match:
        count = int(match.group(1))
        fromStack = int(match.group(2))
        toStack = int(match.group(3))
        makeMove(count, fromStack-1, toStack-1)

    fileI += 1

result = "";
for i in range(len(stacks)):
    result += stacks[i][-1]

print(result)