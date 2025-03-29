import itertools

from Domain.Board.Position import Position


class ShapeGenerator:
    @staticmethod
    def get_all_shapes(rows_number, columns_number):
        all_shapes = []
        min_cells_number = rows_number + columns_number - 1
        max_cells_number = rows_number * columns_number - int(rows_number / 2) * int(columns_number / 2)
        for cells_number in range(min_cells_number, max_cells_number + 1):
            generator = ShapeGenerator()
            shapes = generator._generate_shapes(rows_number, columns_number, cells_number)
            all_shapes.extend(shapes)
        return all_shapes

    @staticmethod
    def around_shape(shape) -> set[Position]:
        shape_set = set(shape)
        enlarged_shape: set[Position] = set()
        for position in shape:
            for position_delta in [Position(-1, 0), Position(1, 0), Position(0, -1), Position(0, 1)]:
                adjacent_cell = position + position_delta
                if adjacent_cell not in shape_set:
                    enlarged_shape.add(adjacent_cell)
        return enlarged_shape

    @staticmethod
    def _generate_shapes(rows_number, columns_number, cells_number):
        all_cells = [(r, c) for r in range(rows_number) for c in range(columns_number)]
        return [set(combination) for combination in itertools.combinations(all_cells, cells_number)
                if ShapeGenerator._covers_entire_grid(combination, rows_number, columns_number)
                and ShapeGenerator._is_connected(combination)
                and not ShapeGenerator._contains_square(combination)]

    @staticmethod
    def _covers_entire_grid(shape, rows_number, columns_number):
        rows = {cell[0] for cell in shape}
        cols = {cell[1] for cell in shape}
        return len(rows) == rows_number and len(cols) == columns_number

    @staticmethod
    def _is_connected(shape):
        visited = set()
        ShapeGenerator._dfs(visited, shape)
        return len(visited) == len(shape)

    @staticmethod
    def _dfs(visited, shape):
        stack = [shape[0]]
        while stack:
            x, y = stack.pop()
            if (x, y) not in visited:
                visited.add((x, y))
                stack.extend((nx, ny) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if (nx := x + dx, ny := y + dy) in shape and (nx, ny) not in visited)

    @staticmethod
    def _contains_square(shape):
        shape_set = set(shape)
        if any((x + 1, y) in shape_set and (x, y + 1) in shape_set and (x + 1, y + 1) in shape_set for x, y in shape):
            return True
