from z3 import Bool, Solver, Not, And, sat, is_true, Sum, Implies, Or

from Grid import Grid


class NorinoriGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number != self.columns_number:
            raise ValueError("The grid must be square")
        if self.rows_number < 6:
            raise ValueError("The grid must be at least 6x6")
        self._colored_regions = self._get_colored_regions()
        if len(self._colored_regions) < 2:
            raise ValueError("The grid must have at least 2 regions")
        self._solver = None
        self._grid_z3 = None

    def get_solution(self) -> Grid | None:
        self._grid_z3 = [[Bool(f"grid_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        self._solver = Solver()
        self._add_constrains()
        if self._solver.check() != sat:
            return None
        model = self._solver.model()
        grid = Grid([[is_true(model.eval(self._grid_z3[i][j])) for j in range(self.columns_number)] for i in range(self.rows_number)])
        return grid

    def _add_constrains(self):
        self._add_constraint_exactly_2_by_region()
        self._add_constraint_2_by_2()

    def _add_constraint_exactly_2_by_region(self):
        for region in self._colored_regions.values():
            self._solver.add(Sum([self._grid_z3[r][c] for r, c in region]) == 2)

    def _add_constraint_2_by_2(self):
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                possible_neighbors = []
                if r > 0:
                    possible_neighbors.append(self._grid_z3[r - 1][c])
                if r < self.rows_number - 1:
                    possible_neighbors.append(self._grid_z3[r + 1][c])
                if c > 0:
                    possible_neighbors.append(self._grid_z3[r][c - 1])
                if c < self.columns_number - 1:
                    possible_neighbors.append(self._grid_z3[r][c + 1])

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
                constraint = Implies(self._grid_z3[r][c], constraint_or)
                self._solver.add(constraint)
                pass

    def _get_colored_regions(self):
        colored_regions = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                if self._grid.value(r, c) not in colored_regions:
                    colored_regions[self._grid.value(r, c)] = []
                colored_regions[self._grid.value(r, c)].append((r, c))
        return colored_regions

    @staticmethod
    def generate_rotations(lst):
        return [lst[i:] + lst[:i] for i in range(1, len(lst))]
