from z3 import z3

from Ports.SolverEngine import SolverEngine


class Z3SolverEngine(SolverEngine):
    def has_constraints(self):
        return self.solver.assertions()

    def If(self, constraint, value_if_true, value_if_false):
        return z3.If(constraint, value_if_true, value_if_false)

    def Or(self, *constraints):
        return z3.Or(*constraints)

    def Implies(self, constraint1, constraint2):
        return z3.Implies(constraint1, constraint2)

    def distinct(self, *param):
        return z3.Distinct(*param)

    def __init__(self):
        self.solver = z3.Solver()

    def int(self, param):
        return z3.Int(param)

    def bool(self, param):
        return z3.Bool(param)

    def sum(self, param):
        return z3.Sum(param)

    def And(self, *constraints):
        return z3.And(*constraints)

    def Not(self, constraint):
        return z3.Not(constraint)

    def is_true(self, param) -> bool:
        return z3.is_true(param)

    def add(self, constraint):
        self.solver.add(constraint)

    def has_solution(self):
        check = self.solver.check()
        return False if check == z3.unsat else check

    def model(self):
        return self.solver.model()

    def eval(self, expr):
        return self.solver.model().eval(expr)
