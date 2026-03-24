from ortools.sat.python import cp_model
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class KohiGyunyuSolver(GameSolver):
    MILK = "W"
    COFFEE = "B"
    CUP = "G"
    EMPTY = "."

    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows = grid.rows_number
        self.cols = grid.columns_number
        self.milks: list[Position] = []
        self.coffees: list[Position] = []
        self.grays: list[Position] = []

        for position, val in self._grid:
            if hasattr(val, "type_char") and val.type_char:
                char = val.type_char.strip()
            else:
                char = str(val).strip()

            if char == self.MILK:
                self.milks.append(position)
            elif char == self.COFFEE:
                self.coffees.append(position)
            elif char == self.CUP:
                self.grays.append(position)

        self._model = cp_model.CpModel()
        self._constraints_added = False
        self._last_solver = None
        self.milk_in_group = []
        self.coffee_in_group = []
        self._connection_vars = []
        self._connection_pairs = []
        self._all_circles = []
        self._circle_group_vars = []

    def get_solution(self) -> IslandGrid:
        if not self.grays:
            return IslandGrid.empty()

        if not self._constraints_added:
            self._add_constraints()
            self._constraints_added = True

        solver = cp_model.CpSolver()
        status = solver.solve(self._model)

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            self._last_solver = solver
            return self._build_grid_from_solver(solver)
        else:
            print(f"Status: {status}")
            if status == cp_model.INFEASIBLE:
                print("Infeasible")
            elif status == cp_model.MODEL_INVALID:
                print("Model invalid")
        return IslandGrid.empty()

    @staticmethod
    def _draw_straight_connection(grid: IslandGrid, p1: Position, p2: Position):
        if p1.r != p2.r and p1.c != p2.c:
            return

        if p1.r == p2.r:
            c_from, c_to = sorted((p1.c, p2.c))
            for c in range(c_from, c_to):
                a = Position(p1.r, c)
                b = Position(p1.r, c + 1)
                grid.value(a).set_bridge_to_position(b, 1)
                grid.value(b).set_bridge_to_position(a, 1)
            return

        r_from, r_to = sorted((p1.r, p2.r))
        for r in range(r_from, r_to):
            a = Position(r, p1.c)
            b = Position(r + 1, p1.c)
            grid.value(a).set_bridge_to_position(b, 1)
            grid.value(b).set_bridge_to_position(a, 1)

    def _add_constraints(self):
        num_grays = len(self.grays)
        num_milks = len(self.milks)
        num_coffees = len(self.coffees)

        all_circles = self.grays + self.milks + self.coffees
        self._all_circles = all_circles

        num_circles = len(all_circles)
        circles_set = set(all_circles)
        circle_map = {pos: i for i, pos in enumerate(all_circles)}

        connections, adj = self._init_variables(num_grays, num_milks, num_coffees, num_circles, all_circles, circles_set)
        circle_group = [self._model.new_int_var(0, num_grays - 1, f"cg_{i}") for i in range(num_circles)]
        self._circle_group_vars = circle_group

        self._add_assignment_constraints(num_milks, num_coffees)
        self._add_balance_constraints(num_grays, num_milks, num_coffees)
        self._add_group_id_constraints(num_grays, num_circles, circle_group, circle_map)
        self._add_connection_logic_constraints(connections, circle_group)
        self._add_crossing_constraints(connections, all_circles)
        self._add_milk_coffee_prohibition_constraints(connections, all_circles)
        self._add_rank_connectivity_constraints(num_grays, num_circles, circle_map, adj, connections)

    def _init_variables(self, num_grays, num_milks, num_coffees, num_circles, all_circles, circles_set):
        connections = {}
        adj = {i: [] for i in range(num_circles)}
        for i, p1 in enumerate(all_circles):
            for j in range(i + 1, num_circles):
                p2 = all_circles[j]
                if not self._circles_visible_without_intermediate_circle(p1, p2, circles_set):
                    continue
                conn_var = self._model.new_bool_var(f"conn_{i}_{j}")
                connections[(i, j)] = conn_var
                adj[i].append(j)
                adj[j].append(i)

        self._connection_vars = list(connections.values())
        self._connection_pairs = [(u, v, var) for (u, v), var in connections.items()]

        self.milk_in_group = [[self._model.new_bool_var(f"milk_{w}_in_g_{g}") for g in range(num_grays)] for w in range(num_milks)]
        self.coffee_in_group = [[self._model.new_bool_var(f"coffee_{b}_in_g_{g}") for g in range(num_grays)] for b in range(num_coffees)]

        return connections, adj

    def _add_assignment_constraints(self, num_milks, num_coffees):
        for w in range(num_milks):
            self._model.add(sum(self.milk_in_group[w]) == 1)
        for b in range(num_coffees):
            self._model.add(sum(self.coffee_in_group[b]) == 1)

    def _add_balance_constraints(self, num_grays, num_milks, num_coffees):
        for g in range(num_grays):
            self._model.add(sum(self.milk_in_group[w][g] for w in range(num_milks)) == sum(self.coffee_in_group[b][g] for b in range(num_coffees)))

    def _add_group_id_constraints(self, num_grays, num_circles, circle_group, circle_map):
        gray_indices = [circle_map[p] for p in self.grays]
        milk_indices = [circle_map[p] for p in self.milks]
        coffee_indices = [circle_map[p] for p in self.coffees]

        for i in range(num_circles):
            if i in gray_indices:
                self._model.add(circle_group[i] == gray_indices.index(i))
            elif i in milk_indices:
                w_idx = milk_indices.index(i)
                for g in range(num_grays):
                    self._model.add(circle_group[i] == g).only_enforce_if(self.milk_in_group[w_idx][g])
            elif i in coffee_indices:
                b_idx = coffee_indices.index(i)
                for g in range(num_grays):
                    self._model.add(circle_group[i] == g).only_enforce_if(self.coffee_in_group[b_idx][g])

    def _add_connection_logic_constraints(self, connections, circle_group):
        for (u, v), conn_var in connections.items():
            self._model.add(circle_group[u] == circle_group[v]).only_enforce_if(conn_var)

    def _add_crossing_constraints(self, connections, all_circles):
        connection_list = list(connections.items())
        for idx1, ((u1, v1), var1) in enumerate(connection_list):
            p1u, p1v = all_circles[u1], all_circles[v1]
            for idx2 in range(idx1 + 1, len(connection_list)):
                ((u2, v2), var2) = connection_list[idx2]
                p2u, p2v = all_circles[u2], all_circles[v2]

                # Check if p1u-p1v and p2u-p2v cross
                if self._is_crossing(p1u, p1v, p2u, p2v):
                    self._model.add(var1 + var2 <= 1)

    def _add_milk_coffee_prohibition_constraints(self, connections, all_circles):
        for (u, v), conn_var in connections.items():
            p1, p2 = all_circles[u], all_circles[v]
            if (p1 in self.milks and p2 in self.coffees) or (p1 in self.coffees and p2 in self.milks):
                self._model.add(conn_var == 0)

    def _add_rank_connectivity_constraints(self, num_grays, num_circles, circle_map, adj, connections):
        gray_indices = [circle_map[p] for p in self.grays]
        ranks = [self._model.new_int_var(0, num_circles - 1, f"rank_{i}") for i in range(num_circles)]

        # Directed parent variables
        parents = {}  # (from, to) -> IntVar
        for (u, v), conn_var in connections.items():
            p_uv = self._model.new_bool_var(f"p_{u}_{v}")
            p_vu = self._model.new_bool_var(f"p_{v}_{u}")
            parents[(u, v)] = p_uv
            parents[(v, u)] = p_vu

            # Link to undirected connection
            self._model.add(conn_var == p_uv + p_vu)

            # Rank constraint: parent has lower rank
            self._model.add(ranks[u] == ranks[v] + 1).only_enforce_if(p_uv)
            self._model.add(ranks[v] == ranks[u] + 1).only_enforce_if(p_vu)

        for i in range(num_circles):
            out_edges = [parents[(i, j)] for j in adj[i]]
            if i in gray_indices:
                self._model.add(ranks[i] == 0)
                self._model.add(sum(out_edges) == 0)
            else:
                self._model.add(sum(out_edges) == 1)

    @staticmethod
    def _is_crossing(p1u: Position, p1v: Position, p2u: Position, p2v: Position) -> bool:
        # Check if line segment (p1u, p1v) and (p2u, p2v) cross
        # Assume p1u.r == p1v.r or p1u.c == p1v.c (and similarly for p2)
        if p1u.r == p1v.r: # Horizontal
            if p2u.c == p2v.c: # Vertical
                r_h = p1u.r
                c_v = p2u.c
                c_h_min, c_h_max = sorted((p1u.c, p1v.c))
                r_v_min, r_v_max = sorted((p2u.r, p2v.r))
                # Cross if r_h is strictly between r_v_min and r_v_max 
                # AND c_v is strictly between c_h_min and c_h_max
                return r_v_min < r_h < r_v_max and c_h_min < c_v < c_h_max
        elif p1u.c == p1v.c: # Vertical
            if p2u.r == p2v.r: # Horizontal
                c_v = p1u.c
                r_h = p2u.r
                r_v_min, r_v_max = sorted((p1u.r, p1v.r))
                c_h_min, c_h_max = sorted((p2u.c, p2v.c))
                return r_v_min < r_h < r_v_max and c_h_min < c_v < c_h_max
        return False

    @staticmethod
    def _circles_visible_without_intermediate_circle(p1: Position, p2: Position, circles_set: set[Position]) -> bool:
        if p1.r != p2.r and p1.c != p2.c:
            return False

        if p1.r == p2.r:
            c_from, c_to = sorted((p1.c, p2.c))
            for c in range(c_from + 1, c_to):
                if Position(p1.r, c) in circles_set:
                    return False
            return c_to > c_from

        r_from, r_to = sorted((p1.r, p2.r))
        for r in range(r_from + 1, r_to):
            if Position(r, p1.c) in circles_set:
                return False
        return r_to > r_from

    def get_other_solution(self) -> IslandGrid:
        if self._last_solver is None:
            return IslandGrid.empty()

        exclude = []
        for w_in_g_list in self.milk_in_group:
            for lit in w_in_g_list:
                exclude.append(lit if not self._last_solver.value(lit) else lit.negated())

        for b_in_g_list in self.coffee_in_group:
            for lit in b_in_g_list:
                exclude.append(lit if not self._last_solver.value(lit) else lit.negated())

        for lit in self._connection_vars:
            exclude.append(lit if not self._last_solver.value(lit) else lit.negated())

        if not exclude:
            return IslandGrid.empty()

        self._model.add_bool_or(exclude)
        solver = cp_model.CpSolver()
        status = solver.solve(self._model)

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return self._build_grid_from_solver(solver)

        return IslandGrid.empty()

    def _build_grid_from_solver(self, solver: cp_model.CpSolver) -> IslandGrid:
        island_matrix = [[Island(Position(r, c), 0) for c in range(self.cols)] for r in range(self.rows)]
        island_grid = IslandGrid(island_matrix)
        island_grid.connections = []

        # Build adjacency for each group
        adj = {}
        for u, v, conn_var in self._connection_pairs:
            if not solver.value(conn_var):
                continue
            p1 = self._all_circles[u]
            p2 = self._all_circles[v]
            self._draw_straight_connection(island_grid, p1, p2)
            island_grid.connections.append((p1, p2))

            group_id = solver.value(self._circle_group_vars[u])
            if group_id not in adj: adj[group_id] = {}
            if p1 not in adj[group_id]: adj[group_id][p1] = []
            if p2 not in adj[group_id]: adj[group_id][p2] = []
            adj[group_id][p1].append(p2)
            adj[group_id][p2].append(p1)

        # Groups will store: { group_id: { 'gray_connections': [], 'other_connections': [] } }
        groups = {}
        for g_idx, gray_pos in enumerate(self.grays):
            groups[g_idx] = {'gray_connections': [], 'other_connections': []}
            if g_idx not in adj:
                continue

            # On veut commencer par les cercles connectés au gris, en traçant vers le gris.
            # Donc on identifie d'abord les voisins du gris.
            visited = {gray_pos}
            gray_neighbors = adj[g_idx].get(gray_pos, [])

            # On les traite en premier
            stack = []
            for neighbor in gray_neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    # Connexion de neighbor -> gray
                    groups[g_idx]['gray_connections'].append((neighbor, gray_pos))
                    stack.append(neighbor)

            # Ensuite on continue le parcours depuis ces voisins
            while stack:
                curr = stack.pop()
                for neighbor in adj[g_idx].get(curr, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
                        # Connexion du cercle non relié (neighbor) vers celui déjà relié (curr)
                        groups[g_idx]['other_connections'].append((neighbor, curr))

        island_grid.groups = groups

        for position, island in island_grid:
            island.set_bridges_count_according_to_directions_bridges()

        return island_grid
