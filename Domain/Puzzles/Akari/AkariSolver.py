from typing import Any

from z3 import Bool, Solver, sat, is_true, Not, Implies, Or

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
        self._solver = Solver()
        self._illuminated_z3: Grid = Grid.empty()
        self._bulbs_z3: Grid = Grid.empty()

    def get_solution(self) -> Grid:
        self._bulbs_z3 = Grid([[Bool(f'bulb_{r}_{c}') for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._illuminated_z3 = Grid([[Bool(f'illuminated_{r}_{c}') for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        if not self._solver.check() == sat:
            return Grid.empty()

        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        raise NotImplementedError("This method is not yet implemented")

    def _compute_solution(self) -> Grid:
        model = self._solver.model()
        solution_grid = Grid([[None] * self.columns_number for _ in range(self.rows_number)])
        for position, var in self._bulbs_z3:
            solution_grid[position] = 1 if is_true(model.eval(var)) else 0
        return solution_grid

    def _add_constraints(self):
        self._add_numbers_constraints()
        self._add_black_cells_constraints()
        self._add_light_constraints()
        self._add_bulbs_constraints()

    def _add_numbers_constraints(self):
        for position, number in self._number_constraints.items():
            adjacent_bulbs = [self._bulbs_z3[neighbor] for neighbor in self._bulbs_z3.neighbors_positions(position) if neighbor not in self._black_cells]
            constraint = sum([adjacent_bulb for adjacent_bulb in adjacent_bulbs]) == number
            self._solver.add(constraint)

    def _add_black_cells_constraints(self):
        for position in self._black_cells:
            self._solver.add(Not(self._bulbs_z3[position]))
            self._solver.add(Not(self._illuminated_z3[position]))

    def _add_light_constraints(self):
        for position, bulb_var in self._bulbs_z3:
            if position in self._black_cells:
                continue
            light_constraints = [bulb_var]

            # Up
            current = self._bulbs_z3.neighbor_up(position)
            while current and current not in self._black_cells:
                light_constraints.append(self._bulbs_z3[current])
                current = self._bulbs_z3.neighbor_up(current)

            # Down
            current = self._bulbs_z3.neighbor_down(position)
            while current and current not in self._black_cells:
                light_constraints.append(self._bulbs_z3[current])
                current = self._bulbs_z3.neighbor_down(current)

            # Left
            current = self._bulbs_z3.neighbor_left(position)
            while current and current not in self._black_cells:
                light_constraints.append(self._bulbs_z3[current])
                current = self._bulbs_z3.neighbor_left(current)

            # Right
            current = self._bulbs_z3.neighbor_right(position)
            while current and current not in self._black_cells:
                light_constraints.append(self._bulbs_z3[current])
                current = self._bulbs_z3.neighbor_right(current)

            constraint = self._illuminated_z3[position] == Or(light_constraints)
            self._solver.add(constraint)
            self._solver.add(self._illuminated_z3[position])

    def _add_bulbs_constraints(self):
        for position, bulb_var in self._bulbs_z3:
            if position not in self._black_cells:
                constraints = []

                # Up
                current = self._bulbs_z3.neighbor_up(position)
                while current and current not in self._black_cells:
                    constraints.append(Implies(bulb_var, Not(self._bulbs_z3[current])))
                    current = self._bulbs_z3.neighbor_up(current)

                # Down
                current = self._bulbs_z3.neighbor_down(position)
                while current and current not in self._black_cells:
                    constraints.append(Implies(bulb_var, Not(self._bulbs_z3[current])))
                    current = self._bulbs_z3.neighbor_down(current)

                # Left
                current = self._bulbs_z3.neighbor_left(position)
                while current and current not in self._black_cells:
                    constraints.append(Implies(bulb_var, Not(self._bulbs_z3[current])))
                    current = self._bulbs_z3.neighbor_left(current)

                # Right
                current = self._bulbs_z3.neighbor_right(position)
                while current and current not in self._black_cells:
                    constraints.append(Implies(bulb_var, Not(self._bulbs_z3[current])))
                    current = self._bulbs_z3.neighbor_right(current)

                self._solver.add(constraints)
