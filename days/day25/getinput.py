from pathlib import Path


def getInput(test):
    if test:
        lines = [
            "1=-0-2",
            "12111",
            "2=0=",
            "21",
            "2=01",
            "111",
            "20012",
            "112",
            "1=-1=",
            "1-12",
            "12",
            "1=",
            "122",
        ]
    else:
        with open(Path(__file__).parent.joinpath("input.txt")) as f:
            lines = f.read().splitlines()

    return lines
