from z3 import Bool

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Ports.SolverEngine import SolverEngine
from GameSolver import GameSolver


class NorinoriSolver(GameSolver):
    def __init__(self, grid: Grid, solver_engine: SolverEngine):
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
        self._solver = solver_engine
        self._grid_z3: Grid = Grid.empty()

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._add_constraints()
        if not self._solver.has_solution():
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[self._solver.is_true(model.eval(self.domino_part(Position(i, j)))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def get_other_solution(self) -> Grid:
        raise NotImplemented("This method is not yet implemented")

    def domino_part(self, position: Position):
        return self._grid_z3[position]

    def _add_constraints(self):
        self._add_constraint_exactly_2_by_region()
        self._add_constraint_2_by_2_without_adjacent()

    def _add_constraint_exactly_2_by_region(self):
        for region in self._regions.values():
            self._solver.add(self._solver.sum([self.domino_part(position) for position in region]) == 2)

    def _add_constraint_2_by_2_without_adjacent(self):
        for position, _ in self._grid_z3:
            possible_neighbors_positions = self._grid_z3.neighbors_positions(position)
            one_is_domino_part_others_is_free = []
            for possible_domino_position in possible_neighbors_positions:
                free_positions = possible_neighbors_positions.copy()
                free_positions.remove(possible_domino_position)
                first_possible_others_free = [self.domino_part(possible_domino_position)]
                for free_position in free_positions:
                    first_possible_others_free.append(self._solver.Not(self.domino_part(free_position)))
                one_is_domino_part_others_is_free.append(self._solver.And(first_possible_others_free))
            self._solver.add(self._solver.Implies(self.domino_part(position), self._solver.Or(one_is_domino_part_others_is_free)))
