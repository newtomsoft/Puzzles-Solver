from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatusOptimal, pulp

from Ports.SolverEngine import SolverEngine


class PulpSolverEngine(SolverEngine):
    def Or(self, *constraints):
        raise NotImplementedError

    def Implies(self, constraint1, constraint2):
        return (1 - constraint1) + constraint2 >= 1

    def If(self, constraint, value_if_true, value_if_false):
        return constraint * value_if_true + (1 - constraint) * value_if_false

    def has_constraints(self):
        return len(self.model.constraints) > 0

    def distinct(self, *param: LpVariable):
        for i in range(len(param)):
            for j in range(i + 1, len(param)):
                self.add(param[i] != param[j])

    def int(self, param):
        return LpVariable(name=param, lowBound=0, cat='Integer')

    def __init__(self, name="problem", sense=LpMaximize):
        self.model = LpProblem(name=name, sense=sense)
        self.variables = {}

    def bool(self, param):
        if param not in self.variables:
            self.variables[param] = LpVariable(name=param, cat='Binary')
        return self.variables[param]

    def sum(self, params):
        return lpSum([*params])

    def And(self, constraints):
        return lpSum(constraints) == len(constraints)

    def Not(self, constraint):
        return 1 - constraint

    def is_true(self, param):
        return param

    def add(self, constraint):
        self.model += constraint

    def has_solution(self):
        return self.model.solve(pulp.PULP_CBC_CMD(msg=False)) == LpStatusOptimal

    def model(self):
        return self.model

    def eval(self, expr: LpVariable):
        if expr.cat == 'Binary':
            return PulpBinary(expr.varValue)
        if expr.cat == 'Integer':
            return PulpInteger(expr.varValue)
        if expr.cat == 'Continuous':
            return expr.varValue
        return expr.varValue


class PulpInteger:
    def __init__(self, value: int):
        self.value = value

    def as_long(self):
        return int(self.value)


class PulpBinary:
    def __init__(self, value: bool):
        self.value = value

    def as_long(self):
        return int(self.value)


def solutions():
    has_solution = solver.has_solution()
    if not has_solution:
        print("No solution")
        return
    print("Solution found")
    print(f"x = {solver.eval(x).as_long()}")
    print(f"y = {solver.eval(y).as_long()}")


if __name__ == "__main__":
    solver = PulpSolverEngine(name="optimisation_simple", sense=LpMaximize)

    x = solver.int("x")
    y = solver.int("y")

    solver.add(x + y == 8)
    solver.add(x >= 3)
    solver.add(y >= 3)

    solutions()
    solver.add(lpSum([x == 4, y == 4]) >= 1)

    # solver.add(x >= 4)
    # solver.add(y >= 4)
    # solver.distinct(x, y)

    solutions()
