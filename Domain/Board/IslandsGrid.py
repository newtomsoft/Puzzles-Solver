from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Island import Island
from Domain.Board.Position import Position


class IslandGrid(Grid[Island]):
    def __init__(self, input_matrix: list[list[int | Island]]):
        super().__init__(input_matrix)
        self.islands: dict[Position, Island] = {}
        for position, island_or_bridges_number in self:
            if isinstance(island_or_bridges_number, Island) and island_or_bridges_number.bridges_count != 0:
                self.islands[position] = island_or_bridges_number
            elif isinstance(island_or_bridges_number, int) and island_or_bridges_number != 0:
                self.islands[position] = Island(position, island_or_bridges_number)

        if len(self.islands) == 0:
            super().__init__([[]])
            self.islands = {}
            return

        self._compute_possible_bridges()
        self.possible_crossover_bridge = self._compute_possible_crossover_bridges()

    @staticmethod
    def from_walls_grid(grid: Grid, with_edges: bool = False) -> 'IslandGrid':
        input_matrix = [[Island(Position(r, c), 1) for c in range(grid.columns_number + 1)] for r in range(grid.rows_number + 1)]
        island_grid = IslandGrid(input_matrix)
        positions_with_bridges = set()
        for position0, position1 in grid.walls:
            if position0 > position1:
                position0, position1 = position1, position0
            if position0.direction_to(position1) == Direction.right():
                island_grid[position1].set_bridge_to_position(position1.down, 1)
                island_grid[position1.down].set_bridge_to_position(position1, 1)
                positions_with_bridges.add(position1)
                positions_with_bridges.add(position1.down)
            elif position0.direction_to(position1) == Direction.down():
                island_grid[position1].set_bridge_to_position(position1.right, 1)
                island_grid[position1.right].set_bridge_to_position(position1, 1)
                positions_with_bridges.add(position1)
                positions_with_bridges.add(position1.right)

        if not with_edges:
            for position, _ in island_grid:
                island_grid[position].set_bridges_count_according_to_directions_bridges()
            return island_grid

        for position in island_grid.edge_up_positions()[:-1]:
            island_grid[position].set_bridge_to_position(position.right, 1)
        for position in island_grid.edge_up_positions()[1:]:
            island_grid[position].set_bridge_to_position(position.left, 1)
        for position in island_grid.edge_down_positions()[:-1]:
            island_grid[position].set_bridge_to_position(position.right, 1)
        for position in island_grid.edge_down_positions()[1:]:
            island_grid[position].set_bridge_to_position(position.left, 1)
        for position in island_grid.edge_left_positions()[:-1]:
            island_grid[position].set_bridge_to_position(position.down, 1)
        for position in island_grid.edge_left_positions()[1:]:
            island_grid[position].set_bridge_to_position(position.up, 1)
        for position in island_grid.edge_right_positions()[:-1]:
            island_grid[position].set_bridge_to_position(position.down, 1)
        for position in island_grid.edge_right_positions()[1:]:
            island_grid[position].set_bridge_to_position(position.up, 1)

        for position, _ in island_grid:
            island_grid[position].set_bridges_count_according_to_directions_bridges()
        return island_grid

    @staticmethod
    def empty() -> 'IslandGrid':
        return IslandGrid([[]])

    def _compute_possible_bridges(self):
        for island in self.islands.values():
            min_distances = {}
            for other_island in self.islands.values():
                direction = island.position.direction_to(other_island.position)
                if direction != Direction.right() and direction != Direction.left() and direction != Direction.up() and direction != Direction.down():
                    continue
                distance = island.position.distance_to(other_island.position)
                if direction == Direction.right() and distance < min_distances.get(Direction.right(), (float('inf'), None))[0]:
                    min_distances[Direction.right()] = (distance, other_island.position)
                    continue
                if direction == Direction.left() and distance < min_distances.get(Direction.left(), (float('inf'), None))[0]:
                    min_distances[Direction.left()] = (distance, other_island.position)
                    continue
                if direction == Direction.up() and distance < min_distances.get(Direction.up(), (float('inf'), None))[0]:
                    min_distances[Direction.up()] = (distance, other_island.position)
                    continue
                if direction == Direction.down() and distance < min_distances.get(Direction.down(), (float('inf'), None))[0]:
                    min_distances[Direction.down()] = (distance, other_island.position)
                    continue

            if min_distances.get(Direction.right()) is not None:
                island.direction_position_bridges[Direction.right()] = min_distances[Direction.right()][1], 0
            if min_distances.get(Direction.left()) is not None:
                island.direction_position_bridges[Direction.left()] = min_distances[Direction.left()][1], 0
            if min_distances.get(Direction.up()) is not None:
                island.direction_position_bridges[Direction.up()] = min_distances[Direction.up()][1], 0
            if min_distances.get(Direction.down()) is not None:
                island.direction_position_bridges[Direction.down()] = min_distances[Direction.down()][1], 0

    def _compute_possible_crossover_bridges(self) -> list[dict[Position, Direction]]:
        possible_multiples_crossover_positions: dict[Position, dict[Position, Direction]] = {}
        for island in self.islands.values():
            island_position = island.position
            for direction, (other_position, _) in island.direction_position_bridges.items():
                if island_position.distance_to(other_position) == 1 or direction == Direction.left() or direction == Direction.up():
                    continue
                cross_positions = island_position.all_positions_between(other_position)
                for cross_position in cross_positions:
                    if possible_multiples_crossover_positions.get(cross_position) is None:
                        possible_multiples_crossover_positions[cross_position] = {}
                    possible_multiples_crossover_positions[cross_position][island_position] = direction

        possible_crossover_bridges = [
            directions_and_positions
            for directions_and_positions in possible_multiples_crossover_positions.values()
            if len(directions_and_positions) == 2
        ]
        return possible_crossover_bridges

    def get_connected_positions(self, exclude_without_bridge=False) -> list[set[Position]]:
        concerned_islands_count = len(self.islands) if not exclude_without_bridge else sum(1 for island in self.islands.values() if island.bridges_count != 0)
        visited_list: list[set[Position]] = []
        visited_flat: set[Position] = set()
        while len(visited_flat) != concerned_islands_count:
            position = next(island.position for island in self.islands.values() if island.position not in visited_flat) if not exclude_without_bridge else next(
                (island.position for island in self.islands.values() if island.bridges_count != 0 and island.position not in visited_flat), None)
            visited = self._depth_first_search_islands(position)
            visited_list.append(visited)
            visited_flat.update(visited)
        return visited_list

    def _depth_first_search_islands(self, position: Position, visited_positions=None) -> set[Position]:
        if visited_positions is None:
            visited_positions = set()
        if position in visited_positions:
            return visited_positions
        visited_positions.add(position)
        position_and_bridges = self.islands[position].direction_position_bridges.values()
        next_positions = [position for position, bridges_count in position_and_bridges if bridges_count > 0 and position not in visited_positions]
        for current_position in next_positions:
            new_visited_positions = self._depth_first_search_islands(current_position, visited_positions)
            if new_visited_positions != visited_positions:
                return new_visited_positions

        return visited_positions

    def compute_linear_connected_positions(self, exclude_without_bridge=False) -> list[set[Position]]:
        concerned_islands_count = len(self.islands) if not exclude_without_bridge else sum(1 for island in self.islands.values() if island.bridges_count != 0)
        visited_list: list[set[Position]] = []
        visited_flat: set[Position] = set()
        while len(visited_flat) != concerned_islands_count:
            position = next(island.position for island in self.islands.values() if island.position not in visited_flat) if not exclude_without_bridge else next(
                (island.position for island in self.islands.values() if island.bridges_count != 0 and island.position not in visited_flat), None)
            visited = self._depth_first_linear_search_islands(position)
            visited_list.append(visited)
            visited_flat.update(visited)
        return visited_list

    def _depth_first_linear_search_islands(self, position: Position, previous_position=None, visited_positions=None, crossed_positions=None) -> set[Position]:
        if visited_positions is None:
            visited_positions = set()
            crossed_positions = set()
        if position in visited_positions - crossed_positions:
            return visited_positions
        visited_positions.add(position)
        position_and_bridges = self.islands[position].direction_position_bridges.values()
        next_positions = [position for position, bridges_count in position_and_bridges if
                          bridges_count > 0 and position not in visited_positions - crossed_positions and position != previous_position]
        if len(next_positions) > 1 and previous_position is not None:
            crossed_positions.add(position)
            direction = previous_position.direction_to(position)
            linear_next_position = position.after(direction)
            next_positions = [linear_next_position]
        for current_position in next_positions:
            new_visited_positions = self._depth_first_linear_search_islands(current_position, position, visited_positions, crossed_positions)
            return new_visited_positions

        return visited_positions

    def get_loop_positions(self) -> set[Position]:
        concerned_islands_count = len(self.islands)
        visited_flat: set[Position] = set()
        while len(visited_flat) != concerned_islands_count:
            position = next(island.position for island in self.islands.values() if island.position not in visited_flat)
            is_loop, positions = self._is_loop(position)
            if is_loop:
                return positions
            visited_flat.update(positions)
        return set()

    def _is_loop(self, position: Position | None = None, visited_positions=None, previous_position=None) -> tuple[bool, set[Position]]:
        if position is None:
            position = next(island.position for island in self.islands.values() if island.bridges_count > 0)
        if visited_positions is None:
            visited_positions = set()
        if position in visited_positions:
            return True, visited_positions
        visited_positions.add(position)
        position_bridges = self.islands[position].direction_position_bridges.values()
        for position_bridge in position_bridges:
            if position_bridge[1] == 0:
                continue
            current_position = position_bridge[0]
            if current_position == previous_position:
                continue
            if current_position in visited_positions:
                return True, visited_positions
            is_loop, _ = self._is_loop(current_position, visited_positions, position)
            if is_loop:
                return True, visited_positions

        return False, visited_positions

    def follow_path(self, position: Position | None = None, previous_position: Position | None = None, visited_positions=None, kept_bridges_by_visited_positions=None) -> list[Position]:
        if position is None:
            position = next(island.position for island in self.islands.values() if island.bridges_count > 0)
        if visited_positions is None:
            visited_positions = []
            kept_bridges_by_visited_positions = {position: self.islands[position].bridges_count - 1}
        visited_positions.append(position)
        position_bridges = self.islands[position].direction_position_bridges.values()
        next_positions_candidates = [position_bridges[0] for position_bridges in position_bridges if
                                     position_bridges[1] > 0 and position_bridges[0] != previous_position]
        if len(next_positions_candidates) == 0:
            return visited_positions
        if len(next_positions_candidates) == 1:
            next_position = next_positions_candidates[0]
        else:
            next_position = position.after(previous_position.direction_to(position)) if previous_position else next_positions_candidates[0]
        bridges_count = self.islands[next_position].bridges_count
        if kept_bridges_by_visited_positions.get(next_position, bridges_count) >= 1:
            kept_bridges_by_visited_positions[next_position] = kept_bridges_by_visited_positions.get(next_position, bridges_count) - 2
            new_visited_positions = self.follow_path(next_position, position, visited_positions, kept_bridges_by_visited_positions)
            if new_visited_positions != visited_positions:
                return new_visited_positions
        return visited_positions

    def __repr__(self) -> str:
        if self.is_empty():
            return 'IslandGrid.empty()'
        current_row = 0
        result = ''
        for position, item in self:
            if position.r != current_row:
                result += '\n'
                current_row = position.r
            if isinstance(item, Island):
                result += repr(item)
            elif isinstance(item, int) or isinstance(item, str):
                result += f' {item} '
            else:
                result += self.get_str(position)
        return result

    def get_str(self, position: Position) -> str:
        island = Island(position, 0)
        for direction in Direction.orthogonal_directions():
            iteration = 1
            while position.after(direction, iteration) in self:
                if position.after(direction, iteration) in self.islands.keys():
                    bridges_numbers = self.islands[position.after(direction, iteration)].bridges_number(direction.opposite)
                    island.set_bridge_to_position(position.after(direction, iteration), bridges_numbers)
                    break
                iteration += 1
        island.set_bridges_count_according_to_directions_bridges()
        island_repr = repr(island)
        return island_repr
