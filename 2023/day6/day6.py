import os
import re

def part1():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()
    line_t = [int(d) for d in re.findall("\d+", lines[0])]
    line_d = [int(d) for d in re.findall("\d+", lines[1])]

    races = list(zip(line_t, line_d))

    result = 1
    for time, distance_best in races:
        ways_to_win = 0

        for hold_time in range(time+1):
            travel_time = time - hold_time
            speed = hold_time
            distance = travel_time * speed
            if distance > distance_best:
                ways_to_win += 1

        result = result * ways_to_win

    print(result)

def part2():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    race_time = int("".join(re.findall("\d+", lines[0])))
    distance_best = int("".join(re.findall("\d+", lines[1])))

    ways_to_win = 0

    for hold_time in range(race_time+1):
        travel_time = race_time - hold_time
        speed = hold_time
        distance = travel_time * speed
        if distance > distance_best:
            ways_to_win += 1

    print(ways_to_win)

part1()
part2()