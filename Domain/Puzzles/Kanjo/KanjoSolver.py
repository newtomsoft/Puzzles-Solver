from collections import defaultdict

from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class KanjoSolver(GameSolver):
    horizontal = -1
    vertical = -2
    empty = None

    def __init__(self, grid: Grid):
        self._input_grid = grid
        self._rows_number, self._columns_number = grid.rows_number, grid.columns_number
        
        raw_clues = {pos: val for pos, val in self._input_grid if isinstance(val, int)}
        self._clues_by_positions = raw_clues
        
        unique_clues = sorted(list(set(raw_clues.values())))
        self._clue_map = {clue: i for i, clue in enumerate(unique_clues)}
        self._loop_count = len(unique_clues)
        
        self._positions_by_clues = defaultdict(list)
        for pos, val in raw_clues.items():
            self._positions_by_clues[val].append(pos)

        self._model = None
        self._solver = None
        
        self._h_arcs = None
        self._v_arcs = None
        self._loop_id = None
        self._loop_id_hor = None
        self._loop_id_ver = None
        self._is_deg2 = None
        self._is_deg4 = None
        
        self._island_grid = None
        self._previous_solution = None

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._create_variables()
        self._add_constraints()

    def get_solution(self) -> Grid:
        if self._model is None:
            self._init_model()
        
        self._solver = cp_model.CpSolver()
        solution, _ = self._ensure_all_islands_grouped()
        return solution

    def get_other_solution(self):
        if self._previous_solution:
             self._exclude_solution(self._previous_solution)
        return self.get_solution()

    def _create_variables(self):
        rows, cols = self._rows_number, self._columns_number
        self._h_arcs = [[self._model.NewBoolVar(f'h_{r}_{c}') for c in range(cols-1)] for r in range(rows)]
        self._v_arcs = [[self._model.NewBoolVar(f'v_{r}_{c}') for c in range(cols)] for r in range(rows-1)]
        
        self._loop_id = [[self._model.NewIntVar(0, self._loop_count - 1, f'id_{r}_{c}') for c in range(cols)] for r in range(rows)]
        self._loop_id_hor = [[self._model.NewIntVar(0, self._loop_count - 1, f'id_h_{r}_{c}') for c in range(cols)] for r in range(rows)]
        self._loop_id_ver = [[self._model.NewIntVar(0, self._loop_count - 1, f'id_v_{r}_{c}') for c in range(cols)] for r in range(rows)]
        
        self._is_deg2 = [[self._model.NewBoolVar(f'd2_{r}_{c}') for c in range(cols)] for r in range(rows)]
        self._is_deg4 = [[self._model.NewBoolVar(f'd4_{r}_{c}') for c in range(cols)] for r in range(rows)]

    def _add_constraints(self):
        rows, cols = self._rows_number, self._columns_number
        
        for r in range(rows):
            for c in range(cols):
                edges = []
                if c > 0: edges.append(self._h_arcs[r][c-1])
                if c < cols - 1: edges.append(self._h_arcs[r][c])
                if r > 0: edges.append(self._v_arcs[r-1][c])
                if r < rows - 1: edges.append(self._v_arcs[r][c])
                
                degree = sum(edges)
                
                # Must be 2 or 4
                self._model.Add(degree == 2).OnlyEnforceIf(self._is_deg2[r][c])
                self._model.Add(degree == 4).OnlyEnforceIf(self._is_deg4[r][c])
                self._model.Add(self._is_deg2[r][c] + self._is_deg4[r][c] == 1)
                
        # 2. Clue Constraints
        for pos, clue_val in self._clues_by_positions.items():
            r, c = pos.r, pos.c
            mapped_id = self._clue_map[clue_val]
            
            # Clues imply degree 2
            self._model.Add(self._is_deg2[r][c] == 1)
            # Clues imply loop_id
            self._model.Add(self._loop_id[r][c] == mapped_id)

        # 3. Pre-filled Bridges
        for r in range(rows):
            for c in range(cols):
                pos = Position(r, c)
                item = self._input_grid[pos]
                if isinstance(item, Island) and not item.has_no_bridge():
                    for direction, (_, val) in item.direction_position_bridges.items():
                        is_bridge = (val == 1)
                        arc = self._get_arc_var(r, c, direction)
                        if arc is not None:
                            self._model.Add(arc == is_bridge)

        # 4. Loop ID Propagation
        for r in range(rows):
            for c in range(cols):
                # Horizontal Connection (Right)
                if c < cols - 1:
                    edge = self._h_arcs[r][c]
                    
                    u_d2 = self._is_deg2[r][c]
                    u_d4 = self._is_deg4[r][c]
                    v_d2 = self._is_deg2[r][c+1]
                    v_d4 = self._is_deg4[r][c+1]
                    
                    # u(2) - v(2)
                    self._model.Add(self._loop_id[r][c] == self._loop_id[r][c+1]).OnlyEnforceIf([edge, u_d2, v_d2])
                    # u(4) - v(2)
                    self._model.Add(self._loop_id_hor[r][c] == self._loop_id[r][c+1]).OnlyEnforceIf([edge, u_d4, v_d2])
                    # u(2) - v(4)
                    self._model.Add(self._loop_id[r][c] == self._loop_id_hor[r][c+1]).OnlyEnforceIf([edge, u_d2, v_d4])
                    # u(4) - v(4)
                    self._model.Add(self._loop_id_hor[r][c] == self._loop_id_hor[r][c+1]).OnlyEnforceIf([edge, u_d4, v_d4])

                # Vertical Connection (Down)
                if r < rows - 1:
                    edge = self._v_arcs[r][c]
                    
                    u_d2 = self._is_deg2[r][c]
                    u_d4 = self._is_deg4[r][c]
                    v_d2 = self._is_deg2[r+1][c]
                    v_d4 = self._is_deg4[r+1][c]
                    
                    # u(2) - v(2)
                    self._model.Add(self._loop_id[r][c] == self._loop_id[r+1][c]).OnlyEnforceIf([edge, u_d2, v_d2])
                    # u(4) - v(2)
                    self._model.Add(self._loop_id_ver[r][c] == self._loop_id[r+1][c]).OnlyEnforceIf([edge, u_d4, v_d2])
                    # u(2) - v(4)
                    self._model.Add(self._loop_id[r][c] == self._loop_id_ver[r+1][c]).OnlyEnforceIf([edge, u_d2, v_d4])
                    # u(4) - v(4)
                    self._model.Add(self._loop_id_ver[r][c] == self._loop_id_ver[r+1][c]).OnlyEnforceIf([edge, u_d4, v_d4])

    def _ensure_all_islands_grouped(self):
        propositions_count = 0
        while True:
            status = self._solver.Solve(self._model)
            if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
                return IslandGrid.empty(), propositions_count
            
            propositions_count += 1
            self._build_island_grid_from_solution()
            
            connected_positions = self._island_grid.compute_linear_connected_positions(exclude_without_bridge=False)
            
            if len(connected_positions) == self._loop_count:
                all_valid = True
                for loop in connected_positions:
                    if self._exclude_loop_without_clue(loop):
                        all_valid = False
                        break 
                    if self._exclude_loop_with_forgotten_clue(loop):
                        all_valid = False
                        break
                
                if all_valid:
                    self._previous_solution = self._island_grid
                    return self._island_grid, propositions_count
            else:
                 for loop in connected_positions:
                    if self._exclude_loop_without_clue(loop): continue
                    self._exclude_loop_with_forgotten_clue(loop)
    
    def _exclude_solution(self, solution):
        constraints = []
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                 pos = Position(r, c)
                 island = solution[pos]
                 
                 if c < self._columns_number - 1:
                     has_right = Direction.right() in island.direction_position_bridges and island.direction_position_bridges[Direction.right()][1] > 0
                     if has_right:
                         constraints.append(self._h_arcs[r][c].Not())
                     else:
                         constraints.append(self._h_arcs[r][c])
                 
                 if r < self._rows_number - 1:
                     has_down = Direction.down() in island.direction_position_bridges and island.direction_position_bridges[Direction.down()][1] > 0
                     if has_down:
                         constraints.append(self._v_arcs[r][c].Not())
                     else:
                         constraints.append(self._v_arcs[r][c])
        self._model.AddBoolOr(constraints)

    def _exclude_loop_without_clue(self, loop):
        has_clue = not loop.isdisjoint(self._clues_by_positions.keys())
        if not has_clue:
            self._exclude_positions_values_together(loop)
            return True
        return False

    def _exclude_loop_with_forgotten_clue(self, loop):
        clue_val = self._get_clue_from_positions(loop)
        if clue_val is None: return False 
        
        required_positions = set(self._positions_by_clues[clue_val])
        if not required_positions.issubset(loop):
            self._exclude_positions_values_together(loop)
            return True
        return False

    def _exclude_positions_values_together(self, positions):
        constraints = []
        for pos in positions:
            r, c = pos.r, pos.c
            for direction in Direction.orthogonal_directions():
                arc = self._get_arc_var(r, c, direction)
                if arc is not None:
                    val = self._solver.Value(arc)
                    if val:
                        constraints.append(arc.Not())
                    else:
                        constraints.append(arc)
        
        self._model.AddBoolOr(constraints)

    def _get_arc_var(self, r, c, direction):
        if direction == Direction.right():
            if c < self._columns_number - 1: return self._h_arcs[r][c]
        elif direction == Direction.left():
            if c > 0: return self._h_arcs[r][c-1]
        elif direction == Direction.down():
            if r < self._rows_number - 1: return self._v_arcs[r][c]
        elif direction == Direction.up():
            if r > 0: return self._v_arcs[r-1][c]
        return None

    def _build_island_grid_from_solution(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self._columns_number)] for r in range(self._rows_number)])
        for r in range(self._rows_number):
            for c in range(self._columns_number):
                pos = Position(r, c)
                island = self._island_grid[pos]
                
                if c < self._columns_number - 1 and self._solver.Value(self._h_arcs[r][c]):
                    island.set_bridge_to_direction(Direction.right(), 1)

                if c > 0 and self._solver.Value(self._h_arcs[r][c-1]):
                    island.set_bridge_to_direction(Direction.left(), 1)

                if r < self._rows_number - 1 and self._solver.Value(self._v_arcs[r][c]):
                    island.set_bridge_to_direction(Direction.down(), 1)

                if r > 0 and self._solver.Value(self._v_arcs[r-1][c]):
                    island.set_bridge_to_direction(Direction.up(), 1)
                
                island.set_bridges_count_according_to_directions_bridges()

    def _get_clue_from_positions(self, loop):
        for pos in loop:
            if pos in self._clues_by_positions:
                return self._clues_by_positions[pos]
        return None