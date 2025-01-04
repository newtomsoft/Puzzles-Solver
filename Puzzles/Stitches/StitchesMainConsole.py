from GridProviders.PuzzleStitchesGridProvider import PuzzleStitchesGridProvider
from GridProviders.StringGridProvider import StringGridProvider
from Puzzles.Stitches.StitchesGame import StitchesGame
from Utils.Direction import Direction
from Utils.Grid import Grid


class StitchesMainConsole:
    @staticmethod
    def main():
        grid, numbers, regions_connections_count = StitchesMainConsole.get_grid()
        StitchesMainConsole.run(grid, numbers, regions_connections_count)

    @staticmethod
    def get_grid():
        print("Queens Game")
        print("Enter url or grid")
        console_input = input()

        url_patterns = {
            "https://www.puzzle-stitches.com": PuzzleStitchesGridProvider,
            "https://fr.puzzle-stitches.com": PuzzleStitchesGridProvider,
        }

        for pattern, provider_class in url_patterns.items():
            if pattern in console_input:
                provider = provider_class()
                return provider.get_grid(console_input)

        return StringGridProvider().get_grid(console_input)

    @staticmethod
    def run(grid: Grid, numbers: dict, regions_connections_count: int):
        game = StitchesGame(grid, numbers, regions_connections_count)
        solution_grid = game.get_solution()
        if solution_grid:
            print(f"Solution found")
            printable_grid = Grid([[str(value) if (value := Direction(solution_grid.value(r, c))) != Direction.none() else ' ' for c in range(grid.columns_number)] for r in range(grid.rows_number)])
            police_color_grid = Grid([[16 for _ in range(grid.columns_number)] for _ in range(grid.rows_number)])
            printable_grid_string = printable_grid.to_console_string(police_color_grid, grid)
            print(printable_grid_string)
        else:
            print(f"No solution found")


if __name__ == '__main__':
    StitchesMainConsole.main()
