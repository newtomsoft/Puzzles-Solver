from ortools.sat.python import cp_model
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Board.Direction import Direction
from Domain.Puzzles.GameSolver import GameSolver


class RabbitsAndTreesSolver(GameSolver):
    EMPTY = None
    RABBIT = 1
    TREE = 2
    NOTHING = 0

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows_number = self._grid.rows_number
        self._columns_number = self._grid.columns_number
        self._model = cp_model.CpModel()
        self._grid_vars = None
        self._previous_solution = None

    def _init_model(self):
        # 0: Empty/Nothing, 1: Rabbit, 2: Tree
        self._grid_vars = Grid([[self._model.new_int_var(0, 2, f"cell_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])

        # Row and Column constraints: Exactly one rabbit and one tree
        for r in range(self._rows_number):
            rabbits = [self._model.new_bool_var(f"r_{r}_{c}") for c in range(self._columns_number)]
            trees = [self._model.new_bool_var(f"t_{r}_{c}") for c in range(self._columns_number)]
            for c in range(self._columns_number):
                self._model.add(self._grid_vars.value(r, c) == self.RABBIT).only_enforce_if(rabbits[c])
                self._model.add(self._grid_vars.value(r, c) != self.RABBIT).only_enforce_if(rabbits[c].Not())
                self._model.add(self._grid_vars.value(r, c) == self.TREE).only_enforce_if(trees[c])
                self._model.add(self._grid_vars.value(r, c) != self.TREE).only_enforce_if(trees[c].Not())
            self._model.add_exactly_one(rabbits)
            self._model.add_exactly_one(trees)

        for c in range(self._columns_number):
            rabbits = [self._model.new_bool_var(f"r_c_{r}_{c}") for r in range(self._rows_number)]
            trees = [self._model.new_bool_var(f"t_c_{r}_{c}") for r in range(self._rows_number)]
            for r in range(self._rows_number):
                self._model.add(self._grid_vars.value(r, c) == self.RABBIT).only_enforce_if(rabbits[r])
                self._model.add(self._grid_vars.value(r, c) != self.RABBIT).only_enforce_if(rabbits[r].Not())
                self._model.add(self._grid_vars.value(r, c) == self.TREE).only_enforce_if(trees[r])
                self._model.add(self._grid_vars.value(r, c) != self.TREE).only_enforce_if(trees[r].Not())
            self._model.add_exactly_one(rabbits)
            self._model.add_exactly_one(trees)

        # Visibility constraints
        for pos, value in self._grid:
            if value is not self.EMPTY:
                # Numbers mean rabbits can't be in the cell itself?
                # "The viewing cell itself is not counted."
                # Usually numbers are clues in empty cells or specific cells.
                # If a cell has a number, it cannot be a rabbit.
                # In most puzzles, cells with hints are strictly empty (NOTHING).
                self._model.add(self._grid_vars[pos] == self.NOTHING)

                visible_rabbits = []
                for direction in Direction.orthogonal_directions():
                    visible_rabbits.extend(self._get_visible_rabbits_in_direction(pos, direction))

                self._model.add(sum(visible_rabbits) == value)

    def _get_visible_rabbits_in_direction(self, pos: Position, direction: Direction):
        visible_vars = []

        path = []
        curr = pos.after(direction)
        while 0 <= curr.r < self._rows_number and 0 <= curr.c < self._columns_number:
            path.append(curr)
            curr = curr.after(direction)

        for i, rabbit_pos in enumerate(path):
            is_rabbit = self._model.new_bool_var(f"is_rabbit_{pos.r}_{pos.c}_{rabbit_pos.r}_{rabbit_pos.c}")
            self._model.add(self._grid_vars[rabbit_pos] == self.RABBIT).only_enforce_if(is_rabbit)
            self._model.add(self._grid_vars[rabbit_pos] != self.RABBIT).only_enforce_if(is_rabbit.Not())

            no_tree_before = self._model.new_bool_var(f"no_tree_before_{pos.r}_{pos.c}_{rabbit_pos.r}_{rabbit_pos.c}")
            trees_before = []
            for j in range(i):
                tree_at_j = self._model.new_bool_var(f"tree_at_{pos.r}_{pos.c}_{path[j].r}_{path[j].c}_before_{rabbit_pos.r}_{rabbit_pos.c}")
                self._model.add(self._grid_vars[path[j]] == self.TREE).only_enforce_if(tree_at_j)
                self._model.add(self._grid_vars[path[j]] != self.TREE).only_enforce_if(tree_at_j.Not())
                trees_before.append(tree_at_j)

            if trees_before:
                self._model.add(sum(trees_before) == 0).only_enforce_if(no_tree_before)
                self._model.add(sum(trees_before) > 0).only_enforce_if(no_tree_before.Not())
            else:
                self._model.add(no_tree_before == 1)

            is_visible = self._model.new_bool_var(f"visible_{pos.r}_{pos.c}_{rabbit_pos.r}_{rabbit_pos.c}")
            self._model.add_bool_and([is_rabbit, no_tree_before]).only_enforce_if(is_visible)
            self._model.add_bool_or([is_rabbit.Not(), no_tree_before.Not()]).only_enforce_if(is_visible.Not())
            visible_vars.append(is_visible)

        return visible_vars

    def get_solution(self) -> Grid:
        if self._grid_vars is None:
            self._init_model()

        solver = cp_model.CpSolver()
        status = solver.solve(self._model)

        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        solution = Grid([[solver.value(self._grid_vars.value(r, c)) for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._previous_solution = solution
        return solution

    def get_other_solution(self):
        if self._previous_solution is None:
            first = self.get_solution()
            self._previous_solution = first
            return first
        if self._previous_solution.is_empty():
            return Grid.empty()

        diff_bools: list[cp_model.BoolVar] = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                prev_val = self._previous_solution.value(r, c)
                b_not_eq = self._model.new_bool_var(f"not_eq_{r}_{c}_{id(self._previous_solution)}")
                var = self._grid_vars.value(r, c)
                self._model.add(var != prev_val).only_enforce_if(b_not_eq)
                self._model.add(var == prev_val).only_enforce_if(b_not_eq.Not())
                diff_bools.append(b_not_eq)

        self._model.add_bool_or(diff_bools)

        solver = cp_model.CpSolver()
        status = solver.solve(self._model)
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            return Grid.empty()

        solution = Grid([[solver.value(self._grid_vars.value(i, j)) for j in range(self._columns_number)] for i in range(self._rows_number)])
        self._previous_solution = solution
        return solution
