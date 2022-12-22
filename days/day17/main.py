from day17 import solve
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from collections import Counter, defaultdict

test = False
verbose = False



def computeValue(cycleStartI, cycleEndI, ds, dss):
    cycleHeight = ds[cycleEndI] - ds[cycleStartI]
    cycleRocks = cycleEndI - cycleStartI
    heightBeforeFirstCycle = solve(cycleStartI-1, test, verbose)[0]
    
    cyclesFill, remainingRocks = divmod(1000000000000 - (cycleStartI-1), cycleRocks)

    neededRocks = remainingRocks
    heightAfterLastCycle = 0
    rockI = cycleEndI+1
    while neededRocks > 0:
        neededRocks -= 1
        heightAfterLastCycle += dss[rockI]
        rockI += 1
    print(heightBeforeFirstCycle, cyclesFill, cycleHeight, heightAfterLastCycle)
    # actual = 1514285714288
    answer = heightBeforeFirstCycle + cyclesFill * cycleHeight + heightAfterLastCycle
    # print(actual)
    print(answer)
    # print(abs(actual - answer))

def plotD(x, dss):
    fig, ax = plt.subplots()
    ax.scatter(x, dss)
    plt.show()

def findRepetition():
    res, X = solve(10000, test=test, verbose=verbose)
    #718, 2438
    ds = [(i,x[8]) for (i,x) in enumerate(X)]
    dss = []
    for i in range(1, len(ds)):
        dss.append((ds[i][0], ds[i][1] - ds[i-1][1]))
    
    # a,b = 0, 10000
    # plotD(list(range(len(dss)))[a:b], [x[1] for x in dss][a:b])
    ids = []
    for i in range(len(dss)):
        if dss[i][1] == 4:
            ids.append((dss[i][0], i, dss[i][1]))
    # plotD(list(range(len(ids))), [x[1] for x in ids])
    idds = []
    for i in range(1, len(ids)):
        idds.append((ids[i][0], ids[i][1] - ids[i-1][1]))

    # plotD([x[1] for x in idds])
    # plotD(idds)
    # cycleStartI = 18
    # cycleEndI = 53
    # computeValue(18, 53, [x[1] for x in ds], [x[1] for x in dss])
    computeValue(720, 2440, [x[1] for x in ds], [x[1] for x in dss])

findRepetition()

# X = np.array(X)
# x = X[:,0].reshape(-1,1)
# y = X[:,1]

# y = np.diff(y)
# windows = set()
# windowSize = 10
# for i in range(len(y)-windowSize):
#     window = tuple(y[i:i+windowSize])
#     if window in windows:
#         print(window, i)
#     else:
#         windows.add(window)

# fix, ax = plt.subplots()
# ax.plot(X[:,0], X[:,1])
# plt.show()
# print(res)
# model = LinearRegression()
# model.fit(x, y)
# print(model.score(x, y))
# print(model.coef_)
# print(model.intercept_)
# print(model.predict(np.array([[1000000000000], [2022]])))

