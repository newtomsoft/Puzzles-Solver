from ortools.sat.python import cp_model

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class IslandSolver(GameSolver):
    cell_empty = None
    sea = -1
    land = 0
    clue = 1

    def __init__(self, grid: Grid):
        self._grid = grid
        self._rows = grid.rows_number
        self._cols = grid.columns_number
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._land_vars = None
        self._clues = []
        self._clue_positions = set()

    def get_solution(self) -> Grid:
        self._init_model()
        status = self._solver.solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return self._build_solution_grid()
        return Grid.empty()

    def get_other_solution(self) -> Grid:
        literals = []
        for position, land_var in self._land_vars:
            literals.append(land_var.negated() if self._solver.boolean_value(land_var) else land_var)
        self._model.add_bool_or(literals)
        
        status = self._solver.solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return self._build_solution_grid()
        return Grid.empty()

    def _init_model(self):
        self._model = cp_model.CpModel()
        self._land_vars = Grid([[self._model.new_bool_var(f'land_{r}_{c}') for c in range(self._cols)] for r in range(self._rows)])
        
        for position, val in ((p, v) for p, v in self._grid if v != self.empty):
            self._clues.append({'pos': position, 'val': val, 'id': len(self._clues)})
            self._clue_positions.add(position)
            self._model.add(self._land_vars[position] == 1)

        self._add_constraints()

    def _add_constraints(self):
        self._add_reachability_constraints()
        self._add_land_ownership_constraints()
        self._add_global_connectivity_constraints()

    def _add_reachability_constraints(self):
        self._reach = []
        for clue in self._clues:
            i, v_i, pos_i = clue['id'], clue['val'], clue['pos']
            reachable_positions = []
            border_positions = []
            r0, c0 = pos_i.r, pos_i.c
            for dr in range(-v_i - 1, v_i + 2):
                for dc in range(-v_i - 1, v_i + 2):
                    r, c = r0 + dr, c0 + dc
                    if 0 <= r < self._rows and 0 <= c < self._cols:
                        pos = Position(r, c)
                        dist = abs(dr) + abs(dc)
                        if pos in self._clue_positions:
                            continue
                        if 0 < dist <= v_i:
                            reachable_positions.append(pos)
                        elif dist == v_i + 1:
                            border_positions.append(pos)
            
            reach_i = {pos: self._model.new_bool_var(f'r_{i}_{pos.r}_{pos.c}') for pos in reachable_positions}
            lp_i = {pos: self._model.new_int_var(1, v_i, f'lp_{i}_{pos.r}_{pos.c}') for pos in reachable_positions}
            self._reach.append(reach_i)

            for pos in reachable_positions + border_positions:
                is_in_reach = pos in reach_i
                if is_in_reach:
                    self._model.add(reach_i[pos] <= self._land_vars[pos])
                
                parents = []
                vars_to_or = []
                has_source = False
                
                for neighbor in self._grid.neighbors_positions(pos):
                    if neighbor == pos_i:
                        has_source = True
                        if is_in_reach:
                            is_parent = self._model.new_bool_var(f'ps_{i}_{pos.r}_{pos.c}')
                            parents.append(is_parent)
                    elif neighbor in reach_i:
                        vars_to_or.append(reach_i[neighbor])
                        if is_in_reach:
                            is_parent = self._model.new_bool_var(f'p_{i}_{pos.r}_{pos.c}_{neighbor.r}_{neighbor.c}')
                            self._model.add(lp_i[neighbor] < lp_i[pos]).only_enforce_if(is_parent)
                            self._model.add(reach_i[neighbor] == 1).only_enforce_if(is_parent)
                            parents.append(is_parent)
                
                if is_in_reach:
                    if parents:
                        self._model.add(sum(parents) >= 1).only_enforce_if(reach_i[pos])
                    else:
                        self._model.add(reach_i[pos] == 0)
                
                has_neigh = self._model.new_bool_var(f'hn_{i}_{pos.r}_{pos.c}')
                if has_source:
                    self._model.add(has_neigh == 1)
                elif not vars_to_or:
                    self._model.add(has_neigh == 0)
                else:
                    self._model.add_bool_or(vars_to_or).only_enforce_if(has_neigh)
                    self._model.add_bool_and([v.negated() for v in vars_to_or]).only_enforce_if(has_neigh.negated())
                
                if is_in_reach:
                    self._model.add(reach_i[pos] == 1).only_enforce_if([self._land_vars[pos], has_neigh])
                else:
                    self._model.add(self._land_vars[pos] == 0).only_enforce_if(has_neigh)
            
            self._model.add(sum(reach_i.values()) == v_i)

    def _add_land_ownership_constraints(self):
        for position, land_var in ((p, v) for p, v in self._land_vars if p not in self._clue_positions):
            potential_owners = [self._reach[i][position] for i in range(len(self._clues)) if position in self._reach[i]]
            if potential_owners:
                self._model.add(sum(potential_owners) >= 1).only_enforce_if(land_var)
            else:
                self._model.add(land_var == 0)

    def _add_global_connectivity_constraints(self):
        gp = Grid([[self._model.new_int_var(0, self._rows * self._cols, f'gp_{r}_{c}') for c in range(self._cols)] for r in range(self._rows)])
        root_pos = self._clues[0]['pos']
        self._model.add(gp[root_pos] == 0)
        
        for position, _ in self._grid:
            if position == root_pos:
                continue
            
            land_var = self._land_vars[position]
            parents = []
            for neighbor in self._grid.neighbors_positions(position):
                is_parent = self._model.new_bool_var(f'pgp_{position.r}_{position.c}_{neighbor.r}_{neighbor.c}')
                self._model.add(gp[neighbor] < gp[position]).only_enforce_if(is_parent)
                self._model.add(self._land_vars[neighbor] == 1).only_enforce_if(is_parent)
                parents.append(is_parent)
            
            self._model.add(sum(parents) >= 1).only_enforce_if(land_var)
            self._model.add(gp[position] == self._rows * self._cols).only_enforce_if(land_var.negated())
            self._model.add(gp[position] > 0).only_enforce_if(land_var)

    def _build_solution_grid(self) -> Grid:
        grid = Grid([[None for _ in range(self._cols)] for _ in range(self._rows)])
        for position, land_value in self._land_vars:
            if self._solver.boolean_value(land_value):
                grid[position] = self.clue if position in self._clue_positions else self.land
            else:
                grid[position] = self.sea
        return grid
