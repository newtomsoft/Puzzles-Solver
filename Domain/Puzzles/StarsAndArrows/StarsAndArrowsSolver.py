from typing import Callable

from z3 import Solver, Not, And, unsat, Bool, is_true

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class StarsAndArrowsSolver(GameSolver):
    def __init__(self, grid: Grid, counts: dict[str, list[int]]):
        self._input_grid = grid
        self._counts_by_edge: dict[str, list[int]] = counts
        self.rows_number = grid.rows_number
        self.columns_number = grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._previous_solution = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Bool(f"cell{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        solution = Grid([[1 if is_true(model.eval(self._grid_z3[r][c])) else 0 for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        constraints = []
        for position, value in self._previous_solution:
            constraints.append(self._grid_z3[position] if value else Not(self._grid_z3[position]))
        self._solver.add(Not(And(constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_columns_count_constraints()
        self._add_rows_count_constraints()
        self._add_one_and_only_one_star_following_each_arrow_constraints()

    def _add_columns_count_constraints(self):
        for c, count in enumerate(self._counts_by_edge['up']):
            if count == -1:
                continue
            self._solver.add(sum([self._grid_z3[Position(r, c)] for r in range(self.rows_number)]) == count)

    def _add_rows_count_constraints(self):
        for r, count in enumerate(self._counts_by_edge['left']):
            if count == -1:
                continue
            self._solver.add(sum([self._grid_z3[Position(r, c)] for c in range(self.columns_number)]) == count)

    def _add_one_and_only_one_star_following_each_arrow_constraints(self) -> None:
        direction_all_positions: dict[str, Callable[[Grid, Position], list[Position]]] = {
            '↓': lambda grid, pos: grid.all_positions_down(pos),
            '↑': lambda grid, pos: grid.all_positions_up(pos),
            '→': lambda grid, pos: grid.all_positions_right(pos),
            '←': lambda grid, pos: grid.all_positions_left(pos),
            '↗': lambda grid, pos: grid.all_positions_up_right(pos),
            '↘': lambda grid, pos: grid.all_positions_down_right(pos),
            '↙': lambda grid, pos: grid.all_positions_down_left(pos),
            '↖': lambda grid, pos: grid.all_positions_up_left(pos),
        }

        seen_counts: dict[Position, int] = {}
        for array_position, array_value in [(position, value) for position, value in self._input_grid if value != '']:
            positions_following_array_fct = direction_all_positions.get(array_value)
            positions_following_array = positions_following_array_fct(self._grid_z3, array_position)
            self._add_one_and_only_one_star_for_following_array_positions_constraint(positions_following_array)

            for position in [pos for pos in positions_following_array if self._input_grid[pos] == '']:
                seen_counts[position] = seen_counts.get(position, 0) + 1

        for position, cnt in seen_counts.items():
            if cnt != 1:
                self._add_no_star_for_multiple_target_arrow_constraint(position)

        for not_following_array_position in [position for position, _ in self._input_grid if position not in seen_counts]:
            self._add_no_star_for_following_neither_array_constraints(not_following_array_position)

    def _add_no_star_for_following_neither_array_constraints(self, positions):
        self._solver.add(Not(self._grid_z3[positions]))

    def _add_no_star_for_multiple_target_arrow_constraint(self, position):
        self._solver.add(Not(self._grid_z3[position]))

    def _add_one_and_only_one_star_for_following_array_positions_constraint(self, positions):
        self._solver.add(sum([self._grid_z3[position] for position in positions]) == 1)
