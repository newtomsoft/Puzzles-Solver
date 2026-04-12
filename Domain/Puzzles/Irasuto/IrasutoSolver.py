from ortools.sat.python import cp_model
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver

class IrasutoSolver(GameSolver):
    empty = None
    white = 'w'
    black = 'b'

    def __init__(self, grid: Grid, initial_colors: Grid = None):
        self._grid = grid
        self._initial_colors = initial_colors
        self._rows = grid.rows_number
        self._cols = grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._color_vars = {}

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
        for r in range(self._rows):
            for c in range(self._cols):
                # self._color_vars[(r, c)] est True si la cellule finale est noire, False si blanche
                self._color_vars[(r, c)] = self._model.new_bool_var(f'color_{r}_{c}')

                # Si une cellule contient un indice, sa couleur finale est fixée par initial_colors
                clue = self._grid[Position(r, c)]
                if clue is not None and self._initial_colors:
                    initial_color = self._initial_colors[Position(r, c)]
                    if initial_color == self.black:
                        self._model.add(self._color_vars[(r, c)] == True)
                    elif initial_color == self.white:
                        self._model.add(self._color_vars[(r, c)] == False)

        self._add_visibility_constraints()

    def _add_visibility_constraints(self):
        for r in range(self._rows):
            for c in range(self._cols):
                clue = self._grid[Position(r, c)]
                if clue is not None:
                    self._add_clue_constraint(r, c, clue)

    def _add_clue_constraint(self, r, c, clue):
        is_source_black = self._color_vars[(r, c)]
        
        dir_counts = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            visible_vars = []
            nr, nc = r + dr, c + dc
            while 0 <= nr < self._rows and 0 <= nc < self._cols:
                # La visibilité s'arrête s'il y a un indice
                if self._grid[Position(nr, nc)] is not None:
                    break
                
                is_visible = self._model.new_bool_var(f'vis_{r}_{c}_{nr}_{nc}')
                
                # is_visible <=> (color(nr, nc) == color(r, c)) AND is_visible(previous)
                same_color = self._model.new_bool_var(f'same_{r}_{c}_{nr}_{nc}')
                self._model.add(is_source_black == self._color_vars[(nr, nc)]).only_enforce_if(same_color)
                self._model.add(is_source_black != self._color_vars[(nr, nc)]).only_enforce_if(same_color.Not())
                
                if not visible_vars:
                    self._model.add(is_visible == same_color)
                else:
                    self._model.add_bool_and([same_color, visible_vars[-1]]).only_enforce_if(is_visible)
                    self._model.add_bool_or([same_color.Not(), visible_vars[-1].Not()]).only_enforce_if(is_visible.Not())

                visible_vars.append(is_visible)
                nr += dr
                nc += dc
            
            if visible_vars:
                count_in_dir = self._model.new_int_var(0, max(self._rows, self._cols), f'count_{r}_{c}_{dr}_{dc}')
                self._model.add(count_in_dir == sum(visible_vars))
                dir_counts.append(count_in_dir)
            
        self._model.add(sum(dir_counts) == clue)

    def _build_solution_grid(self) -> Grid:
        solution_data = [[None for _ in range(self._cols)] for _ in range(self._rows)]
        for (r, c), var in self._color_vars.items():
            if self._solver.boolean_value(var):
                solution_data[r][c] = self.black
            else:
                solution_data[r][c] = self.white
        return Grid(solution_data)
