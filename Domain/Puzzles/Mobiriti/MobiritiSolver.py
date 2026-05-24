from ortools.sat.python import cp_model
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver

class MobiritiSolver(GameSolver):
    empty = None
    white = 'w'
    black = 'b'

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows = grid.rows_number
        self._cols = grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._color_vars = {}
        self._circle_positions = set()
        for r in range(self._rows):
            for c in range(self._cols):
                if grid.value(r, c) is not None:
                    self._circle_positions.add((r, c))

    def get_solution(self) -> Grid:
        self._init_model()
        status = self._solver.solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return self._build_solution_grid()
        return Grid.empty()

    def get_other_solution(self) -> Grid:
        if not self._color_vars:
            self._init_model()
        
        literals = []
        for r in range(self._rows):
            for c in range(self._cols):
                is_black = self._solver.boolean_value(self._color_vars[(r, c)])
                if is_black:
                    literals.append(self._color_vars[(r, c)].Not())
                else:
                    literals.append(self._color_vars[(r, c)])
        self._model.add_bool_or(literals)

        status = self._solver.solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return self._build_solution_grid()
        return Grid.empty()

    def _init_model(self):
        # 0 = Blanc, 1 = Noir
        for r in range(self._rows):
            for c in range(self._cols):
                self._color_vars[(r, c)] = self._model.new_bool_var(f'color_{r}_{c}')

        for r, c in self._circle_positions:
            clue = self._grid.value(r, c)
            self._model.add(self._color_vars[(r, c)] == 0)
            self._add_clue_constraint(r, c, clue)
        
        # On essaie AVEC la contrainte de connectivité
        self._add_global_connectivity_constraint()

    def _add_clue_constraint(self, r, c, clue):
        visibility_vars = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            curr_r, curr_c = r + dr, c + dc
            prev_visible = None
            while 0 <= curr_r < self._rows and 0 <= curr_c < self._cols:
                is_other_circle = (curr_r, curr_c) in self._circle_positions and (curr_r, curr_c) != (r, c)
                is_visible = self._model.new_bool_var(f'is_visible_{r}_{c}_{curr_r}_{curr_c}')
                
                if is_other_circle:
                    self._model.add(is_visible == 0)
                    prev_visible = 0
                else:
                    is_white = self._color_vars[(curr_r, curr_c)].Not()
                    if prev_visible is None:
                        self._model.add(is_visible == is_white)
                    else:
                        if prev_visible == 0:
                            self._model.add(is_visible == 0)
                        else:
                            self._model.add_bool_and([is_white, prev_visible]).only_enforce_if(is_visible)
                            self._model.add_bool_or([is_white.Not(), prev_visible.Not()]).only_enforce_if(is_visible.Not())
                    prev_visible = is_visible
                
                if not is_other_circle:
                    visibility_vars.append(is_visible)
                
                curr_r += dr
                curr_c += dc
        
        self._model.add(sum(visibility_vars) == clue)

    def _add_global_connectivity_constraint(self):
        # On choisit une cellule blanche comme racine (une cellule avec un cercle)
        if not self._circle_positions:
            return
        root_pos = list(self._circle_positions)[0]
        
        # Variables de distance depuis la racine pour toutes les cellules blanches
        dist_vars = {}
        for r in range(self._rows):
            for c in range(self._cols):
                dist_vars[(r, c)] = self._model.new_int_var(0, self._rows * self._cols, f'gdist_{r}_{c}')
        
        self._model.add(dist_vars[root_pos] == 0)
        
        for r in range(self._rows):
            for c in range(self._cols):
                if (r, c) == root_pos:
                    continue
                
                neighbors = []
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self._rows and 0 <= nc < self._cols:
                        neighbors.append((nr, nc))
                
                connection_options = []
                for nr, nc in neighbors:
                    is_parent = self._model.new_bool_var(f'gparent_{r}_{c}_{nr}_{nc}')
                    self._model.add(self._color_vars[(nr, nc)] == 0).only_enforce_if(is_parent)
                    self._model.add(dist_vars[(nr, nc)] < dist_vars[(r, c)]).only_enforce_if(is_parent)
                    connection_options.append(is_parent)
                
                # Si la cellule est blanche, elle doit être connectée à la racine
                self._model.add_bool_or(connection_options).only_enforce_if(self._color_vars[(r, c)].Not())

    def _build_solution_grid(self) -> Grid:
        solution_data = [[None for _ in range(self._cols)] for _ in range(self._rows)]
        for (r, c), var in self._color_vars.items():
            if self._solver.boolean_value(var):
                solution_data[r][c] = self.black
            else:
                solution_data[r][c] = self.white
        return Grid(solution_data)
