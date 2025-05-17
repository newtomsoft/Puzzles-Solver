from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class NorinoriSolver(GameSolver):
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 6:
            raise ValueError("The grid must be at least 6x6")
        self._regions = self._grid.get_regions()
        if len(self._regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._model = cp_model.CpModel()
        self._grid_vars: Grid = Grid.empty()

    def get_solution(self) -> Grid:
        self._grid_vars = Grid([[self._model.NewBoolVar(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()

        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)

        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        grid = Grid([[solver.Value(self.domino_part(Position(i, j))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def get_other_solution(self) -> Grid:
        raise NotImplemented("This method is not yet implemented")

    def domino_part(self, position: Position):
        return self._grid_vars[position]

    def _add_constraints(self):
        self._add_constraint_exactly_2_by_region()
        self._add_constraint_2_by_2_without_adjacent()

    def _add_constraint_exactly_2_by_region(self):
        for region in self._regions.values():
            self._model.Add(sum([self.domino_part(position) for position in region]) == 2)

    def _add_constraint_2_by_2_without_adjacent(self):
        for position, _ in self._grid_vars:
            possible_neighbors_positions = self._grid_vars.neighbors_positions(position)

            config_vars = {}
            for possible_domino_position in possible_neighbors_positions:
                config_var = self._model.NewBoolVar(f"config_{position.r}_{position.c}_{possible_domino_position.r}_{possible_domino_position.c}")
                config_vars[possible_domino_position] = config_var

                self._model.Add(self.domino_part(possible_domino_position) == 1).OnlyEnforceIf(config_var)

                free_positions = possible_neighbors_positions.copy()
                free_positions.remove(possible_domino_position)
                for free_position in free_positions:
                    self._model.Add(self.domino_part(free_position) == 0).OnlyEnforceIf(config_var)

            self._model.AddBoolOr(list(config_vars.values())).OnlyEnforceIf(self.domino_part(position))
            self._model.Add(sum(config_vars.values()) == 0).OnlyEnforceIf(self.domino_part(position).Not())
