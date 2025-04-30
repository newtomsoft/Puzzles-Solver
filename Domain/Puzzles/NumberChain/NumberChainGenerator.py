import os
import pickle
import random
import time

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

    def __init__(self, row_number: int, column_number: int, path_cells_number: int):
        self.grid_path = None
        self.grid: Grid = Grid.empty()
        self.row_number = row_number
        self.column_number = column_number
        self.path_length = path_cells_number
        self.values_to_fill = list(range(2, self.path_length))
        min_way_length = column_number + row_number - 1
        max_way_length = column_number * row_number
        if not min_way_length <= path_cells_number <= max_way_length:
            raise ValueError(f"La longueur du chemin doit être entre {min_way_length} et {max_way_length}")
        self.directions = Direction.orthogonals()

    def generate_grid(self):
        self._generate_as_linear_path_grid()
        is_filled = self._fill_grid()
        if not is_filled:
            return
        self._record_grid()

    def _generate_path(self):
        last_exception = None
        for _ in range(1000):
            try:
                return self._try_generate_path()
            except Exception as e:
                last_exception = e
        raise Exception(f"Impossible de générer une grille avec les contraintes données. Dernière erreur: {str(last_exception)}")

    def _try_generate_path(self):
        grid = [[0 for _ in range(self.row_number)] for _ in range(self.row_number)]

        current_pos = Position(0, 0)
        target_pos = Position(self.row_number - 1, self.row_number - 1)

        path = [current_pos]
        grid[current_pos.r][current_pos.c] = 1

        preferred_directions = [2, 3]

        while len(path) < self.path_length:
            if current_pos == target_pos:
                break

            manhattan_dist = abs(current_pos.r - target_pos.r) + abs(current_pos.c - target_pos.c)
            remaining_steps = self.path_length - len(path)
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

                if self.row_number > new_pos.r >= 0 == grid[new_pos.r][new_pos.c] and 0 <= new_pos.c < self.row_number:
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

                    if (0 <= new_pos.row < self.row_number and
                            0 <= new_pos.col < self.row_number):

                        new_dist = abs(new_pos.row - target_pos.r) + abs(new_pos.col - target_pos.c)

                        if new_dist < best_distance:
                            best_distance = new_dist
                            best_direction = direction

                current_pos = current_pos.add(best_direction)
                path.append(current_pos)
                grid[current_pos.row][current_pos.col] = 1

        if len(path) != self.path_length:
            raise Exception(f"Chemin généré de longueur {len(path)}, mais {self.path_length} demandé")

        return grid

    def _generate_as_grid(self):
        grid_data = self._generate_path()
        return Grid(grid_data)

    def _generate_as_linear_path_grid(self):
        is_single_path = False
        single_path_tries = 0
        while not is_single_path:
            single_path_tries += 1
            self.grid = self._generate_as_grid()
            self.grid.set_value(Position(0, 0), 1)
            self.grid.set_value(Position(self.row_number - 1, self.row_number - 1), 2)
            has_multy_path = LinearPathGrid.has_multy_path(self.grid, Position(0, 0), Position(self.row_number - 1, self.row_number - 1))
            if not has_multy_path:
                is_single_path = True
                self.grid_path = LinearPathGrid.from_grid_and_checkpoints(self.grid, {1: Position(0, 0), 2: Position(self.row_number - 1, self.row_number - 1)})

    def _fill_grid(self) -> bool:
        self._fill_path()
        max_retry = 20
        for _ in tqdm(range(max_retry), "try filling grid"):
            self._fill_grid_except_path()
            if self._is_single_solution():
                return True
        return False

    def _fill_path(self):
        self.grid.set_value(Position(0, 0), 1)
        self.grid.set_value(Position(self.row_number - 1, self.column_number - 1), self.path_length)
        random.shuffle(self.values_to_fill)
        for i, candidate_to_fill in enumerate(self.values_to_fill):
            position = self.grid_path.path[i + 1]
            self.grid.set_value(position, candidate_to_fill)

    def _fill_grid_except_path(self):
        first_step_filled_positions = []
        for position in [p for p, _ in self.grid if p not in self.grid_path.path and not any([neighbor in self.grid_path.path for neighbor in p.neighbors()])]:
            self.grid.set_value(position, random.choice(self.values_to_fill))
            first_step_filled_positions.append(position)
        positions_to_fill = [position for position, _ in self.grid if position not in self.grid_path.path and position not in first_step_filled_positions]
        for position in positions_to_fill:
            self.grid.set_value(position, random.choice(self.values_to_fill))

    def _is_single_solution(self):
        game_solver = NumberChainSolver(self.grid, self.get_solver_engine())
        _ = game_solver.get_solution()
        other_solution = game_solver.get_other_solution()
        return other_solution == Grid.empty()

    def _record_grid(self):
        grid_id = f"{self.row_number}x{self.column_number}_{float(time.time())}"

        grid_data = {
            "id": grid_id,
            "grid": self.grid,
            "grid_path": self.grid_path,
            "row_number": self.row_number,
            "column_number": self.column_number,
            "path_length": self.path_length
        }

        file_path = "number_chain_grids.bin"

        existing_grids = {}
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                try:
                    existing_grids = pickle.load(file)
                except EOFError:
                    existing_grids = {}

        existing_grids[grid_id] = grid_data

        with open(file_path, "wb") as file:
            pickle.dump(existing_grids, file)

        print(f"Grille enregistrée avec l'identifiant: {grid_id}")
        return grid_id

    @staticmethod
    def extract_grid(grid_id):
        file_path = "number_chain_grids.bin"

        if not os.path.exists(file_path):
            print("Fichier de grilles introuvable.")
            return None

        with open(file_path, "rb") as file:
            all_grids = pickle.load(file)

        if grid_id in all_grids:
            grid_data = all_grids[grid_id]
            return grid_data["grid"]

        return None


if __name__ == "__main__":
    line_number = int(input("grid dimension ? "))

    line_number_last_number = {
        4: 11,
        5: 15,
        6: 17,
        7: 21,
        8: 27,
        9: 31,
        10: 33,
        11: 37,
        12: 41,
        13: 43,
        14: 47,
        15: 51,
    }

    last_number = line_number_last_number[line_number]

    generator = NumberChainGenerator(line_number, line_number, last_number)

    grid = generator.extract_grid("15x15_1746003072.4328187")

    for i in range(10):
        generator.generate_grid()
