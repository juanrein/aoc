import os
file = os.path.join(os.path.dirname(__file__), "input.txt")
with open(file) as f:
    lines = f.readlines()

elves = [0]
for line in lines:
    if len(line.strip()) > 0:
        amount = int(line)
        elves[-1] += amount
    else:
        elves.append(0)

print(sum(sorted(elves, reverse=True)[:3]))