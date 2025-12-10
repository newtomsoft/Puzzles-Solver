from ortools.sat.python import cp_model
from Domain.Puzzles.GameSolver import GameSolver
from Domain.Board.Grid import Grid
from Domain.Board.SlantGrid import SlantGrid
from Domain.Board.Position import Position

class SlantSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.grid = grid
        # The grid provided represents the intersections (clues).
        # The playable area (cells) is (rows-1) x (columns-1).
        self.rows = self.grid.rows_number - 1
        self.cols = self.grid.columns_number - 1
        self._init_solver()

    def _init_solver(self):
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

        # Variables: True = Backslash (\), False = Slash (/)
        self._cells = {}
        for r in range(self.rows):
            for c in range(self.cols):
                self._cells[(r, c)] = self.model.NewBoolVar(f"cell_{r}_{c}")

        # Clue Constraints (Intersections)
        for r in range(self.grid.rows_number):
            for c in range(self.grid.columns_number):
                clue = self.grid[r][c]
                if clue is None:
                    continue

                connections = []

                # Top-Left cell (r-1, c-1) connects if Backslash (\) -> True
                if r > 0 and c > 0:
                    connections.append(self._cells[(r-1, c-1)])

                # Top-Right cell (r-1, c) connects if Slash (/) -> False
                if r > 0 and c < self.grid.columns_number - 1:
                    connections.append(self._cells[(r-1, c)].Not())

                # Bottom-Left cell (r, c-1) connects if Slash (/) -> False
                if r < self.grid.rows_number - 1 and c > 0:
                    connections.append(self._cells[(r, c-1)].Not())

                # Bottom-Right cell (r, c) connects if Backslash (\) -> True
                if r < self.grid.rows_number - 1 and c < self.grid.columns_number - 1:
                    connections.append(self._cells[(r, c)])

                self.model.Add(sum(connections) == clue)

    def get_solution(self):
        status = self.solver.Solve(self.model)

        while status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            cycle = self.find_cycle()
            if not cycle:
                return self._build_solution_grid()

            # Block the cycle
            blocking_clause = []
            for (r, c), val in cycle:
                if val: # Was True
                    blocking_clause.append(self._cells[(r, c)].Not())
                else: # Was False
                    blocking_clause.append(self._cells[(r, c)])

            self.model.AddBoolOr(blocking_clause)
            status = self.solver.Solve(self.model)

        return SlantGrid.empty()

    def get_other_solution(self):
        # Block current solution
        current_sol_clause = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.solver.Value(self._cells[(r, c)]):
                    current_sol_clause.append(self._cells[(r, c)].Not())
                else:
                    current_sol_clause.append(self._cells[(r, c)])

        self.model.AddBoolOr(current_sol_clause)
        return self.get_solution()

    def find_cycle(self):
        adj = {}
        # Build graph from current solution
        # Nodes are intersections (0..rows) x (0..cols)
        # Edges determined by cell values

        for r in range(self.rows):
            for c in range(self.cols):
                val = self.solver.Value(self._cells[(r, c)]) == 1

                # Determine connected intersections
                if val: # Backslash \
                    u = (r, c)
                    v = (r+1, c+1)
                else: # Slash /
                    u = (r, c+1)
                    v = (r+1, c)

                if u not in adj: adj[u] = []
                if v not in adj: adj[v] = []
                # Edge info: neighbor, cell_pos, cell_value
                adj[u].append((v, (r, c), val))
                adj[v].append((u, (r, c), val))

        global_visited = set()
        nodes = list(adj.keys())

        for start_node in nodes:
            if start_node in global_visited:
                continue

            # path_map: node -> (parent, edge_info_from_parent)
            path_map = {start_node: (None, None)}
            # stack stores nodes to process
            stack = [start_node]

            while stack:
                u = stack[-1]
                stack.pop()

                if u not in global_visited:
                    global_visited.add(u)

                if u in adj:
                    for v, cell_pos, cell_val in adj[u]:
                        parent_u, _ = path_map[u]
                        if v == parent_u:
                            continue

                        if v in path_map:
                            # Cycle detected
                            # v is visited in the current traversal component
                            # Find the cycle by tracing back from u and v to their LCA
                            cycle_edges = []
                            cycle_edges.append((cell_pos, cell_val))

                            # Build path from u to root
                            path_u = []
                            curr = u
                            while curr is not None:
                                path_u.append(curr)
                                curr = path_map[curr][0]

                            # Build path from v to root
                            path_v = []
                            curr = v
                            while curr is not None:
                                path_v.append(curr)
                                curr = path_map[curr][0]

                            # Find LCA (first common node)
                            path_u_set = set(path_u)
                            lca = None
                            for node in path_v:
                                if node in path_u_set:
                                    lca = node
                                    break

                            # Trace u -> LCA
                            curr = u
                            while curr != lca:
                                p, edge = path_map[curr]
                                cycle_edges.append(edge)
                                curr = p

                            # Trace v -> LCA
                            curr = v
                            while curr != lca:
                                p, edge = path_map[curr]
                                cycle_edges.append(edge)
                                curr = p

                            return cycle_edges

                        else:
                            # Add v to stack and map
                            path_map[v] = (u, (cell_pos, cell_val))
                            stack.append(v)

        return None

    def _build_solution_grid(self):
        # Use SlantGrid for correct string representation
        matrix = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.solver.Value(self._cells[(r, c)]) == 1
                matrix[r][c] = val
        return SlantGrid(matrix)
