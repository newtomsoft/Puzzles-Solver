from GridProviders.PuzzleAquariumGridProvider import PuzzleAquariumGridProvider
from GridProviders.StringGridProvider import StringGridProvider
from Puzzles.Aquarium.AquariumGame import AquariumGame
from Utils.Grid import Grid


class AquariumMainConsole:
    @staticmethod
    def main():
        grid, numbers = AquariumMainConsole.get_grid()
        AquariumMainConsole.run(grid, numbers)

    @staticmethod
    def get_grid():
        print("Queens Game")
        print("Enter url or grid")
        console_input = input()

        url_patterns = {
            "https://www.puzzle-aquarium.com": PuzzleAquariumGridProvider,
            "https://fr.puzzle-aquarium.com": PuzzleAquariumGridProvider,
        }

        for pattern, provider_class in url_patterns.items():
            if pattern in console_input:
                provider = provider_class()
                return provider.get_grid(console_input)

        return StringGridProvider().get_grid(console_input)

    @staticmethod
    def run(grid: Grid, numbers: list[int]):
        game = AquariumGame(grid, numbers)
        solution_grid = game.get_solution()
        if solution_grid:
            print(f"Solution found")
            printable_grid = Grid([['*' if solution_grid.value(r, c) else ' ' for c in range(grid.columns_number)] for r in range(grid.rows_number)])
            police_color_grid = Grid([[16 for _ in range(grid.columns_number)] for _ in range(grid.rows_number)])
            printable_grid_string = printable_grid.to_console_string(police_color_grid, grid)
            print(printable_grid_string)
        else:
            print(f"No solution found")


if __name__ == '__main__':
    AquariumMainConsole.main()
