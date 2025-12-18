import asyncio
import inspect
import time

from GameComponentFactory import GameComponentFactory

from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver


class PuzzleMainConsole:
    @staticmethod
    async def main():
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
        game_solver, data_game, game_player, playwright = await game_component_factory.create_components_from_url(url)
        solution = PuzzleMainConsole.run_solver(game_solver, data_game)

        if game_player is not None and solution != Grid.empty():
            await game_player.play(solution)

        if playwright:
            await playwright.stop()


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