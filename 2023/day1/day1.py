import os


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

sum = 0

def is_end(line, i, reverse: bool):
    if reverse and i < 0:
        return
    return i >= len(line)

def find_num(line: str, reverse: bool):
    if reverse:
        i = len(line) - 1
    else:
        i = 0

    while not is_end(line, i, reverse):
        if line.startswith("one", i):
            return "1"
        elif line.startswith("two", i):
            return "2"
        elif line.startswith("three", i):
            return "3"
        elif line.startswith("four", i):
            return "4"
        elif line.startswith("five", i):
            return "5"
        elif line.startswith("six", i):
            return "6"
        elif line.startswith("seven", i):
            return "7"
        elif line.startswith("eight", i):
            return "8"
        elif line.startswith("nine", i):
            return "9"
        elif line[i].isdigit():
            return line[i]
        else:
            if reverse:
                i -= 1
            else:
                i += 1
        
    raise ValueError(line)

    
for line in lines:
    num1 = find_num(line, False)
    num2 = find_num(line, True)

    val = int(num1 + num2)
    sum += val

print(sum)