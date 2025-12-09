from z3 import Solver, And, Not, sat, Bool, is_true

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver
from Domain.Puzzles.Slant.SlantGrid import SlantGrid


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

        self._previous_solution = self._ensure_no_loop()
        return self._previous_solution

    def get_other_solution(self) -> SlantGrid:
        if self._previous_solution == SlantGrid.empty():
            return SlantGrid.empty()

        blocking_clause = []
        for position, val in self._previous_solution:
            blocking_clause.append(self._grid_z3[position] == val)

        self._solver.add(Not(And(blocking_clause)))
        return self.get_solution()

    def _ensure_no_loop(self) -> SlantGrid:
        while self._solver.check() == sat:
            model = self._solver.model()
            cycle_found, blocking_constraints, solution_grid = self._find_loop_or_solution(model)

            if cycle_found:
                self._solver.add(Not(And(blocking_constraints)))
            else:
                return solution_grid

        return SlantGrid.empty()

    def _find_loop_or_solution(self, model) -> tuple[bool, list, SlantGrid]:
        current_grid = SlantGrid([[is_true(model[self._grid_z3[r][c]]) for c in range(self._columns_number)] for r in range(self._rows_number)])
        path_nodes = current_grid.get_first_cycle_path()
        if path_nodes:
            cycle_constraints = []

            for i in range(len(path_nodes) - 1):
                u = path_nodes[i]
                v = path_nodes[i+1]
                r1, c1 = u
                r2, c2 = v
                cell_r = min(r1, r2)
                cell_c = min(c1, c2)
                cell_z3 = self._grid_z3[cell_r][cell_c]
                is_backslash_edge = (r1 - r2) == (c1 - c2)
                cycle_constraints.append(cell_z3 == is_backslash_edge)

            return True, cycle_constraints, SlantGrid.empty()

        return False, [], current_grid

    def _add_constraints(self):
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
