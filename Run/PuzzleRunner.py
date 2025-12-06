import time
from Domain.Board.Grid import Grid
from Domain.Puzzles.GameSolver import GameSolver
from GridPlayers.GridPlayer import GridPlayer

class PuzzleRunner:
    def __init__(self, solver: GameSolver, player: GridPlayer | None):
        self.solver = solver
        self.player = player

    def run(self):
        print("Solving...")
        start_time = time.time()
        solution = self.solver.get_solution()
        end_time = time.time()
        execution_time = end_time - start_time

        self.print_solution(execution_time, solution)

        if self.player is not None and solution != Grid.empty():
            self.player.play(solution)

    @staticmethod
    def print_solution(execution_time, solution):
        if solution != Grid.empty():
            print(f"Solution found in {execution_time:.2f} seconds")
            print(solution)
        else:
            print(f"No solution found")
