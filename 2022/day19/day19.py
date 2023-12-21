from getinput import getInput
import functools
from robotingTypes import BluePrint
from collections import deque


def oreOption(resources, robots, blueprint: BluePrint, time):
    ore, clay, obsidian, geode = resources
    oreR, clayR, obsidianR, geodeR = robots

    needed = ore - blueprint.oreRobotCost
    timeNeeded = 0
    while needed < 0:
        needed += oreR  # there are always ore robots
        timeNeeded += 1
    # resources after (during build minute new ore is collected),
    # robots after,
    # time after robot was built
    return (
        (needed + oreR, clay + clayR * (timeNeeded+1), obsidian +
         obsidianR * (timeNeeded+1), geode + geodeR * (timeNeeded+1)),
        (oreR+1, clayR, obsidianR, geodeR),
        time + timeNeeded + 1
    )


def clayOption(resources, robots, blueprint: BluePrint, time):
    ore, clay, obsidian, geode = resources
    oreR, clayR, obsidianR, geodeR = robots

    needed = ore - blueprint.clayRobotCost
    timeNeeded = 0
    while needed < 0:
        needed += oreR  # there are always ore robots
        timeNeeded += 1
    # resources after (during build minute new ore is collected),
    # robots after,
    # time after robot was built
    return (
        (needed + oreR, clay + clayR * (timeNeeded+1), obsidian +
         obsidianR * (timeNeeded+1), geode + geodeR * (timeNeeded+1)),
        (oreR, clayR+1, obsidianR, geodeR),
        time + timeNeeded + 1
    )


def obsidianOption(resources, robots, blueprint: BluePrint, time):
    ore, clay, obsidian, geode = resources
    oreR, clayR, obsidianR, geodeR = robots

    neededOre = ore - blueprint.obsidianRobotOreCost
    neededClay = clay - blueprint.obsidianRobotClayCost
    timeNeeded = 0
    while neededOre < 0 or neededClay < 0:
        if neededOre < 0:
            neededOre += oreR  # there are always ore robots
        if neededClay < 0:
            neededClay += clayR
        timeNeeded += 1

    # resources after (during build minute new ore is collected),
    # robots after,
    # time after robot was built
    return (
        (neededOre + oreR, neededClay + clayR, obsidian +
         obsidianR * (timeNeeded+1), geode + geodeR * (timeNeeded+1)),
        (oreR, clayR, obsidianR+1, geodeR),
        time + timeNeeded + 1
    )


def geodeOption(resources, robots, blueprint: BluePrint, time):
    ore, clay, obsidian, geode = resources
    oreR, clayR, obsidianR, geodeR = robots

    neededOre = ore - blueprint.geodeRobotOreCost
    neededObsidian = obsidian - blueprint.geodeRobotObsidianCost
    timeNeeded = 0
    while neededOre < 0 or neededObsidian < 0:
        if neededOre < 0:
            neededOre += oreR  # there are always ore robots
        if neededObsidian < 0:
            neededObsidian += obsidianR
        timeNeeded += 1
    # resources after (during build minute new ore is collected),
    # robots after,
    # time after robot was built
    return (
        (neededOre + oreR, clay + clayR * (timeNeeded+1),
         neededObsidian + obsidianR, geode + geodeR * (timeNeeded+1)),
        (oreR, clayR, obsidianR, geodeR + 1),
        time + timeNeeded + 1
    )


def doNothingOption(resources, robots, blueprint: BluePrint, time):
    ore, clay, obsidian, geode = resources
    oreR, clayR, obsidianR, geodeR = robots

    return (
        (ore+oreR, clay+clayR, obsidian+obsidianR, geode+geodeR),
        robots,
        time+1
    )


def getMoves(resources, robots, blueprint: BluePrint, time: int, totalTime):
    moves = []

    oreB = oreOption(resources, robots, blueprint, time)
    if oreB[2] <= totalTime:
        moves.append(oreB)

    clayB = clayOption(resources, robots, blueprint, time)
    if clayB[2] <= totalTime:
        moves.append(clayB)

    if robots[1] > 0:  # if clay robots
        obsidianB = obsidianOption(resources, robots, blueprint, time)
        if obsidianB[2] <= totalTime:
            moves.append(obsidianB)

    if robots[2] > 0:  # if obsidian robots
        geodeB = geodeOption(resources, robots, blueprint, time)
        if geodeB[2] <= totalTime:
            moves.append(geodeB)

    doNothingB = doNothingOption(resources, robots, blueprint, time)
    if doNothingB[2]-1 <= totalTime:
        moves.append(doNothingB)

    # get rid of unncessessary robots
    movesActual = []
    maxOreR = max(blueprint.oreRobotCost, blueprint.clayRobotCost,
                  blueprint.obsidianRobotOreCost, blueprint.geodeRobotOreCost)
    maxClayR = blueprint.obsidianRobotClayCost
    maxObsidianR = blueprint.geodeRobotObsidianCost
    for res, (oreR, clayR, obsidianR, geodeR), t in moves:
        if oreR > maxOreR or clayR > maxClayR or obsidianR > maxObsidianR:
            continue
        movesActual.append((res, (oreR, clayR, obsidianR, geodeR), t))
    return movesActual


def optimalSolution3(blueprint: BluePrint, totalTime: int):
    outerBest = 0

    Q = deque([((0, 0, 0, 0), (1, 0, 0, 0), 1)])
    # Q = [((0, 0, 0, 0), (1, 0, 0, 0), 1)]
    visited = set()

    while len(Q) > 0:
        params = Q.popleft()
        # params = Q.pop()
        if params in visited:
            continue

        resources, robots, time = params
        # if len(visited) > 1_000_000:
        #     visited = set(list(visited)[(len(visited)//2):])

        if time > totalTime:
            outerBest = max(outerBest, resources[3])
            continue

        outerBest = max(outerBest, resources[3])
        timeLeft = totalTime - time + 1
        # can't be better
        if not ((resources[3] + robots[3] * timeLeft + timeLeft * (timeLeft-1) // 2) > outerBest):
            continue

        visited.add(params)

        moves = getMoves(resources, robots, blueprint, time, totalTime)

        for move in moves:
            Q.append(move)

    return outerBest


def solve(test: bool, time: int):
    blueprints = getInput(test)

    geodesOpened = []
    qualityLevels = []
    for blueprint in blueprints:
        print(blueprint)
        print("computing", blueprint.blueprintId)
        # qo = optimalSolution2(blueprint, time)
        qo = optimalSolution3(blueprint, time)
        geodesOpened.append(qo)
        qualityLevel = qo * blueprint.blueprintId
        qualityLevels.append(qualityLevel)
        print(qo)

    # [9,12]
    print("geodes opened", geodesOpened)
    #[9, 24]
    print("quality levels", qualityLevels)
    # 33
    print("sum of quality levels", sum(qualityLevels))
    # the amount of robots of certain type that is optimal seems to be based on the ore costs
    return sum(qualityLevels)


def solve2(test: bool, time: int):
    if test:
        blueprints = getInput(True)
    else:
        blueprints = getInput(False)[:3]

    geodesOpened = []
    for blueprint in blueprints:
        print(blueprint)
        print("computing", blueprint.blueprintId)
        qo = optimalSolution3(blueprint, time)
        geodesOpened.append(qo)
        print(qo)

    print("geodes opened", geodesOpened)
    res = functools.reduce(lambda x, y: x*y, geodesOpened)
    print(res)
    # the amount of robots of certain type that is optimal seems to be based on the ore costs
    return res
