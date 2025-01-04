from z3 import Solver, Implies, And, Or, sat, Int

from Utils.Direction import Direction
from Utils.Grid import Grid
from Utils.Position import Position


class DominosaGame:
    def __init__(self, grid: Grid):
        self._grid = grid
        self.rows_number = self._grid.rows_number
        self.columns_number = self._grid.columns_number
        if self.rows_number < 2 or self.columns_number < 3:
            raise ValueError("The grid must be at least 2x3")
        if self.columns_number != self.rows_number + 1:
            raise ValueError("The grid must be RxC with C = R + 1")
        self.dominoes_count = self.rows_number * self.columns_number // 2
        self.min_number_on_domino = min(self._grid.value(r, c) for r in range(self.rows_number) for c in range(self.columns_number))
        self.max_number_on_domino = max(self._grid.value(r, c) for r in range(self.rows_number) for c in range(self.columns_number))
        self.len_range_number_on_domino = self.rows_number
        if self.max_number_on_domino - self.min_number_on_domino + 1 != self.len_range_number_on_domino:
            raise ValueError(f"Values on dominoes must be between x and x + {self.len_range_number_on_domino - 1}")
        self._solver = None
        self._dominoes_positions_z3 = {
            (value0, value1): [(Int(f"{value0}_{value1}_r0"), Int(f"{value0}_{value1}_c0")), (Int(f"{value0}_{value1}r1"), Int(f"{value0}_{value1}c1"))]
            for value0 in range(self.min_number_on_domino, self.max_number_on_domino + 1)
            for value1 in range(self.min_number_on_domino, value0 + 1)
        }
        self._possibles_neighbors: dict[tuple[int, int], set[tuple[int, int]]] = {}

    def get_solution(self):
        self._solver = Solver()
        self._add_constraints()
        if self._solver.check() != sat:
            return Grid.empty()
        model = self._solver.model()
        dominoes_positions = {
            (value0, value1): [Position(int(model.eval(r).as_long()), int(model.eval(c).as_long())) for r, c in positions]
            for (value0, value1), positions in self._dominoes_positions_z3.items()
        }
        solution_grid = Grid([[0 for _ in range(self.columns_number)] for _ in range(self.rows_number)])
        for _, positions in dominoes_positions.items():
            direction01 = positions[0].direction_to(positions[1])
            direction10 = positions[1].direction_to(positions[0])
            solution_grid.set_value(positions[0], direction01)
            solution_grid.set_value(positions[1], direction10)

        return solution_grid

    def _add_constraints(self):
        self._range_positions_dominoes_constraints()
        self._dominoes_constraints()

    def _range_positions_dominoes_constraints(self):
        [self._solver.add(r >= 0, r < self.rows_number, c >= 0, c < self.columns_number) for z3_positions in self._dominoes_positions_z3.values() for r, c in z3_positions]

    def _dominoes_constraints(self):
        possibles_dominoes_positions_by_value = self._get_all_possible_domino_positions_by_value()
        possibles_dominoes_positions_by_value = self.set_dominoes_positions_when_1_possibility_by_value(possibles_dominoes_positions_by_value)

        constraints_implies = []
        constraints_positions_dominos = []
        dominoes_positions_z3 = self._dominoes_positions_z3

        for domino_value_0, domino_value_1 in possibles_dominoes_positions_by_value.keys():
            constraints_positions_domino = []
            possible_positions = possibles_dominoes_positions_by_value[(domino_value_0, domino_value_1)]
            rc0_z3, rc1_z3 = dominoes_positions_z3[(domino_value_0, domino_value_1)]
            r0z3, c0z3 = rc0_z3
            r1z3, c1z3 = rc1_z3

            for (possible_r0, possible_c0), (possible_r1, possible_c1) in possible_positions:
                constraint_positions_domino = And(r0z3 == possible_r0, c0z3 == possible_c0, r1z3 == possible_r1, c1z3 == possible_c1)
                constraints_positions_domino.append(constraint_positions_domino)

                others_dominoes_compliant_positions = {
                    key: [positions for positions in possibles_dominoes_positions_by_value[key]
                          if (possible_r0, possible_c0) not in positions and (possible_r1, possible_c1) not in positions]
                    for key in possibles_dominoes_positions_by_value.keys() if key != (domino_value_0, domino_value_1)
                }

                for key, positions in others_dominoes_compliant_positions.items():
                    constraints_compliant_positions_domino = [
                        And(dominoes_positions_z3[key][0][0] == position[0][0], dominoes_positions_z3[key][0][1] == position[0][1],
                            dominoes_positions_z3[key][1][0] == position[1][0], dominoes_positions_z3[key][1][1] == position[1][1])
                        for position in positions
                    ]
                    constraints_implies.append(Implies(constraint_positions_domino, Or(constraints_compliant_positions_domino)))

            constraints_positions_dominos.append(Or(constraints_positions_domino))

        self._solver.add(constraints_implies)
        self._solver.add(constraints_positions_dominos)

    def _get_all_possible_domino_positions_by_value(self):
        directions = [(0, 1), (1, 0)]
        possible_domino_positions = {
            (value0, value1): []
            for value0 in range(self.min_number_on_domino, self.max_number_on_domino + 1)
            for value1 in range(self.min_number_on_domino, value0 + 1)
        }
        for r0z3 in range(self.rows_number):
            for c0z3 in range(self.columns_number):
                domino_value_0: int = self._grid.value(r0z3, c0z3)
                for dr, dc in directions:
                    r1z3, c1z3 = r0z3 + dr, c0z3 + dc
                    if 0 <= r1z3 < self.rows_number and 0 <= c1z3 < self.columns_number:
                        domino_value_1: int = self._grid.value(r1z3, c1z3)
                        value_max, value_min = (max(domino_value_0, domino_value_1), min(domino_value_0, domino_value_1))
                        possible_domino_positions[value_max, value_min].append([(r0z3, c0z3), (r1z3, c1z3)])
        return possible_domino_positions

    def set_dominoes_positions_when_1_possibility_by_value(self, possibles_dominoes_positions_by_value):
        possibles_neighbors = {
            (r, c): {(r + dr, c + dc) for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)] if 0 <= r + dr < self.rows_number and 0 <= c + dc < self.columns_number}
            for r in range(self.rows_number)
            for c in range(self.columns_number)
        }
        to_set = True
        while to_set:
            to_set = False
            for domino_value_0, domino_value_1 in list(possibles_dominoes_positions_by_value.keys()):
                if len(possibles_dominoes_positions_by_value[(domino_value_0, domino_value_1)]) == 1:
                    to_set = True
                    (r0, c0), (r1, c1) = possibles_dominoes_positions_by_value[(domino_value_0, domino_value_1)][0]
                    rc0_z3, rc1_z3 = self._dominoes_positions_z3[(domino_value_0, domino_value_1)]
                    r0z3, c0z3 = rc0_z3
                    r1z3, c1z3 = rc1_z3
                    self._solver.add(r0z3 == r0, c0z3 == c0, r1z3 == r1, c1z3 == c1)

                    possibles_neighbors = self._remove_position_from_possibles_neighbors((r0, c0), possibles_neighbors)
                    possibles_neighbors = self._remove_position_from_possibles_neighbors((r1, c1), possibles_neighbors)

                    possibles_dominoes_positions_by_value = {
                        key: [positions for positions in positions_list if (r0, c0) not in positions and (r1, c1) not in positions]
                        for key, positions_list in possibles_dominoes_positions_by_value.items() if key != (domino_value_0, domino_value_1)
                    }

            isolated_positions = {
                ((r0, c0), next(iter(possibles_neighbors[(r0, c0)])))
                for r0 in range(self.rows_number)
                for c0 in range(self.columns_number)
                if len(possibles_neighbors[(r0, c0)]) == 1
            }

            if isolated_positions:
                to_set = True
                for isolated_position in isolated_positions:
                    positions = list(isolated_position)
                    domino_value_0 = self._grid.value(positions[0][0], positions[0][1])
                    domino_value_1 = self._grid.value(positions[1][0], positions[1][1])
                    domino_values = (max(domino_value_0, domino_value_1), min(domino_value_0, domino_value_1))
                    possibles_dominoes_positions_by_value[domino_values] = [positions]

        return possibles_dominoes_positions_by_value

    @staticmethod
    def _remove_position_from_possibles_neighbors(position, possibles_neighbors):
        [possibles_neighbors[neighbor].remove(position) for neighbor in possibles_neighbors[position]]
        possibles_neighbors[position].clear()
        return possibles_neighbors
