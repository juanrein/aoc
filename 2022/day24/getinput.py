from pathlib import Path


def getInput(test):
    if test:
        # lines = [
        #     "#.#####",
        #     "#.....#",
        #     "#>....#",
        #     "#.....#",
        #     "#...v.#",
        #     "#.....#",
        #     "#####.#",
        # ]
        lines = [
            "#.######",
            "#>>.<^<#",
            "#.<..<<#",
            "#>v.><>#",
            "#<^v^^>#",
            "######.#",
        ]
    else:
        with open(Path(__file__).parent.joinpath("input.txt")) as f:
            lines = f.read().splitlines()

    grid = [[None for _ in range(len(lines[0]))] for _ in range(len(lines))]
    for y, line in enumerate(lines):
        for x, pos in enumerate(line):
            grid[y][x] = pos

    start = grid[0].index(".")
    end = grid[-1].index(".")

    return grid, (0, start), (len(grid)-1, end)
