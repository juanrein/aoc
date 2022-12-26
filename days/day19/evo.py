from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM

from robotingTypes import BluePrint

def simulate(x, blueprint: BluePrint, totalTime):
    res = (0, 0, 0, 0)
    robots = (1, 0, 0, 0)
    overbudget = 0

    for i in range(totalTime):
        res = (res[0]+robots[0], res[1]+robots[1], res[2]+robots[2], res[3]+robots[3])
        if x[i] == 0: # no building
            pass
        elif x[i] == 1: # ore robot
            if res[0] - blueprint.oreRobotCost - robots[0] < 0:
                overbudget += blueprint.oreRobotCost - res[0] + robots[0]
                break
            res = (res[0]-blueprint.oreRobotCost, res[1], res[2], res[3])
            robots = (robots[0]+1, robots[1], robots[2], robots[3])

        elif x[i] == 2: # clay robot
            if res[0] - blueprint.clayRobotCost - robots[0] < 0:
                overbudget += blueprint.clayRobotCost - res[0] + robots[0]
                break
            res = (res[0]-blueprint.clayRobotCost, res[1], res[2], res[3])
            robots = (robots[0], robots[1]+1, robots[2], robots[3])
            
        elif x[i] == 3: # obsidian robot
            if res[0] - blueprint.obsidianRobotOreCost - robots[0] < 0:
                overbudget += blueprint.obsidianRobotOreCost - res[0] + robots[0]
            if res[1] - blueprint.obsidianRobotClayCost - robots[1] < 0:
                overbudget += blueprint.obsidianRobotClayCost - res[1] + robots[1]
            if overbudget > 0:
                break            

            res = (res[0]-blueprint.obsidianRobotOreCost, res[1] - blueprint.obsidianRobotClayCost, res[2], res[3])
            robots = (robots[0], robots[1], robots[2]+1, robots[3])

        elif x[i] == 4: # geode robot
            if res[0]-blueprint.geodeRobotOreCost - robots[0] < 0:
                overbudget += blueprint.geodeRobotOreCost - res[0] + robots[0]
            if res[2] - blueprint.geodeRobotObsidianCost - robots[2] < 0:
                overbudget += blueprint.geodeRobotObsidianCost - res[2] +  robots[2]
            if overbudget > 0:
                break
            res = (res[0]-blueprint.geodeRobotOreCost, res[1], res[2] - blueprint.geodeRobotObsidianCost, res[3])
            robots = (robots[0], robots[1], robots[2], robots[3]+1)
    if overbudget == 0:
        overbudget = -(res[0] + res[1] + res[2] + res[3])
        return {
            "geodes": res[3],
            "overbudget": overbudget
        }
    return {
        "geodes": 0,
        "overbudget": overbudget
    }

class RobotProblem(ElementwiseProblem):
    def __init__(self, blueprint: BluePrint, time):
        super().__init__(n_var=time, n_obj=1, n_ieq_constr=1, xl=0, xu=4)
        self.blueprint = blueprint
        self.time = time

    def _evaluate(self, x, out, *args, **kwargs):
        res = simulate(x, self.blueprint, self.time)
        out["F"] = -res["geodes"]
        out["G"] = res["overbudget"]
        
# print(simulate([0,0,2,0,2,0,2,0,0,0,3,2,0,0,3,0,0,4,0,0,4,0,0,0], getInput(True)[0], 24))

def optimalSolution3(blueprint: BluePrint, time):
    algorithm = GA(
        pop_size=100,
        sampling=IntegerRandomSampling(),
        crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
        eliminate_duplicates=True
    )
    problem = RobotProblem(blueprint, time)
    res = minimize(
        problem,
        algorithm,
        seed = 1,
        termination=("n_gen", 1000),
        verbose = False
    )

    print(res.X, res.F, res.G)
    return -round(res.F[0])