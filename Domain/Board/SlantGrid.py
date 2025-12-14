from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


class SlantGrid(Grid):
    backslash = True
    slash = False
    empty_cell = None

    @classmethod
    def from_slant_str(cls, grid_str: str) -> 'SlantGrid':
        if grid_str is None:
            return cls.empty()

        lines = [line for line in grid_str.splitlines() if line is not None and len(line) > 0]
        if not lines:
            return cls.empty()

        columns_number = len(lines[0])
        matrix: list[list[bool | None]] = []
        char_to_val = {
            '╲': cls.backslash,
            '╱': cls.slash,
            '·': cls.empty_cell,
        }

        for line in lines:
            if len(line) != columns_number:
                raise ValueError('Invalid slant grid string: non-rectangular rows')
            row: list[bool | None] = []
            for ch in line:
                if ch not in char_to_val:
                    raise ValueError(f"Invalid character in slant grid: {ch}")
                row.append(char_to_val[ch])
            matrix.append(row)

        return cls(matrix)

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

    def get_all_loops(self) -> list[list[Position]]:
        ds = {}
        def find(i):
            path_nodes = []
            root = i
            while ds.get(root, root) != root:
                path_nodes.append(root)
                root = ds[root]
            for node in path_nodes:
                ds[node] = root
            return root

        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                ds[root_i] = root_j
                return True
            return False

        adj = {}
        loops: list[list[Position]] = []

        for u, v in self._get_edges():
            if union(u, v):
                adj.setdefault(u, []).append(v)
                adj.setdefault(v, []).append(u)
            else:
                path = self._find_path(u, v, adj)
                if path:
                    path.append(u)
                    cell_path: list[Position] = []
                    for a, b in zip(path, path[1:]):
                        cell = self._edge_to_cell(a, b)
                        if cell is not None:
                            cell_path.append(cell)
                    if cell_path and cell_path[0] != cell_path[-1]:
                        cell_path.append(cell_path[0])
                    normalized = self._normalize_loop(cell_path)
                    loops.append(normalized)

        return loops

    def _get_edges(self):
        for position, val in self:
            if val == self.empty_cell:
                continue

            if val == self.backslash:
                yield position, position.down_right
            else:
                yield position.right, position.down

    @staticmethod
    def _find_path(start, end, adj) -> list[Position] | None:
        queue = [(start, [start])]
        visited = {start}
        
        idx = 0
        while idx < len(queue):
            node, path = queue[idx]
            idx += 1
            
            if node == end:
                return path

            for neighbor in adj.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None

    @staticmethod
    def _normalize_loop(path: list[Position]) -> list[Position]:
        if not path:
            return path
        if path[0] != path[-1]:
            path = path + [path[0]]

        core = path[:-1]
        min_idx = min(range(len(core)), key=lambda i: (core[i].r, core[i].c))

        rotated = core[min_idx:] + core[:min_idx]
        rotated.append(rotated[0])

        if len(rotated) >= 2:
            first, second = rotated[0], rotated[1]
            if (second.r, second.c) < (first.r, first.c):
                body = rotated[:-1]
                body.reverse()
                rotated = body + [body[0]]

        return rotated

    @staticmethod
    def _edge_to_cell(u: Position, v: Position) -> Position | None:
        dr = v.r - u.r
        dc = v.c - u.c
        if abs(dr) == 1 and abs(dc) == 1:
            if dr == dc:
                return Position(min(u.r, v.r), min(u.c, v.c))
            else:
                return Position(min(u.r, v.r), max(u.c, v.c) - 1)
        return None

    @staticmethod
    def empty() -> 'SlantGrid':
        return SlantGrid([[]])