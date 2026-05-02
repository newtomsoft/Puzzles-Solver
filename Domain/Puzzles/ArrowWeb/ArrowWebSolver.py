from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class ArrowWebSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = grid.rows_number
        self._columns_number = grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._shaded_vars = []
        self._initialized = False
        self._previous_solution = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._shaded_vars = [[self._model.new_bool_var(f"shaded_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)]
        self._add_constraints()
        self._initialized = True

    def _add_constraints(self):
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                direction = self._grid[r, c]
                ray_positions = self._get_ray_positions(r, c, direction)
                ray_vars = [self._shaded_vars[p.r][p.c] for p in ray_positions]
                self._model.add(sum(ray_vars) == 1)

    def _get_ray_positions(self, r: int, c: int, direction: str) -> list[Position]:
        positions = []
        dr, dc = self._direction_delta(direction)
        nr, nc = r + dr, c + dc
        while 0 <= nr < self._rows_number and 0 <= nc < self._columns_number:
            positions.append(Position(nr, nc))
            nr += dr
            nc += dc
        return positions

    @staticmethod
    def _direction_delta(direction: str) -> tuple[int, int]:
        direction_map = {
            'u': (-1, 0),
            'd': (1, 0),
            'l': (0, -1),
            'r': (0, 1),
            'ru': (-1, 1),
            'rd': (1, 1),
            'lu': (-1, -1),
            'ld': (1, -1),
        }
        return direction_map.get(direction, (0, 0))

    def get_solution(self) -> Grid:
        if not self._initialized:
            self._init_model()
        status = self._solver.solve(self._model)
        if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return Grid.empty()
        solution = Grid([[self._solver.value(self._shaded_vars[r][c]) for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._previous_solution = solution
        return solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()
        diff_vars = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                val = self._previous_solution[r, c]
                b = self._model.new_bool_var(f"diff_{r}_{c}")
                if val == 1:
                    self._model.add(self._shaded_vars[r][c] == 0).only_enforce_if(b)
                    self._model.add(self._shaded_vars[r][c] == 1).only_enforce_if(b.negated())
                else:
                    self._model.add(self._shaded_vars[r][c] == 1).only_enforce_if(b)
                    self._model.add(self._shaded_vars[r][c] == 0).only_enforce_if(b.negated())
                diff_vars.append(b)
        self._model.add(sum(diff_vars) > 0)
        return self.get_solution()
