from pathlib import Path
import re
from mathtypes import NumberNode, OperatorNode 

def getInput(test):
    if test:
        lines = [
            "root: pppw + sjmn",
            "dbpl: 5",
            "cczh: sllz + lgvd",
            "zczc: 2",
            "ptdq: humn - dvpt",
            "dvpt: 3",
            "lfqf: 4",
            "humn: 5",
            "ljgn: 2",
            "sjmn: drzm * dbpl",
            "sllz: 4",
            "pppw: cczh / lfqf",
            "lgvd: ljgn * ptdq",
            "drzm: hmdt - zczc",
            "hmdt: 32",
        ]
        # lines = [
        #     "root: a + b",
        #     "a: 1",
        #     "b: c - d",
        #     "c: 2",
        #     "d: 3"
        # ]
    else:
        with open(Path(__file__).parent.joinpath("input.txt")) as f:
            lines = f.read().splitlines()

    numberPattern = re.compile("(.+): (-?\d+)")
    operPattern = re.compile("(.+): (.+) ([\+\-\*/]) (.+)")

    monkeys = []
    for line in lines:
        m = numberPattern.match(line)
        if m:
            monkeys.append(NumberNode(m.group(1), int(m.group(2))))
        else:
            m = operPattern.match(line)
            if m:
                monkeys.append(OperatorNode(m.group(1), m.group(3), m.group(2), m.group(4)))
            else:
                raise ValueError(line)
    return monkeys