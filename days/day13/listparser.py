def parse(s):
    stack = []
    i = 0
    if len(s) == 0:
        return None
    while i < len(s):
        if s[i] == "[":
            stack.append("[")
            i += 1
        elif s[i] == "]":
            items = []
            prevItem = None
            while True:
                if len(stack) == 0:
                    return None
                item = stack.pop()
                if item == "[":
                    if prevItem is not None:
                        items.append(prevItem)
                    stack.append(list(reversed(items)))
                    break
                elif item == ",":
                    if prevItem is None:
                        return None
                    items.append(prevItem)
                    prevItem = None
                else:
                    prevItem = item
            i += 1
        elif s[i] == ",":
            stack.append(",")
            i += 1
        elif s[i] == " ":
            i += 1
        else:
            num = ""
            neg = False
            if s[i] == "-":
                neg = True
                i += 1
            while i < len(s) and s[i].isdigit():
                num += s[i]
                i += 1
            if len(num) == 0:
                return None
            if neg:
                stack.append(-int(num))
            else:
                stack.append(int(num))

    if not isinstance(stack[0], list):
        return None
    return stack[0]

# print(parse("[[[3,2,100],1,2,3],1,[1,[1,[1,2,3]]]]"))
