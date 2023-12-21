import os

fileName = os.path.join(os.path.dirname(__file__), "input.txt")
with open(fileName) as f:
    lines = f.read().splitlines()

currentDir = {}
fs = currentDir
fileNames = []
for line in lines:
    if line.startswith("$ cd"):
        dir = line[5:]
        if dir == "..":
            currentDir = currentDir[".."]
        else:
            fileNames.append(dir)
            if dir not in currentDir:
                currentDir[dir] = {"..": currentDir}
            currentDir = currentDir[dir]
    elif not line.startswith("$ ls"):
        if line.startswith("dir"):
            dir = line[4:]
            currentDir[dir] = {"..": currentDir}
        else:
            parts = line.split(" ")
            size = int(parts[0])
            name = parts[1]
            currentDir[name] = size

def traverse(fs, results):
    result = 0
    for k,v in fs.items():
        if k == "..":
            continue
        if isinstance(v, int):
            result += v
        else:
            result += traverse(v, results)

    if result <= 100000:
        results.append(result)

    return result

def findDeletable(name, fs, needed, results):
    result = 0
    for k,v in fs.items():
        if k == "..":
            continue
        if isinstance(v, int):
            result += v
        else:
            result += findDeletable(k, v, needed, results)
    if result >= needed:
        results[name] = result
    return result

results = []
totalUsed = traverse(fs, results)
print(totalUsed)
print(results)
print(sum(results))

fsSize = 70000000
unused = fsSize - totalUsed
needed = 30000000 - unused
results = {}
findDeletable("/", fs, needed, results)
print(results)
print(min(results.items(), key = lambda x: x[1]))