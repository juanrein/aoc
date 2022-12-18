import os
import itertools
import functools
from graph_f import makeGraph, makeWGraph, dijkstra, expandPaths, shortestPaths
from collections import deque
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.problems import get_problem
from pymoo.optimize import minimize
import numpy as np
from pymoo.core.problem import Problem
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.crossover.pntx import PointCrossover, SinglePointCrossover, TwoPointCrossover
import math

def getTestInput():
    return [
        "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
        "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
        "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
        "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
        "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
        "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
        "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
        "Valve HH has flow rate=22; tunnel leads to valve GG",
        "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
        "Valve JJ has flow rate=21; tunnel leads to valve II",
    ]


def getInput():
    fileName = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(fileName) as f:
        lines = f.read().splitlines()
    # lines = getTestInput()

    data = []

    for line in lines:
        parts = line.split("; ")
        a = parts[0][6:8]
        b = int(parts[0][23:])
        if "valves" in parts[1]:
            c = parts[1][23:].split(", ")
        else:
            c = [parts[1][22:]]
        data.append((a, b, c))
    return data


def explore3(graph, wgraph, start, time, visited, memo={}):
    memokey = (start, time, visited)
    if memokey in memo:
        return memo[memokey]
    if time <= 0:
        return 0
    best = 0
    for k in wgraph[start]["c"]:
        res1 = 0
        d = wgraph[start][k]
        if start not in visited:
            visitedC = tuple(sorted(visited + (start,)))
            amount1 = (time-1) * graph[start]["rate"]
            res1 = amount1 + explore3(graph, wgraph, k, time-d-1, visitedC)

        res2 = explore3(graph, wgraph, k, time-d, visited)
        best = max(best, res1, res2)

    memo[memokey] = best
    return memo[memokey]

def explore4(graph, wgraph, start1, start2, time1, time2, visited, memo={}):
    memokey = (start1, start2, time1, time2, visited)

    if memokey in memo:
        return memo[memokey]
    if time1 <= 2 and time2 <= 2:
        return 0
    amount = 0
    amount += (time1-1) * graph[start1]["rate"]
    amount += (time2-1) * graph[start2]["rate"]

    best = 0
    for k1, k2 in itertools.product(wgraph[start1]["c"], wgraph[start2]["c"]):
        res1 = 0
        if k1 not in visited and k2 not in visited:
            d1 = wgraph[start1][k1]
            d2 = wgraph[start2][k2]
            visitedC = tuple(sorted(visited + (start1, start2)))
            res1 = amount + explore4(graph, wgraph, k1, k2, time1 - d1-1, time2-d2-1, visitedC)

        best = max(best, res1)

    memo[memokey] = best
    return memo[memokey]

def isLegitPath(graph, current, x):
    if x[0]["name"] == current:
        return True
    return False


class RouteProblem(Problem):
    def __init__(self, graph):
        # openablePositions = []
        # for i,k in enumerate(graph):
        #     if graph[k]["rate"] != 0:
        #         openablePositions.append(i)
        super().__init__(n_var=len(graph), n_obj=1, n_ieq_constr=1, xl=0, xu=29)
        self.graph = graph
        self.rates = [graph[k]["rate"] for k in graph]
        # self.openablePositions = openablePositions

    def _evaluate(self, x, out, *args, **kwargs):
        res = []
        for xi in x:
            total = 0
            for i, xii in enumerate(xi):
                if xii > 0 and xii < 30:
                    total += self.rates[i] * xii
            res.append(total)
        con = []
        for xi in x:
            total = 0
            xis = []
            nodes = list(self.graph.keys())
            for i,t in enumerate(xi):
                xis.append({"name": nodes[i], "time": t})
            xis = sorted(xis, key=lambda x: x["time"], reverse=True)
            y = isLegitPath(self.graph, "AA", xis)
            if not y:
                total += 10
            if len(xi) != len(set(xi)):
                total += 10
            con.append(total)
        out["F"] = -np.array(res)
        out["G"] = np.array(con)


def explore(graph):
    problem = RouteProblem(graph)

    algorithm = GA(
        pop_size=100,
        eliminate_duplicates=True, 
        sampling=IntegerRandomSampling(), 
        crossover=TwoPointCrossover(), 
        mutation=BitflipMutation()
    )
    
    res = minimize(problem,
                   algorithm,
                   seed=1,
                   verbose=True)

    print("Best solution found: \nX = %s\nF = %s" % (res.X, -res.F))

