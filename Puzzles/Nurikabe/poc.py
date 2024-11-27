from z3 import *

# Définir les variables booléennes
a = Bool('a')
b = Bool('b')
c = Bool('c')

# Créer un solveur
solver = Solver()

# Ajouter des contraintes avec des noms
solver.assert_and_track(a, "constraint_a_true")
solver.assert_and_track(Not(b), "constraint_b_false")
solver.assert_and_track(Or(a, c), "constraint_a_or_c")
solver.assert_and_track(And(b, c), "constraint_b_and_c")



# Vérifier la satisfaisabilité
if solver.check() == sat:
    print("Satisfiable!")
    print(solver.model())
else:
    print("Unsatisfiable!")
    print("Unsat core:", solver.unsat_core())
