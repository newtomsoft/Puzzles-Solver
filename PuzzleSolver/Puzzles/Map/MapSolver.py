from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.GameSolver import GameSolver

red = 1
yellow = 2
green = 3
brown = 4


class MapSolver(GameSolver):
    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self._model = cp_model.CpModel()
        self._grid_z3: Grid | None = None
        self._previous_solution: Grid | None = None
        self.neighbours = None
        self._region_z3: list = []
        self._counter = 0

    def get_solution(self) -> Grid:
        self._region_z3 = [self._model.NewIntVar(1, 4, f"regions_{i}") for i in range(20)]
        self.neighbours = self._get_neighbours()
        self._add_constraints()

        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        bs = []
        for position, value in self._previous_solution:
            b = self._model.NewBoolVar(f"block_{self._counter}")
            self._counter += 1
            self._model.Add(self._grid_z3[position] == value).OnlyEnforceIf(b)
            self._model.Add(self._grid_z3[position] != value).OnlyEnforceIf(b.Not())
            bs.append(b)
        self._model.Add(sum(bs) <= len(bs) - 1)
        self._previous_solution = self._compute_solution()
        return self._previous_solution

    def _compute_solution(self) -> Grid:
        if self._solver.Solve(self._model) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return Grid.empty()

        return Grid([[0]])

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_neighbours_constraints()

    def _get_neighbours(self):
        return {
            self._region_z3[0]: [self._region_z3[1], self._region_z3[4], self._region_z3[6]],
            self._region_z3[1]: [self._region_z3[0], self._region_z3[2], self._region_z3[4], self._region_z3[5]],
            self._region_z3[2]: [self._region_z3[1], self._region_z3[3], self._region_z3[5], self._region_z3[7], self._region_z3[8], self._region_z3[10]],
            self._region_z3[3]: [self._region_z3[2], self._region_z3[8], self._region_z3[12]],
            self._region_z3[4]: [self._region_z3[0], self._region_z3[1], self._region_z3[5], self._region_z3[6], self._region_z3[7]],
            self._region_z3[5]: [self._region_z3[1], self._region_z3[2], self._region_z3[4], self._region_z3[7]],
            self._region_z3[6]: [self._region_z3[0], self._region_z3[4], self._region_z3[9]],
            self._region_z3[7]: [self._region_z3[2], self._region_z3[4], self._region_z3[5], self._region_z3[9], self._region_z3[10], self._region_z3[13], self._region_z3[17], self._region_z3[18]],
            self._region_z3[8]: [self._region_z3[2], self._region_z3[3], self._region_z3[11]],
            self._region_z3[9]: [self._region_z3[6], self._region_z3[7], self._region_z3[13]],
            self._region_z3[10]: [self._region_z3[2], self._region_z3[7], self._region_z3[11], self._region_z3[14], self._region_z3[19]],
            self._region_z3[11]: [self._region_z3[8], self._region_z3[10], self._region_z3[12], self._region_z3[14]],
            self._region_z3[12]: [self._region_z3[3], self._region_z3[11], self._region_z3[15]],
            self._region_z3[13]: [self._region_z3[7], self._region_z3[9], self._region_z3[16]],
            self._region_z3[14]: [self._region_z3[10], self._region_z3[11], self._region_z3[15], self._region_z3[19]],
            self._region_z3[15]: [self._region_z3[12], self._region_z3[14]],
            self._region_z3[16]: [self._region_z3[13], self._region_z3[17]],
            self._region_z3[17]: [self._region_z3[7], self._region_z3[16], self._region_z3[18]],
            self._region_z3[18]: [self._region_z3[7], self._region_z3[17], self._region_z3[19]],
            self._region_z3[19]: [self._region_z3[10], self._region_z3[14], self._region_z3[18]],
        }

    def _add_initial_constraints(self):
        for i in range(20):
            self._model.Add(self._region_z3[i] >= red)
            self._model.Add(self._region_z3[i] <= brown)
        self._model.Add(self._region_z3[0] == green)
        self._model.Add(self._region_z3[3] == yellow)
        self._model.Add(self._region_z3[6] == red)
        self._model.Add(self._region_z3[8] == brown)
        self._model.Add(self._region_z3[9] == brown)
        self._model.Add(self._region_z3[11] == green)
        self._model.Add(self._region_z3[12] == red)
        self._model.Add(self._region_z3[14] == brown)
        self._model.Add(self._region_z3[15] == green)
        self._model.Add(self._region_z3[16] == green)
        self._model.Add(self._region_z3[18] == red)
        self._model.Add(self._region_z3[19] == green)

    def _add_neighbours_constraints(self):
        for region, neighbours in self.neighbours.items():
            for neighbour in neighbours:
                self._model.Add(region != neighbour)
