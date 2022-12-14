import os

fileName = os.path.join(os.path.dirname(__file__), "input.txt")
with open(fileName) as f:
    lines = f.read().splitlines()

# lines = [
#     "R 5",
#     "U 8",
#     "L 8",
#     "D 3",
#     "R 17",
#     "D 10",
#     "L 25",
#     "U 20"
# ]


def isClose(head, tail):
    ax, ay = tail
    bx, by = head
    for i in range(ax-1, ax+2):
        for j in range(ay-1, ay+2):
            if bx == i and by == j:
                return True
    return False


def adjustTail(head, tail):
    tailX, tailY = tail
    headX, headY = head
    if isClose(head, tail):
        return (tailX, tailY)
    if headX == tailX + 2:
        if tailY == headY:
            return (tailX+1, tailY)
        else:
            if tailY < headY:
                return (tailX+1, tailY+1)
            else:
                return (tailX+1, tailY-1)
    elif headX == tailX - 2:
        if tailY == headY:
            return (tailX-1, tailY)
        else:
            if tailY < headY:
                return (tailX-1, tailY+1)
            else:
                return (tailX-1, tailY-1)
    elif headY == tailY + 2:
        if tailX == headX:
            return (tailX, tailY+1)
        else:
            if tailX < headX:
                return (tailX+1, tailY+1)
            else:
                return (tailX-1, tailY+1)
    elif headY == tailY - 2:
        if tailX == headX:
            return (tailX, tailY-1)
        else:
            if tailX < headX:
                return (tailX+1, tailY-1)
            else:
                return (tailX-1, tailY-1)


def main():
    rope = [
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
    ]

    visited = set()
    visited.add((0, 0))
    for line in lines:
        parts = line.split(" ")
        dir = parts[0]
        amount = int(parts[1])
        if dir == "U":
            for i in range(amount):
                rope[0] = (rope[0][0], rope[0][1] + 1)
                for j in range(1, len(rope)):
                    newX, newY = adjustTail(rope[j-1], rope[j])
                    rope[j] = (newX, newY)
                visited.add(rope[j])

        elif dir == "D":
            for i in range(amount):
                rope[0] = (rope[0][0], rope[0][1] - 1)
                for j in range(1, len(rope)):
                    newX, newY = adjustTail(rope[j-1], rope[j])
                    rope[j] = (newX, newY)
                visited.add(rope[-1])
        elif dir == "L":
            for i in range(amount):
                rope[0] = (rope[0][0] - 1, rope[0][1])
                for j in range(1, len(rope)):
                    newX, newY = adjustTail(rope[j-1], rope[j])
                    rope[j] = (newX, newY)
                visited.add(rope[-1])
        elif dir == "R":
            for i in range(amount):
                rope[0] = (rope[0][0] + 1, rope[0][1])
                for j in range(1, len(rope)):
                    newX, newY = adjustTail(rope[j-1], rope[j])
                    rope[j] = (newX, newY)

                visited.add(rope[-1])
    print(visited)
    print(len(visited))


main()
