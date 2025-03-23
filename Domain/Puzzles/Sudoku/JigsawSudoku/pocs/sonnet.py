from z3 import *

def solve_jigsaw_sudoku(regions, grid=None):
    solver = Solver()
    cells = [[Int(f"cell_{i}_{j}") for j in range(9)] for i in range(9)]

    for i in range(9):
        for j in range(9):
            solver.add(cells[i][j] >= 1, cells[i][j] <= 9)

    if grid is not None:
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    solver.add(cells[i][j] == grid[i][j])

    for i in range(9):
        solver.add(Distinct([cells[i][j] for j in range(9)]))
        solver.add(Distinct([cells[j][i] for j in range(9)]))

    for region in regions:
        solver.add(Distinct([cells[i][j] for i, j in region]))

    if solver.check() == sat:
        model = solver.model()
        return [[model.evaluate(cells[i][j]).as_long()
                 for j in range(9)] for i in range(9)]
    return None

def create_region_map(regions):
    region_map = [[-1 for _ in range(9)] for _ in range(9)]
    for region_id, region in enumerate(regions):
        for i, j in region:
            region_map[i][j] = region_id
    return region_map

def print_grid(grid, regions):
    region_map = create_region_map(regions)

    # Caractères pour les différents types de bordures
    TOP_LEFT = "┌"
    TOP_RIGHT = "┐"
    BOTTOM_LEFT = "└"
    BOTTOM_RIGHT = "┘"
    HORIZONTAL = "─"
    VERTICAL = "│"

    def get_horizontal_separator(row):
        line = ""
        for col in range(9):
            # Vérifie si les cellules au-dessus et en-dessous sont dans des régions différentes
            current_region = region_map[row][col]
            next_region = region_map[row + 1][col]

            # Détermine si on doit tracer une ligne horizontale
            if current_region != next_region:
                # Vérifie les connexions à gauche et à droite pour les coins
                left_different = (col > 0 and
                                  (region_map[row][col-1] != current_region or
                                   region_map[row+1][col-1] != next_region))
                right_different = (col < 8 and
                                   (region_map[row][col+1] != current_region or
                                    region_map[row+1][col+1] != next_region))

                if left_different and right_different:
                    line += "───"
                elif left_different:
                    line += "── "
                elif right_different:
                    line += " ──"
                else:
                    line += "───"
            else:
                line += "   "
        return line

    # Affichage de la bordure supérieure
    print(TOP_LEFT + "─" * 35 + TOP_RIGHT)

    # Affichage de la grille
    for i in range(9):
        # Ligne avec les nombres
        row = VERTICAL + " "
        for j in range(9):
            value = str(grid[i][j]) if grid[i][j] != 0 else "."
            if j < 8:
                if region_map[i][j] != region_map[i][j + 1]:
                    row += f" {value} {VERTICAL}"
                else:
                    row += f" {value}  "
            else:
                row += f" {value} "
        row += VERTICAL
        print(row)

        # Séparateur horizontal si ce n'est pas la dernière ligne
        if i < 8:
            separator = VERTICAL + " " + get_horizontal_separator(i) + " " + VERTICAL
            print(separator)

    # Affichage de la bordure inférieure
    print(BOTTOM_LEFT + "─" * 35 + BOTTOM_RIGHT)

# Définition des régions
regions = [
    # Région 1 (en haut à gauche)
    [(0,0), (0,1), (1,0), (1,1), (2,1), (2,2), (3,1), (3,2), (4,2)],
    # Région 2
    [(0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)],
    # Région 3
    [(0,5), (0,6), (0,7), (0,8), (1,5), (1,6), (2,5), (2,6), (2,7)],
    # Région 4
    [(1,7), (1,8), (2,8), (3,7), (3,8), (4,7), (4,8), (5,7), (5,8)],
    # Région 5
    [(2,0), (3,0), (4,0), (4,1), (5,0), (5,1), (5,2), (6,0), (6,1)],
    # Région 6
    [(3,3), (3,5), (3,6), (4,3), (4,4), (4,5), (4,6), (5,4), (5,5)],
    # Région 7
    [(5,3), (6,2), (6,3), (6,4), (7,2), (7,3), (7,4), (8,2), (8,3)],
    # Région 8
    [(5,6), (6,5), (6,6), (6,7), (6,8), (7,5), (7,6), (7,7), (8,6)],
    # Région 9
    [(7,0), (7,1), (8,0), (8,1), (8,4), (8,5), (8,7), (8,8), (7,8)]
]

# Grille initiale
initial_grid = [
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 7, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 0, 0, 0, 0, 0]
]

print("Grille initiale :")
print_grid(initial_grid, regions)
print("\nRésolution en cours...")

solution = solve_jigsaw_sudoku(regions, initial_grid)
if solution:
    print("\nSolution trouvée :")
    print_grid(solution, regions)
else:
    print("\nPas de solution trouvée")