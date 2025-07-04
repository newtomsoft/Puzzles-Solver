from typing import Generator

from z3 import Solver, Not, And, Or, Bool, is_true, sat

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class SeeThroughSolver(GameSolver):
    def __init__(self, input_grid: Grid):
        self._input_grid = input_grid
        self.rows_number, self.columns_number = input_grid.rows_number, input_grid.columns_number
        self._grid_z3: Grid | None = None
        self._solver = Solver()
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid(
            [[{k: Bool(f"{k}_{r}{c}") for k in ['left', 'right', 'up', 'down']} for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_rooms_connected()
        return solution

    def _ensure_all_rooms_connected(self) -> tuple[Grid, int]:
        proposition_count = 0
        while self._solver.check() == sat:
            proposition_count += 1
            model = self._solver.model()
            custom_proposition = Grid([
                [{edge: is_true(model.eval(self._grid_z3[Position(r, c)][edge])) for edge in ['left', 'right', 'up', 'down']} for c in range(self.columns_number)]
                for r in range(self.rows_number)
            ])

            grid_fully_true_with_walls = Grid([[True for _ in range(self.columns_number)] for _ in range(self.rows_number)])
            for position, value in [(position, value) for position, value in custom_proposition]:
                if value['down'] and position.down in self._input_grid:
                    grid_fully_true_with_walls.add_wall([position, position.down])
                if value['right'] and position.right in self._input_grid:
                    grid_fully_true_with_walls.add_wall([position, position.right])

            connected_positions = grid_fully_true_with_walls.get_connected_positions()
            if len(connected_positions) == 1:
                self._previous_solution = custom_proposition
                return IslandGrid.from_walls_grid(grid_fully_true_with_walls, with_edges=True), proposition_count

            smallest_connected_positions = min(connected_positions, key=len)
            constraints = []

            for position in smallest_connected_positions:
                constraints += [self._grid_z3[position][edge] == custom_proposition[position][edge] for edge in ['left', 'right', 'up', 'down']]

            self._solver.add(Not(And(constraints)))

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        constraints = []
        for position, value in self._previous_solution:
            constraints += [self._grid_z3[position][edge] == value[edge] for edge in ['left', 'right', 'up', 'down']]
        self._solver.add(Not(And(constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_opposite_constraints()
        self._add_numbers_constraints()

    def _add_initials_constraints(self):
        for position in self._input_grid.edge_up_positions():
            self._solver.add(self._grid_z3[position]['up'])
        for position in self._input_grid.edge_down_positions():
            self._solver.add(self._grid_z3[position]['down'])
        for position in self._input_grid.edge_left_positions():
            self._solver.add(self._grid_z3[position]['left'])
        for position in self._input_grid.edge_right_positions():
            self._solver.add(self._grid_z3[position]['right'])

    def _add_opposite_constraints(self):
        for position, _ in self._input_grid:
            if position.up in self._grid_z3:
                self._solver.add(self._grid_z3[position]['up'] == self._grid_z3[position.up]['down'])
            if position.down in self._grid_z3:
                self._solver.add(self._grid_z3[position]['down'] == self._grid_z3[position.down]['up'])
            if position.left in self._grid_z3:
                self._solver.add(self._grid_z3[position]['left'] == self._grid_z3[position.left]['right'])
            if position.right in self._grid_z3:
                self._solver.add(self._grid_z3[position]['right'] == self._grid_z3[position.right]['left'])

    def _add_numbers_constraints(self):
        for position, number in [(position, number) for position, number in self._input_grid if number > 0]:
            self._add_number_constraints(position, number)

    def _add_number_constraints(self, position: Position, number: int):
        constraints = []
        for up_count, down_count, right_count, left_count in self.find_combinations(number):
            if (up_position := position.after(Direction.up(), up_count)) not in self._grid_z3:
                continue
            if (down_position := position.after(Direction.down(), down_count)) not in self._grid_z3:
                continue
            if (left_position := position.after(Direction.left(), left_count)) not in self._grid_z3:
                continue
            if (right_position := position.after(Direction.right(), right_count)) not in self._grid_z3:
                continue

            constraint_up = self._grid_z3[up_position]['up']
            if up_count > 0:
                for between_position in [position] + position.all_positions_between(up_position):
                    constraint_up = And(constraint_up, Not(self._grid_z3[between_position]['up']))
            constraint_down = self._grid_z3[down_position]['down']
            if down_count > 0:
                for between_position in [position] + position.all_positions_between(down_position):
                    constraint_down = And(constraint_down, Not(self._grid_z3[between_position]['down']))
            constraint_left = self._grid_z3[left_position]['left']
            if left_count > 0:
                for between_position in [position] + position.all_positions_between(left_position):
                    constraint_left = And(constraint_left, Not(self._grid_z3[between_position]['left']))
            constraint_right = self._grid_z3[right_position]['right']
            if right_count > 0:
                for between_position in [position] + position.all_positions_between(right_position):
                    constraint_right = And(constraint_right, Not(self._grid_z3[between_position]['right']))

            constraints.append(And(constraint_up, constraint_down, constraint_left, constraint_right))

        self._solver.add(Or(constraints))

    @staticmethod
    def find_combinations(number) -> Generator[tuple[int, int, int, int], None, None]:
        for up_count in range(0, number + 1):
            for down_count in range(0, number - up_count + 1):
                for right_count in range(0, number - up_count - down_count + 1):
                    left_count = number - up_count - down_count - right_count
                    yield up_count, down_count, right_count, left_count
