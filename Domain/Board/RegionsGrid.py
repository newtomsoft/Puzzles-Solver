from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


class RegionsGrid(Grid):
    directions_map = {
        'right': Direction.right(),
        'left': Direction.left(),
        'bottom': Direction.down(),
        'top': Direction.up()
    }

    @classmethod
    def from_grid(cls, grid: Grid):
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
        for new_position in [position.after(cls.directions_map[dirct]) for dirct in cls.directions_map if dirct in opened_on and position.after(cls.directions_map[dirct]) in grid]:
            new_visited = cls._depth_first_search_regions(grid, new_position, visited)
            if new_visited != visited:
                return new_visited

        return visited
