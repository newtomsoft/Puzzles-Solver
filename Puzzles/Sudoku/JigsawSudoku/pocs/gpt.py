from typing import List, Dict, Tuple, Set

from z3 import Int, Solver, And, Distinct, sat


class JigsawSudokuBoard:
    def __init__(self, givens: Dict[Tuple[int, int], int], regions: List[Set[Tuple[int, int]]]):
        self.size = 9
        self.givens = givens
        self.regions = regions

    def get_region_cells(self, region_id: int) -> Set[Tuple[int, int]]:
        return self.regions[region_id]

    def get_all_region_ids(self) -> List[int]:
        return list(range(len(self.regions)))


class SudokuConstraintBuilder:
    def __init__(self, board: JigsawSudokuBoard):
        self.board = board

    def build(self, grid: List[List[Int]], solver: Solver) -> None:
        size = self.board.size

        for i in range(size):
            for j in range(size):
                solver.add(And(grid[i][j] >= 1, grid[i][j] <= size))

        for i in range(size):
            solver.add(Distinct(grid[i]))

        for j in range(size):
            solver.add(Distinct([grid[i][j] for i in range(size)]))

        for region_id in self.board.get_all_region_ids():
            cells = self.board.get_region_cells(region_id)
            if all(0 <= i < size and 0 <= j < size for (i, j) in cells):  # Vérification validité
                solver.add(Distinct([grid[i][j] for (i, j) in cells]))

        for (i, j), value in self.board.givens.items():
            solver.add(grid[i][j] == value)


class JigsawSudokuSolver:
    def __init__(self, board: JigsawSudokuBoard, constraint_builder: SudokuConstraintBuilder):
        self.board = board
        self.constraint_builder = constraint_builder

    def solve(self) -> List[List[int]]:
        size = self.board.size
        solver = Solver()
        grid = [[Int(f"cell_{i}_{j}") for j in range(size)] for i in range(size)]

        self.constraint_builder.build(grid, solver)

        if solver.check() == sat:
            model = solver.model()
            return [[model.evaluate(grid[i][j]).as_long() for j in range(size)] for i in range(size)]
        else:
            raise Exception("Aucune solution trouvée.")


def print_solution(solution: List[List[int]]) -> None:
    for row in solution:
        print(" ".join(str(val) for val in row))


# --- Définition des régions corrigées ---
regions = [
    {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)},
    {(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (2, 3), (2, 4), (3, 3), (3, 4)},
    {(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (2, 6), (2, 7), (3, 6), (3, 7)},
    {(1, 2), (1, 5), (1, 8), (2, 2), (2, 5), (2, 8), (3, 2), (3, 5), (3, 8)},
    {(4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (6, 0), (6, 1), (7, 0), (7, 1)},
    {(4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (6, 3), (6, 4), (7, 3), (7, 4)},
    {(4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (6, 6), (6, 7), (7, 6), (7, 7)},
    {(5, 2), (5, 5), (5, 8), (6, 2), (6, 5), (6, 8), (7, 2), (7, 5), (7, 8)},
    {(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)}
]

# Quelques valeurs données
givens = {
    (0, 0): 5, (1, 3): 6, (2, 7): 9, (3, 8): 4, (4, 4): 7, (5, 1): 2, (6, 5): 8, (7, 6): 3, (8, 8): 1
}

# Instanciation des objets
board = JigsawSudokuBoard(givens, regions)
constraint_builder = SudokuConstraintBuilder(board)
solver = JigsawSudokuSolver(board, constraint_builder)

try:
    solution = solver.solve()
    print("\nSolution du Jigsaw Sudoku :")
    print_solution(solution)
except Exception as e:
    print(f"Erreur : {e}")
