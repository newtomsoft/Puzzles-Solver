from GridProviders.StringGridProvider import StringGridProvider
from PuzzleNonogramGridProvider import PuzzleNonogramGridProvider
from Puzzles.Nonogram.NonogramGame import NonogramGame


class NonogramMainConsole:
    @staticmethod
    def main():
        numbers_by_top_left = NonogramMainConsole.get_grid()
        NonogramMainConsole.run(numbers_by_top_left)

    @staticmethod
    def get_grid():
        print("Nonogram Game")
        print("Enter url or grid")
        console_input = input()

        url_patterns = {
            r"https://fr.puzzle-nonograms.com/": PuzzleNonogramGridProvider,
            r"https://www.puzzle-nonograms.com/": PuzzleNonogramGridProvider
        }

        for pattern, provider_class in url_patterns.items():
            if pattern in console_input:
                provider = provider_class()
                return provider.get_grid(console_input)

        return StringGridProvider().get_grid(console_input)

    @staticmethod
    def run(numbers_by_top_left):
        game = NonogramGame(numbers_by_top_left)
        solution_grid = game.get_solution()
        if solution_grid:
            print(f"Solution found:")
            print(solution_grid.to_console_string())
            pass
            # NonogramMainConsole.generate_html(solution_grid)
        else:
            print(f"No solution found")


if __name__ == '__main__':
    NonogramMainConsole.main()
