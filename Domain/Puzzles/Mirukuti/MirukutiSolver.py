from ortools.sat.python import cp_model
from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver

class MirukutiSolver(GameSolver):
    MILK = 'W'
    COOKIE = 'B'

    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows = grid.rows_number
        self.cols = grid.columns_number
        self.milks = []
        self.biscuits = []
        for r in range(self.rows):
            for c in range(self.cols):
                val = grid.value(r, c)
                # Handle Island objects which might have type_char or need to check repr
                if hasattr(val, 'type_char') and val.type_char:
                    char = val.type_char
                elif hasattr(val, 'has_no_bridge'):
                    char = repr(val).strip()
                else:
                    char = str(val).strip()

                if char == self.MILK:
                    self.milks.append(Position(r, c))
                elif char == self.COOKIE:
                    self.biscuits.append(Position(r, c))
        
        self._model = cp_model.CpModel()
        self._constraints_added = False
        self._previous_solution = None

    def get_solution(self) -> IslandGrid:
        if not self.biscuits:
            return IslandGrid.empty()
            
        if not self._constraints_added:
            self._add_constraints()
            self._constraints_added = True
        
        solver = cp_model.CpSolver()
        # solver.parameters.log_search_progress = True
        status = solver.solve(self._model)
        
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            self._last_solver = solver
            # Create a matrix of Islands
            island_matrix = [[Island(Position(r, c), 0) for c in range(self.cols)] for r in range(self.rows)]
            
            # Set type_char for circles
            for m_pos in self.milks:
                island_matrix[m_pos.r][m_pos.c].type_char = self.MILK
            for b_pos in self.biscuits:
                island_matrix[b_pos.r][b_pos.c].type_char = self.COOKIE
                
            island_grid = IslandGrid(island_matrix)
            island_grid.biscuits = []
            
            for b_idx, biscuit_pos in enumerate(self.biscuits):
                j_r = solver.value(self._j_r[b_idx])
                j_c = solver.value(self._j_c[b_idx])
                junction_pos = Position(j_r, j_c)
                
                biscuit_info = {
                    'pos': biscuit_pos,
                    'junction': junction_pos,
                    'milks': []
                }
                
                # Bar: top1 to top2 through junction
                # Stem: biscuit to junction
                
                # Draw stem
                curr = biscuit_pos
                d_stem = biscuit_pos.direction_to(junction_pos)
                if d_stem != Direction.none():
                    dist = abs(biscuit_pos.r - junction_pos.r) + abs(biscuit_pos.c - junction_pos.c)
                    for _ in range(dist):
                        nxt = curr.after(d_stem)
                        island_grid.value(curr).set_bridge_to_position(nxt, 1)
                        island_grid.value(nxt).set_bridge_to_position(curr, 1)
                        curr = nxt
                
                # Draw bar
                # Find which Milk corresponds to which end
                for e in [0, 1]:
                    for m_idx, m_pos in enumerate(self.milks):
                        if solver.value(self._milk_assigned[m_idx][b_idx][e]):
                            biscuit_info['milks'].append(m_pos)
                            curr = m_pos
                            d_bar = m_pos.direction_to(junction_pos)
                            if d_bar != Direction.none():
                                dist = abs(m_pos.r - junction_pos.r) + abs(m_pos.c - junction_pos.c)
                                for _ in range(dist):
                                    nxt = curr.after(d_bar)
                                    island_grid.value(curr).set_bridge_to_position(nxt, 1)
                                    island_grid.value(nxt).set_bridge_to_position(curr, 1)
                                    curr = nxt
                
                island_grid.biscuits.append(biscuit_info)
                
            for r in range(self.rows):
                for c in range(self.cols):
                    island_grid.value(r, c).set_bridges_count_according_to_directions_bridges()
            
            self._previous_solution = island_grid
            return self._previous_solution
        return IslandGrid.empty()

    def _add_constraints(self):
        num_biscuits = len(self.biscuits)
        num_milks = len(self.milks)
        all_circle_positions_set = set((p.r, p.c) for p in (self.milks + self.biscuits))

        # Decision variables
        self._j_r = [self._model.new_int_var(0, self.rows - 1, f'j_r_{i}') for i in range(num_biscuits)]
        self._j_c = [self._model.new_int_var(0, self.cols - 1, f'j_c_{i}') for i in range(num_biscuits)]
        
        # milk_assigned[m_idx][b_idx][end_idx] where end_idx is 0 or 1
        self._milk_assigned = [[[self._model.new_bool_var(f'm_{m}_b_{b}_e_{e}') 
                                 for e in range(2)] 
                                for b in range(num_biscuits)] 
                               for m in range(num_milks)]
        
        # Segment variables for conflicts
        seg_h = [[[] for _ in range(self.cols - 1)] for _ in range(self.rows)]
        seg_v = [[[] for _ in range(self.cols)] for _ in range(self.rows - 1)]

        # Precompute valid configurations for each biscuit
        for b_idx in range(num_biscuits):
            b_pos = self.biscuits[b_idx]
            valid_configs = [] # (jr, jc, m1_idx, m2_idx)
            
            # Possible junctions (must be aligned with biscuit, no obstacles)
            possible_junctions = []
            for r in range(self.rows):
                for c in range(self.cols):
                    if r != b_pos.r and c != b_pos.c: continue
                    dist = abs(r - b_pos.r) + abs(c - b_pos.c)
                    d = b_pos.direction_to(Position(r, c))
                    possible = True
                    if d != Direction.none():
                        curr = b_pos.after(d)
                        for _ in range(dist - 1):
                            if (curr.r, curr.c) in all_circle_positions_set:
                                possible = False
                                break
                            curr = curr.after(d)
                    if possible:
                        possible_junctions.append((r, c, d))
            
            config_vars = []
            for jr, jc, stem_d in possible_junctions:
                # For each junction, find valid milk pairs
                # Bar must be perpendicular to stem
                bar_is_vert = (stem_d.value in [Direction._RIGHT, Direction._LEFT] or stem_d == Direction.none())
                
                # Find candidate milks for each end
                milks_end0 = [] # (m_idx, dist)
                milks_end1 = []
                
                for m_idx, m_pos in enumerate(self.milks):
                    if (m_pos.r == jr and m_pos.c == jc): continue # junction cannot be a milk
                    
                    if bar_is_vert:
                        if m_pos.c != jc: continue
                        dist = m_pos.r - jr
                        if dist < 0: milks_end0.append((m_idx, abs(dist)))
                        else: milks_end1.append((m_idx, dist))
                    else:
                        if m_pos.r != jr: continue
                        dist = m_pos.c - jc
                        if dist < 0: milks_end0.append((m_idx, abs(dist)))
                        else: milks_end1.append((m_idx, dist))
                
                # For each valid pair (m0, m1)
                for m0_idx, d0 in milks_end0:
                    # Check path jr to m0
                    if not self._is_path_clear(Position(jr, jc), self.milks[m0_idx], all_circle_positions_set): continue
                    for m1_idx, d1 in milks_end1:
                        # Check path jr to m1
                        if not self._is_path_clear(Position(jr, jc), self.milks[m1_idx], all_circle_positions_set): continue
                        
                        # This is a valid configuration
                        cv = self._model.new_bool_var(f'conf_{b_idx}_{jr}_{jc}_{m0_idx}_{m1_idx}')
                        config_vars.append(cv)
                        
                        # Link config to junction and milks
                        self._model.add(self._j_r[b_idx] == jr).only_enforce_if(cv)
                        self._model.add(self._j_c[b_idx] == jc).only_enforce_if(cv)
                        self._model.add(self._milk_assigned[m0_idx][b_idx][0] == 1).only_enforce_if(cv)
                        self._model.add(self._milk_assigned[m1_idx][b_idx][1] == 1).only_enforce_if(cv)
                        
                        # Segments for this configuration
                        # Stem segments
                        if stem_d != Direction.none():
                            self._add_segments(b_pos, Position(jr, jc), cv, seg_h, seg_v)
                        # Bar segments
                        self._add_segments(Position(jr, jc), self.milks[m0_idx], cv, seg_h, seg_v)
                        self._add_segments(Position(jr, jc), self.milks[m1_idx], cv, seg_h, seg_v)

            # Exactly one configuration must be chosen for each biscuit
            self._model.add(sum(config_vars) == 1)

        # Global constraints (unchanged logic, applied to optimized segment lists)
        for m_idx in range(num_milks):
            self._model.add(sum(self._milk_assigned[m_idx][b][e] for b in range(num_biscuits) for e in range(2)) <= 1)
        
        for r in range(self.rows):
            for c in range(self.cols - 1):
                if seg_h[r][c]: self._model.add(sum(seg_h[r][c]) <= 1)
        for r in range(self.rows - 1):
            for c in range(self.cols):
                if seg_v[r][c]: self._model.add(sum(seg_v[r][c]) <= 1)

        # Degree and circle constraints
        for r in range(self.rows):
            for c in range(self.cols):
                incident = []
                if c > 0 and seg_h[r][c-1]: incident.extend(seg_h[r][c-1])
                if c < self.cols - 1 and seg_h[r][c]: incident.extend(seg_h[r][c])
                if r > 0 and seg_v[r-1][c]: incident.extend(seg_v[r-1][c])
                if r < self.rows - 1 and seg_v[r][c]: incident.extend(seg_v[r][c])
                
                if not incident: continue
                self._model.add(sum(incident) <= 3)
                
                val = self._grid.value(r, c)
                char = getattr(val, 'type_char', str(val).strip())
                
                if char == self.MILK:
                    m_idx = next(i for i, p in enumerate(self.milks) if p.r == r and p.c == c)
                    is_used = self._model.new_bool_var(f'm_used_{r}_{c}')
                    self._model.add(sum(self._milk_assigned[m_idx][b][e] for b in range(num_biscuits) for e in range(2)) == is_used)
                    self._model.add(sum(incident) == 1).only_enforce_if(is_used)
                    self._model.add(sum(incident) == 0).only_enforce_if(is_used.Not())
                elif char == self.COOKIE:
                    b_idx = next(i for i, p in enumerate(self.biscuits) if p.r == r and p.c == c)
                    is_j = self._model.new_bool_var(f'b_is_j_{b_idx}')
                    self._model.add(self._j_r[b_idx] == r).only_enforce_if(is_j)
                    self._model.add(self._j_c[b_idx] == c).only_enforce_if(is_j)
                    # Use a trick to find if it's the junction: if junction is (r,c), bridges = 3, else 1
                    self._model.add(sum(incident) == 3).only_enforce_if(is_j)
                    self._model.add(sum(incident) == 1).only_enforce_if(is_j.Not())
                else:
                    self._model.add(sum(incident) != 1)

    def _is_path_clear(self, p1, p2, circles):
        d = p1.direction_to(p2)
        if d == Direction.none(): return False
        dist = abs(p1.r - p2.r) + abs(p1.c - p2.c)
        curr = p1.after(d)
        for _ in range(dist - 1):
            if (curr.r, curr.c) in circles: return False
            curr = curr.after(d)
        return True

    def _add_segments(self, p1, p2, cond, seg_h, seg_v):
        d = p1.direction_to(p2)
        dist = abs(p1.r - p2.r) + abs(p1.c - p2.c)
        curr = p1
        for _ in range(dist):
            nxt = curr.after(d)
            if d.value in [Direction._RIGHT, Direction._LEFT]:
                seg_h[curr.r][min(curr.c, nxt.c)].append(cond)
            else:
                seg_v[min(curr.r, nxt.r)][curr.c].append(cond)
            curr = nxt

    def get_other_solution(self) -> IslandGrid:
        if not self._previous_solution or self._previous_solution.is_empty():
            return self.get_solution()

        # Exclude previous solution
        # A solution is defined by which milk is assigned to which biscuit and where the junctions are.
        num_biscuits = len(self.biscuits)
        num_milks = len(self.milks)

        exclusion_elements = []

        # Milk assignments
        for m in range(num_milks):
            for b in range(num_biscuits):
                for e in range(2):
                    var = self._milk_assigned[m][b][e]
                    val = self._last_solver.value(var)
                    if val:
                        exclusion_elements.append(var.Not())
                    else:
                        exclusion_elements.append(var)

        # Junction positions
        for b in range(num_biscuits):
            val_r = self._last_solver.value(self._j_r[b])
            val_c = self._last_solver.value(self._j_c[b])
            
            # We want to add a literal that is true IF (j_r[b] != val_r OR j_c[b] != val_c)
            # which is equivalent to NOT (j_r[b] == val_r AND j_c[b] == val_c)
            
            is_different_j = self._model.new_bool_var(f'diff_j_{b}_{val_r}_{val_c}')
            j_r_same = self._model.new_bool_var(f'j_r_same_{b}_{val_r}')
            j_c_same = self._model.new_bool_var(f'j_c_same_{b}_{val_c}')
            
            self._model.add(self._j_r[b] == val_r).only_enforce_if(j_r_same)
            self._model.add(self._j_r[b] != val_r).only_enforce_if(j_r_same.Not())
            self._model.add(self._j_c[b] == val_c).only_enforce_if(j_c_same)
            self._model.add(self._j_c[b] != val_c).only_enforce_if(j_c_same.Not())
            
            # is_different_j is true if NOT (j_r_same AND j_c_same)
            self._model.add_bool_or([j_r_same.Not(), j_c_same.Not()]).only_enforce_if(is_different_j)
            self._model.add_bool_and([j_r_same, j_c_same]).only_enforce_if(is_different_j.Not())
            
            exclusion_elements.append(is_different_j)
            
        # To exclude the solution, at least one decision must change.
        self._model.add_bool_or(exclusion_elements)

        return self.get_solution()
