from z3 import Solver, Or, And, Not, If, Sum, sat, Bool, is_true
from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class SlantSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.grid = grid
        # Input grid is clues (N+1 x M+1)
        # Solution grid is cells (N x M)
        self.rows_number = grid.rows_number - 1
        self.columns_number = grid.columns_number - 1
        self.solver = Solver()
        self.cells = [[Bool(f'cell_{r}_{c}') for c in range(self.columns_number)] for r in range(self.rows_number)]

    def get_solution(self) -> Grid:
        self._add_constraints()
        while self.solver.check() == sat:
            model = self.solver.model()
            solution_matrix = [['' for _ in range(self.columns_number)] for _ in range(self.rows_number)]

            # Using simple adjacency list for cycle detection
            # Nodes are intersection points (r, c) where 0 <= r <= rows, 0 <= c <= cols
            adj = {}

            cycle_found = False

            # Helper to find path in current graph
            # Returns list of nodes [start, ..., end]
            def get_path_bfs(start_node, end_node, graph_adj):
                queue = [(start_node, [start_node])]
                visited = {start_node}
                while queue:
                    curr, path = queue.pop(0)
                    if curr == end_node:
                        return path
                    for neighbor, _ in graph_adj.get(curr, []):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append((neighbor, path + [neighbor]))
                return None

            for r in range(self.rows_number):
                for c in range(self.columns_number):
                    is_backslash = is_true(model[self.cells[r][c]])
                    solution_matrix[r][c] = '\\' if is_backslash else '/'

                    if is_backslash:
                        u, v = (r, c), (r+1, c+1)
                    else:
                        u, v = (r, c+1), (r+1, c)

                    # Check if adding edge (u, v) creates a cycle
                    path = get_path_bfs(u, v, adj)
                    if path:
                        # Cycle found!
                        # Construct blocking clause
                        cycle_constraints = []
                        # Current edge constraint
                        cycle_constraints.append(self.cells[r][c] == is_backslash)

                        # Constraints for edges in the path
                        for i in range(len(path) - 1):
                            n1, n2 = path[i], path[i+1]
                            # Find edge between n1 and n2 in adj
                            # adj[n1] contains (n2, constraint)
                            found = False
                            for neighbor, constr in adj[n1]:
                                if neighbor == n2:
                                    cycle_constraints.append(constr)
                                    found = True
                                    break
                            if not found:
                                raise Exception("Path edge not found in adjacency list")

                        self.solver.add(Not(And(*cycle_constraints)))
                        cycle_found = True
                        break # Break inner loop

                    # Add edge to graph
                    if u not in adj: adj[u] = []
                    if v not in adj: adj[v] = []
                    constraint = (self.cells[r][c] == is_backslash)
                    adj[u].append((v, constraint))
                    adj[v].append((u, constraint))

                if cycle_found: break

            if not cycle_found:
                return Grid(solution_matrix)

        return None

    def _add_constraints(self):
        for r in range(self.grid.rows_number):
            for c in range(self.grid.columns_number):
                clue = self.grid[r][c]
                if clue is not None and str(clue).isdigit():
                    clue_val = int(clue)
                    connections = []

                    # (r-1, c-1) connects to (r,c) if \ (True)
                    if r > 0 and c > 0:
                        connections.append(If(self.cells[r-1][c-1], 1, 0))
                    # (r-1, c) connects to (r,c) if / (False)
                    if r > 0 and c < self.columns_number:
                        connections.append(If(self.cells[r-1][c], 0, 1))
                    # (r, c-1) connects to (r,c) if / (False)
                    if r < self.rows_number and c > 0:
                        connections.append(If(self.cells[r][c-1], 0, 1))
                    # (r, c) connects to (r,c) if \ (True)
                    if r < self.rows_number and c < self.columns_number:
                        connections.append(If(self.cells[r][c], 1, 0))

                    self.solver.add(Sum(connections) == clue_val)

    def get_other_solution(self) -> Grid:
        return self.get_solution()
