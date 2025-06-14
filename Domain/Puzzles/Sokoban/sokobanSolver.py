from collections import deque

W = '#'
B = '$'
T = '.'
P = '@'
_ = ' '

def print_grid(grid, player_pos, box_positions):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    display_grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == '#':
                display_grid[y][x] = '#'
            elif grid[y][x] == '.':
                display_grid[y][x] = '.'

    for bx, by in box_positions:
        if display_grid[by][bx] == '.':
            display_grid[by][bx] = '*'  # Caisse sur cible
        else:
            display_grid[by][bx] = '$'  # Caisse normale

    px, py = player_pos
    display_grid[py][px] = '@'

    for row in display_grid:
        print(''.join(row))
    print()


def is_valid_move(grid, player_pos, box_positions, dx, dy):
    px, py = player_pos
    nx, ny = px + dx, py + dy

    # Vérifier si la nouvelle position est dans la grille
    if nx < 0 or ny < 0 or ny >= len(grid) or nx >= len(grid[0]):
        return False, -1

    # Vérifier si la nouvelle position est un mur
    if grid[ny][nx] == '#':
        return False, -1

    # Vérifier si la nouvelle position contient une caisse
    box_idx = -1
    for i, (bx, by) in enumerate(box_positions):
        if nx == bx and ny == by:
            box_idx = i
            break

    # Si pas de caisse, le mouvement est valide
    if box_idx == -1:
        return True, -1

    # Si caisse, vérifier si elle peut être poussée
    bx, by = box_positions[box_idx]
    nbx, nby = bx + dx, by + dy  # Nouvelle position de la caisse

    # Vérifier si la nouvelle position de la caisse est dans la grille
    if nbx < 0 or nby < 0 or nby >= len(grid) or nbx >= len(grid[0]):
        return False, -1

    # Vérifier si la nouvelle position de la caisse est un mur
    if grid[nby][nbx] == '#':
        return False, -1

    # Vérifier si la nouvelle position de la caisse contient une autre caisse
    for i, (bx, by) in enumerate(box_positions):
        if i != box_idx and nbx == bx and nby == by:
            return False, -1


    # Le mouvement est valide, et on pousse la caisse
    return True, box_idx


def get_targets(grid):
    targets = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '.':
                targets.append((x, y))
    return targets


def is_solved(box_positions, targets):
    for target in targets:
        if target not in box_positions:
            return False
    return True


def solve_sokoban_bfs(grid, max_steps):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Trouver la position initiale du joueur, des caisses et des cibles
    initial_player_pos = None
    initial_box_positions = []
    targets = []

    for y in range(rows):
        for x in range(cols):
            cell = grid[y][x]
            if cell == '@':
                initial_player_pos = (x, y)
            elif cell == '$':
                initial_box_positions.append((x, y))
            elif cell == '*':
                initial_box_positions.append((x, y))
                targets.append((x, y))
            elif cell == '.':
                targets.append((x, y))

    # Vérifications de base
    if initial_player_pos is None:
        raise ValueError("La grille doit contenir exactement un joueur.")
    if len(initial_box_positions) == 0:
        raise ValueError("La grille ne contient aucune caisse.")
    if len(targets) == 0:
        raise ValueError("La grille ne contient aucune cible.")
    if len(initial_box_positions) != len(targets):
        raise ValueError("Le nombre de caisses doit être égal au nombre de cibles.")

    # Convertir les positions des caisses en tuple pour pouvoir les utiliser comme clés de dictionnaire
    initial_box_positions = tuple(sorted(initial_box_positions))

    # File d'attente pour BFS
    queue = deque([(initial_player_pos, initial_box_positions, 0, [])])

    # Ensemble des états visités (position du joueur, positions des caisses)
    visited = {(initial_player_pos, initial_box_positions)}

    # Directions possibles: haut, bas, gauche, droite
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while queue:
        player_pos, box_positions, steps, path = queue.popleft()

        # Vérifier si on a atteint le nombre maximum d'étapes
        if steps > max_steps:
            continue

        # Vérifier si toutes les caisses sont sur des cibles
        if all((bx, by) in targets for bx, by in box_positions):
            return steps, path

        # Essayer chaque direction
        for dx, dy in directions:
            valid, box_idx = is_valid_move(grid, player_pos, box_positions, dx, dy)

            if valid:
                # Calculer la nouvelle position du joueur
                new_player_pos = (player_pos[0] + dx, player_pos[1] + dy)

                # Calculer les nouvelles positions des caisses
                new_box_positions = list(box_positions)

                # Si on pousse une caisse, mettre à jour sa position
                if box_idx != -1:
                    old_box_pos = new_box_positions[box_idx]
                    new_box_pos = (old_box_pos[0] + dx, old_box_pos[1] + dy)
                    new_box_positions[box_idx] = new_box_pos

                # Convertir en tuple pour l'utiliser comme clé
                new_box_positions = tuple(sorted(new_box_positions))

                # Vérifier si cet état a déjà été visité
                new_state = (new_player_pos, new_box_positions)
                if new_state not in visited:
                    visited.add(new_state)
                    # Ajouter le nouvel état à la file d'attente
                    new_path = path + [(new_player_pos, new_box_positions)]
                    queue.append((new_player_pos, new_box_positions, steps + 1, new_path))

    # Si on sort de la boucle sans trouver de solution
    return False, None


def print_solution_path(grid, path):
    for i, (player_pos, box_positions) in enumerate(path):
        print(f"Étape {i}:")
        print_grid(grid, player_pos, box_positions)

def recherche_solution(grid_str, max_steps):
    grid = [list(line) for line in grid_str.split('\n')]
    steps, path = solve_sokoban_bfs(grid, max_steps)
    if steps is False:
        print("Aucune solution trouvée dans la limite des étapes.")
        return False

    print(f"Solution trouvée en {steps} étapes.")
    print_solution_path(grid, path)
    return steps
