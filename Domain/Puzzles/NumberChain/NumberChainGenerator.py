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
        self.grid: Grid | None = None
        self.row_count = row_count
        self.column_count = column_count
        self.way_number = way_number
        min_way_length = column_count + row_count - 1
        max_way_length = column_count * row_count
        if not min_way_length <= way_number <= max_way_length:
            raise ValueError(f"La longueur du chemin doit être entre {min_way_length} et {max_way_length}")
        self.directions = Direction.orthogonals()

    def generate_path(self):
        last_exception = None
        for _ in range(10000):
            try:
                return self._try_generate_path()
            except Exception as e:
                last_exception = e

        if last_exception:
            raise Exception(f"Impossible de générer une grille avec les contraintes données. Dernière erreur: {str(last_exception)}")
        else:
            raise Exception("Impossible de générer une grille avec les contraintes données")

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

    def generate_as_linear_path_grid(self):
        is_single_path = False
        while not is_single_path:
            self.grid = self.generate_as_grid()
            self.grid.set_value(Position(0, 0), 1)
            self.grid.set_value(Position(row_count - 1, row_count - 1), 2)
            has_multy_path = LinearPathGrid.has_multy_path(self.grid, Position(0, 0), Position(row_count - 1, column_count - 1))
            if not has_multy_path:
                is_single_path = True
                self.grid_path = LinearPathGrid.from_grid_and_checkpoints(self.grid, {1: Position(0, 0), 2: Position(row_count - 1, column_count - 1)})

    def fill_grid(self):
        self.grid.set_value(Position(0, 0), 1)
        self.grid.set_value(Position(self.row_count - 1, self.column_count - 1), way_count)
        to_fill = list(range(2, way_count))
        random.shuffle(to_fill)
        for i, number_to_fill in enumerate(to_fill):
            position = self.grid_path.path[i + 1]
            self.grid.set_value(position, number_to_fill)

        for position, value in tqdm([(p, v) for p, v in self.grid if p not in self.grid_path.path]):
            while True:
                self.grid.set_value(position, random.randint(1, way_count))
                game_solver = NumberChainSolver(self.grid, self.get_solver_engine())
                solution = game_solver.get_solution()
                if solution == Grid.empty():
                    raise Exception("Impossible de trouver une solution")
                other_solution = game_solver.get_other_solution()
                if other_solution == Grid.empty():
                    break


if __name__ == "__main__":
    row_count = 14
    column_count = 14
    way_count = 47

    generator = NumberChainGenerator(row_count, column_count, way_count)
    generator.generate_as_linear_path_grid()
    print(generator.grid_path)
    generator.fill_grid()
    grid = generator.grid
    print(grid)