from typing import Collection

from Domain.Board.Position import Position


def positions(tuples: Collection[tuple]) -> Collection[Position]:
    return [Position(r, c) for r, c in tuples]