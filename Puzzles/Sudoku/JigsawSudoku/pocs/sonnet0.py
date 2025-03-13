from typing import List, Tuple

import numpy as np


class JigsawSudoku:
    def __init__(self, grid: List[List[int]], regions: List[List[Tuple[int, int]]]):
        """
        Initialise le Jigsaw Sudoku
        grid: grille initiale (0 pour les cases vides)
        regions: liste des régions, chaque région étant une liste de tuples (row, col)
        """
        self.grid = np.array(grid)
        self.regions = regions
        self.size = 9

        # Validation des régions
        all_cells = set()
        for region in regions:
            all_cells.update(region)
        expected_cells = {(i, j) for i in range(9) for j in range(9)}
        if all_cells != expected_cells:
            missing = expected_cells - all_cells
            extra = all_cells - expected_cells
            raise ValueError(f"Régions invalides. Cases manquantes: {missing}, Cases en trop: {extra}")

    def is_valid(self, row: int, col: int, num: int) -> bool:
        """Vérifie si un nombre peut être placé à la position donnée"""
        # Vérifie la ligne
        if num in self.grid[row]:
            return False

        # Vérifie la colonne
        if num in self.grid[:, col]:
            return False

        # Vérifie la région
        region = next(reg for reg in self.regions if (row, col) in reg)
        region_values = {self.grid[r][c] for r, c in region if self.grid[r][c] != 0}
        if num in region_values:
            return False

        return True

    def find_empty(self) -> Tuple[int, int]:
        """Trouve une case vide dans la grille"""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def solve(self) -> bool:
        """Résout le Jigsaw Sudoku en utilisant le backtracking"""
        empty = self.find_empty()
        if not empty:
            return True

        row, col = empty
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.solve():
                    return True
                self.grid[row][col] = 0

        return False

    def print_grid(self):
        """Affiche la grille"""
        print("+" + "-" * 25 + "+")
        for i in range(self.size):
            print("|", end=" ")
            for j in range(self.size):
                print(self.grid[i][j], end=" ")
            print("|")
        print("+" + "-" * 25 + "+")

def main():
    # Exemple de grille avec quelques valeurs initiales
    grid = [
        [5, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 7, 0],
        [0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 3, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 8]
    ]

    # Définition des régions (formes irrégulières, couvrant toute la grille)
    regions = [
        [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1), (2,2), (3,0), (3,1)],  # Région 1
        [(0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,3)],  # Région 2
        [(0,5), (0,6), (0,7), (0,8), (1,5), (1,6), (1,7), (1,8), (2,8)],  # Région 3
        [(2,5), (2,6), (2,7), (3,4), (3,5), (3,6), (3,7), (3,8), (4,6)],  # Région 4
        [(3,2), (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (5,0), (5,1)],  # Région 5
        [(4,7), (4,8), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8)],  # Région 6
        [(6,0), (6,1), (6,2), (7,0), (7,1), (7,2), (8,0), (8,1), (8,2)],  # Région 7
        [(6,3), (6,4), (6,5), (6,6), (7,3), (7,4), (7,5), (8,3), (8,4)],  # Région 8
        [(6,7), (6,8), (7,6), (7,7), (7,8), (8,5), (8,6), (8,7), (8,8)]   # Région 9
    ]

    try:
        # Création et résolution du puzzle
        puzzle = JigsawSudoku(grid, regions)
        print("Grille initiale:")
        puzzle.print_grid()

        if puzzle.solve():
            print("\nSolution:")
            puzzle.print_grid()
        else:
            print("\nPas de solution possible!")
    except ValueError as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()