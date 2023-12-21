import os
from collections import defaultdict
from itertools import product

def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    res = []
    for line in lines:
        parts = line.split(" ")
        hand = parts[0]
        bid = int(parts[1])

        res.append((hand, bid))

    return res
    

def is_five_of_kind(hand: str, part2: bool = False) -> bool:
    d = defaultdict[str, int](int)
    for c in hand:
        d[c] += 1

    items = list(sorted(d.items(), key=lambda x: x[1]))
    return len(items) == 1

def is_four_of_kind(hand: str, part2: bool = False) -> bool:
    d = defaultdict[str, int](int)
    for c in hand:
        d[c] += 1

    items = list(sorted(d.items(), key=lambda x: x[1]))

    return len(items) == 2 and (items[0][1] == 4 or items[1][1] == 4)


def is_full_house(hand: str, part2: bool = False) -> bool:
    d = defaultdict[str, int](int)
    for c in hand:
        d[c] += 1

    items = list(sorted(d.items(), key=lambda x: x[1]))

    return len(items) == 2 and (items[0][1] == 3 or items[1][1] == 3)

def is_three_of_kind(hand: str, part2: bool = False) -> bool:
    d = defaultdict[str, int](int)
    for c in hand:
        d[c] += 1

    items = list(sorted(d.items(), key=lambda x: x[1]))

    return len(items) == 3 and (items[0][1] == 3 or items[1][1] == 3 or items[2][1] == 3)


def is_two_pair(hand: str, part2: bool = False) -> bool:
    d = defaultdict[str, int](int)
    for c in hand:
        d[c] += 1

    items = list(sorted(d.items(), key=lambda x: x[1]))
    return len(items) == 3 and items[0][1] == 1 and items[1][1] == 2 and items[2][1] == 2

def is_one_pair(hand: str, part2: bool = False) -> bool:
    d = defaultdict[str, int](int)
    for c in hand:
        d[c] += 1

    items = list(sorted(d.items(), key=lambda x: x[1]))
    return len(items) == 4 and items[0][1] == 1 and items[1][1] == 1 and items[2][1] == 1 and items[3][1] == 2

def is_high_card(hand: str, part2: bool = False) -> bool:
    d = defaultdict[str, int](int)
    for c in hand:
        d[c] += 1

    items = list(sorted(d.items(), key=lambda x: x[1]))
    return len(items) == 5


def get_type(hand: str) -> int:
    if is_five_of_kind(hand):
        return 7
    if is_four_of_kind(hand):
        return 6
    if is_full_house(hand):
        return 5
    if is_three_of_kind(hand):
        return 4
    if is_two_pair(hand):
        return 3
    if is_one_pair(hand):
        return 2
    if is_high_card(hand):
        return 1
    
    raise ValueError(hand)

def get_type2(hand: str) -> int:
    variations = []
    for c in hand:
        if c == "J":
            variations.append(["2","3","4","5","6","7","8","9","T","J","Q","K","A"])
        else:
            variations.append([c])

    best = 0
    for vari in product(*variations):
        best = max(get_type("".join(vari)), best)
    
    return best
        
def get_strength(hand: str):
    card_to_num = {
        "2": 1,
        "3": 2,
        "4": 3,
        "5": 4,
        "6": 5,
        "7": 6,
        "8": 7,
        "9": 8,
        "T": 9,
        "J": 10,
        "Q": 11,
        "K": 12,
        "A": 13
    }

    return tuple(map(lambda x: card_to_num[x], hand))

def get_strength2(hand: str):
    card_to_num = {
        "J": 0,
        "2": 1,
        "3": 2,
        "4": 3,
        "5": 4,
        "6": 5,
        "7": 6,
        "8": 7,
        "9": 8,
        "T": 9,
        "Q": 11,
        "K": 12,
        "A": 13
    }

    return tuple(map(lambda x: card_to_num[x], hand))

def part1():
    hands = parse_input()

    hands = sorted(hands, key = lambda x: (get_type(x[0]), get_strength(x[0])))

    total_winnings = 0
    for i, (hand, bid) in enumerate(hands):
        total_winnings += (i+1) * bid

    print(total_winnings)


hands = parse_input()

hands = sorted(hands, key = lambda x: (get_type2(x[0]), get_strength2(x[0])))

total_winnings = 0
for i, (hand, bid) in enumerate(hands):
    total_winnings += (i+1) * bid

print(total_winnings)
