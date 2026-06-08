from ortools.sat.python import cp_model
from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver

class MirukutiTeaseSolver(GameSolver):
    WHITE = 'W'
    BLACK = 'B'

    def __init__(self, grid: Grid):
        super().__init__()
        self._grid = grid
        self.rows = grid.rows_number
        self.cols = grid.columns_number
        self.circles = []
        for r in range(self.rows):
            for c in range(self.cols):
                cell = grid.value(r, c)
                val = None
                if cell is not None:
                    if hasattr(cell, 'type_char') and cell.type_char:
                        val = cell.type_char
                    else:
                        s_val = str(cell).strip()
                        if s_val in (self.WHITE, self.BLACK):
                            val = s_val
                
                if val in (self.WHITE, self.BLACK):
                    self.circles.append({'pos': Position(r, c), 'color': val})
        
        self._model = cp_model.CpModel()
        self._constraints_added = False
        self._previous_solution = None

    def get_solution(self) -> IslandGrid:
        if not self.circles:
            return IslandGrid.empty()
            
        if not self._constraints_added:
            self._add_constraints()
            self._constraints_added = True
        
        status = self._solver.solve(self._model)
        
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            island_matrix = [[Island(Position(r, c), 0) for c in range(self.cols)] for r in range(self.rows)]
            
            for circle in self.circles:
                island_matrix[circle['pos'].r][circle['pos'].c].type_char = circle['color']
                
            island_grid = IslandGrid(island_matrix)
            island_grid.biscuits = []
            
            for jr, jc, stem_end_idx, bar_end1_idx, bar_end2_idx, cv in self._all_configs:
                if self._solver.value(cv):
                    stem_end_pos = self.circles[stem_end_idx]['pos']
                    bar_end1_pos = self.circles[bar_end1_idx]['pos']
                    bar_end2_pos = self.circles[bar_end2_idx]['pos']
                    junction_pos = Position(jr, jc)
                    
                    island_grid.biscuits.append({
                        'junction': junction_pos,
                        'stem_end': stem_end_pos,
                        'bar_end1': bar_end1_pos,
                        'bar_end2': bar_end2_pos
                    })
                    
                    # Draw bridges
                    self._draw_bridges(island_grid, stem_end_pos, junction_pos)
                    self._draw_bridges(island_grid, bar_end1_pos, junction_pos)
                    self._draw_bridges(island_grid, bar_end2_pos, junction_pos)

            for r in range(self.rows):
                for c in range(self.cols):
                    island_grid.value(r, c).set_bridges_count_according_to_directions_bridges()
            
            self._previous_solution = island_grid
            return island_grid
        return IslandGrid.empty()

    def _draw_bridges(self, island_grid, p1, p2):
        d = p1.direction_to(p2)
        if d == Direction.none(): return
        dist = abs(p1.r - p2.r) + abs(p1.c - p2.c)
        curr = p1
        for _ in range(dist):
            nxt = curr.after(d)
            island_grid.value(curr).set_bridge_to_position(nxt, 1)
            island_grid.value(nxt).set_bridge_to_position(curr, 1)
            curr = nxt

    def _add_constraints(self):
        num_circles = len(self.circles)
        num_t_shapes = num_circles // 3
        all_circle_positions_set = set((c['pos'].r, c['pos'].c) for c in self.circles)

        # seg_h[r][c] and seg_v[r][c] to store conditions that a segment is used
        seg_h = [[[] for _ in range(self.cols - 1)] for _ in range(self.rows)]
        seg_v = [[[] for _ in range(self.cols)] for _ in range(self.rows - 1)]

        # Possible configurations for EACH T-shape
        # Actually, it's easier to say: partition circles into triplets and for each triplet, choose a junction
        # But even simpler: for each potential T-shape (triplet + junction), create a boolean variable.
        # But that's too many.
        
        # Let's use the triplet approach. 
        # For each circle i, it belongs to exactly one T-shape.
        circle_in_t = [self._model.new_int_var(0, num_t_shapes - 1, f'c_in_t_{i}') for i in range(num_circles)]
        
        # For each T-shape t, it has exactly 3 circles.
        for t in range(num_t_shapes):
            self._model.add(sum(self._model.new_bool_var(f't_{t}_c_{i}') for i in range(num_circles)) == 3)
            # Link t_t_c_i to circle_in_t[i]
            for i in range(num_circles):
                t_t_c_i = self._model.new_bool_var(f't_{t}_c_{i}')
                self._model.add(circle_in_t[i] == t).only_enforce_if(t_t_c_i)
                self._model.add(circle_in_t[i] != t).only_enforce_if(t_t_c_i.negated())

        # Wait, that's not efficient. Let's pre-find potential T-shapes.
        potential_ts = []
        for i in range(num_circles):
            for j in range(i + 1, num_circles):
                for k in range(j + 1, num_circles):
                    triplet = [i, j, k]
                    colors = [self.circles[idx]['color'] for idx in triplet]
                    # Check colors: 2 same, 1 different
                    if colors.count(self.WHITE) == 2 and colors.count(self.BLACK) == 1:
                        stem_end_idx = triplet[colors.index(self.BLACK)]
                        bar_ends_indices = [idx for idx in triplet if idx != stem_end_idx]
                    elif colors.count(self.BLACK) == 2 and colors.count(self.WHITE) == 1:
                        stem_end_idx = triplet[colors.index(self.WHITE)]
                        bar_ends_indices = [idx for idx in triplet if idx != stem_end_idx]
                    else:
                        continue
                    
                    # Find potential junctions for this triplet
                    c_stem = self.circles[stem_end_idx]['pos']
                    c_bar1 = self.circles[bar_ends_indices[0]]['pos']
                    c_bar2 = self.circles[bar_ends_indices[1]]['pos']
                    
                    # Junction J must be:
                    # 1. On the line between bar_ends (can be one of them)
                    # 2. Aligned with stem_end
                    # 3. Path J-bar1, J-bar2, J-stem_end must be clear of OTHER circles
                    
                    # Case 1: Bar is horizontal
                    if c_bar1.r == c_bar2.r:
                        jr = c_bar1.r
                        cmin, cmax = min(c_bar1.c, c_bar2.c), max(c_bar1.c, c_bar2.c)
                        for jc in range(cmin, cmax + 1):
                            if self._is_valid_junction(jr, jc, c_stem, c_bar1, c_bar2, all_circle_positions_set):
                                potential_ts.append((stem_end_idx, bar_ends_indices[0], bar_ends_indices[1], jr, jc))
                    
                    # Case 2: Bar is vertical
                    if c_bar1.c == c_bar2.c:
                        jc = c_bar1.c
                        rmin, rmax = min(c_bar1.r, c_bar2.r), max(c_bar1.r, c_bar2.r)
                        for jr in range(rmin, rmax + 1):
                            if self._is_valid_junction(jr, jc, c_stem, c_bar1, c_bar2, all_circle_positions_set):
                                potential_ts.append((stem_end_idx, bar_ends_indices[0], bar_ends_indices[1], jr, jc))

        # Variables for potential Ts
        t_vars = [self._model.new_bool_var(f't_var_{idx}') for idx in range(len(potential_ts))]
        
        # Each circle must be in exactly one T-shape
        for i in range(num_circles):
            self._model.add(sum(t_vars[idx] for idx, t in enumerate(potential_ts) if i in (t[0], t[1], t[2])) == 1)
            
        # Segment constraints (no crossing)
        for idx, (se_idx, be1_idx, be2_idx, jr, jc) in enumerate(potential_ts):
            cond = t_vars[idx]
            self._add_segments(self.circles[se_idx]['pos'], Position(jr, jc), cond, seg_h, seg_v)
            self._add_segments(self.circles[be1_idx]['pos'], Position(jr, jc), cond, seg_h, seg_v)
            self._add_segments(self.circles[be2_idx]['pos'], Position(jr, jc), cond, seg_h, seg_v)

        for r in range(self.rows):
            for c in range(self.cols - 1):
                if seg_h[r][c]: self._model.add(sum(seg_h[r][c]) <= 1)
        for r in range(self.rows - 1):
            for c in range(self.cols):
                if seg_v[r][c]: self._model.add(sum(seg_v[r][c]) <= 1)

        # Circle degree and junction logic
        for r in range(self.rows):
            for c in range(self.cols):
                incident = []
                if c > 0 and seg_h[r][c-1]: incident.extend(seg_h[r][c-1])
                if c < self.cols - 1 and seg_h[r][c]: incident.extend(seg_h[r][c])
                if r > 0 and seg_v[r-1][c]: incident.extend(seg_v[r-1][c])
                if r < self.rows - 1 and seg_v[r][c]: incident.extend(seg_v[r][c])
                
                if not incident: continue
                self._model.add(sum(incident) <= 3)
                
                # If (r,c) is a circle
                circle_idx = next((i for i, circ in enumerate(self.circles) if circ['pos'].r == r and circ['pos'].c == c), None)
                if circle_idx is not None:
                    # Circle is either an end (degree 1) or the junction (degree 3)
                    # If it's the junction of the T it belongs to, degree 3, else degree 1.
                    is_j = self._model.new_bool_var(f'is_j_{r}_{c}')
                    relevant_t_vars = [t_vars[idx] for idx, t in enumerate(potential_ts) if circle_idx in (t[0], t[1], t[2]) and t[3] == r and t[4] == c]
                    if relevant_t_vars:
                        self._model.add(is_j == sum(relevant_t_vars))
                    else:
                        self._model.add(is_j == 0)
                    
                    self._model.add(sum(incident) == 3).only_enforce_if(is_j)
                    self._model.add(sum(incident) == 1).only_enforce_if(is_j.negated())
                else:
                    # Not a circle: either a junction (degree 3) or a pass-through (degree 2) or empty
                    is_j = self._model.new_bool_var(f'not_circle_j_{r}_{c}')
                    relevant_t_vars = [t_vars[idx] for idx, t in enumerate(potential_ts) if t[3] == r and t[4] == c]
                    if relevant_t_vars:
                        self._model.add(is_j == sum(relevant_t_vars))
                    else:
                        self._model.add(is_j == 0)
                    self._model.add(sum(incident) == 3).only_enforce_if(is_j)
                    self._model.add(sum(incident) != 1).only_enforce_if(is_j.negated())

        self._all_configs = []
        # Store for extraction
        self._all_configs = [(t[3], t[4], t[0], t[1], t[2], t_vars[idx]) for idx, t in enumerate(potential_ts)]

    def _is_valid_junction(self, jr, jc, c_stem, c_bar1, c_bar2, circles_set):
        pj = Position(jr, jc)
        # Check alignment with stem
        if pj.r != c_stem.r and pj.c != c_stem.c: return False
        
        # Check paths
        for p_end in [c_stem, c_bar1, c_bar2]:
            if p_end == pj: continue
            d = pj.direction_to(p_end)
            if d == Direction.none(): return False
            dist = abs(pj.r - p_end.r) + abs(pj.c - p_end.c)
            curr = pj.after(d)
            for _ in range(dist - 1):
                if (curr.r, curr.c) in circles_set: return False
                curr = curr.after(d)
        return True

    def _add_segments(self, p1, p2, cond, seg_h, seg_v):
        d = p1.direction_to(p2)
        if d == Direction.none(): return
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
        # A solution is defined by which T-shapes are chosen.
        exclusion_elements = []

        for jr, jc, stem_end_idx, bar_end1_idx, bar_end2_idx, cv in self._all_configs:
            val = self._solver.value(cv)
            if val:
                exclusion_elements.append(cv.negated())
            else:
                exclusion_elements.append(cv)

        if exclusion_elements:
            self._model.add_bool_or(exclusion_elements)

        return self.get_solution()
