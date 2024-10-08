import re

from Grid import Grid
from GridProviders.PuzzleMinesweeperMosaicGridProvider import PuzzleMinesweeperMosaicGridProvider
from GridProviders.StringGridProvider import StringGridProvider
from Puzzles.MinesweeperMosaic.MinesweeperMosaicGame import MinesweeperMosaicGame


class MinesweeperMosaicMainConsole:
    @staticmethod
    def main():
        grid = MinesweeperMosaicMainConsole.get_grid()
        MinesweeperMosaicMainConsole.run(grid)

    @staticmethod
    def get_grid():
        print("MinesweeperMosaic Game")
        print("Enter url or grid")
        console_input = input()

        url_patterns = {
            r"https://www\.puzzle-minesweeper\.com/mosaic.*": PuzzleMinesweeperMosaicGridProvider,
            r"https://www\.puzzle-minesweeper\.com/.*-mosaic/": PuzzleMinesweeperMosaicGridProvider,
        }

        for pattern, provider_class in url_patterns.items():
            if re.match(pattern, console_input):
                provider = provider_class()
                return provider.get_grid(console_input)

        return StringGridProvider().get_grid(console_input)

    @staticmethod
    def run(grid):
        game = MinesweeperMosaicGame(grid)
        solution_grid = game.get_solution()
        if solution_grid:
            print(f"Solution found:")
            for r in range(solution_grid.rows_number):
                for c in range(solution_grid.columns_number):
                    if solution_grid.value(r, c) is False:
                        solution_grid.set_value(r, c, 16)
                    if solution_grid.value(r, c) is True:
                        solution_grid.set_value(r, c, 6)
            police_color_grid = Grid([[11 for _ in range(solution_grid.columns_number)] for _ in range(solution_grid.rows_number)])
            clean_grid = Grid([[grid.value(r, c) if grid.value(r, c) != -1 else ' ' for c in range(grid.columns_number)] for r in range(grid.rows_number)])
            print(clean_grid.to_console_string(police_color_grid, solution_grid))
            MinesweeperMosaicMainConsole.generate_html(grid, solution_grid)
        else:
            print(f"No solution found")

    @staticmethod
    def generate_html(grid: Grid, solution_grid: Grid):
        with open("solution.html", "w") as file:
            file.write("<html><head><style>table {border-collapse: collapse;} td {border: 1px solid black; width: 20px; height: 20px; text-align: center;}</style></head><body><table>")
            for r in range(solution_grid.rows_number):
                file.write("<tr>")
                for c in range(solution_grid.columns_number):
                    background_color = "black" if solution_grid.value(r, c) == '■' else "white"
                    font_color = "white" if solution_grid.value(r, c) == '■' else "black"
                    file.write(f"<td style='background-color: {background_color}; color: {font_color};'>{grid.value(r, c) if grid.value(r, c) != -1 else ' '}</td>")
                file.write("</tr>")
            file.write("</table></body></html>")


if __name__ == '__main__':
    MinesweeperMosaicMainConsole.main()
