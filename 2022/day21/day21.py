from getinput import getInput
from mathtypes import NumberNode, OperatorNode, Node, Variable
from collections import deque

def computeValue(monkeys: dict[str, Node], root: Node):
    if isinstance(root, NumberNode):
        return root.val
    elif isinstance(root, OperatorNode):
        left = computeValue(monkeys, monkeys[root.leftName])
        right = computeValue(monkeys, monkeys[root.rightName])

        if root.operator == "+":
            return left + right
        if root.operator == "-":
            return left - right
        if root.operator == "*":
            return left * right
        if root.operator == "/":
            return left // right

def solve(test):
    monkeys = getInput(test)
    monkeys = {m.name: m for m in monkeys}

    val = computeValue(monkeys, monkeys["root"])

    return val

def computeValue2(monkeys: dict[str, Node], root: Node):
    if root.name == "humn":
        return Variable("x")
    if isinstance(root, NumberNode):
        return root.val
    elif isinstance(root, OperatorNode):
        left = computeValue2(monkeys, monkeys[root.leftName])
        right = computeValue2(monkeys, monkeys[root.rightName])
        if root.name == "root":
            return (left, "=", right)
        if isinstance(left, int) and isinstance(right, int):
            if root.operator == "+":
                return left + right
            if root.operator == "-":
                return left - right
            if root.operator == "*":
                return left * right
            if root.operator == "/":
                return left // right
        else:
            # if isinstance(left, Variable) and root.operator == "*" and isinstance(right, int):
            #     return left * right
            # if isinstance(left, int) and root.operator == "*" and isinstance(right, Variable):
            #     return right * left
            # if isinstance(left, Variable) and root.operator == "/" and isinstance(right, int):
            #     return left // right
            # if isinstance(left, tuple) and isinstance(left, tuple):

            return (left, root.operator, right)

def solveEq(a,b):
    if isinstance(a, Variable):
        return b
    if isinstance(b, Variable):
        return a

    if isinstance(a, tuple):
        left, op, right = a
        target = b
    else:
        left, op, right = b
        target = a

    if isinstance(left, int):
        val = left
        rest = right
    elif isinstance(right, int):
        val = right
        rest = left

    if op == "*": # 10 = 5 * (x-1) => 10/5 = (x-1)
        reduced = target // val
    elif op == "/" and isinstance(right,int): # 10 = (x-1)/5 => 10*5 = (x-1) 
        reduced = target * val      
    elif op == "/" and isinstance(left, int): # 10 = 5/(x-1) => 10(x-1) = 5 => 5//10
        reduced = val // target
    elif op == "+":
        reduced = target - val
    elif op == "-" and isinstance(right, int): # 10 = (x-1) - 5 => 10+5
        reduced = target + val
    elif op == "-" and isinstance(left, int): # 10 = 5 - (x-1) => 10 - 5 = -(x-1) => -(10-5)
        reduced = -(target - val)

    return solveEq(reduced, rest)


def solve2(test):
    monkeys = getInput(test)
    monkeys = {m.name: m for m in monkeys}

    a,_,b = computeValue2(monkeys, monkeys["root"])

    xVal = solveEq(a,b)

    return xVal
    