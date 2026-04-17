from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


class RegionsGrid(Grid):
    @classmethod
    def from_opened_grid(cls, grid: Grid):
        grid = cls._compute_regions_grid(grid)
        return cls(grid.matrix)

    @classmethod
    def _compute_regions_grid(cls, input_grid: Grid) -> Grid:
        cells_number = input_grid.rows_number * input_grid.columns_number
        while True:
            visited_regions = set()
            regions_count = 0
            grid = Grid([[None for _ in range(input_grid.columns_number)] for _ in range(input_grid.rows_number)])
            for position, _ in input_grid:
                if position in visited_regions:
                    continue
                regions_count += 1
                region = cls._depth_first_search_regions(input_grid, position)
                for current_position in region:
                    grid[current_position] = regions_count
                visited_regions.update(region)
            if len(visited_regions) == cells_number:
                break
        return grid

    @classmethod
    def _depth_first_search_regions(cls, grid: Grid, position: Position, visited=None) -> set[Position]:
        if visited is None: visited = set()
        if position in visited: return visited

        visited.add(position)
        opened_on = grid[position]
        for new_position in [position.after(dirct) for dirct in Direction.orthogonal_directions() if dirct in opened_on and position.after(dirct) in grid]:
            new_visited = cls._depth_first_search_regions(grid, new_position, visited)
            if new_visited != visited:
                return new_visited

        return visited

    def __str__(self) -> str:
        rows = self.rows_number
        cols = self.columns_number

        char_map = {
            (False, False, False, False): ' ',
            (False, False, False, True): '╶',
            (False, False, True, False): '╴',
            (False, False, True, True): '─',
            (False, True, False, False): '╷',
            (False, True, False, True): '┌',
            (False, True, True, False): '┐',
            (False, True, True, True): '┬',
            (True, False, False, False): '╵',
            (True, False, False, True): '└',
            (True, False, True, False): '┘',
            (True, False, True, True): '┴',
            (True, True, False, False): '│',
            (True, True, False, True): '├',
            (True, True, True, False): '┤',
            (True, True, True, True): '┼',
        }

        def get_val(r, c):
            if 0 <= r < rows and 0 <= c < cols:
                return self._matrix[r][c]
            return -1

        result = []
        for r in range(rows + 1):
            line_chars = ['']
            for c in range(cols + 1):
                tl = get_val(r - 1, c - 1)
                tr = get_val(r - 1, c)
                bl = get_val(r, c - 1)
                br = get_val(r, c)

                up = (tl != tr)
                down = (bl != br)
                left = (tl != bl)
                right = (tr != br)

                line_chars.append(char_map[(up, down, left, right)])

                if c < cols:
                    val_above = get_val(r - 1, c)
                    val_below = get_val(r, c)
                    if val_above != val_below:
                        line_chars.append('─')
                    else:
                        line_chars.append(' ')

            line_chars.append('\n')
            result.append("".join(line_chars))

        return "".join(result)

    @staticmethod
    def empty() -> 'RegionsGrid':
        return RegionsGrid([[]])