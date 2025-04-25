import random

from Board.LinearPathGrid import LinearPathGrid
from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


class NumberChainGenerator:
    def __init__(self, row_count: int, column_count: int, way_number: int):
        self.row_column_count = row_count
        self.column_count = column_count
        self.way_number = way_number
        min_way_length = column_count + row_count - 1
        max_way_length = column_count * row_count
        if not min_way_length <= way_number <= max_way_length:
            raise ValueError(f"La longueur du chemin doit être entre {min_way_length} et {max_way_length}")
        self.directions = Direction.orthogonals()

    def generate(self):
        for _ in range(100):
            try:
                return self._try_generate()
            except Exception:
                continue
        raise Exception("Impossible de générer une grille avec les contraintes données")

    def _try_generate(self):
        grid = [[0 for _ in range(self.row_column_count)] for _ in range(self.row_column_count)]

        current_pos = Position(0, 0)
        target_pos = Position(self.row_column_count - 1, self.row_column_count - 1)

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

                if self.row_column_count > new_pos.r >= 0 == grid[new_pos.r][new_pos.c] and 0 <= new_pos.c < self.row_column_count:
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

                    if (0 <= new_pos.row < self.row_column_count and
                            0 <= new_pos.col < self.row_column_count):

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
        grid_data = self.generate()
        return Grid(grid_data)


if __name__ == "__main__":
    row_count = 10
    column_count = 10
    way_count = 33
    is_single_path = False
    while not is_single_path:
        generator = NumberChainGenerator(row_count, column_count, way_count)
        grid = generator.generate_as_grid()
        grid.set_value(Position(0, 0), 1)
        grid.set_value(Position(row_count - 1, row_count - 1), 2)
        has_multy_path = LinearPathGrid.has_multy_path(grid, Position(0, 0), Position(row_count - 1, column_count - 1))
        if has_multy_path:
            print("Il y a plusieurs chemins possibles")
        else:
            is_single_path = True
            grid_path = LinearPathGrid.from_grid_and_checkpoints(grid, {1: Position(0, 0), 2: Position(row_count - 1, column_count - 1)})
            print(grid_path)

    # 
    # grid_multy = Grid([
    #     [1, 1, 1],
    #     [1, 1, 1],
    #     [1, 1, 2],
    #     ])
    # has_many_multy = LinearPathGrid.compute_multy_path(grid_multy, Position(0, 0), Position(2, 2))
    # 
    # grid_single = Grid([
    #     [1, 1, 0],
    #     [1, 1, 0],
    #     [1, 1, 2],
    # ])
    # has_many_single = LinearPathGrid.compute_multy_path(grid_single, Position(0, 0), Position(2, 2))
    # print("Il y a plusieurs chemins possibles: OK") if has_many_multy else print("Il y a un seul chemin possible: KO")
    # print("Il y a un seul chemin possible: OK") if not has_many_single else print("Il y a plusieurs chemins possibles: KO")
    # print("")
    # print("result OK") if not has_many_single and has_many_multy else print("result KO")
