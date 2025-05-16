from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class StitchesSolver(GameSolver):
    def __init__(self, grid: Grid, dots_by_column_row: dict[str, list[int]], regions_connections_count: int):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 5:
            raise ValueError("The grid must be at least 5x5")
        self._regions = self._grid.get_regions()
        if len(self._regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self.regions_connections = regions_connections_count
        if regions_connections_count < 1:
            raise ValueError("The grid must require at least 1 connection between regions")
        self._dots_by_column = dots_by_column_row['column']
        self._dots_by_row = dots_by_column_row['row']
        if len(self._dots_by_column) != self.columns_number or len(self._dots_by_row) != self.rows_number:
            raise ValueError("The dots count must have the same size as the columns")
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_connexion_var: Grid | None = None
        self._previous_solution_grid: Grid | None = None

    def _init_solver(self):
        # 0: no connection, 1: right, 2: down, 3: left, 4: up
        self._grid_connexion_var = Grid([[self._model.NewIntVar(0, 4, f"connexion_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

    def get_solution(self) -> Grid | None:
        if self._grid_connexion_var is None:
            self._init_solver()
        status = self._solver.Solve(self._model)
        if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
            return Grid.empty()
        grid = Grid([[self._solver.Value(self._grid_connexion_var[r][c]) for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._previous_solution_grid = grid
        return grid

    def get_other_solution(self):
        self._exclude_solution(self._previous_solution_grid)
        solution = self.get_solution()
        return solution

    def _exclude_solution(self, solution_grid: Grid):
        previous_solution_literals = []
        for position, value in [(position, value) for position, value in self._grid if value > 0]:
            temp_var = self._model.NewBoolVar(f"prev_{position}")
            self._model.Add(self._grid_connexion_var[position] == solution_grid[position]).OnlyEnforceIf(temp_var)
            self._model.Add(self._grid_connexion_var[position] != solution_grid[position]).OnlyEnforceIf(temp_var.Not())
            previous_solution_literals.append(temp_var)

        if previous_solution_literals:
            self._model.AddBoolOr([lit.Not() for lit in previous_solution_literals])

    def _add_constraints(self):
        self._add_constraint_dots_in_rows_and_columns()
        self._add_constraint_2_dots_crossing_2_regions()
        self._add_constraint_dots_between_regions()

    def _add_constraint_dots_between_regions(self):
        for region_number in self._regions.keys():
            region_positions = self._regions[region_number]
            current_region_with_others_regions = {}
            for position in region_positions:
                neighbors_positions = self._grid.neighbors_positions(position)
                for neighbor_position in neighbors_positions:
                    if (other_region_number := self._grid[neighbor_position]) != region_number:
                        if other_region_number in current_region_with_others_regions.keys():
                            current_region_with_others_regions[other_region_number].add((position, neighbor_position))
                        else:
                            current_region_with_others_regions[other_region_number] = {(position, neighbor_position)}

            all_regions_possible_dot_positions = set()
            for positions in current_region_with_others_regions.values():
                self._add_constraint_dots_between_regions_at(positions)
                all_regions_possible_dot_positions.update(positions0[0] for positions0 in positions)

            if len(all_regions_possible_dot_positions) == 0:
                continue

            has_connection_vars = []
            for position in all_regions_possible_dot_positions:
                has_connection_var = self._model.NewBoolVar(f"region_{region_number}_pos_{position}_has_connection")
                self._model.Add(self._grid_connexion_var[position] > 0).OnlyEnforceIf(has_connection_var)
                self._model.Add(self._grid_connexion_var[position] == 0).OnlyEnforceIf(has_connection_var.Not())
                has_connection_vars.append(has_connection_var)

            self._model.Add(sum(has_connection_vars) == len(current_region_with_others_regions) * self.regions_connections)

    def _add_constraint_dots_between_regions_at(self, positions: list[tuple[Position, Position]]):
        region0_to_region1_connections = []
        for position0, position1 in positions:
            direction_value = position0.direction_to(position1).value
            connection_var = self._model.NewBoolVar(f"connection_{position0}_to_{position1}")
            self._model.Add(self._grid_connexion_var[position0] == direction_value).OnlyEnforceIf(connection_var)
            self._model.Add(self._grid_connexion_var[position0] != direction_value).OnlyEnforceIf(connection_var.Not())
            region0_to_region1_connections.append(connection_var)

        self._model.Add(sum(region0_to_region1_connections) == self.regions_connections)

        region1_to_region0_connections = []
        for position0, position1 in positions:
            direction_value = position0.direction_from(position1).value
            connection_var = self._model.NewBoolVar(f"connection_{position1}_to_{position0}")
            self._model.Add(self._grid_connexion_var[position1] == direction_value).OnlyEnforceIf(connection_var)
            self._model.Add(self._grid_connexion_var[position1] != direction_value).OnlyEnforceIf(connection_var.Not())
            region1_to_region0_connections.append(connection_var)

        self._model.Add(sum(region1_to_region0_connections) == self.regions_connections)

    def _add_constraint_dots_in_rows_and_columns(self):
        for r, row in enumerate(self._grid_connexion_var.matrix):
            row_has_connection = [self._model.NewBoolVar(f"row_{r}_col_{c}_has_connection") for c in range(self.columns_number)]
            for c, cell in enumerate(row):
                self._model.Add(cell > 0).OnlyEnforceIf(row_has_connection[c])
                self._model.Add(cell == 0).OnlyEnforceIf(row_has_connection[c].Not())
            self._model.Add(sum(row_has_connection) == self._dots_by_row[r])

        for c in range(self.columns_number):
            column_has_connection = [self._model.NewBoolVar(f"row_{r}_col_{c}_has_connection") for r in range(self.rows_number)]
            for r in range(self.rows_number):
                self._model.Add(self._grid_connexion_var.matrix[r][c] > 0).OnlyEnforceIf(column_has_connection[r])
                self._model.Add(self._grid_connexion_var.matrix[r][c] == 0).OnlyEnforceIf(column_has_connection[r].Not())
            self._model.Add(sum(column_has_connection) == self._dots_by_column[c])

    def _add_constraint_2_dots_crossing_2_regions(self):
        for position, _ in self._grid_connexion_var:
            self._add_constraint_2_dots_crossing_2_regions_at(position)

    def _add_constraint_2_dots_crossing_2_regions_at(self, position: Position):
        region = self._grid[position]
        neighbors_positions = self._grid.neighbors_positions(position)
        other_region_positions = []
        for neighbor_position in neighbors_positions:
            if self._grid[neighbor_position] != region:
                other_region_positions.append(neighbor_position)

        self._add_constraint_other_region_dot_positions(position, other_region_positions)

    def _add_constraint_other_region_dot_positions(self, position: Position, other_region_dot_positions: list[Position]):
        if len(other_region_dot_positions) == 0:
            self._model.Add(self._grid_connexion_var[position] == 0)
            return

        direction_vars = []

        no_connection_var = self._model.NewBoolVar(f"pos_{position}_no_connection")
        self._model.Add(self._grid_connexion_var[position] == Direction.none().value).OnlyEnforceIf(no_connection_var)
        direction_vars.append(no_connection_var)

        for other_position in other_region_dot_positions:
            direction = position.direction_to(other_position)
            direction_var = self._model.NewBoolVar(f"pos_{position}_direction_{direction.value}")

            self._model.Add(self._grid_connexion_var[position] == direction.value).OnlyEnforceIf(direction_var)
            direction_vars.append(direction_var)

            opposite_direction_var = self._model.NewBoolVar(f"pos_{other_position}_direction_{direction.opposite.value}")
            self._model.Add(self._grid_connexion_var[other_position] == direction.opposite.value).OnlyEnforceIf(opposite_direction_var)
            self._model.Add(self._grid_connexion_var[other_position] != direction.opposite.value).OnlyEnforceIf(opposite_direction_var.Not())

            self._model.AddImplication(direction_var, opposite_direction_var)

        self._model.AddExactlyOne(direction_vars)
