from GridProviders.StringGridProvider import StringGridProvider
from PuzzleKakurasuGridProvider import PuzzleKakurasuGridProvider
from Puzzles.Kakurasu.KakurasuGame import KakurasuGame
from Utils.Grid import Grid


class KakurasuMainConsole:
    @staticmethod
    def main():
        numbers_by_top_left = KakurasuMainConsole.get_grid()
        KakurasuMainConsole.run(numbers_by_top_left)

    @staticmethod
    def get_grid():
        print("Kakurasu Game")
        print("Enter url or grid")
        console_input = input()

        url_patterns = {
            r"https://fr.puzzle-kakurasu.com/": PuzzleKakurasuGridProvider,
            r"https://www.puzzle-kakurasu.com/": PuzzleKakurasuGridProvider
        }

        for pattern, provider_class in url_patterns.items():
            if pattern in console_input:
                provider = provider_class()
                return provider.get_grid(console_input)

        return StringGridProvider().get_grid(console_input)

    @staticmethod
    def run(numbers_by_side_top):
        game = KakurasuGame(numbers_by_side_top)
        solution = game.get_solution()

        if not solution.is_empty():
            print(f"Solution found:")
            print(KakurasuMainConsole.get_console_grid(solution))
        else:
            print(f"No solution found")
        # KakurasuMainConsole.generate_html(solution_grid)

    @staticmethod
    def get_console_grid(solution_grid):
        background_grid = Grid([[1 if solution_grid.value(r, c) else 0 for c in range(solution_grid.columns_number)] for r in range(solution_grid.rows_number)])
        text_grid = Grid([[' ' for _ in range(solution_grid.columns_number)] for _ in range(solution_grid.rows_number)])
        console_grid = text_grid.to_console_string(None, background_grid)
        return console_grid


if __name__ == '__main__':
    KakurasuMainConsole.main()
