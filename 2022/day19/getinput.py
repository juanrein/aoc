from pathlib import Path
import re

from robotingTypes import BluePrint


def getInput(test: bool) -> list[BluePrint]:
    if not test:
        with open(Path(__file__).parent.joinpath("input.txt")) as f:
            lines = f.read().splitlines()
    else:
        lines = [
            "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.",
            "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."
        ]
    data = []
    for line in lines:
        numbers = re.findall("\d+", line)
        numbers = list(map(int, numbers))
        data.append(BluePrint(
            numbers[0],
            numbers[1],
            numbers[2],
            numbers[3],
            numbers[4],
            numbers[5],
            numbers[6],
        ))

    return data
