import os

fileName = os.path.join(os.path.dirname(__file__), "input.txt")
with open(fileName) as f:
    lines = f.read().splitlines()
ex = []
for line in lines:
    ex.append(list(line))

# ex = [
#     list("30373"),
#     list("25512"),
#     list("65332"),
#     list("33549"),
#     list("35390")
# ]


def scenicScore(ex, i, j):
    left = 0
    right = 0
    up = 0
    down = 0
    # left
    for k in range(j-1, -1, -1):
        left += 1
        if ex[i][j] <= ex[i][k]:
            break
    # right
    for k in range(j+1, len(ex[0])):
        right += 1
        if ex[i][j] <= ex[i][k]:
            break
    # up
    for k in range(i-1, -1, -1):
        up += 1
        if ex[i][j] <= ex[k][j]:
            break
    # down
    for k in range(i+1, len(ex)):
        down += 1
        if ex[i][j] <= ex[k][j]:
            break
    # left = max(1, left)
    # right = max(1, right)
    # up = max(1, up)
    # down = max(1, down)

    return left * right * up * down


scores = []
for i in range(len(ex)):
    for j in range(len(ex[0])):
        scores.append(scenicScore(ex,i,j))

print(scores)
print(max(scores))