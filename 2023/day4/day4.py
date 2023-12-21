import os

def parse_input() -> list[tuple[list[int], list[int]]]:
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    cards = []

    for line in lines:
        parts = line.split(": ")
        leftright = parts[1].split(" | ")

        winning_numbers = list(map(int, leftright[0].split()))
        own_numbers = list(map(int, leftright[1].split()))

        cards.append((winning_numbers, own_numbers))

    return cards

def part1():
    cards = parse_input()

    points = 0
    for winning, own in cards:
        card_points = 0
        winningSet = set(winning)
        for ownI in own:
            if ownI in winningSet:
                if card_points == 0:
                    card_points = 1
                else:
                    card_points = card_points * 2

        points += card_points



    print(points)

def part2():
    cards = parse_input()

    cache = [-1 for i in range(len(cards))]

    def compute_winnings(cards: list[tuple[list[int], list[int]]], i: int, wins: list[int]) -> int:
        if cache[i] != -1:
            return cache[i]
        n_wins = 0
        for j in range(i+1, min(i+wins[i]+1, len(cards))):
            n_wins += compute_winnings(cards, j, wins)

        cache[i] = wins[i] + n_wins
        return wins[i] + n_wins

    wins = []
    for winning, own in cards:
        winningSet = set(winning)
        n_wins = 0
        for ownI in own:
            if ownI in winningSet:
                n_wins += 1
        wins.append(n_wins)

    n_scratchcards = 0

    for i in range(len(cards)):
        n_scratchcards += 1 + compute_winnings(cards, i, wins)

    print(n_scratchcards)

part2()