import asyncio
import logging
import os
import time

from GameComponentFactory import GameComponentFactory

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver
from GridPlayers.Base.PlayStatus import PlayStatus


class PuzzleMainConsole:
    @staticmethod
    def setup_logging():
        log_level = os.environ.get("PUZZLE_LOG_LEVEL", "DEBUG").upper()
        numeric_level = getattr(logging, log_level, logging.INFO)
        logging.basicConfig(
            level=numeric_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    @staticmethod
    async def main():
        PuzzleMainConsole.setup_logging()
        print("Puzzle Solver")
        print("Enter game url")
        url = input()

        match url:
            case "queens":
                url = "https://www.linkedin.com/games/queens"
            case "zip":
                url = "https://www.linkedin.com/games/zip"
            case "tango":
                url = "https://www.linkedin.com/games/tango"

        game_component_factory = GameComponentFactory()
        game_solver, data_game, game_player, browser_context, playwright = await game_component_factory.create_components_from_url(url)
        
        solution = PuzzleMainConsole.run_solver(game_solver, data_game)

        if game_player is not None and solution != Grid.empty():
            result = await game_player.play(solution)
            if result is None:
                print("Submission failed: No result returned")
            elif result == PlayStatus.FAILED_NO_SUCCESS_SELECTOR:
                print("Submission failed: No success selector found")
            elif result == PlayStatus.FAILED_NO_SUBMIT_BUTTON:
                print("Submission failed: No submit button found")
            else:
                print("Game played successfully")

        if browser_context is not None:
            await browser_context.close()
            print("Browser context closed")

        if playwright:
            await playwright.stop()
            print("Playwright stopped")


    @staticmethod
    def run_solver(puzzle_game: type[GameSolver], data_game):
        from GameComponentFactory import GameComponentFactory
        game_component_factory = GameComponentFactory()
        print("Solving...")
        game_solver = game_component_factory.create_solver(puzzle_game, data_game)

        start_time = time.time()
        solution = game_solver.get_solution()
        end_time = time.time()
        execution_time = end_time - start_time

        PuzzleMainConsole.print_solution(execution_time, solution)
        return solution

    @staticmethod
    def print_solution(execution_time, solution):
        if solution != Grid.empty():
            print(f"Solution found in {execution_time:.2f} seconds")
            print(solution)
        else:
            print("No solution found")


if __name__ == '__main__':
    asyncio.run(PuzzleMainConsole.main())