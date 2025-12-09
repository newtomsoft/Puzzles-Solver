from Domain.Board.Grid import Grid


class SlantGrid(Grid):
    def __str__(self):
        result = ""
        for r in range(self.rows_number):
            row_str = ""
            for c in range(self.columns_number):
                val = self[r][c]
                if val is None:
                    row_str += '·'
                    continue
                if val:
                    row_str += '╲'
                    continue
                row_str += '╱'

            result += row_str + '\n'
        return result

    def has_loop(self) -> bool:
        return self.get_first_cycle_path() is not None

    def get_first_cycle_path(self):
        adj = {}

        for position, val in self:
            r, c = position.r, position.c
            if val is None:
                continue

            if val is True:
                u, v = (r, c), (r + 1, c + 1)
            else:
                u, v = (r, c + 1), (r + 1, c)

            if u not in adj: adj[u] = []
            if v not in adj: adj[v] = []
            adj[u].append(v)
            adj[v].append(u)

        visited = set()

        # We need a proper cycle finding DFS that tracks the path in the current recursion stack
        # For undirected graphs, we just need to ensure we don't go back to parent.

        def find_cycle(u, p, current_path, visited_nodes):
            visited_nodes.add(u)
            current_path.append(u)

            for v in adj.get(u, []):
                if v == p:
                    continue
                if v in visited_nodes:
                    # Cycle detected.
                    # v must be in current_path because it's a back-edge in DFS tree (for connected component)
                    # For undirected graph, if we hit a visited node that is not parent, it is a cycle.
                    # Since we use a fresh visited set for each component traversal if we want strictly tree edges,
                    # but here we just want ANY cycle.
                    # Ideally, v is already in current_path.
                    if v in current_path:
                        idx = current_path.index(v)
                        return current_path[idx:] + [v] # Return the loop
                    else:
                        # Cross edge to already finished tree?
                        # In undirected graph DFS, there are no cross edges, only back edges.
                        # So v MUST be in current_path if it's visited and not parent.
                        # However, let's be safe.
                        continue

                res = find_cycle(v, u, current_path, visited_nodes)
                if res:
                    return res

            current_path.pop()
            return None

        # Iterate over all nodes to handle disconnected components
        all_nodes = list(adj.keys())
        global_visited = set()

        for node in all_nodes:
            if node not in global_visited:
                # We start a fresh DFS. We only need to track visited for this component
                # to avoid re-processing, but for cycle detection, we need the recursion stack.
                # Actually, in undirected graph, if we hit ANY visited node (not parent), it's a cycle.
                # But to reconstruct path, we need the stack.
                res = find_cycle(node, -1, [], global_visited)
                if res:
                    return res

        return None

    @staticmethod
    def empty() -> 'SlantGrid':
        return SlantGrid([[]])