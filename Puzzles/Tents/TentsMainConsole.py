import time

from SolverEngine.Z3SolverEngine import Z3SolverEngine
from playwright.sync_api import BrowserContext

from GridProviders.PuzzleTentsGridProvider import PuzzleTentsGridProvider
from Puzzles.Tents.TentsSolver import TentsSolver
from Utils.Grid import Grid


class PuzzleMainConsole:
    @staticmethod
    def main():
        data_game, browser = PuzzleMainConsole.get_game_and_grid()
        solution = PuzzleMainConsole.run(data_game)
        PuzzleMainConsole.play_solution(solution, browser)
        pass

    @staticmethod
    def get_game_and_grid():
        return PuzzleTentsGridProvider().get_grid("https://fr.puzzle-tents.com/?pl=789559083c3ea21c9e3b49cb0a535926675ed7980f117")

    @staticmethod
    def run(data_game):
        game_solver = TentsSolver(data_game[0], data_game[1], Z3SolverEngine())
        start_time = time.time()
        solution_grid = game_solver.get_solution()
        end_time = time.time()
        execution_time = end_time - start_time
        if solution_grid != Grid.empty():
            print(f"Solution found in {execution_time:.2f} seconds")
            print(solution_grid.to_console_string())
        else:
            print(f"No solution found")
        return solution_grid

    @classmethod
    def play_solution(cls, solution, browser: BrowserContext):
        page = browser.pages[0]
        grid_cell_divs = page.query_selector_all('div.cell:not(.task)')
        columns_count = len([cell for cell in grid_cell_divs if 'top: 3px' in cell.get_attribute('style')])
        count = 0
        page.evaluate("document.querySelector('.board-mask').remove()")
        # page.evaluate("document.querySelector('.board-mask').style.pointerEvents = 'none'")
        page.locator(".tents-cell-back > div:nth-child(3)").click()
        page.locator(".tents-cell-back > div:nth-child(4)").click()
        page.locator(".tents-cell-back > div:nth-child(5)").click()
        page.locator(".tents-cell-back > div:nth-child(6)").click()
        page.locator(".tents-cell-back > div:nth-child(7)").click()
        for i, cell_div in enumerate(grid_cell_divs):
            if solution[i // columns_count][i % columns_count]:
                count += 1
        print(f"{count} tents placed")


if __name__ == '__main__':
    PuzzleMainConsole.main()
