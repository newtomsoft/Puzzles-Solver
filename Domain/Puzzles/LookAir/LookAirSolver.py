from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class LookAirSolver(GameSolver):

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._grid_vars: Grid | None = None
        self._model = cp_model.CpModel()
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.NewBoolVar(f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_solver()

        solution, _ = self._ensure_squares_visibility()
        return solution

    def _ensure_squares_visibility(self) -> tuple[Grid, int]:
        proposition_count = 0
        solution = self._compute_solution()

        while not solution.is_empty():
            proposition_count += 1

            impossible_segments = self._impossible_segments(solution)
            if len(impossible_segments) == 0:
                return solution, proposition_count

            for positions in impossible_segments:
                literals = []
                for position in positions:
                    literals.append(self._grid_vars[position].Not()) if solution[position] == 1 else literals.append(self._grid_vars[position])
                self._model.AddBoolOr(literals)

            solution = self._compute_solution()

        return Grid.empty(), proposition_count

    def get_other_solution(self) -> Grid:
        pass

    def _compute_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        self._previous_solution = Grid([[solver.Value(self._grid_vars.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
        return self._previous_solution

    def _add_constraints(self):
        self._add_neighbors_constraints()
        self._add_all_shapes_are_squares_constraints()

    def _add_neighbors_constraints(self):
        for position, number in [(position, value) for position, value in self._grid if value >= 0]:
            concerned_positions = list(self._grid.neighbors_positions(position)) + [position]
            self._model.Add(sum([self._grid_vars[position] for position in concerned_positions]) == number)

    def _add_all_shapes_are_squares_constraints(self):
        squares = {}
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                for s in range(min(self._rows_number, self._columns_number)):
                    if r + s < self._rows_number and c + s < self._columns_number:
                        squares[(r, c, s)] = self._model.NewBoolVar(f'square_{r}_{c}_{s}')

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                squares_containing_pixel = []
                for sr in range(self._rows_number):
                    for sc in range(self._columns_number):
                        for size in range(min(self._rows_number, self._columns_number)):
                            if (sr, sc, size) in squares:
                                if sr <= r <= sr + size and sc <= c <= sc + size:
                                    squares_containing_pixel.append(squares[(sr, sc, size)])

                self._model.Add(sum(squares_containing_pixel) == self._grid_vars[Position(r, c)])

        for r1 in range(self._rows_number):
            for c1 in range(self._columns_number):
                for s1 in range(min(self._rows_number, self._columns_number)):
                    if (r1, c1, s1) in squares:
                        for r2 in range(self._rows_number):
                            for c2 in range(self._columns_number):
                                for s2 in range(min(self._rows_number, self._columns_number)):
                                    if (r2, c2, s2) in squares and (r1, c1, s1) != (r2, c2, s2):

                                        r1_min, r1_max = r1, r1 + s1
                                        c1_min, c1_max = c1, c1 + s1
                                        r2_min, r2_max = r2, r2 + s2
                                        c2_min, c2_max = c2, c2 + s2

                                        rect1 = (r1_min, c1_min, r1_max, c1_max)
                                        rect2 = (r2_min, c2_min, r2_max, c2_max)

                                        if self.are_adjacent(rect1, rect2):
                                            self._model.AddBoolOr([squares[(r1, c1, s1)].Not(), squares[(r2, c2, s2)].Not()])



    def _impossible_segments(self, proposition: Grid) -> list[list[Position]]:
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

    @staticmethod
    def are_adjacent(rect1: tuple[int, int, int, int], rect2: tuple[int, int, int, int]) -> bool:
        r1_min, c1_min, r1_max, c1_max = rect1
        r2_min, c2_min, r2_max, c2_max = rect2
        return (
                (r1_min <= r2_max and r2_min <= r1_max and (c1_max + 1 == c2_min or c2_max + 1 == c1_min))
                or
                (c1_min <= c2_max and c2_min <= c1_max and (r1_max + 1 == r2_min or r2_max + 1 == r1_min))
        )
