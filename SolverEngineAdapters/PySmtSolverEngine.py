from SolverEngine.SolverEngine import SolverEngine
from pysmt.shortcuts import Symbol, And, Not, Plus, Solver
from pysmt.typing import BOOL


class PysmtSolverEngine(SolverEngine):
    def __init__(self):
        self.solver = Solver()

    def bool(self, param):
        return Symbol(param, BOOL)

    def sum(self, param):
        return Plus(param)

    def And(self, constraints):
        return And(constraints)

    def Not(self, constraint):
        return Not(constraint)

    def is_true(self, param):
        return self.solver.get_value(param).is_true()

    def add(self, constraint):
        self.solver.add_assertion(constraint)

    def has_solution(self):
        return self.solver.solve()

    def model(self):
        return self.solver.get_model()

    def eval(self, expr):
        return self.solver.get_value(expr)