def floydWarshall(data: list):
    N = len(data)
    # dist = [[math.inf for _ in range(N)] for _ in range(N)]
    dist = [[100000 for _ in range(N)] for _ in range(N)]
    rates = [k[1] for k in data]
    mapping = {k[0]: v for k,v in zip(data, range(N))}
    keys = [a for a,b,c in data]
    startI = keys.index("AA")
    for a,b,c in data:
        i = mapping[a]
        for k in c:
            j = mapping[k]
            dist[i][j] = 1
    for i in range(N):
        dist[i][i] = 0
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if i == j or i == k or j == k:
                    continue
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    unnessaryIs = [i for i in range(N) if rates[i] == 0 and i != startI]
    # unnessaryIs = [i for i in range(N) if rates[i] == 0]
    distF = []
    ratesF = []
    for i in range(N):
        if i in unnessaryIs:
            continue
        ratesF.append(rates[i])
        distFrow = []
        for j in range(N):
            if j in unnessaryIs:
                continue
            distFrow.append(dist[i][j])
        distF.append(distFrow)
    startII = startI - len([i for i in unnessaryIs if i < startI])

    return distF, ratesF, startII

def solutions(data):
    distF, ratesF, startII = floydWarshall(data)
    @functools.lru_cache(maxsize=None)
    def compute(start: int, time: int, visited: tuple):
        if time <= 0 or len(visited) == len(distF):
            return 0
        best = 0
        score = (time) * ratesF[start]
        for i in range(len(distF)):
            if i == start:
                continue
            if i not in visited:
                visitedC = tuple(sorted(visited + (i, )))
                val = compute(i, time-1-distF[start][i], visitedC)
                best = max(best, score + val)
        return best

    @functools.lru_cache(maxsize=None)
    def compute2(start1, start2, time1, time2, visited):
        if time1 <= 2 and time2 <= 2 or len(visited) == len(distF):
            return 0

        best = 0
        score = (time1-1) * ratesF[start1] + (time2-1) * ratesF[start2]

        rest1 = filter(lambda x: x not in visited and time1 - distF[start1][x] > 0, range(len(distF)))
        rest2 = filter(lambda x: x not in visited and time2 - distF[start2][x] > 0, range(len(distF)))
        for i,j in itertools.product(rest1, rest2):
            if i == j:
                continue
            visitedC = tuple(sorted(visited + (i, j)))
            val = compute2(i, j, time1-distF[start1][i]-1, time2-distF[start2][j]-1, visitedC)
            best = max(best, score + val)
                
        return best

    def createPaths(start, time, visited):
        if len(visited) == len(distF):
            return [visited]

        # is there any move to make that is feasible in given time
        minEffort = min([d for i,d in enumerate(distF[start]) if i not in visited])
        # if time <= 2 or len(visited) == len(distF):
        if time <= minEffort+2:
            return [visited]

        movable = []
        for i in range(len(distF)):
            if i in visited:
                continue
            d = distF[start][i]
            # opening takes one minute
            timeLeft = time - d - 1
            visitedC = visited + [i]
            if timeLeft > 1:
                movable.append((i,timeLeft, visitedC))
        res = []
        for m,t,v in movable:
            p = createPaths(m, t, v)
            for pi in p:
                res.append(pi)
        return res

    def getPathScore(p, maxTime):
        time = maxTime
        score = 0
        for i in range(1, len(p)):
            d = distF[p[i-1]][p[i]]
            time = time - d - 1
            score += time * ratesF[p[i]]
        return score

    def computeScore(paths, maxTime):
        best = 0
        bestPath = None
        for p in paths:
            time = maxTime
            score = 0
            for i in range(1, len(p)):
                d = distF[p[i-1]][p[i]]
                time = time - d - 1
                score += time * ratesF[p[i]]
            if score > best:
                best = score
                bestPath = p

        return best, bestPath

    def createPaths2(start1: int, start2: int, time1: int, time2: int, visited: list):
        if len(visited) == len(distF):
            return [visited]
        if time1 <= 2 and time2 <= 2:
            return [visited]
        # is there any move to make that is feasible in given time
        minEffort1 = min([d for i,d in enumerate(distF[start1]) if i not in visited])
        minEffort2 = min([d for i,d in enumerate(distF[start2]) if i not in visited])
        if time1 <= minEffort1+2 and time2 <= minEffort2+2:
            return [visited]
        if time1 <= minEffort1+2:
            return [visited]
            # return createPaths(start2, time2, visited)
        if time2 <= minEffort2+2:
            return [visited]
            # return createPaths(start1, time1, visited)

        movable = []
        for i in range(len(distF)):
            if i in visited:
                    continue
            for j in range(len(distF)):
                if j in visited:
                    continue
                if i == j:
                    continue
                d1 = distF[start1][i]
                d2 = distF[start2][j]
                # opening takes one minute
                timeLeft1 = time1 - d1 - 1
                timeLeft2 = time2 - d2 - 1
                visitedC = visited + [i, j]
                #maybe should be >=
                if timeLeft1 > 1 and timeLeft2 > 1:
                    movable.append((i,j, timeLeft1, timeLeft2, visitedC))
        res = []
        for m1,m2, t1, t2, v in movable:
            p = createPaths2(m1, m2, t1, t2, v)
            for pi in p:
                res.append(pi)
        return res

    def computeScore2(paths, maxTime):
        print("begin compute score with paths len", len(paths))
        best = 0
        for p in paths:
            time1 = maxTime
            time2 = maxTime
            score = 0
            for i in range(1, len(p)):
                d1 = distF[p[i-1][0]][p[i][0]]
                d2 = distF[p[i-1][1]][p[i][1]]
                time1 = time1 - d1 - 1
                time2 = time2 - d2 - 1
                score += time1 * ratesF[p[i][0]] + time2 * ratesF[p[i][1]]
            best = max(best, score)
        return best


    # paths = createPaths(startII, 30, [startII])
    # bestScore, bestPath = computeScore(paths, 30)
    # print(bestScore, bestPath)
    # paths = createPaths(startII, 26, [startII])
    # print(len(paths))
    # bestScore = 0
    # amount = 0
    # for p in paths:
    #     for p2 in paths:
    #         amount += 1
    #         if amount % 1_000_000 == 0:
    #             print(amount)
    #         visited: set[int] = set()
    #         time1 = 26
    #         time2 = 26
    #         score = 0
    #         i = 1
    #         j = 1
    #         while True:
    #             if i >= len(p) and j >= len(p2) or len(visited) == len(distF):
    #                 break
    #             if i < len(p):
    #                 if p[i] not in visited:
    #                     time1 = time1 - distF[p[i-1]][p[i]] - 1
    #                     score += (time1 * ratesF[p[i]])
    #                     visited.add(p[i])
    #                 i += 1
    #             if j < len(p2):
    #                 if p2[j] not in visited:
    #                     time2 = time2 - distF[p2[j-1]][p2[j]] - 1
    #                     score += (time2 * ratesF[p2[j]])
    #                     visited.add(p2[j])
    #                 j += 1

    #         if bestScore < score:
    #             bestScore = score
    # print(bestScore)
    # paths = createPaths2(startII, startII, 26, 26, [startII])
    # bestScore = 0
    # for p in paths:
    #     time1 = 26
    #     time2 = 26
    #     p1 = [p[0]] + list(range(1, len(p), 2))
    #     p2 = [p[0]] + list(range(2, len(p), 2))
    #     score = 0
    #     for i in range(1, len(p1)):
    #         d1 = distF[p1[i-1]][p1[i]]
    #         d2 = distF[p2[i-1]][p2[i]]
    #         time1 = time1 - d1 - 1
    #         time2 = time2 - d2 - 1
    #         score += time1 * ratesF[p1[i]]
    #         score += time2 * ratesF[p2[i]]
    #     bestScore = max(bestScore, score)

    # print(bestScore)
    # paths = createPaths2(startII, startII, 26, 26, [startII], [startII])
    # bestScore2 = computeScore2(paths, 26)
    # print(bestScore2)
    # res = compute(startII, 30, (startII, ))
    # res = compute(startII, 30, ()) #1421
    # res = compute2(startII, startII, 26, 26, (startII,))
    # return res
