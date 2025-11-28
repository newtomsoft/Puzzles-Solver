from typing import Collection

from Domain.Board.Position import Position


def positions(list_of_tuples: Collection[tuple]) -> Collection[Position]:
    return [Position(r, c) for r, c in list_of_tuples]