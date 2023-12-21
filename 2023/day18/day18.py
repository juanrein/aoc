import os

def parse_input(part2):
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    dirMap = {0: "R",1: "D", 2: "L", 3: "U"}
    commands = []
    for line in lines:
        if not part2:
            parts = line.split()
            command = (parts[0], int(parts[1]))
            commands.append(command)
        else:
            hex = line.split()[2].strip("(#)")
            distance = int(hex[0:5], 16)
            direction = dirMap[int(hex[5])]
            commands.append((direction, distance))

    return commands

def get_vertices(part2):
    commands = parse_input(part2)

    pos = (0,0)

    vertices = [pos]

    length = 0
    for d, steps in commands:
        i,j = pos
        length += steps
        match d:
            case "U":
                pos = (i - steps, j)
            case "D":
                pos = (i + steps, j)
            case "L":
                pos = (i, j-steps)
            case "R":
                pos = (i, j+steps)
        
        vertices.append(pos)

    return vertices, length

def get_area(part2):
    total = 0
    vertices, borders = get_vertices(part2)
    for i in range(1, len(vertices)):
        y1,x1 = vertices[i-1]
        y2,x2 = vertices[i]
        det = x1*y2 - x2*y1
        total += det

    print(total // 2 + borders // 2 + 1)

get_area(False)
get_area(True)