def solver(data):
    distF, ratesF, startII = floydWarshall(data)
    @functools.cache
    def pairCompute(start1, start2, time1, time2, visited):
        bestScore = 0
        for i in range(len(distF)):
            if i in visited:
                continue
            visitedC = tuple(sorted(visited + (i,)))
            if start1 != i and time1 - distF[start1][i] >= 1:
                timeLeft = time1 - distF[start1][i] - 1
                score = timeLeft * ratesF[i] + pairCompute(i, start2, timeLeft, time2, visitedC)
                bestScore = max(bestScore, score)
            if start2 != i and time2 - distF[start2][i] >= 1:
                timeLeft = time2 - distF[start2][i] - 1
                score = timeLeft * ratesF[i] + pairCompute(start1, i, time1, timeLeft, visitedC)
                bestScore = max(bestScore, score)

        return bestScore

    res = pairCompute(startII, startII, 26, 26, ())
    return res

def solve(data):
    return solver(data)
    # score = floydWarshall(data)
    # return score
    # graph = makeGraph(data)
    # explore(graph)
    # wgraph = makeWGraph(graph)
    # expanded = expandPaths(shortestPaths(graph))
    # res = explore3(graph, wgraph, "AA", 30, ())
    # print(adjacent)
    # return res
    # paths = expandPaths(shortestPaths(graph))
    # print(paths)
    # return explore(graph, "AA", 30, (), getCountOpenable(graph))
    # return explore4(graph, wgraph, "AA", "AA", 26, 26, ("AA", ))
    # return explore2(graph, "AA", "AA", 26, 26, (), getCountOpenable(graph))
    # paths = shortestPaths(graph)
    # expanded = expandPaths(paths)
    # return res


def main():
    data = getInput()
    res = solve(data)
    print(res)
    # 2474 too low


main()
