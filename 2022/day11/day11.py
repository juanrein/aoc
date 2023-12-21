import os

def makeFunc(op):
    byself = False
    if op[1] == "old":
        byself = True
    else:
        opp = int(op[1])

    if op[0] == "*":
        if byself:
            opf = lambda old: old * old
        else:
            opf = lambda old: old * opp
    elif op[0] == "+":
        if byself:
            opf = lambda old: old + old
        else:
            opf = lambda old: old + opp

    return opf

def getData():
    fileName = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(fileName) as f:
        lines = f.read().splitlines()

    data = []
    for i in range(0, len(lines), 7):
        nums = list(map(int, lines[i+1][18:].split(", ")))

        op = lines[i+2][23:].split(" ")
        opf = makeFunc(op)

        test = int(lines[i+3][21:])
        trueTarget = int(lines[i+4][29:])
        falseTarget = int(lines[i+5][30:])

        data.append({
            "items": nums,
            "op": opf,
            "test": test,
            "trueTarget": trueTarget,
            "falseTarget": falseTarget,
            "inspects": 0
        })


    return data

def process(monkey, item, number):
    val = monkey["op"](item)
    val = val % number
    if val % monkey["test"] == 0:
        return monkey["trueTarget"], val
    return monkey["falseTarget"], val

def doRound(data, number):
    for monkey in data:
        deletable = []
        for item in monkey["items"]:
            monkey["inspects"] += 1
            target, val = process(monkey, item, number)
            data[target]["items"].append(val)
            deletable.append(item)
        monkey["items"] = list(filter(lambda x: x not in deletable, monkey["items"]))

    return data

def saveHistory(history):
    fileName = os.path.join(os.path.dirname(__file__), "history.txt")
    with open(fileName, mode="w+") as f:
        for x in history:
            f.write(str(x) + "\n")


def solve(data):
    #history = []
    numbers = list(map(lambda x: x["test"], data))
    number = 1
    for num in numbers:
        print(num)
        number *= num
    print(number)
    for i in range(10000):
        if i % 1000 == 0:
            print(i)
        data = doRound(data, number)
        
        #history.append(list(map(lambda monkey: monkey["items"], data)))

    #saveHistory(history)
    return list(map(lambda monkey: monkey["inspects"], data))

    
def main():
    data = getData()
    res = solve(data)
    print(res)
    ress = sorted(res, reverse=True)
    print(ress)
    print(ress[0] * ress[1])
main()