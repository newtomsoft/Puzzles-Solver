import itertools

from z3 import *


def solve_killer_sudoku(cages, size=9):
    """
    Résout un Sudoku Killer
    
    Args:
        cages: liste de tuples (somme, [(row1, col1), (row2, col2), ...])
              représentant les cages avec leur somme cible et les cellules concernées
        size: taille de la grille (par défaut 9x9)
    
    Returns:
        Solution sous forme de liste de listes ou None si pas de solution
    """
    # Créer le solveur
    solver = Solver()

    # Créer les variables pour chaque cellule
    cells = [[Int(f"cell_{i}_{j}") for j in range(size)] for i in range(size)]

    # Contraintes de base du Sudoku
    # 1. Chaque cellule contient un nombre entre 1 et 9
    for i, j in itertools.product(range(size), range(size)):
        solver.add(cells[i][j] >= 1, cells[i][j] <= size)

    # 2. Chaque ligne contient des nombres différents
    for i in range(size):
        solver.add(Distinct(cells[i]))

    # 3. Chaque colonne contient des nombres différents
    for j in range(size):
        solver.add(Distinct([cells[i][j] for i in range(size)]))

    # 4. Chaque bloc 3x3 contient des nombres différents
    for block_i in range(0, size, 3):
        for block_j in range(0, size, 3):
            block = []
            for i in range(3):
                for j in range(3):
                    block.append(cells[block_i + i][block_j + j])
            solver.add(Distinct(block))

    # 5. Contraintes des cages (spécifique au Killer Sudoku)
    for cage_sum, cage_cells in cages:
        # Créer la liste des variables pour cette cage
        cage_vars = [cells[i][j] for i, j in cage_cells]
        # La somme des cellules doit être égale à la valeur cible
        solver.add(Sum(cage_vars) == cage_sum)
        # Les nombres dans une cage doivent être différents
        solver.add(Distinct(cage_vars))

    # Résoudre le puzzle
    if solver.check() == sat:
        model = solver.model()
        # Convertir le modèle en grille solution
        solution = [[model.evaluate(cells[i][j]).as_long()
                     for j in range(size)]
                    for i in range(size)]
        return solution
    return None

def print_grid(grid):
    """Affiche la grille de manière formatée"""
    if grid is None:
        print("Pas de solution")
        return

    for i in range(len(grid)):
        if i % 3 == 0 and i != 0:
            print("-" * 25)

        for j in range(len(grid[0])):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(grid[i][j], end=" ")
        print()

# Exemple d'utilisation
def main():
    # Exemple de cages pour un Killer Sudoku
    # Format: (somme_cible, [(ligne1, colonne1), (ligne2, colonne2), ...])
    example_cages = [
        (7, [(0, 0), (0, 1)]),
        (16, [(0, 2), (1, 2), (2, 2)]),
        (14, [(0, 3), (0, 4)]),
        (17, [(0, 5), (1, 5), (2, 5)]),
        (13, [(0, 6), (0, 7), (0, 8)]),
        (11, [(1, 0), (2, 0)]),
        (3, [(1, 1), (2, 1)]),
        # Ajoutez d'autres cages selon votre puzzle...
    ]

    solution = solve_killer_sudoku(example_cages)
    print_grid(solution)

if __name__ == "__main__":
    main()