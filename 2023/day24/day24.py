import os
import re
import matplotlib.pyplot as plt
from sympy import symbols, solve, Eq, nsolve
import numpy as np
from scipy.optimize import minimize, differential_evolution


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        lines = f.read().splitlines()

    stones = []
    for line in lines:
        nums = [int(x) for x in re.findall(r"-?\d+", line)]

        pos = nums[0], nums[1], nums[2]
        velocity = nums[3], nums[4], nums[5]

        stones.append((pos, velocity))

    return stones

def intersect(x0,y0, vx,vy, x20, y20, v2x,v2y):
    x1 = x0+vx
    y1 = y0+vy
    x21 = x20 + v2x
    y21 = y20 + v2y
    k = (y0-y1) / (x0-x1)
    k2 = (y20-y21) / (x20 - x21)

    if k-k2 == 0:
        return None

    x = (-k2*x20 + y20 + k*x0 - y0) / (k-k2)

    y = k * x - k * x0 + y0

    t = (x-x0) / vx
    
    t2 = (x-x20) / v2x

    # happens in the past
    if t < 0 or t2 < 0:
        return None
    
    return x,y

def plot_stones():
    stones = parse_input()

    xs = []
    ys = []
    zs = []

    for stone in stones:
        ((x,y,z),(vx,vy,vz)) = stone
        xs.append(x)
        ys.append(y)
        zs.append(z)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xs,ys,zs)

    plt.show()

def part1():
    res = 0
    stones = parse_input()
    for i in range(len(stones)):
        for j in range(i+1, len(stones)):
            (x0,y0,z0), (vx,vy,vz) = stones[i]
            (x20,y20,z20), (v2x,v2y,v2z) = stones[j]

            xy = intersect(x0,y0, vx,vy, x20, y20, v2x,v2y)

            if xy is not None:
                least = 200000000000000
                most = 400000000000000
                x,y = xy
                if least <= x <= most and least <= y <= most:
                    res += 1
    print(res)


def part2():
    stones = parse_input()
    x = symbols("x")
    y = symbols("y")
    z = symbols("z")
    v1 = symbols("v1")
    v2 = symbols("v2")
    v3 = symbols("v3")

    eqs = []

    variables = [x,y,z,v1,v2,v3]

    # solve system of equations
    # not neccesary to use all stones as unique solution is found pretty easily
    for i, ((p1,p2,p3), (d1,d2,d3)) in enumerate(stones[:3]):
        t = symbols("t" + str(i))
        variables.append(t)

        eqs.append(Eq(x + v1 * t, p1 + d1 * t))
        eqs.append(Eq(y + v2 * t, p2 + d2 * t))
        eqs.append(Eq(z + v3 * t, p3 + d3 * t))


    res = solve(eqs, variables)
    print(res)



def solve_numeric():
    stones = parse_input()

    P = []
    D = []

    for pos, d in stones:
        P.append(pos)
        D.append(d)

    P = np.array(P)
    D = np.array(D)

    def f(x):
        """
        sum of shortest distance between line x and every other line
        """
        d = 0
        p0 = x[:3]
        d0 = x[3:]
        for i in range(len(P)):
            di = D[i]
            pi = P[i]
            n = np.cross(di, d0)
            d += abs(np.dot(n, (p0 - pi))) / np.linalg.norm(n)

        return d

    # plot_stones()

    res = minimize(f, np.array([0,0,0,1,1,-1]))
    print(res.x)
    print(f(res.x))

