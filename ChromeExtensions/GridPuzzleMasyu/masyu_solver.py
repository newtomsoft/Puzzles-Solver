import js
import base64
import sys

# ------------------------------------------------------------------
# Masyu Solver Implementation (Optimized Backtracking)
# ------------------------------------------------------------------

class MasyuSolverWASM:
    def __init__(self, pqq, size):
        self.size = int(size)
        self.grid = self._parse_pqq(pqq)
        # 0: Unknown, 1: Path, -1: Wall
        self.h_edges = [[0] * (self.size - 1) for _ in range(self.size)]
        self.v_edges = [[0] * self.size for _ in range(self.size - 1)]
        self.degree = [[0] * self.size for _ in range(self.size)]

        # Directions: 0:Right, 1:Down, 2:Left, 3:Up
        self.deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def _parse_pqq(self, pqq):
        if "==" in pqq or (len(pqq) > 20 and len(pqq) % 4 == 0 and '|' not in pqq):
             try:
                 decoded = base64.b64decode(pqq).decode('utf-8')
                 if len(decoded) >= self.size * self.size:
                     pqq = decoded
             except:
                 pass

        cells = []
        if '|' in pqq:
            raw = pqq.split('|')
        else:
            raw = list(pqq)

        matrix = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                idx = r * self.size + c
                if idx < len(raw):
                    val = raw[idx]
                    if val == 'B': row.append(2) # Black
                    elif val == 'W': row.append(1) # White
                    else: row.append(0)
                else:
                    row.append(0)
            matrix.append(row)
        return matrix

    def solve(self):
        # Apply strict initial constraints
        if not self._apply_initial_heuristics():
            return []

        if self._solve_recursive():
            return self._extract_segments()
        return []

    def _extract_segments(self):
        segs = []
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.h_edges[r][c] == 1:
                    segs.append([r, c, r, c+1])
        for r in range(self.size - 1):
            for c in range(self.size):
                if self.v_edges[r][c] == 1:
                    segs.append([r, c, r+1, c])
        return segs

    def get_edge_val(self, r, c, d):
        if d == 0: # Right
            if c < self.size - 1: return self.h_edges[r][c]
        elif d == 1: # Down
            if r < self.size - 1: return self.v_edges[r][c]
        elif d == 2: # Left
            if c > 0: return self.h_edges[r][c-1]
        elif d == 3: # Up
            if r > 0: return self.v_edges[r-1][c]
        return -1 # Boundary

    def set_edge_val(self, r, c, d, val):
        curr = self.get_edge_val(r, c, d)
        if curr != 0 and curr != val: return False
        if curr == val: return True

        if d == 0: self.h_edges[r][c] = val
        elif d == 1: self.v_edges[r][c] = val
        elif d == 2: self.h_edges[r][c-1] = val
        elif d == 3: self.v_edges[r-1][c] = val

        if val == 1:
            self.degree[r][c] += 1
            dr, dc = self.deltas[d]
            self.degree[r + dr][c + dc] += 1

        return True

    def _apply_initial_heuristics(self):
        # 1. Pearls near edges
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 2: # Black
                    # Must have 2 legs. If near border, some edges are impossible
                    pass # Handled by degree check implicitly? No, need specific logic.
                    # Black pearl on edge -> Impossible?
                    # Actually standard Masyu: Black pearl on edge is impossible.
                    # But checking boundary neighbors:
                    if r == 0 or r == self.size-1 or c == 0 or c == self.size-1:
                        # Black pearl at border is invalid
                        pass

                if self.grid[r][c] == 1: # White
                    # White on border must run parallel
                    if r == 0 or r == self.size-1:
                        # Must be horizontal
                        if not self.set_edge_val(r, c, 0, 1): return False
                        if not self.set_edge_val(r, c, 2, 1): return False
                    if c == 0 or c == self.size-1:
                        # Must be vertical
                        if not self.set_edge_val(r, c, 1, 1): return False
                        if not self.set_edge_val(r, c, 3, 1): return False
        return True

    def _solve_recursive(self):
        # Fast fail checks
        if not self._check_consistency(): return False

        next_edge = self._find_next_edge()
        if next_edge is None:
            return self._validate_solution()

        r, c, d = next_edge

        # Try Path (1)
        if self.set_edge_val(r, c, d, 1):
             if self._solve_recursive(): return True
             # Backtrack: Unset
             self._unset_edge_val(r, c, d, 1)

        # Try Wall (-1)
        if self.set_edge_val(r, c, d, -1):
             if self._solve_recursive(): return True
             # Backtrack
             self._unset_edge_val(r, c, d, -1)

        return False

    def _unset_edge_val(self, r, c, d, old_val):
        # Revert change
        if d == 0: self.h_edges[r][c] = 0
        elif d == 1: self.v_edges[r][c] = 0
        elif d == 2: self.h_edges[r][c-1] = 0
        elif d == 3: self.v_edges[r-1][c] = 0

        if old_val == 1:
            self.degree[r][c] -= 1
            dr, dc = self.deltas[d]
            self.degree[r + dr][c + dc] -= 1

    def _check_consistency(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.degree[r][c] > 2: return False

                # Count available edges (0 or 1)
                available = 0
                for d in range(4):
                    if self.get_edge_val(r, c, d) != -1: available += 1

                # If Pearl, need exactly 2.
                if self.grid[r][c] != 0:
                     if available < 2: return False
                # If non-pearl, usually degree 2 or 0. But if degree > available, fail.
                # Actually, a non-pearl node can be degree 0 (not part of loop).
                # But if we have 1 edge set to 1, we MUST find another.
                if self.degree[r][c] == 1 and available == 1: return False

                # Black Pearl Logic (Strict)
                if self.grid[r][c] == 2:
                    # If we have 2 paths, they MUST NOT be straight (abs diff != 2)
                    paths = [d for d in range(4) if self.get_edge_val(r, c, d) == 1]
                    if len(paths) == 2:
                        if abs(paths[0] - paths[1]) == 2: return False

                    # Also, legs must be length 2.
                    # Check leg 1 extension
                    for d in paths:
                         dr, dc = self.deltas[d]
                         nr, nc = r+dr, c+dc
                         # The edge leaving (nr, nc) in direction d must be 1
                         next_edge = self.get_edge_val(nr, nc, d)
                         if next_edge == -1: return False # Blocked
                         # If 0, we can't fail yet, but we could enforce?
                         # For now, only fail on contradiction (-1)

                # White Pearl Logic (Strict)
                if self.grid[r][c] == 1:
                    paths = [d for d in range(4) if self.get_edge_val(r, c, d) == 1]
                    # If we have 2 paths, they MUST be straight
                    if len(paths) == 2:
                        if abs(paths[0] - paths[1]) != 2: return False

                        # Must turn immediately before or after
                        # i.e. at (r-1, c) or (r+1, c) etc.
                        # Check extensions. At least one side must turn.
                        # If both sides extend straight, FAIL.
                        # Extend path 1
                        d1 = paths[0]
                        dr1, dc1 = self.deltas[d1]
                        nr1, nc1 = r+dr1, c+dc1

                        d2 = paths[1] # Opposite
                        dr2, dc2 = self.deltas[d2]
                        nr2, nc2 = r+dr2, c+dc2

                        # Check if turns are blocked (walls on sides) or forced straight
                        # If extension is forced straight (edge in same dir is 1)
                        # We need turns.
                        # If next edge (straight) is 1, then we didn't turn.
                        ext1 = self.get_edge_val(nr1, nc1, d1)
                        ext2 = self.get_edge_val(nr2, nc2, d2)

                        if ext1 == 1 and ext2 == 1: return False # Both continued straight -> Invalid
        return True

    def _find_next_edge(self):
        # Priority: Edges connected to pearls, then edges connected to existing paths
        # To speed up, iterate near filled nodes
        for r in range(self.size):
            for c in range(self.size):
                if self.degree[r][c] == 1: # Essential to close path
                     for d in range(4):
                         if self.get_edge_val(r, c, d) == 0: return (r, c, d)

        # Then Pearls
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    for d in range(4):
                        if self.get_edge_val(r, c, d) == 0: return (r, c, d)

        # Standard Scan
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.h_edges[r][c] == 0: return (r, c, 0)
        for r in range(self.size - 1):
            for c in range(self.size):
                if self.v_edges[r][c] == 0: return (r, c, 1)
        return None

    def _validate_solution(self):
        # 1. Pearls satisfied (Degree 2)
        # 2. Single Loop

        # Check degrees
        pearl_count = 0
        for r in range(self.size):
            for c in range(self.size):
                d = self.degree[r][c]
                if self.grid[r][c] != 0:
                    pearl_count += 1
                    if d != 2: return False
                if d != 0 and d != 2: return False

        # Connectivity
        start = None
        nodes_on_loop = 0
        for r in range(self.size):
            for c in range(self.size):
                if self.degree[r][c] == 2:
                    if start is None: start = (r, c)
                    nodes_on_loop += 1

        if start is None: return pearl_count == 0 # Empty valid?

        # BFS/DFS to count connected component
        q = [start]
        seen = {start}
        count = 0
        while q:
            curr = q.pop()
            count += 1
            r, c = curr
            for d in range(4):
                if self.get_edge_val(r, c, d) == 1:
                    dr, dc = self.deltas[d]
                    nr, nc = r+dr, c+dc
                    if (nr, nc) not in seen:
                        seen.add((nr, nc))
                        q.append((nr, nc))

        if count != nodes_on_loop: return False # Disconnected components

        # Final Strict Pearl Check (Leg Lengths)
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 2: # Black
                    # Paths are not straight (checked in consistency).
                    # Check legs length >= 2
                    paths = [d for d in range(4) if self.get_edge_val(r, c, d) == 1]
                    for d in paths:
                        dr, dc = self.deltas[d]
                        nr, nc = r+dr, c+dc
                        # Next edge in same direction MUST be 1
                        if self.get_edge_val(nr, nc, d) != 1: return False

                if self.grid[r][c] == 1: # White
                    # Paths are straight.
                    # Must turn immediately before or after.
                    # Paths are d and d_opposite.
                    # Check extensions.
                    paths = [d for d in range(4) if self.get_edge_val(r, c, d) == 1]
                    if len(paths) != 2: return False # Should be caught by degree

                    d1 = paths[0]
                    dr1, dc1 = self.deltas[d1]
                    nr1, nc1 = r+dr1, c+dc1
                    ext1 = self.get_edge_val(nr1, nc1, d1)

                    d2 = paths[1]
                    dr2, dc2 = self.deltas[d2]
                    nr2, nc2 = r+dr2, c+dc2
                    ext2 = self.get_edge_val(nr2, nc2, d2)

                    # If BOTH extend straight, invalid.
                    if ext1 == 1 and ext2 == 1: return False

        return True

# ------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------

try:
    pqq = js.globals.get("gpl_pqq")
    size = js.globals.get("gpl_size")
    print(f"Python solving Masyu size {size}...")
    solver = MasyuSolverWASM(pqq, size)
    segments = solver.solve()
    js.globals.set("solution_segments", segments)
except Exception as e:
    print(f"Solver Error: {e}")
    js.globals.set("solution_segments", [])
