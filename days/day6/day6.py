import os
import re

fileName = os.path.join(os.path.dirname(__file__), "input.txt")
with open(fileName) as f:
    line = f.readline()

window = list(line[:14])
for i in range(4, len(line)):
    if len(set(window)) == 14:
        print(i)
        break
    window.pop(0)
    window.append(line[i])
