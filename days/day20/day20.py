from getinput import getInput


class Node:
    def __init__(self, originalIndex: int, shift: int):
        self.originalIndex = originalIndex
        self.shift = shift
        self.next: Node = None
        self.prev: Node = None

    def __str__(self):
        return str(self.shift)

    def __repr__(self):
        return "Node:" + str(self.shift)


def printLoopedList(root: Node):
    print(root, end=" ")
    current = root.next
    while current.originalIndex != root.originalIndex:
        print(current, end=" ")
        current = current.next
    print()


def shift(root: Node, originalI: int, N: int):
    while root.originalIndex != originalI:
        root = root.next

    if root.shift == 0:
        return root

    shifts = root.shift % (N-1)

    
    # move to target position
    current = root
    for _ in range(shifts):
        current = current.next

    movedNode = Node(originalI, root.shift)
    # insert into position
    current.next.prev = movedNode
    movedNode.next = current.next
    current.next = movedNode
    movedNode.prev = current

    # remove node
    current = root
    current.prev.next = current.next
    current.next.prev = current.prev

    return movedNode


def createList(numbers):
    root = Node(0, numbers[0])
    prev = root
    for i in range(1, len(numbers)):
        current = Node(i, numbers[i])
        prev.next = current
        current.prev = prev
        prev = current

    # looping
    root.prev = current
    current.next = root

    return root


def groveGoordinates(root: Node):
    current = root
    while current.shift != 0:
        current = current.next

    x = [0]
    current = current.next
    while current.shift != 0:
        x.append(current.shift)
        current = current.next

    a = x[1000 % len(x)]
    b = x[2000 % len(x)]
    c = x[3000 % len(x)]

    return a, b, c


def solve(test):
    numbers = getInput(test)
    N = len(numbers)
    root = createList(numbers)

    for i in range(len(numbers)):
        root = shift(root, i, N)

    a, b, c = groveGoordinates(root)
    print(a,b,c)
    return a+b+c


def solve2(test):
    numbers = getInput(test)
    N = len(numbers)

    decryptionKey = 811589153
    numbers = [x * decryptionKey for x in numbers]
    root = createList(numbers)

    for _ in range(10):
        for i in range(len(numbers)):
            root = shift(root, i, N)
        
    a,b,c = groveGoordinates(root)
    print(a,b,c)
    return a+b+c