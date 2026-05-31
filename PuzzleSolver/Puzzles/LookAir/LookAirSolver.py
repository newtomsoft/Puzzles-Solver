from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class LookAirSolver(GameSolver):

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._grid_vars: Grid | None = None
        self._model = cp_model.CpModel()
        self._previous_solution: Grid | None = None

    def _init_solver(self):
        self._grid_vars = Grid([[self._model.new_bool_var(f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
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
                    literals.append(self._grid_vars[position].negated()) if solution[position] == 1 else literals.append(self._grid_vars[position])
                self._model.add_bool_or(literals)

            solution = self._compute_solution()

        return Grid.empty(), proposition_count

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None or self._previous_solution.is_empty():
            return Grid.empty()

        literals = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                if self._previous_solution[r][c] == 1:
                    literals.append(self._grid_vars[Position(r, c)].negated())
                else:
                    literals.append(self._grid_vars[Position(r, c)])
        self._model.add_bool_or(literals)

        solution, _ = self._ensure_squares_visibility()
        return solution

    def _compute_solution(self) -> Grid:
        solver = cp_model.CpSolver()
        solver.parameters.use_sat_inprocessing = True
        status = solver.solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        self._previous_solution = Grid([[solver.value(self._grid_vars.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
        return self._previous_solution

    def _add_constraints(self):
        self._add_neighbors_constraints()
        self._add_all_shapes_are_squares_constraints()

    def _add_neighbors_constraints(self):
        for position, number in [(position, value) for position, value in self._grid if value >= 0]:
            concerned_positions = list(self._grid.neighbors_positions(position)) + [position]
            self._model.add(sum([self._grid_vars[position] for position in concerned_positions]) == number)

    def _add_all_shapes_are_squares_constraints(self):
        # Une cellule de valeur 0 est forcément inactive : aucun carré ne peut la couvrir.
        # Une cellule de valeur 1 ou 2 ne peut pas être dans un carré de taille > 1,
        # car un carré >= 2x2 impliquerait au moins 3 cellules actives dans son
        # voisinage de von Neumann (la cellule + 2 voisins orthogonaux au minimum).
        forced_inactive = set()
        no_big_square = set()
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                v = self._grid[Position(r, c)]
                if v == 0:
                    forced_inactive.add((r, c))
                    self._model.add(self._grid_vars[Position(r, c)] == 0)
                elif v in (1, 2):
                    no_big_square.add((r, c))

        # Variables pour représenter les coins supérieurs gauches des carrés
        # squares[r][c][s] = 1 si il y a un carré de taille (s+1)x(s+1) commençant en (r,c)
        squares = {}
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                max_size = min(self._rows_number - r, self._columns_number - c)
                for s in range(max_size):
                    # Ignorer les carrés couvrant une cellule inactive (valeur 0)
                    # ou une cellule de valeur 1/2 avec une taille > 1
                    valid = True
                    for dr in range(s + 1):
                        for dc in range(s + 1):
                            cell = (r + dr, c + dc)
                            if cell in forced_inactive:
                                valid = False
                                break
                            if s > 0 and cell in no_big_square:
                                valid = False
                                break
                        if not valid:
                            break
                    if valid:
                        squares[(r, c, s)] = self._model.new_bool_var(f'square_{r}_{c}_{s}')

        # Pré-calculer les carrés contenant chaque pixel
        pixel_to_squares = [[[] for _ in range(self._columns_number)] for _ in range(self._rows_number)]
        for (sr, sc, size), var in squares.items():
            for r in range(sr, sr + size + 1):
                for c in range(sc, sc + size + 1):
                    pixel_to_squares[r][c].append(var)

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                # Si cell_values[(r, c)] = 1, le pixel doit appartenir à exactement un carré
                # Si cell_values[(r, c)] = 0, le pixel ne doit appartenir à aucun carré
                self._model.add(sum(pixel_to_squares[r][c]) == self._grid_vars[Position(r, c)])

        # Contrainte : les carrés ne doivent pas être adjacents
        # Deux carrés sont adjacents s'ils se touchent horizontalement ou verticalement
        square_list = list(squares.items())
        for i, ((r1, c1, s1), var1) in enumerate(square_list):
            for j in range(i + 1, len(square_list)):
                (r2, c2, s2), var2 = square_list[j]

                # Calculer les bords des carrés
                r1_min, r1_max = r1, r1 + s1
                c1_min, c1_max = c1, c1 + s1
                r2_min, r2_max = r2, r2 + s2
                c2_min, c2_max = c2, c2 + s2

                # Vérifier l'adjacence (distance de 1 dans une direction)
                adjacent = False
                # Adjacence horizontale
                if (r1_min <= r2_max and r2_min <= r1_max and
                        (c1_max + 1 == c2_min or c2_max + 1 == c1_min)):
                    adjacent = True
                # Adjacence verticale
                elif (c1_min <= c2_max and c2_min <= c1_max and
                      (r1_max + 1 == r2_min or r2_max + 1 == r1_min)):
                    adjacent = True

                if adjacent:
                    # Les carrés ne peuvent pas être tous les deux présents
                    self._model.add_bool_or([
                        var1.negated(),
                        var2.negated()
                    ])



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
