from typing import Any
from Domain.Abstractions.i_puzzle_solver import IPuzzleSolver

class PuzzleFactory:
    @staticmethod
    def create_solver(solver_class: type[IPuzzleSolver], data_game: Any) -> IPuzzleSolver:
        if isinstance(data_game, tuple):
            grid = data_game[0]
            extra_data = data_game[1:]
            return solver_class(grid, *extra_data)

        return solver_class(data_game)
