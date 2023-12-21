import os


fileName = os.path.join(os.path.dirname(__file__), "input.txt")
with open(fileName) as f:
    lines = f.read().splitlines()

def priority(c):
    if "A" <= c <= "Z":
        return ord(c) - ord("A") + 2 + (ord("z") - ord("a"))
    return ord(c) - ord("a") + 1

result = 0
for i in range(0, len(lines), 3):
    elf1 = set(lines[i])
    elf2 = set(lines[i+1])
    elf3 = set(lines[i+2])
    common = elf1 & elf2 & elf3
    same = list(common)[0]
    result += priority(same)

print(result)
