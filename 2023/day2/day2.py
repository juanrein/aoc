import os

def parse_input() -> list[tuple[int, list[list[tuple[int, str]]]]]:
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    games = []

    for line in lines:
        parts = line.split(": ")
        id = int(parts[0].split(" ")[1])

        throws = parts[1].split("; ")

        samples = []
        for throw in throws:
            pairs = throw.split(", ")
            sample = []
            
            for pair in pairs:
                countColor = pair.split(" ")
                count = int(countColor[0])
                color = countColor[1]
                sample.append((count, color))

            samples.append(sample)
        games.append((id, samples))

    return games



def is_possible(throw: list[tuple[int, str]]) -> bool:
    r = 0
    g = 0
    b = 0

    n_red = 12
    n_green = 13
    n_blue = 14

    for count, color in throw:
        match color:
            case "red":
                r += count
            case "green":
                g += count
            case "blue":
                b += count
    return r <= n_red and g <= n_green and b <= n_blue


def is_possible_line(throws: list[list[tuple[int, str]]]):
    for throw in throws:
        if not is_possible(throw):
            return False

    return True


def part1():
    games = parse_input()
    result = 0

    for id, throws in games:
        if is_possible_line(throws):
            result += id

    print(result)

def part2():
    games = parse_input()

    result = 0
    for id, throws in games:
        needed_red = 0
        needed_green = 0
        needed_blue = 0

        for throw in throws:
            for count, color in throw:
                match color:
                    case "red" if count > needed_red:
                        needed_red = count
                    case "green" if count > needed_green:
                        needed_green = count
                    case "blue" if count > needed_blue:
                        needed_blue = count

        power = needed_red * needed_green * needed_blue

        result += power

    print(result)

part1()
part2()