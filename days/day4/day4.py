import os


fileName = os.path.join(os.path.dirname(__file__), "input.txt")
with open(fileName) as f:
    lines = f.read().splitlines()

result = 0
for line in lines:
    parts = line.split(",")
    p1 = parts[0]
    p2 = parts[1]
    p1parts = p1.split("-")
    p2parts = p2.split("-")
    a1 = int(p1parts[0])
    a2 = int(p1parts[1])
    b1 = int(p2parts[0])
    b2 = int(p2parts[1])

    if a1 <= b1 <= a2:
        result += 1
    elif a1 <= b2 <= a2:
        result += 1
    elif b1 <= a1 <= b2:
        result += 1
    elif b1 <= a2 <= b2:
        result += 1

print(result)