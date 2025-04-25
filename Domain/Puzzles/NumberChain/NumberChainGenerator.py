import random

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


class NumberChainGenerator:
    def __init__(self, n: int, way_number: int):
        self.n = n
        self.way_number = way_number

        min_way_length = 2 * n - 1
        max_way_length = n * n

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
        grid = [[0 for _ in range(self.n)] for _ in range(self.n)]

        current_pos = Position(0, 0)
        target_pos = Position(self.n - 1, self.n - 1)

        path = [current_pos]
        grid[current_pos.r][current_pos.c] = 1

        preferred_directions = [0, 1]

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

            if random.random() < 0.7:  # 70% de chance de privilégier ces directions
                random_directions = preferred_directions + [d for d in random_directions if d not in preferred_directions]
            else:
                random.shuffle(random_directions)

            for dir_idx in random_directions:
                direction = self.directions[dir_idx]
                new_pos = current_pos.after(direction)

                if self.n > new_pos.r >= 0 == grid[new_pos.r][new_pos.c] and 0 <= new_pos.c < self.n:
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

                    if (0 <= new_pos.row < self.n and
                            0 <= new_pos.col < self.n):

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
    generator = NumberChainGenerator(4, 11)
    grid = generator.generate_as_grid()
    print(grid)
