
class MasyuDeductionSolver:
    def __init__(self, grid):
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.grid = grid
        # 0: unknown, 1: line, -1: noline
        self.h_edges = [[0] * (self.cols - 1) for _ in range(self.rows)]
        self.v_edges = [[0] * self.cols for _ in range(self.rows - 1)]

    def get_h(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols - 1:
            return self.h_edges[r][c]
        return -1 # Boundary is noline

    def get_v(self, r, c):
        if 0 <= r < self.rows - 1 and 0 <= c < self.cols:
            return self.v_edges[r][c]
        return -1

    def set_h(self, r, c, val):
        if 0 <= r < self.rows and 0 <= c < self.cols - 1:
            if self.h_edges[r][c] != 0 and self.h_edges[r][c] != val:
                return False # Conflict
            self.h_edges[r][c] = val
            return True
        return val == -1

    def set_v(self, r, c, val):
        if 0 <= r < self.rows - 1 and 0 <= c < self.cols:
            if self.v_edges[r][c] != 0 and self.v_edges[r][c] != val:
                return False
            self.v_edges[r][c] = val
            return True
        return val == -1

    def neighbors(self, r, c):
        # returns [(type, r, c), ...]
        ns = []
        if r > 0: ns.append(('v', r-1, c)) # Up
        if r < self.rows - 1: ns.append(('v', r, c)) # Down
        if c > 0: ns.append(('h', r, c-1)) # Left
        if c < self.cols - 1: ns.append(('h', r, c)) # Right
        return ns

    def get_edge_val(self, kind, r, c):
        if kind == 'h': return self.get_h(r, c)
        return self.get_v(r, c)

    def set_edge_val(self, kind, r, c, val):
        if kind == 'h': return self.set_h(r, c, val)
        return self.set_v(r, c, val)

    def propagate(self):
        changed = True
        while changed:
            changed = False
            # 1. Degree constraints (must be 0 or 2)
            # Actually for Masyu, loop passes through ALL circles, but non-circles can be empty.
            # Wait, standard Masyu: loop visits SOME cells. Circles MUST be visited.

            for r in range(self.rows):
                for c in range(self.cols):
                    ns = self.neighbors(r, c)
                    lines = [n for n in ns if self.get_edge_val(*n) == 1]
                    nolines = [n for n in ns if self.get_edge_val(*n) == -1]
                    unknown = [n for n in ns if self.get_edge_val(*n) == 0]

                    # If circle, degree must be 2
                    is_circle = self.grid[r][c] in ['b', 'w']
                    if is_circle:
                        # Logic for circles
                        if len(lines) > 2: return False
                        if len(lines) == 2:
                            for u in unknown:
                                if not self.set_edge_val(*u, -1): return False
                                changed = True
                        if len(lines) + len(unknown) < 2: return False
                        if len(lines) + len(unknown) == 2:
                            for u in unknown:
                                if not self.set_edge_val(*u, 1): return False
                                changed = True
                    else:
                        # Empty cell: degree 0 or 2
                        if len(lines) > 2: return False
                        if len(lines) == 2:
                             for u in unknown:
                                if not self.set_edge_val(*u, -1): return False
                                changed = True
                        if len(lines) == 1 and len(unknown) == 0: return False # Dead end
                        if len(nolines) == 3 and len(lines) == 1: return False # Forced dead end
                        if len(nolines) == 4: pass # Isolated, ok

                        # If 3 neighbors are blocked, the 4th must be blocked
                        if len(nolines) == 3 and len(unknown) == 1:
                             if not self.set_edge_val(*unknown[0], -1): return False
                             changed = True

            # 2. Black circle constraints
            # - Must turn (90 deg)
            # - Must extend 2 segments on both legs
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r][c] == 'b':
                        ns = self.neighbors(r, c)
                        # Identify edges: up, down, left, right
                        up = ('v', r-1, c)
                        down = ('v', r, c)
                        left = ('h', r, c-1)
                        right = ('h', r, c)

                        # Rule: Must turn -> cannot have (up AND down) OR (left AND right)
                        # Block straight passage
                        if self.get_edge_val(*up) == 1:
                            if not self.set_edge_val(*down, -1): return False
                            changed = True
                        if self.get_edge_val(*down) == 1:
                            if not self.set_edge_val(*up, -1): return False
                            changed = True
                        if self.get_edge_val(*left) == 1:
                            if not self.set_edge_val(*right, -1): return False
                            changed = True
                        if self.get_edge_val(*right) == 1:
                             if not self.set_edge_val(*left, -1): return False
                             changed = True

                        # Extension rule: if we go Up, we must go Up again from (r-1, c)
                        # i.e. v_edge(r-2, c) must be 1
                        if self.get_edge_val(*up) == 1:
                             if not self.set_edge_val('v', r-2, c, 1): return False # might be OOB -> False
                             changed = True
                        if self.get_edge_val(*down) == 1:
                             if not self.set_edge_val('v', r+1, c, 1): return False
                             changed = True
                        if self.get_edge_val(*left) == 1:
                             if not self.set_edge_val('h', r, c-2, 1): return False
                             changed = True
                        if self.get_edge_val(*right) == 1:
                             if not self.set_edge_val('h', r, c+1, 1): return False
                             changed = True

            # 3. White circle constraints
            # - Must go straight
            # - Must turn on one side immediately
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r][c] == 'w':
                        up = ('v', r-1, c)
                        down = ('v', r, c)
                        left = ('h', r, c-1)
                        right = ('h', r, c)

                        # Cannot turn -> (up and left/right), (down and left/right) forbidden
                        # Effectively: either (up and down) OR (left and right)
                        # If we have Up, we MUST have Down.
                        if self.get_edge_val(*up) == 1:
                            if not self.set_edge_val(*down, 1): return False
                            changed = True
                        if self.get_edge_val(*down) == 1:
                            if not self.set_edge_val(*up, 1): return False
                            changed = True
                        if self.get_edge_val(*left) == 1:
                            if not self.set_edge_val(*right, 1): return False
                            changed = True
                        if self.get_edge_val(*right) == 1:
                             if not self.set_edge_val(*left, 1): return False
                             changed = True

                        # If vertical, check turns at neighbors
                        # If (up, down) are 1:
                        # Then at (r-1, c), it MUST turn or at (r+1, c) it MUST turn.
                        # This implies: it cannot be that (r-1,c) goes straight AND (r+1,c) goes straight.
                        # Straight at (r-1, c) vertical means v(r-2, c) == 1
                        pass # Complex logic for "at least one side turns", leave for backtracking or deep lookahead

        return True

    def solve(self):
        if not self.propagate():
            return None

        # Check if solved
        unknowns = []
        for r in range(self.rows):
            for c in range(self.cols - 1):
                if self.h_edges[r][c] == 0: unknowns.append(('h', r, c))
        for r in range(self.rows - 1):
            for c in range(self.cols):
                if self.v_edges[r][c] == 0: unknowns.append(('v', r, c))

        if not unknowns:
            return {'h': self.h_edges, 'v': self.v_edges} # Validation needed?

        # Backtrack
        edge = unknowns[0]

        # Try 1
        saved_h = [row[:] for row in self.h_edges]
        saved_v = [row[:] for row in self.v_edges]

        if self.set_edge_val(*edge, 1):
            res = self.solve()
            if res: return res

        # Restore
        self.h_edges = saved_h
        self.v_edges = saved_v

        # Try -1 (no line)
        if self.set_edge_val(*edge, -1):
            res = self.solve()
            if res: return res

        return None

def solve_masyu_deduction(grid_matrix):
    solver = MasyuDeductionSolver(grid_matrix)
    res = solver.solve()
    if res:
        # Convert -1 to 0 for output
        h = [[1 if x==1 else 0 for x in row] for row in res['h']]
        v = [[1 if x==1 else 0 for x in row] for row in res['v']]
        return {'h': h, 'v': v}
    return None
