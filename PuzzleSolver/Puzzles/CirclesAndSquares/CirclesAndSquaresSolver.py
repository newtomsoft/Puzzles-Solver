from typing import Any
from ortools.sat.python import cp_model

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class CirclesAndSquaresSolver(GameSolver):
    Black = True
    White = False
    cell_empty = None

    def __init__(self, data_game: dict[str, Any] | Grid):
        super().__init__()
        if isinstance(data_game, Grid):
            self.rows_number = len(data_game.matrix)
            self.columns_number = len(data_game.matrix[0]) if self.rows_number > 0 else 0
            self._black_circles = set()
            self._white_circles = set()
            for r in range(self.rows_number):
                for c in range(self.columns_number):
                    p = Position(r, c)
                    val = data_game[p]
                    if val is self.Black:
                        self._black_circles.add(p)
                    elif val is self.White:
                        self._white_circles.add(p)
        else:
            self._data_game = data_game
            self.rows_number = self._data_game['rows_number']
            self.columns_number = self._data_game['columns_number']
            self._black_circles = {Position(r, c) for r, c in self._data_game['black_circles']}
            self._white_circles = {Position(r, c) for r, c in self._data_game['white_circles']}
        
        # Validate that black and white circles don't overlap
        if self._black_circles & self._white_circles:
            raise ValueError("Black and white circles cannot overlap")

        self._model = None
        self._black_cells_vars = None
        self._status = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        
        # Create variables for black cells (1 = black, 0 = white)
        self._black_cells_vars = Grid([[
            self._model.new_bool_var(f'black_{r}_{c}') 
            for c in range(self.columns_number)]
            for r in range(self.rows_number)
        ])
        
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()

        self._status = self._solver.solve(self._model)
        if self._status == cp_model.OPTIMAL or self._status == cp_model.FEASIBLE:
            return self._compute_solution()

        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return self.get_solution()

        current_vars = []
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                p = Position(r, c)
                var = self._black_cells_vars[p]
                if self._solver.boolean_value(var):
                    current_vars.append(var.negated())
                else:
                    current_vars.append(var)

        if current_vars:
            self._model.add_bool_or(current_vars)

        self._status = self._solver.solve(self._model)
        if self._status == cp_model.OPTIMAL or self._status == cp_model.FEASIBLE:
            return self._compute_solution()

        return Grid.empty()

    def _compute_solution(self) -> Grid:
        solution_grid = Grid([[self.White] * self.columns_number for _ in range(self.rows_number)])
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                p = Position(r, c)
                if self._solver.boolean_value(self._black_cells_vars[p]):
                    solution_grid[p] = self.Black  # Black cell
                else:
                    solution_grid[p] = self.White  # White cell
        return solution_grid

    def _add_constraints(self):
        self._add_initial_circles_constraints()
        self._add_no_2x2_black_area_constraints()
        self._add_connectivity_constraints()
        self._add_square_regions_constraint()

    def _add_initial_circles_constraints(self):
        for pos in self._black_circles:
            self._model.add(self._black_cells_vars[pos] == 1)
        
        for pos in self._white_circles:
            self._model.add(self._black_cells_vars[pos] == 0)

    def _add_no_2x2_black_area_constraints(self):
        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                area_vars = [
                    self._black_cells_vars[r, c],
                    self._black_cells_vars[r, c+1],
                    self._black_cells_vars[r+1, c],
                    self._black_cells_vars[r+1, c+1]
                ]
                self._model.add(sum(area_vars) <= 3)

    def _add_connectivity_constraints(self):
        num_cells = self.rows_number * self.columns_number
        ranks = Grid([[self._model.new_int_var(0, num_cells - 1, f'rank_{r}_{c}') 
                       for c in range(self.columns_number)] 
                      for r in range(self.rows_number)])
        
        is_root = Grid([[self._model.new_bool_var(f'is_root_{r}_{c}') 
                         for c in range(self.columns_number)] 
                        for r in range(self.rows_number)])

        self._model.add(sum(cell for row in is_root.matrix for cell in row) == 1)

        for r in range(self.rows_number):
            for c in range(self.columns_number):
                pos = Position(r, c)
                u_is_black = self._black_cells_vars[pos]
                u_rank = ranks[pos]
                u_is_root = is_root[pos]

                # Un root doit être noir et avoir un rang 0
                self._model.add(u_is_black == 1).only_enforce_if(u_is_root)
                self._model.add(u_rank == 0).only_enforce_if(u_is_root)
                
                # Si une cellule n'est pas noire, elle ne peut pas être root
                self._model.add(u_is_root == 0).only_enforce_if(u_is_black.negated())

                # Chaque cellule noire non-root doit avoir au moins un voisin noir avec un rang inférieur
                has_parent = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows_number and 0 <= nc < self.columns_number:
                        v_pos = Position(nr, nc)
                        v_is_black = self._black_cells_vars[v_pos]
                        v_rank = ranks[v_pos]

                        p = self._model.new_bool_var(f'parent_{r}_{c}_{nr}_{nc}')
                        self._model.add(v_is_black == 1).only_enforce_if(p)
                        self._model.add(v_rank < u_rank).only_enforce_if(p)
                        has_parent.append(p)

                # Si u est noir et n'est pas root, il doit avoir un parent (donc connecté au root)
                self._model.add_bool_or(has_parent).only_enforce_if([u_is_black, u_is_root.negated()])
                
                # Optionnel : si u n'est pas noir, son rang est 0 (pour simplifier le domaine)
                self._model.add(u_rank == 0).only_enforce_if(u_is_black.negated())

    def _add_square_regions_constraint(self):
        is_white = Grid([[self._black_cells_vars[r, c].negated() for c in range(self.columns_number)] for r in range(self.rows_number)])

        h_run = Grid([[self._model.new_int_var(0, self.columns_number, f'h_run_{r}_{c}') for c in range(self.columns_number)] for r in range(self.rows_number)])
        v_run = Grid([[self._model.new_int_var(0, self.rows_number, f'v_run_{r}_{c}') for c in range(self.rows_number)] for r in range(self.rows_number)])
        
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                self._model.add(h_run[r, c] == 0).only_enforce_if(is_white[r, c].negated())
                self._model.add(v_run[r, c] == 0).only_enforce_if(is_white[r, c].negated())
                
                if c == 0:
                    self._model.add(h_run[r, c] == 1).only_enforce_if(is_white[r, c])
                else:
                    self._model.add(h_run[r, c] == h_run[r, c-1] + 1).only_enforce_if(is_white[r, c])
                
                if r == 0:
                    self._model.add(v_run[r, c] == 1).only_enforce_if(is_white[r, c])
                else:
                    self._model.add(v_run[r, c] == v_run[r-1, c] + 1).only_enforce_if(is_white[r, c])

        for r in range(self.rows_number - 1):
            for c in range(self.columns_number - 1):
                w1 = is_white[r, c]
                w2 = is_white[r, c+1]
                w3 = is_white[r+1, c]
                w4 = is_white[r+1, c+1]
                
                self._model.add_bool_or([w1.negated(), w2.negated(), w3.negated(), w4])
                self._model.add_bool_or([w1.negated(), w2.negated(), w4.negated(), w3])
                self._model.add_bool_or([w1.negated(), w3.negated(), w4.negated(), w2])
                self._model.add_bool_or([w2.negated(), w3.negated(), w4.negated(), w1])
                
        for r in range(self.rows_number):
            for c in range(self.columns_number):
                below_is_black = self._black_cells_vars[r+1, c] if r < self.rows_number - 1 else 1
                right_is_black = self._black_cells_vars[r, c+1] if c < self.columns_number - 1 else 1
                is_br = self._model.new_bool_var(f'is_br_{r}_{c}')
                
                self._model.add_bool_and([is_white[r, c], below_is_black, right_is_black]).only_enforce_if(is_br)
                
                not_br = [is_white[r, c].negated()]
                if not isinstance(below_is_black, int): not_br.append(below_is_black.negated())
                elif below_is_black == 0: not_br.append(1)
                if not isinstance(right_is_black, int): not_br.append(right_is_black.negated())
                elif right_is_black == 0: not_br.append(1)
                self._model.add_bool_or(not_br).only_enforce_if(is_br.negated())
                
                self._model.add(h_run[r, c] == v_run[r, c]).only_enforce_if(is_br)