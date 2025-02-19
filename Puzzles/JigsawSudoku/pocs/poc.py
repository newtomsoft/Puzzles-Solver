from z3 import Solver, Int, Distinct, And, sat

class SudokuSolver:
    """Classe de base abstraite pour les solveurs de Sudoku"""
    def __init__(self):
        self.solver = Solver()
        self.grid = [[Int(f'cell_{r}_{c}') for c in range(9)] for r in range(9)]
        self._add_basic_constraints()

    def _add_basic_constraints(self):
        """Ajoute les contraintes de base communes à tous les Sudokus"""
        for r in range(9):
            for c in range(9):
                self.solver.add(And(self.grid[r][c] >= 1, self.grid[r][c] <= 9))

        for r in range(9):
            self.solver.add(Distinct(self.grid[r]))

        for c in range(9):
            self.solver.add(Distinct([self.grid[r][c] for r in range(9)]))

    def solve(self):
        """Méthode template pour la résolution"""
        if self.solver.check() == sat:
            return self._extract_solution()
        raise ValueError("Pas de solution trouvée")

    def _extract_solution(self):
        """Extrait la solution du modèle (à implémenter par les sous-classes)"""
        raise NotImplementedError

class JigsawSudokuSolver(SudokuSolver):
    """Implémentation spécifique pour les Jigsaw Sudoku"""
    def __init__(self, regions):
        super().__init__()
        self.regions = regions
        self._add_jigsaw_constraints()

    def _add_jigsaw_constraints(self):
        """Ajoute les contraintes spécifiques au Jigsaw Sudoku"""
        for region in self.regions:
            self.solver.add(Distinct([self.grid[r][c] for (r, c) in region]))

    def _extract_solution(self):
        """Extrait la solution du modèle Z3"""
        model = self.solver.model()
        return [[model[self.grid[r][c]].as_long() for c in range(9)] for r in range(9)]

# Exemple d'utilisation
if __name__ == "__main__":
    # Définition des régions (exemple simplifié)
    regions = [
        # Région 0 (exemple de forme arbitraire)
        [(0,0), (0,1), (0,2), (1,0), (1,1), (2,0), (2,1), (3,0), (3,1)],
        # Ajouter ici les 8 autres régions...
    ]

    try:
        solver = JigsawSudokuSolver(regions)
        solution = solver.solve()
        for row in solution:
            print(row)
    except ValueError as e:
        print(e)