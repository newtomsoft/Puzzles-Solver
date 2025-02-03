from SolverEngine.SolverEngine import SolverEngine
from pyomo.environ import ConcreteModel, Var, Constraint, SolverFactory, Objective, maximize


class PyomoSolverEngine(SolverEngine):
    def __init__(self):
        self.model = ConcreteModel()
        self.solver = SolverFactory('glpk')

    def sum(self, param):
        return sum(param)

    def And(self, constraints):
        return all(constraints)

    def is_true(self, param):
        return self.model.component(param).value == 1

    def add(self, constraint):
        self.model.add_component(f'constraint_{len(self.model.component_map(Constraint))}', Constraint(expr=constraint))

    def has_solution(self):
        result = self.solver.solve(self.model)
        return result.solver.termination_condition == 'optimal'

    def model(self):
        return self.model

    def eval(self, expr):
        return expr()

    def push(self):
        pass  # Pyomo does not support push/pop

    def pop(self):
        pass  # Pyomo does not support push/pop

    def reset(self):
        self.model = ConcreteModel()

    def __str__(self):
        return str(self.model)

    def __repr__(self):
        return repr(self.model)


if __name__ != '__main__':
    exit()



# Création du modèle
model = ConcreteModel()

# Variables de décision
model.x = Var(within=NonNegativeReals)
model.y = Var(within=NonNegativeReals)

# Fonction objectif : Max z = 3x + 5y
model.obj = Objective(expr=3*model.x + 5*model.y, sense=maximize)

# Contraintes
model.constraint1 = Constraint(expr=2*model.x + 3*model.y <= 12)
model.constraint2 = Constraint(expr=model.x + model.y <= 5)

# Résolution avec un solveur (nécessite un solveur comme CBC ou GLPK)
solver = SolverFactory('glpk')
result = solver.solve(model)

# Affichage des résultats
print(f"x = {model.x.value}")
print(f"y = {model.y.value}")
print(f"Valeur objective = {model.obj()}")
