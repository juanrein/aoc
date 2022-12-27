from pathlib import Path


def getInput(test):
    if test:
        lines = [
            "1",
            "2",
            "-3",
            "3",
            "-2",
            "0",
            "4",
        ]
    else:
        with open(Path(__file__).parent.joinpath("input.txt")) as f:
            lines = f.read().splitlines()

    return list(map(int, lines))