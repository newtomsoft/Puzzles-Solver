from typing import Any

from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class AkariSolver(GameSolver):
    def __init__(self, data_game: dict[str, Any]):
        self._data_game = data_game
        self.rows_number = self._data_game['rows_number']
        self.columns_number = self._data_game['columns_number']
        self._black_cells = {Position(r, c) for r, c in self._data_game['black_cells']}
        self._number_constraints = {Position(r, c): v for (r, c), v in self._data_game['number_constraints'].items()}

        if self.rows_number < 7 or self.columns_number < 7:
            raise ValueError("Akari grid must be at least 7x7")

        self._solver = cp_model.CpSolver()
        self._model = cp_model.CpModel()
        self._bulbs_vars = None

    def get_solution(self) -> Grid:
        self._model = cp_model.CpModel()
        self._bulbs_vars = Grid([[self._model.NewBoolVar(f'bulb_{r}_{c}') if Position(r, c) not in self._black_cells else None
                                  for c in range(self.columns_number)]
                                 for r in range(self.rows_number)])

        self._add_constraints()

        status = self._solver.Solve(self._model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return self._compute_solution()

        return Grid.empty()

    def get_other_solution(self) -> Grid:
        raise NotImplementedError("This method is not yet implemented")

    def _compute_solution(self) -> Grid:
        solution_grid = Grid([[0] * self.columns_number for _ in range(self.rows_number)])
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                p = Position(r, c)
                if p not in self._black_cells:
                     if self._solver.BooleanValue(self._bulbs_vars[p]):
                          solution_grid[p] = 1
                     else:
                          solution_grid[p] = 0
                else:
                    solution_grid[p] = 0
        return solution_grid

    def _add_constraints(self):
        # 1. Number constraints
        for pos, number in self._number_constraints.items():
            neighbors = [n for n in self._bulbs_vars.neighbors_positions(pos) if n not in self._black_cells]
            self._model.Add(sum(self._bulbs_vars[n] for n in neighbors) == number)

        # Precompute segments
        # Horizontal segments
        h_segments = []
        cell_to_h_segment = {}
        for r in range(self.rows_number):
            current_segment = []
            for c in range(self.columns_number):
                p = Position(r, c)
                if p in self._black_cells:
                    if current_segment:
                        h_segments.append(current_segment)
                        current_segment = []
                else:
                    current_segment.append(p)
            if current_segment:
                h_segments.append(current_segment)

        for seg in h_segments:
            # Constraint: At most one bulb per segment
            self._model.Add(sum(self._bulbs_vars[p] for p in seg) <= 1)
            for p in seg:
                cell_to_h_segment[p] = seg

        # Vertical segments
        v_segments = []
        cell_to_v_segment = {}
        for c in range(self.columns_number):
            current_segment = []
            for r in range(self.rows_number):
                p = Position(r, c)
                if p in self._black_cells:
                    if current_segment:
                        v_segments.append(current_segment)
                        current_segment = []
                else:
                    current_segment.append(p)
            if current_segment:
                v_segments.append(current_segment)

        for seg in v_segments:
             self._model.Add(sum(self._bulbs_vars[p] for p in seg) <= 1)
             for p in seg:
                 cell_to_v_segment[p] = seg

        # 3. Coverage: Every white cell must be illuminated
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                p = Position(r, c)
                if p not in self._black_cells:
                    h_seg = cell_to_h_segment.get(p, [])
                    v_seg = cell_to_v_segment.get(p, [])
                    relevant_positions = set(h_seg) | set(v_seg)
                    self._model.Add(sum(self._bulbs_vars[rp] for rp in relevant_positions) >= 1)
