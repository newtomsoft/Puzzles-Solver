from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class YajikabeSolver(GameSolver):
    direction_map = {
        '→': Direction.right(),
        '↓': Direction.down(),
        '←': Direction.left(),
        '↑': Direction.up()
    }

    def __init__(self, grid: Grid):
        self._input_grid = grid
        self.rows_number = self._input_grid.rows_number
        self.columns_number = self._input_grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_vars = {}
        self._previous_solution = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._grid_vars = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                self._grid_vars[(r, c)] = self._model.new_bool_var(f"cell_{r}_{c}")

        self._add_initial_constraints()
        self._add_black_cell_constraints()
        self._add_no_black_2x2_constraints()
        self._add_connectivity_constraints()

    def get_solution(self) -> Grid:
        if not self._grid_vars:
            self._init_model()

        status = self._solver.solve(self._model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            solution_data = []
            for r in range(self.rows_number):
                row = []
                for c in range(self.columns_number):
                    row.append(bool(self._solver.value(self._grid_vars[(r, c)])))
                solution_data.append(row)
            self._previous_solution = Grid(solution_data)
            return self._previous_solution
        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._previous_solution is None:
            return self.get_solution()

        # Exclude previous solution
        exclusion = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                if self._previous_solution[pos]:
                    exclusion.append(self._grid_vars[(r, c)].Not())
                else:
                    exclusion.append(self._grid_vars[(r, c)])
        self._model.add_bool_or(exclusion)

        return self.get_solution()

    def _add_initial_constraints(self):
        for position, value in self._input_grid:
            if value != '':
                self._model.add(self._grid_vars[(position.r, position.c)] == 0)

    def _add_black_cell_constraints(self):
        for position, value in self._input_grid:
            if value != '':
                count, direction = self._convert_cell_value(value)
                positions = [p for p in self._input_grid.all_positions_in_direction(position, direction) if
                             self._input_grid[p] == '']
                self._model.add(sum(self._grid_vars[(p.r, p.c)] for p in positions) == count)

    def _add_no_black_2x2_constraints(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                self._model.add(
                    sum([
                        self._grid_vars[(r, c)],
                        self._grid_vars[(r + 1, c)],
                        self._grid_vars[(r, c + 1)],
                        self._grid_vars[(r + 1, c + 1)]
                    ]) < 4
                )

    def _add_connectivity_constraints(self):
        num_cells = self.rows_number * self.columns_number
        rank_vars = {}
        is_root = {}
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                rank_vars[(r, c)] = self._model.new_int_var(0, num_cells - 1, f"rank_{r}_{c}")
                is_root[(r, c)] = self._model.new_bool_var(f"root_{r}_{c}")

        any_black = self._model.new_bool_var("any_black")
        self._model.add_max_equality(any_black, list(self._grid_vars.values()))
        self._model.add(sum(is_root.values()) == any_black)

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = (r, c)
                gv = self._grid_vars[pos]
                rv = rank_vars[pos]
                root = is_root[pos]

                # If root, must be black and have rank 0
                self._model.add(gv == 1).only_enforce_if(root)
                self._model.add(rv == 0).only_enforce_if(root)

                neighbors = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows_number and 0 <= nc < self.columns_number:
                        neighbors.append((nr, nc))

                has_parent = self._model.new_bool_var(f"has_parent_{r}_{c}")
                parent_indicators = []
                for n_pos in neighbors:
                    p_ind = self._model.new_bool_var(f"p_{pos}_{n_pos}")
                    self._model.add(self._grid_vars[n_pos] == 1).only_enforce_if(p_ind)
                    self._model.add(rank_vars[n_pos] == rv - 1).only_enforce_if(p_ind)
                    parent_indicators.append(p_ind)

                # has_parent <=> OR(parent_indicators)
                self._model.add_bool_or(parent_indicators).only_enforce_if(has_parent)
                for p_ind in parent_indicators:
                    self._model.add_implication(p_ind, has_parent)

                # If black and not root, must have parent
                self._model.add(has_parent == 1).only_enforce_if([gv, root.Not()])

                # If root or white, cannot have parent
                self._model.add(has_parent == 0).only_enforce_if(root)
                self._model.add(has_parent == 0).only_enforce_if(gv.Not())

    @staticmethod
    def _convert_cell_value(cell_value: str) -> tuple[int, Direction]:
        if len(cell_value) < 2:
            raise ValueError(f"Invalid cell value: {cell_value}")
        count = int(cell_value[:-1])
        direction = YajikabeSolver.direction_map[cell_value[-1]]
        return count, direction
