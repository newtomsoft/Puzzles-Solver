from __future__ import annotations

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.GameSolver import GameSolver


def outside_from_grid(grid: Grid) -> frozenset[tuple[int, int]]:
    outside: set[tuple[int, int]] = set()
    for pos, value in grid:
        if value == GameSolver.cell_outside:
            outside.add((pos.r, pos.c))
    return frozenset(outside)


def is_active(pos: tuple[int, int] | object, outside: frozenset[tuple[int, int]]) -> bool:
    if hasattr(pos, "r") and hasattr(pos, "c"):
        return (pos.r, pos.c) not in outside
    return pos not in outside