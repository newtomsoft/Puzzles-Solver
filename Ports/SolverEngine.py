from abc import ABC, abstractmethod


class SolverEngine(ABC):
    @abstractmethod
    def has_solution(self):
        pass

    @abstractmethod
    def model(self):
        pass

    @abstractmethod
    def add(self, constraint):
        pass

    @abstractmethod
    def Not(self, constraint):
        pass

    @abstractmethod
    def And(self, *constraints):
        pass

    @abstractmethod
    def Or(self, *constraints):
        pass

    @abstractmethod
    def sum(self, param):
        pass

    @abstractmethod
    def distinct(self, *param):
        pass

    @abstractmethod
    def Implies(self, constraint1, constraint2):
        pass

    @abstractmethod
    def bool(self, param):
        pass

    @abstractmethod
    def int(self, param):
        pass

    @abstractmethod
    def eval(self, expr):
        pass

    @abstractmethod
    def is_true(self, param):
        pass

    @abstractmethod
    def If(self, constraint, value_if_true, value_if_false):
        pass

    @abstractmethod
    def has_constraints(self):
        pass
