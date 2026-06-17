from __future__ import annotations

from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


def outside_from_grid(grid: Grid | None) -> frozenset[tuple[int, int]]:
    if grid is None:
        return frozenset()
    outside: set[tuple[int, int]] = set()
    for pos, value in grid:
        if value == GameSolver.cell_outside:
            outside.add((pos.r, pos.c))
    return frozenset(outside)


def resolve_outside(grid: Grid | None = None, outside: set[tuple[int, int]] | frozenset[tuple[int, int]] | None = None) -> frozenset[tuple[int, int]]:
    result = set(outside or ())
    result.update(outside_from_grid(grid))
    return frozenset(result)


def is_active(pos: Position | tuple[int, int], outside: frozenset[tuple[int, int]]) -> bool:
    if isinstance(pos, Position):
        return (pos.r, pos.c) not in outside
    return pos not in outside


def is_outside_region(positions, outside: frozenset[tuple[int, int]]) -> bool:
    if not outside:
        return False
    return all((p.r, p.c) in outside for p in positions)