import os

def fileLines(file):
    """
    Lines of input.txt file
    """
    fileName = os.path.join(os.path.dirname(file), "input.txt")
    with open(fileName) as f:
        lines = f.read().splitlines()

    return lines

