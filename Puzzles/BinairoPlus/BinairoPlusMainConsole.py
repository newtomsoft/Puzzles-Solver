import time

from Grid import Grid
from GridProviders.StringGridProvider import StringGridProvider
from PuzzleBinairoPlusGridProvider import PuzzleBinairoPlusGridProvider
from Puzzles.BinairoPlus.BinairoPlusGame import BinairoPlusGame


class BinairoMainConsole:
    @staticmethod
    def main():
        grid, comparison_operators = BinairoMainConsole.get_grid()
        BinairoMainConsole.run(grid, comparison_operators)

    @staticmethod
    def get_grid():
        print("BinairoPlus Game")
        print("Enter url or grid")
        console_input = input()

        url_patterns = {
            "https://www.puzzle-binairo.com": PuzzleBinairoPlusGridProvider,
            "https://fr.puzzle-binairo.com": PuzzleBinairoPlusGridProvider,
        }

        for pattern, provider_class in url_patterns.items():
            if pattern in console_input:
                provider = provider_class()
                return provider.get_grid(console_input)

        return StringGridProvider().get_grid(console_input)

    @staticmethod
    def run(grid, comparison_operators):
        game = BinairoPlusGame(grid, comparison_operators)
        start_time = time.time()
        solution_grid = game.get_solution()
        end_time = time.time()
        execution_time = end_time - start_time
        if solution_grid != Grid.empty():
            print(f"Solution found in {execution_time:.2f} seconds")
            print(solution_grid.to_console_string())
            # BinairoMainConsole.generate_html(solution_grid)
        else:
            print(f"No solution found")

    @staticmethod
    def generate_html(solution_grid: Grid):
        with open("solution.html", "w") as file:
            file.write("<html><head><style>table {border-collapse: collapse;} td {border: 1px solid black; width: 20px; height: 20px; text-align: center;}</style></head><body><table>")
            for r in range(solution_grid.rows_number):
                file.write("<tr>")
                for c in range(solution_grid.columns_number):
                    file.write(f"<td style='background-color: white; color: black;'>{BinairoMainConsole.int_to_base26(solution_grid.value(r, c).as_long())}</td>")
                file.write("</tr>")
            file.write("</table></body></html>")


if __name__ == '__main__':
    BinairoMainConsole.main()
