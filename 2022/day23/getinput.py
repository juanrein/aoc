from pathlib import Path

def getInput(test):
    if test:
        lines = [
            ".....",
            "..##.",
            "..#..",
            ".....",
            "..##.",
            ".....",
        ]
    else:
        with open(Path(__file__).parent.joinpath("input.txt")) as f:
            lines = f.read().splitlines()

    occupied = set()
    for y,line in enumerate(lines):
        for x,pos in enumerate(line):
            if pos == "#":
                occupied.add((y,x))
    
    return occupied
    