import os
import functools
from listparser import parse

def testInput():
    return [
        "[1,1,3,1,1]",
        "[1,1,5,1,1]",
        "",
        "[[1],[2,3,4]]",
        "[[1],4]",
        "",
        "[9]",
        "[[8,7,6]]",
        "",
        "[[4,4],4,4]",
        "[[4,4],4,4,4]",
        "",
        "[7,7,7,7]",
        "[7,7,7]",
        "",
        "[]",
        "[3]",
        "",
        "[[[]]]",
        "[[]]",
        "",
        "[1,[2,[3,[4,[5,6,7]]]],8,9]",
        "[1,[2,[3,[4,[5,6,0]]]],8,9]",
    ]


def getData():
    fileName = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(fileName) as f:
        lines = f.read().splitlines()
    # lines = testInput() 
    pairs = []
    for i in range(0, len(lines), 3):
        first = lines[i]
        second = lines[i+1]
        pair = first, second
        pairs.append(pair)

    return pairs

def list_compare(a,b):
    # print(a,b)
    if isinstance(a, int) and isinstance(b, int):
        return b - a
        
    if isinstance(a, int):
        a = [a] 
        return list_compare(a, b)
    if isinstance(b, int):
        b = [b]
        return list_compare(a, b)

    for i in range(max(len(a), len(b))):
        if i < len(a) and i < len(b):
            c = list_compare(a[i], b[i])
            if c < 0:
                return -1
            if c > 0:
                return 1
        elif i < len(a):
            return -1
        elif i < len(b):
            return 1

    return 0

def list_comp(a,b):
    return list_compare(a["val"], b["val"])

def solve(pairs):

    packets = []
    for i, (a,b) in enumerate(pairs):
        # ae = eval(a)
        # be = eval(b)
        ae = parse(a)
        be = parse(b)

        packets.append({"id": i, "val": ae})
        packets.append({"id": i, "val": be})

    packets.append({"id": -1, "val": [[6]]})
    packets.append({"id": -2, "val": [[2]]})

    return sorted(packets, key=functools.cmp_to_key(list_comp), reverse=True)

def main():
    data = getData()
    res = solve(data)
    a = None
    b = None
    for i,row in enumerate(res):
        if row["id"] == -1:
            a = i+1
        elif row["id"] == -2:
            b = i+1
    # f = open(os.path.join(os.path.dirname(__file__), "test.txt") , mode="w+")
    # for ff in res:
        # f.write(str(ff["val"]) + "\n")
    # f.close()
    # print(res)
    print(a, b, a * b)

main()
