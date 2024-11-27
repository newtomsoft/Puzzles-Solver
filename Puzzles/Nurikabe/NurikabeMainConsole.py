from GridProviders.StringGridProvider import StringGridProvider
from PuzzleNurikabeGridProvider import PuzzleNurikabeGridProvider
from Puzzles.Nurikabe.NurikabeGame import NurikabeGame
from Utils.Grid import Grid


class NurikabeMainConsole:
    @staticmethod
    def main():
        grid = NurikabeMainConsole.get_grid()
        NurikabeMainConsole.run(grid)

    @staticmethod
    def get_grid():
        print("Nurikabe Game")
        print("Enter url or grid")
        console_input = input()

        url_patterns = {
            "https://www.puzzle-nurikabe.com": PuzzleNurikabeGridProvider,
            "https://fr.puzzle-nurikabe.com": PuzzleNurikabeGridProvider,
        }

        for pattern, provider_class in url_patterns.items():
            if pattern in console_input:
                provider = provider_class()
                return provider.get_grid(console_input)

        return StringGridProvider().get_grid(console_input)

    @staticmethod
    def run(grid):
        nurikabe = NurikabeGame(grid)
        solution_grid, attempts = nurikabe.get_solution()
        if solution_grid != Grid.empty():
            print(f"Solution found after {attempts} attempts :")
            for r in range(solution_grid.rows_number):
                for c in range(solution_grid.columns_number):
                    if solution_grid.value(r, c) is False:
                        solution_grid.set_value(r, c, '■')
            print(solution_grid.to_console_string())
        else:
            print(f"No solution found ({attempts} attempts)")


if __name__ == '__main__':
    NurikabeMainConsole.main()
