from z3 import Bool, Solver, Not, And, sat, is_true, Sum, Implies, Or

from Position import Position
from Utils.Grid import Grid


class NorinoriGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 6:
            raise ValueError("The grid must be at least 6x6")
        self._regions = self._grid.get_regions_new()
        if len(self._regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._solver = None
        self._grid_z3 = None

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._solver = Solver()
        self._add_constraints()
        if self._solver.check() != sat:
            return Grid.empty()
        model = self._solver.model()
        grid = Grid([[is_true(model.eval(self.domino_part(Position(i, j)))) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def domino_part(self, position: Position):
        return self._grid_z3[position]

    def _add_constraints(self):
        self._add_constraint_exactly_2_by_region()
        self._add_constraint_2_by_2_without_adjacents()

    def _add_constraint_exactly_2_by_region(self):
        for region in self._regions.values():
            self._solver.add(Sum([self.domino_part(position) for position in region]) == 2)

    def _add_constraint_2_by_2_without_adjacents(self):
        for position, value in self._grid_z3:
            r, c = position
            possible_neighbors = []
            if r > 0:
                possible_neighbors.append(self.domino_part(position.up))
            if r < self.rows_number - 1:
                possible_neighbors.append(self.domino_part(position.down))
            if c > 0:
                possible_neighbors.append(self.domino_part(position.left))
            if c < self.columns_number - 1:
                possible_neighbors.append(self.domino_part(position.right))

            all_possible_neighbors = NorinoriGame.generate_rotations(possible_neighbors)
            all_possible_neighbors.append(possible_neighbors)
            constraint_ands = []
            for neighbors in all_possible_neighbors:
                ands = [neighbors[0]]
                for neighbor in neighbors[1:]:
                    ands.append(Not(neighbor))
                constraint_and = And(ands)
                constraint_ands.append(constraint_and)
            constraint_or = Or(constraint_ands)
            constraint = Implies(self.domino_part(r)[c], constraint_or)
            self._solver.add(constraint)

    @staticmethod
    def generate_rotations(lst):
        return [lst[i:] + lst[:i] for i in range(1, len(lst))]
