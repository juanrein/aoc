from getinput import getInput


def snafuToDecimal(s: str) -> int:
    b = 1
    mapping = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}
    val = 0
    for i in range(len(s)-1, -1, -1):
        c = s[i]
        a = mapping[c]
        val += a * b
        b *= 5
    return val

def getExponent(d: int):
    ex = 0
    while True:
        if d <= 2 * 5 ** ex:
            break
        ex += 1
    return ex  

def decimalToSnafu(val: int) -> str:
    res = ""
    mapping = {0: "=", 1: "-", 2: "0", 3: "1", 4: "2"}

    while val > 0:
        val, r = divmod(val+2, 5)
        res += mapping[r]

    return "".join(reversed(res))


def solve(test):
    lines = getInput(test)

    nums = []
    for line in lines:
        d = snafuToDecimal(line)
        nums.append(d)

    # print(nums)
    s = sum(nums)
    print("sum", s)
    y = decimalToSnafu(s)

    return y
