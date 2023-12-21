import os

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    seeds = list(map(int, lines[0].split(": ")[1].split()))

    i = 3

    result = [seeds]
 
    for _ in range(7):
        xs = []

        while i < len(lines) and lines[i] != "":
            nums = lines[i].split()
            xs.append((int(nums[0]), int(nums[1]), int(nums[2])))
            i+=1

        i += 2

        result.append(xs)

    return result



def mapping(x: int, mapping: list[tuple[int, int, int]]) -> int:
    for dest, src, length in mapping:
        if src <= x and x <= src + length - 1:
            d = x - src
            return dest + d
        
    return x

def better(res, loc):
    if res is None:
        return loc
    else:
        return min(loc, res)


def part1():
    res = None

    inputs = parse_input()

    seeds = inputs[0]
    mappings = inputs[1:]
    for seed in seeds:
        source = seed
        for m in mappings:
            source = mapping(source, m)

        res = better(res, source)

    print(res)



def mapRanges(fromR: list[tuple[int, int]], toR: list[tuple[int, int, int]]):
    ranges = []

    for start, end in fromR:
        found = False

        for dest, src, length in toR:
            start2 = src
            end2 = src + length - 1

            # fully cover
            if start <= start2 and end2 <= end:
                ranges.append((dest, dest + length - 1))
                found = True
            # inside
            elif start2 <= start and end <= end2:
                ranges.append((dest + start - start2, dest + end - start2 - 1))
                found = True
            # left inside
            elif start <= start2 and start2 <= end:
                ranges.append((dest, dest + end - start2))
                found = True
            # right inside
            elif start <= end2 and end2 <= end:
                ranges.append((dest + start - start2, dest + length - 1))
                found = True
        # no overlap
        if not found:
            ranges.append((start, end))

    return ranges
        
def part2():
    seedsRanges = []

    inputs = parse_input()
    seeds = inputs[0]
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        end = start + seeds[i+1]-1

        seedsRanges.append((start, end))

    source = seedsRanges
    for m in inputs[1:]:
        source = mapRanges(source, m)

    res = None

    for a,_ in source:
        res = better(res, a)

    print(res)

part1()
part2()