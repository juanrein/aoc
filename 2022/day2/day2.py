import os

fileName = os.path.join(os.path.dirname(__file__), "input.txt")

with open(fileName) as f:
    lines = f.readlines()


mapping = {
    "A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3
}
lose = 1
tie = 2
win = 3
rock = 1
paper = 2
scissors = 3

def chooseHand(goal):
    if goal == lose:
        if op == rock:
            return scissors, 0
        elif op == paper:
            return rock, 0
        elif op == scissors:
            return paper, 0
    elif goal == tie:
        return op, 3
    elif goal == win:
        if op == rock:
            return paper, 6
        elif op == paper:
            return scissors, 6
        elif op == scissors:
            return rock, 6

    
score = 0
for line in lines:
    parts = line.strip().split(" ")

    op = mapping[parts[0]]
    myGoal = mapping[parts[1]]

    my, outcomeScore = chooseHand(myGoal)

    score += my
    score += outcomeScore

print(score)
