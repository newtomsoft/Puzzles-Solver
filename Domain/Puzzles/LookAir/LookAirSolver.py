from z3 import Solver, Not, And, Bool, is_true, Implies, Or, sat

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class LookAirSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._grid_z3: Grid = Grid.empty()
        self._solver = Solver()
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_z3 = Grid([[Bool(f"cell_{r}-{c}") for c in range(self._grid.columns_number)] for r in range(self._grid.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[Grid, int]:
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            proposition = Grid([[1 if is_true(model.eval(self._grid_z3.value(i, j))) else 0 for j in range(self._columns_number)] for i in range(self._rows_number)])

            impossible_segments = self.impossible_segments(proposition)
            if len(impossible_segments) == 0:
                self._previous_solution = proposition
                return proposition, proposition_count

            for positions in impossible_segments:
                self._solver.add(Not(And([self._grid_z3[position] == (proposition[position] == 1) for position in positions])))

        return Grid.empty(), proposition_count

    def get_other_solution(self):
        constraints = []
        for position, value in self._previous_solution:
            constraints.append(self._grid_z3[position] if value else Not(self._grid_z3[position]))
        self._solver.add(Not(And(constraints)))
        return self.get_solution()

    def _add_constraints(self):
        self._add_neighbors_constraints()
        self._add_all_shapes_are_squares_constraints()

    def _add_neighbors_constraints(self):
        for position, number in [(position, value) for position, value in self._grid if value >= 0]:
            concerned_positions = list(self._grid.neighbors_positions(position)) + [position]
            self._solver.add(sum([self._grid_z3[position] for position in concerned_positions]) == number)

    def _add_all_shapes_are_squares_constraints(self):
        for comparison_offset in range(1, self._rows_number - 1):  # no test if grid is fully filled
            for position, _ in self._grid_z3:
                self._add_square_constraint(position, comparison_offset)

    def _add_square_constraint(self, position: Position, comparison_offset: int):
        for comparison_direction in [Direction.down(), Direction.right()]:
            max_position = position.after(comparison_direction, comparison_offset)
            if max_position not in self._grid_z3:
                continue

            to_fill_direction = Direction.down() if comparison_direction == Direction.right() else Direction.right()

            comparison_positions = position.all_positions_and_bounds_between(max_position)
            values_filled = []
            for fill_offset in [fill_offset for fill_offset in range(-comparison_offset, comparison_offset + 1) if
                                fill_offset != 0 and position.after(to_fill_direction, fill_offset) in self._grid_z3]:
                values_filled.append(And([self._grid_z3[position.after(to_fill_direction, fill_offset)] for position in comparison_positions]))

            if len(values_filled) >= 1:
                offset = 0
                positions_filled_constraint = []
                while offset + comparison_offset <= len(values_filled):
                    selected_values_filled = values_filled[offset:offset + comparison_offset]
                    positions_filled_constraint.append(And(selected_values_filled))
                    offset += 1

                implies = Implies(And([self._grid_z3[position] for position in comparison_positions]), Or(positions_filled_constraint))
                self._solver.add(implies)

    def impossible_segments(self, proposition: Grid) -> list[list[Position]]:
        segments: list[list[Position]] = []
        segments.extend(self._impossible_segments_by_direction(proposition, Direction.right()))
        segments.extend(self._impossible_segments_by_direction(proposition, Direction.down()))
        return segments

    def _impossible_segments_by_direction(self, proposition: Grid, direction: Direction) -> list[list[Position]]:
        segments: list[list[Position]] = []

        primary_range = range(self._rows_number) if direction == Direction.right() else range(self._columns_number)
        secondary_range = range(self._columns_number) if direction == Direction.right() else range(self._rows_number)

        for primary_idx in primary_range:
            started = False
            start_position = Position(-1, -1)
            end_position = Position(-1, -1)
            for secondary_idx in secondary_range:
                position = Position(primary_idx, secondary_idx) if direction == Direction.right() else Position(secondary_idx, primary_idx)

                if proposition[position] == 1 and not started:
                    started = True
                    start_position = position
                    end_position = position
                    continue
                if proposition[position] == 1:
                    end_position = position
                    continue
                if not started:
                    continue

                length = int(start_position.distance_to(end_position)) + 1
                search_after_position = end_position.after(direction)
                if search_after_position.after(direction, length) not in proposition:
                    break

                to_parse_positions = proposition.all_positions_in_direction(search_after_position, direction)
                last_found_position = self._end_position_if_same_length(length, to_parse_positions, proposition)
                if last_found_position is not None:
                    if (before := start_position.before(direction)) in proposition:
                        start_position = before
                    segment = start_position.all_positions_and_bounds_between(last_found_position)
                    segments.append(segment)
                started = False

        return segments

    @staticmethod
    def _end_position_if_same_length(length: int, positions: list[Position], proposition: Grid) -> Position | None:
        started = False
        start_index = -1
        end_index = -1

        for i, position in enumerate(positions):
            if proposition[position] == 1 and not started:
                started = True
                start_index = i
                end_index = i
                continue

            if proposition[position] == 1:
                end_index = i
                if end_index - start_index + 1 > length:
                    return None
                continue

            if not started:
                continue

            if end_index - start_index + 1 == length:
                return positions[end_index + 1] if end_index < len(positions) - 1 else positions[end_index]

        if started and end_index - start_index + 1 == length:
            return positions[end_index + 1] if end_index < len(positions) - 1 else positions[end_index]

        return None
