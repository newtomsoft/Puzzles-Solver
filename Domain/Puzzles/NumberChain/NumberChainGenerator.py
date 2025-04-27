import random

from tqdm import tqdm

from Board.LinearPathGrid import LinearPathGrid
from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from NumberChain.NumberChainSolver import NumberChainSolver
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine


class NumberChainGenerator:
    @staticmethod
    def get_solver_engine():
        return Z3SolverEngine()

    def __init__(self, row_count: int, column_count: int, way_number: int):
        self.grid_path = None
        self.grid: Grid = Grid.empty()
        self.row_count = row_count
        self.column_count = column_count
        self.way_number = way_number
        min_way_length = column_count + row_count - 1
        max_way_length = column_count * row_count
        if not min_way_length <= way_number <= max_way_length:
            raise ValueError(f"La longueur du chemin doit être entre {min_way_length} et {max_way_length}")
        self.directions = Direction.orthogonals()

    def generate_grid(self):
        self._generate_as_linear_path_grid()
        self._fill_grid()
        return self.grid

    def generate_path(self):
        last_exception = None
        for _ in range(10000):
            try:
                return self._try_generate_path()
            except Exception as e:
                last_exception = e

        raise Exception(f"Impossible de générer une grille avec les contraintes données. Dernière erreur: {str(last_exception)}")

    def _try_generate_path(self):
        grid = [[0 for _ in range(self.row_count)] for _ in range(self.row_count)]

        current_pos = Position(0, 0)
        target_pos = Position(self.row_count - 1, self.row_count - 1)

        path = [current_pos]
        grid[current_pos.r][current_pos.c] = 1

        preferred_directions = [2, 3]

        while len(path) < self.way_number:
            if current_pos == target_pos:
                break

            manhattan_dist = abs(current_pos.r - target_pos.r) + abs(current_pos.c - target_pos.c)
            remaining_steps = self.way_number - len(path)
            if remaining_steps < manhattan_dist:
                raise Exception("Impossible de générer un chemin avec la longueur demandée")

            must_go_toward_target = remaining_steps - manhattan_dist <= 1
            valid_directions = []
            random_directions = list(range(len(self.directions)))

            if random.random() < 0.2:
                random_directions = preferred_directions + [d for d in random_directions if d not in preferred_directions]
            else:
                random.shuffle(random_directions)

            for dir_idx in random_directions:
                direction = self.directions[dir_idx]
                new_pos = current_pos.after(direction)

                if self.row_count > new_pos.r >= 0 == grid[new_pos.r][new_pos.c] and 0 <= new_pos.c < self.row_count:
                    if must_go_toward_target:
                        new_dist = abs(new_pos.r - target_pos.r) + abs(new_pos.c - target_pos.c)
                        if new_dist >= manhattan_dist:
                            continue

                    valid_directions.append(direction)

            if not valid_directions:
                raise Exception("Chemin bloqué")

            chosen_direction = random.choice(valid_directions)
            current_pos = current_pos.after(chosen_direction)
            path.append(current_pos)
            grid[current_pos.r][current_pos.c] = 1

        if current_pos != target_pos:
            while current_pos != target_pos:
                best_direction = None
                best_distance = float('inf')

                for direction in self.directions:
                    new_pos = current_pos.add(direction)

                    if (0 <= new_pos.row < self.row_count and
                            0 <= new_pos.col < self.row_count):

                        new_dist = abs(new_pos.row - target_pos.r) + abs(new_pos.col - target_pos.c)

                        if new_dist < best_distance:
                            best_distance = new_dist
                            best_direction = direction

                current_pos = current_pos.add(best_direction)
                path.append(current_pos)
                grid[current_pos.row][current_pos.col] = 1

        if len(path) != self.way_number:
            raise Exception(f"Chemin généré de longueur {len(path)}, mais {self.way_number} demandé")

        return grid

    def generate_as_grid(self):
        grid_data = self.generate_path()
        return Grid(grid_data)

    def _generate_as_linear_path_grid(self):
        is_single_path = False
        single_path_tries = 0
        while not is_single_path:
            single_path_tries += 1
            self.grid = self.generate_as_grid()
            self.grid.set_value(Position(0, 0), 1)
            self.grid.set_value(Position(row_count - 1, row_count - 1), 2)
            has_multy_path = LinearPathGrid.has_multy_path(self.grid, Position(0, 0), Position(row_count - 1, column_count - 1))
            if not has_multy_path:
                is_single_path = True
                self.grid_path = LinearPathGrid.from_grid_and_checkpoints(self.grid, {1: Position(0, 0), 2: Position(row_count - 1, column_count - 1)})
        print(f"single path tries: {single_path_tries}")

    def _fill_grid(self):
        self.grid.set_value(Position(0, 0), 1)
        self.grid.set_value(Position(self.row_count - 1, self.column_count - 1), way_count)
        way_to_fill = list(range(2, way_count))
        random.shuffle(way_to_fill)
        for i, candidate_to_fill in enumerate(way_to_fill):
            position = self.grid_path.path[i + 1]
            self.grid.set_value(position, candidate_to_fill)

        pre_filled = []
        for position, value in [(p, v) for p, v in self.grid if p not in self.grid_path.path and not any([neighbor in self.grid_path.path for neighbor in p.neighbors()])]:
            self.grid.set_value(position, random.choice(way_to_fill))
            pre_filled.append(position)

        positions_reprocessed_count = 0
        positions_to_fill = [position for position, _ in self.grid if position not in self.grid_path.path and position not in pre_filled]
        random.shuffle(positions_to_fill)
        for position in tqdm(positions_to_fill):
            filled = False
            random.shuffle(way_to_fill)
            extremity = [1, way_count]
            random.shuffle(extremity)
            candidates_to_fill = way_to_fill + extremity
            for candidate_to_fill in candidates_to_fill:
                self.grid.set_value(position, candidate_to_fill)
                game_solver = NumberChainSolver(self.grid, self.get_solver_engine())
                _ = game_solver.get_solution()
                other_solution = game_solver.get_other_solution()
                if other_solution == Grid.empty():
                    filled = True
                    break
                positions_reprocessed_count += 1
            if not filled:
                raise Exception("Impossible de remplir la grille")
        print("positions reprocessed", positions_reprocessed_count)


if __name__ == "__main__":
    row_count = 8
    column_count = 8
    way_count = 27

    generator = NumberChainGenerator(row_count, column_count, way_count)
    generator.generate_grid()
    print(generator.grid_path)
    print(generator.grid)
