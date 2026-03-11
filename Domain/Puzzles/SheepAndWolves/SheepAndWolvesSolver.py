from ortools.sat.python import cp_model

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class SheepAndWolvesSolver(GameSolver):
    S = 'S'
    W = 'W'

    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._island_bridges: dict[Position, dict[Direction, cp_model.BoolVar]] = {}
        self._cell_inside: dict[Position, cp_model.BoolVar] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number + 1)] for r in range(self.input_grid.rows_number + 1)])

    def _init_solver(self):
        self._island_bridges = {island.position: {direction: self._model.new_bool_var(f"bridge_{island.position}_{direction}") for direction in Direction.orthogonal_directions()} for island in self._island_grid.islands.values()}
        self._cell_inside = {Position(r, c): self._model.new_bool_var(f"inside_{r}_{c}") for r in range(self.input_grid.rows_number) for c in range(self.input_grid.columns_number)}
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        if not self._model.proto.constraints:
            self._init_solver()

        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        status = self._solver.solve(self._model)
        while status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            proposition_count += 1
            for position, direction_bridges in self._island_bridges.items():
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges:
                        continue
                    bridges_number = self._solver.value(bridges)
                    if bridges_number > 0:
                        self._island_grid[position].set_bridge_to_position(position.after(direction), bridges_number)
                    elif position in self._island_grid and direction in self._island_grid[position].direction_position_bridges:
                        # Clear old bridges from previous attempt if any
                        # In SurizaSolver they do .pop, but we need to be careful with Island object state
                        pass
                
                # Reset bridges and count based on solver values
                current_island = self._island_grid[position]
                current_island.direction_position_bridges = {}
                for direction, bridges in self._island_bridges[position].items():
                    bridges_number = self._solver.value(bridges)
                    if bridges_number > 0 and position.after(direction) in self._island_bridges:
                        neighbor_pos = position.after(direction)
                        current_island.direction_position_bridges[direction] = (neighbor_pos, bridges_number)
                current_island.set_bridges_count_according_to_directions_bridges()

            connected_positions = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_positions) <= 1:
                # One loop (or no loop, but constraints should force a loop)
                # Check if there is at least one bridge to avoid empty solution if not intended
                has_bridges = any(island.bridges_count > 0 for island in self._island_grid.islands.values())
                if has_bridges:
                    self._previous_solution = self._island_grid
                    return self._island_grid, proposition_count
                else:
                    # If no bridges, and it's allowed by Slitherlink rules (all numbers 0 or empty), 
                    # but usually there's at least one loop.
                    # Sheep/Wolves might force a loop.
                    pass

            # Multiple components or no loop. Add constraints to break sub-loops or force connection.
            # Standard Slitherlink approach: add constraint that at least one edge of each component must be different.
            for positions in connected_positions:
                not_all_equal = []
                for position in positions:
                    for direction, bridges in self._island_bridges[position].items():
                        if position.after(direction) not in self._island_bridges:
                            continue
                        val = self._solver.value(bridges)
                        different = self._model.new_bool_var(f"diff_{position}_{direction}_{proposition_count}")
                        self._model.add(bridges != val).only_enforce_if(different)
                        not_all_equal.append(different)

                self._model.add_bool_or(not_all_equal)

            status = self._solver.solve(self._model)

        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        if self._previous_solution is None:
            return IslandGrid.empty()
            
        not_all_equal = []
        for position, direction_bridges in self._island_bridges.items():
            for direction, bridges in direction_bridges.items():
                if position.after(direction) not in self._island_bridges:
                    continue

                island = self._previous_solution[position]
                val = 0
                if direction in island.direction_position_bridges:
                    val = island.direction_position_bridges[direction][1]
                
                different = self._model.new_bool_var(f"diff_other_{position}_{direction}")
                self._model.add(bridges != val).only_enforce_if(different)
                not_all_equal.append(different)
        
        self._model.add_bool_or(not_all_equal)
        return self.get_solution()

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_numbers_constraints()
        self._add_inside_outside_constraints()

    def _add_initial_constraints(self):
        for col in range(self._island_grid.columns_number):
            self._model.add_bool_and(self._island_bridges[Position(0, col)][Direction.up()].Not())
            self._model.add_bool_and(self._island_bridges[Position(self._island_grid.rows_number - 1, col)][Direction.down()].Not())

        for row in range(self._island_grid.rows_number):
            self._model.add_bool_and(self._island_bridges[Position(row, self._island_grid.columns_number - 1)][Direction.right()].Not())
            self._model.add_bool_and(self._island_bridges[Position(row, 0)][Direction.left()].Not())

    def _add_opposite_bridges_constraints(self):
        for island in self._island_grid.islands.values():
            for direction in Direction.orthogonal_directions():
                neighbor_pos = island.position.after(direction)
                if neighbor_pos in self._island_bridges:
                    self._model.add(self._island_bridges[island.position][direction] == self._island_bridges[neighbor_pos][direction.opposite])
                else:
                    self._model.add_bool_and(self._island_bridges[island.position][direction].Not())

    def _add_bridges_sum_constraints(self):
        for island in self._island_grid.islands.values():
            bridge_sum = sum(self._island_bridges[island.position][direction] for direction in Direction.orthogonal_directions())
            is_sum_0 = self._model.new_bool_var(f"is_sum_0_{island.position}")
            is_sum_2 = self._model.new_bool_var(f"is_sum_2_{island.position}")

            self._model.add_bool_or([is_sum_0, is_sum_2])
            self._model.add(bridge_sum == 0).only_enforce_if(is_sum_0)
            self._model.add(bridge_sum == 2).only_enforce_if(is_sum_2)

    def _add_numbers_constraints(self):
        for position, value in self.input_grid:
            if isinstance(value, int) or (isinstance(value, str) and value.isdigit()):
                number = int(value)
                top = self._island_bridges[position][Direction.right()]
                bottom = self._island_bridges[position.down][Direction.right()]
                left = self._island_bridges[position][Direction.down()]
                right = self._island_bridges[position.right][Direction.down()]
                
                self._model.add(top + bottom + left + right == number)

    def _add_inside_outside_constraints(self):
        for pos, value in self.input_grid:
            inside = self._cell_inside[pos]
            
            if value == self.S:
                self._model.add_bool_or(inside)
            elif value == self.W:
                self._model.add_bool_and(inside.Not())
            
            # Right neighbor
            if pos.c + 1 < self.input_grid.columns_number:
                right_inside = self._cell_inside[pos.right]
                border_right = self._island_bridges[pos.right][Direction.down()]
                self._add_xor_constraint(inside, right_inside, border_right)
            else:
                # Border of grid
                border_right = self._island_bridges[pos.right][Direction.down()]
                self._model.add(inside == border_right)
            
            # Left border (only for first column)
            if pos.c == 0:
                border_left = self._island_bridges[pos][Direction.down()]
                self._model.add(inside == border_left)

            # Bottom neighbor
            if pos.r + 1 < self.input_grid.rows_number:
                bottom_inside = self._cell_inside[pos.down]
                border_bottom = self._island_bridges[pos.down][Direction.right()]
                self._add_xor_constraint(inside, bottom_inside, border_bottom)
            else:
                # Border of grid
                border_bottom = self._island_bridges[pos.down][Direction.right()]
                self._model.add(inside == border_bottom)
            
            # Top border (only for first row)
            if pos.r == 0:
                border_top = self._island_bridges[pos][Direction.right()]
                self._model.add(inside == border_top)

    def _add_xor_constraint(self, inside, neighbor_inside, border):
        self._model.add_allowed_assignments([inside, neighbor_inside, border], [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)])
