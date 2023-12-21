class Node:
    def __init__(self, name):
        self.name = name

class NumberNode(Node):
    def __init__(self, name, val):
        super().__init__(name)
        self.val = val
    
    def __str__(self):
        return self.name + ": " + str(self.val)

    def __repr__(self):
        return self.name + ": " + str(self.val)

class OperatorNode(Node):
    def __init__(self, name, operator, leftName, rightName):
        super().__init__(name)
        self.operator = operator
        self.leftName = leftName
        self.rightName = rightName
        # self.left = None
        # self.right = None
   
    def __repr__(self) -> str:
        return self.name + " " + self.leftName + " " + self.operator + " " + self.rightName

    
class Variable:
    def __init__(self, name, k = 1):
        self.k = k
        self.name = name

    def __str__(self):
        return str(self.k) + "*" + self.name

    def __repr__(self):
        return str(self.k) + "*" + self.name

    def __mul__(self, other):
        return Variable(self.name, self.k * other)

    def __floordiv__(self, other):
        return Variable(self.name, self.k // other)

