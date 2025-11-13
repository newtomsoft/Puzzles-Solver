from typing import Dict

from z3 import ArithRef, Solver, Not, And, Or, Int, sat

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver
from Utils.ShapeGenerator import ShapeGenerator


class MoonsunSolver(GameSolver):
    white = 'w'
    black = 'b'
    no_circle = None

    def __init__(self, circle_grid: Grid, regions_grid: Grid):
        self._circle_grid = circle_grid
        self._regions_grid = regions_grid
        self._regions = regions_grid.get_regions()
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._solver = Solver()
        self._island_bridges_z3: Dict[Position, Dict[Direction, ArithRef]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid(
            [[Island(Position(r, c), 2) for c in range(self._circle_grid.columns_number)] for r in range(self._circle_grid.rows_number)])

    def _init_solver(self):
        self._island_bridges_z3 = {island.position: {direction: Int(f"{island.position}_{direction}") for direction in Direction.orthogonals()} for island in
                                   self._island_grid.islands.values()}
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._solver.assertions():
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        while self._solver.check() == sat:
            model = self._solver.model()
            proposition_count += 1
            for position, direction_bridges in self._island_bridges_z3.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_z3:
                        continue
                    bridges_number = model.eval(bridges).as_long()
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(self._island_grid[position].direction_position_bridges[direction][0], bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        self._island_grid[position].direction_position_bridges.pop(direction)
                self._island_grid[position].set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count

            not_loop_constraints = []
            for positions in connected_positions:
                cell_constraints = []
                for position in positions:
                    for direction, (_, value) in self._island_grid[position].direction_position_bridges.items():
                        cell_constraints.append(self._island_bridges_z3[position][direction] == value)
                not_loop_constraints.append(Not(And(cell_constraints)))
            self._solver.add(And(not_loop_constraints))
            self._init_island_grid()

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        previous_solution_constraints = []
        for island in self._previous_solution.islands.values():
            for direction, (_, value) in island.direction_position_bridges.items():
                previous_solution_constraints.append(self._island_bridges_z3[island.position][direction] == value)
        self._solver.add(Not(And(previous_solution_constraints)))

        self._init_island_grid()
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_single_path_by_region_constraints()
        self._add_all_same_color_in_region_crossed_constraints()
        self._add_all_regions_crossed_constraints()
        self._add_alternating_black_and_withe_constraints()

    def _add_initial_constraints(self):
        constraints = [Or(direction_bridges == 0, direction_bridges == 1) for _island_bridges_z3 in self._island_bridges_z3.values() for direction_bridges in
                       _island_bridges_z3.values()]
        self._solver.add(constraints)
        constraints_border_up = [self._island_bridges_z3[Position(0, c)][Direction.up()] == 0 for c in range(self._island_grid.columns_number)]
        constraints_border_down = [self._island_bridges_z3[Position(self._island_grid.rows_number - 1, c)][Direction.down()] == 0 for c in
                                   range(self._island_grid.columns_number)]
        constraints_border_right = [self._island_bridges_z3[Position(r, self._island_grid.columns_number - 1)][Direction.right()] == 0 for r in
                                    range(self._island_grid.rows_number)]
        constraints_border_left = [self._island_bridges_z3[Position(r, 0)][Direction.left()] == 0 for r in range(self._island_grid.rows_number)]
        self._solver.add(constraints_border_down + constraints_border_up + constraints_border_right + constraints_border_left)

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in [Direction.right(), Direction.down(), Direction.left(), Direction.up()]:
                if island.direction_position_bridges.get(direction) is not None:
                    self._solver.add(
                        self._island_bridges_z3[island.position][direction] == self._island_bridges_z3[island.direction_position_bridges[direction][0]][
                            direction.opposite])
                else:
                    self._solver.add(self._island_bridges_z3[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            sum0_constraint = sum([self._island_bridges_z3[island.position][direction] for direction in Direction.orthogonals()]) == 0
            sum2_constraint = sum([self._island_bridges_z3[island.position][direction] for direction in Direction.orthogonals()]) == 2
            self._solver.add(Or(sum0_constraint, sum2_constraint))

    def _add_single_path_by_region_constraints(self):
        for region_positions in self._regions.values():
            region_edges_positions = [position for position in ShapeGenerator.edges(region_positions) if position in self._island_bridges_z3]
            out_directions = []
            for pos in region_edges_positions:
                out_directions += [self._island_bridges_z3[pos][dir] for dir in Direction.orthogonals() if pos.after(dir) not in region_positions and pos.after(dir) in self._island_bridges_z3]
            self._solver.add(sum(out_directions) == 2)  # 1 for in and 1 for out

    def _add_all_regions_crossed_constraints(self):
        for region in self._regions.values():
            self._add_regions_crossed_constraints(region)

    def _add_regions_crossed_constraints(self, region: frozenset[Position]):
        sum_for_positions_constraints = []
        for position in region:
            sum_for_positions_constraints.append(sum([self._island_bridges_z3[position][direction] for direction in Direction.orthogonals()]) == 2)
        self._solver.add(Or(sum_for_positions_constraints))

    def _add_alternating_black_and_withe_constraints(self):
        # Variable binaire par position pour l'alternance globale (0/1)
        positions = list(self._island_bridges_z3.keys())
        pos_state = {position: Int(f"s_{position}") for position in positions}

        # Domaine des variables d'état: 0 ou 1
        self._solver.add([Or(pos_state[p] == 0, pos_state[p] == 1) for p in positions])

        # Si un pont est utilisé entre deux positions voisines, leurs états doivent être opposés
        for p in positions:
            for d in Direction.orthogonals():
                q = p.after(d)
                if q in self._island_bridges_z3:
                    self._solver.add(Or(self._island_bridges_z3[p][d] == 0, pos_state[p] + pos_state[q] == 1))

        # Si une case colorée est traversée (degré == 2), l'état est fixé selon la couleur
        for p in positions:
            deg = sum([self._island_bridges_z3[p][direction] for direction in Direction.orthogonals()])
            cell = self._circle_grid[p]
            if cell == self.white:
                # traversée => état 1
                self._solver.add(Or(deg != 2, pos_state[p] == 1))
            elif cell == self.black:
                # traversée => état 0
                self._solver.add(Or(deg != 2, pos_state[p] == 0))

    def _add_all_same_color_in_region_crossed_constraints(self):
        for region in self._regions.values():
            self._add_same_color_in_region_crossed_constraints(region)

    def _add_same_color_in_region_crossed_constraints(self, region):
        white_positions = [position for position in region if self._circle_grid[position] == self.white]
        black_positions = [position for position in region if self._circle_grid[position] == self.black]

        if len(white_positions) == 0:
            white_constraint = False
            not_white_constraint = True
        else:
            white_constraints = []
            not_white_constraints = []
            for position in white_positions:
                white_constraints.append(sum([self._island_bridges_z3[position][direction] for direction in Direction.orthogonals()]) == 2)
                not_white_constraints.append(sum([self._island_bridges_z3[position][direction] for direction in Direction.orthogonals()]) == 0)
            white_constraint = And(white_constraints)
            not_white_constraint = And(not_white_constraints)

        if len(black_positions) == 0:
            black_constraint = False
            not_black_constraint = True
        else:
            black_constraints = []
            not_black_constraints = []
            for position in black_positions:
                black_constraints.append(sum([self._island_bridges_z3[position][direction] for direction in Direction.orthogonals()]) == 2)
                not_black_constraints.append(sum([self._island_bridges_z3[position][direction] for direction in Direction.orthogonals()]) == 0)
            black_constraint = And(black_constraints)
            not_black_constraint = And(not_black_constraints)

        self._solver.add(Or(And(white_constraint, not_black_constraint), And(black_constraint, not_white_constraint)))