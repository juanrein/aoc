import os


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        s = f.read().strip()

    steps = s.split(",")

    return steps


def ascii_hash(step: str) -> int:
    value = 0
    for c in step:
        d = ord(c)

        value += d

        value = value * 17

        value = value % 256

    return value

def part1():
    steps = parse_input()

    res = 0

    for step in steps:
        value = ascii_hash(step)
        res += value

    print("total", res)

def part2():
    boxes = []
    for _ in range(256):
        boxes.append([])


    for step in parse_input():
        if "=" in step:
            ab = step.split("=")
            label = ab[0]
            focal_length = int(ab[1])

            label_hash = ascii_hash(label)

            found = False
            for i in range(len(boxes[label_hash])):
                label2 = boxes[label_hash][i][0]

                if label2 == label:
                    boxes[label_hash][i] = (label, focal_length)
                    found = True
                    break
            if not found:
                boxes[label_hash].append((label, focal_length))
        else:
            label = step[:len(step)-1]
            label_hash = ascii_hash(label)
            for i in range(len(boxes[label_hash])):
                label2, focal_length2 = boxes[label_hash][i]
                if label2 == label:
                    boxes[label_hash].remove((label2, focal_length2))
                    break


    res = 0
    for i,box in enumerate(boxes):
        for j, (label, focal_length) in enumerate(box):
            focusing_power = (i+1) * (j+1) * focal_length

            res += focusing_power

    print(res)
