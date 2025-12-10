from z3 import Solver, And, Not, sat, Bool, is_true

from Domain.Board.Grid import Grid
from Domain.Board.SlantGrid import SlantGrid
from Domain.Puzzles.GameSolver import GameSolver


class SlantSolver(GameSolver):
    empty = None

    def __init__(self, clues_grid: Grid):
        self._clues_grid = clues_grid
        self._rows_number = clues_grid.rows_number - 1
        self._columns_number = clues_grid.columns_number - 1
        self._solver = Solver()
        self._grid_z3 = SlantGrid.empty()
        self._previous_solution = SlantGrid.empty()

    def _init_solver(self):
        self._grid_z3 = SlantGrid([[Bool(f'cell_{r}_{c}') for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> SlantGrid:
        if not self._solver.assertions():
            self._init_solver()

        self._previous_solution, _ = self._ensure_no_loop()
        return self._previous_solution

    def get_other_solution(self) -> SlantGrid:
        if self._previous_solution == SlantGrid.empty():
            return SlantGrid.empty()

        blocking_clause = []
        for position, val in self._previous_solution:
            blocking_clause.append(self._grid_z3[position] == val)

        self._solver.add(Not(And(blocking_clause)))
        return self.get_solution()

    def _ensure_no_loop(self) -> tuple[SlantGrid, int]:
        attempt_count = 0
        while self._solver.check() == sat:
            attempt_count += 1
            model = self._solver.model()
            current_grid = SlantGrid([[is_true(model[self._grid_z3[r][c]]) for c in range(self._columns_number)] for r in range(self._rows_number)])

            loops = current_grid.get_all_loops()
            if len(loops) == 0:
                print ("Solved after", attempt_count, "attempts")
                return current_grid, attempt_count

            for loop in loops:
                loop_constraint = And([self._grid_z3[position] == current_grid[position] for position in loop])
                self._solver.add(Not(loop_constraint))

        return SlantGrid.empty(), attempt_count

    def _add_constraints(self):
        self._add_clues_constraints()
        self._add_not_minimal_loop_constraint()

    def _add_clues_constraints(self):
        for position, clue in [(position, clue) for position, clue in self._clues_grid if clue != self.empty] :
            connections = []
            if (up_left:=position.up_left) in self._grid_z3:
                connections.append(self._grid_z3[up_left])
            if (up:=position.up) in self._grid_z3:
                connections.append(Not(self._grid_z3[up]))
            if (left:=position.left) in self._grid_z3:
                connections.append(Not(self._grid_z3[left]))
            if position in self._grid_z3:
                connections.append(self._grid_z3[position])

            self._solver.add(sum(connections) == clue)

    def _add_not_minimal_loop_constraint(self):
        for position, value in [(position, value) for position, value in self._grid_z3 if position not in self._grid_z3.edge_down_positions() + self._grid_z3.edge_right_positions()]:
            up_left = self._grid_z3[position] == SlantGrid.slash
            up_right = self._grid_z3[position.right] == SlantGrid.backslash
            down_left = self._grid_z3[position.down] == SlantGrid.backslash
            down_right = self._grid_z3[position.down_right] == SlantGrid.slash
            self._solver.add(Not(And(up_left, up_right, down_left, down_right)))
