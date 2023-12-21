import os

fileName = os.path.join(os.path.dirname(__file__), "input.txt")
with open(fileName) as f:
    lines = f.read().splitlines()



def drawPixed(cycle, image, x):
    if x-1 == (cycle % 40) or x == (cycle % 40) or x+1 == (cycle % 40):
        image += "#"
    else:
        image += "."
    if cycle > 1 and (cycle+1) % 40 == 0:
        image += "\n"
    return image

def main():
    x = 1
    cycle = 0
    cycleTarget = 40
    wasTwo = False
    image = ""

    for line in lines:
        if wasTwo:
            image = drawPixed(cycle, image, x)
        else:
            image = drawPixed(cycle, image, x)
        if cycle == cycleTarget:
            cycleTarget += 40
        if line == "noop":
            cycle += 1
            wasTwo = False
        else:
            image = drawPixed(cycle+1, image, x)
            if cycle+1 == cycleTarget:
                cycleTarget += 40

            d = int(line.split(" ")[1])
            x += d
            cycle += 2
            wasTwo = True
    return image

print(main())