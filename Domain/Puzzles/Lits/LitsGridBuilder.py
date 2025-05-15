from Domain.Board.Grid import Grid
from Domain.Puzzles.Lits.LitsType import LitsType


class LitsGridBuilder:
    _L = {
        Grid([[1, 0], [1, 0], [1, 1]]),
        Grid([[0, 1], [0, 1], [1, 1]]),
        Grid([[1, 1], [0, 1], [0, 1]]),
        Grid([[1, 1], [1, 0], [1, 0]]),
        Grid([[1, 0, 0], [1, 1, 1]]),
        Grid([[0, 0, 1], [1, 1, 1]]),
        Grid([[1, 1, 1], [1, 0, 0]]),
        Grid([[1, 1, 1], [0, 0, 1]]),
    }
    _I = {
        Grid([[1], [1], [1], [1]]),
        Grid([[1, 1, 1, 1]]),
    }
    _T = {
        Grid([[1, 1, 1], [0, 1, 0]]),
        Grid([[1, 0], [1, 1], [1, 0]]),
        Grid([[0, 1, 0], [1, 1, 1]]),
        Grid([[0, 1], [1, 1], [0, 1]]),
    }
    _S = {
        Grid([[0, 1, 1], [1, 1, 0]]),
        Grid([[1, 0], [1, 1], [0, 1]]),
        Grid([[1, 1, 0], [0, 1, 1]]),
        Grid([[0, 1], [1, 1], [1, 0]]),
    }

    @staticmethod
    def all(lits_type: LitsType):
        if lits_type == LitsType.L:
            return LitsGridBuilder.all_l()
        if lits_type == LitsType.I:
            return LitsGridBuilder.all_i()
        if lits_type == LitsType.T:
            return LitsGridBuilder.all_t()
        if lits_type == LitsType.S:
            return LitsGridBuilder.all_s()
        raise ValueError(f"Unknown lits type: {lits_type}")

    @staticmethod
    def all_l():
        return LitsGridBuilder._L

    @staticmethod
    def all_i():
        return LitsGridBuilder._I

    @staticmethod
    def all_t():
        return LitsGridBuilder._T

    @staticmethod
    def all_s():
        return LitsGridBuilder._S
