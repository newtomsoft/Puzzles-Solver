from z3 import Solver, Not, And, Or, Int, Implies, unsat, If, BoolRef

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class NeighboursSolver(GameSolver):
    empty = None

    def __init__(self, clues_clues_grid: Grid):
        self._clues_grid = clues_clues_grid
        self._rows_number = clues_clues_grid.rows_number
        self._columns_number = clues_clues_grid.columns_number
        self._solver = Solver()
        self._grid_z3: Grid | None = None
        self._clue_by_position = dict([(position, value) for position, value in self._clues_grid if value != NeighboursSolver.empty])
        self._clue_position_by_region_id = {index + 1: position for index, position in enumerate(self._clue_by_position.keys())}
        self._regions_count = len(self._clue_by_position)

    def get_solution(self) -> Grid:
        self._grid_z3 = Grid([[Int(f"grid_{r}_{c}") for c in range(self._columns_number)] for r in range(self._rows_number)])
        self._add_constraints()
        return self._compute_solution()

    def get_other_solution(self) -> Grid:
        self._solver.add(Not(And([self._grid_z3[position] == value for position, value in self._previous_solution])))
        return self._compute_solution()

    def _compute_solution(self) -> Grid:
        if self._solver.check() == unsat:
            return Grid.empty()
        model = self._solver.model()
        solution = Grid([[(model.eval(self._grid_z3.value(i, j))).as_long() for j in range(self._columns_number)] for i in range(self._rows_number)])
        self._previous_solution = solution
        return solution

    def _add_constraints(self):
        self._add_initials_constraints()
        self._add_area_regions_constraints()
        self._add_connected_cells_regions_constraints()
        self._add_neighbours_clues_constraints()

    def _add_initials_constraints(self):
        for region_id, position in self._clue_position_by_region_id.items():
            self._solver.add(self._grid_z3[position] == region_id)

    def _add_area_regions_constraints(self):
        area = self._rows_number * self._columns_number // self._regions_count
        for region_id in self._clue_position_by_region_id.keys():
            self._solver.add(sum([self._grid_z3[position] == region_id for position, _ in self._clues_grid]) == area)

    def _add_connected_cells_regions_constraints(self):
        steps = [Grid([[Int(f'step{region_id}_{r}_{c}') for c in range(self._columns_number)] for r in range(self._rows_number)]) for region_id in
                 range(1, self._regions_count + 1)]
        for region_id in self._clue_position_by_region_id.keys():
            self._add_connected_cells_region_constraints(steps[region_id - 1], region_id)

    def _add_connected_cells_region_constraints(self, step: Grid, region_id: int):
        self._solver.add([If(self._grid_z3[position] == region_id, step[position] >= 1, step[position] == 0) for position, _ in self._clues_grid])

        roots = [And(self._grid_z3[position] == region_id, step[position] == 1) for position, _ in self._clues_grid]
        self._solver.add(Or(roots))

        self._solver.add([Not(And(roots[i], roots[j])) for i in range(len(roots)) for j in range(i + 1, len(roots))])

        for r in range(self._rows_number):
            for c in range(self._columns_number):
                current_step = step[r][c]
                adjacents = []
                if r > 0:
                    adjacents.append(And(self._grid_z3[r - 1][c] == region_id, step[r - 1][c] == current_step - 1))
                if r < self._rows_number - 1:
                    adjacents.append(And(self._grid_z3[r + 1][c] == region_id, step[r + 1][c] == current_step - 1))
                if c > 0:
                    adjacents.append(And(self._grid_z3[r][c - 1] == region_id, step[r][c - 1] == current_step - 1))
                if c < self._columns_number - 1:
                    adjacents.append(And(self._grid_z3[r][c + 1] == region_id, step[r][c + 1] == current_step - 1))

                self._solver.add(Implies(And(self._grid_z3[r][c] == region_id, current_step > 1), Or(adjacents)))

    def _add_neighbours_clues_constraints(self):
        # Construire la liste des paires de cellules adjacentes (orthogonales), unique (position < voisin)
        adjacent_edges: list[tuple[Position, Position]] = []
        for position, _ in self._clues_grid:
            for neighbor in self._clues_grid.neighbors_positions(position):
                if position < neighbor:  # éviter les doublons (u,v) et (v,u)
                    adjacent_edges.append((position, neighbor))

        # Pour chaque paire de régions (i, j), définir une contrainte «Adj(i,j)» signifiant
        # qu'il existe au moins une arête (u,v) telle que grid[u]==i et grid[v]==j (ou l'inverse).
        # Puis imposer pour chaque région i que le nombre de régions adjacentes égale l'indice (clue) de i.
        region_ids = list(self._clue_position_by_region_id.keys())
        # Pré-calcul des formules d'adjacence entre régions
        adj_between_regions: dict[tuple[int, int], BoolRef] = {}
        for i in region_ids:
            for j in region_ids:
                if i >= j:
                    continue
                disjuncts = []
                for (u, v) in adjacent_edges:
                    disjuncts.append(And(self._grid_z3[u] == i, self._grid_z3[v] == j))
                    disjuncts.append(And(self._grid_z3[u] == j, self._grid_z3[v] == i))
                adj_between_regions[(i, j)] = Or(disjuncts) if disjuncts else Or([])

        # Compter, pour chaque région i, le nombre de régions j adjacentes distinctes
        for i in region_ids:
            clue_position = self._clue_position_by_region_id[i]
            clue_value = self._clue_by_position[clue_position]
            terms = []
            for j in region_ids:
                if j == i:
                    continue
                key = (i, j) if i < j else (j, i)
                terms.append(If(adj_between_regions[key], 1, 0))
            self._solver.add(sum(terms) == clue_value)
