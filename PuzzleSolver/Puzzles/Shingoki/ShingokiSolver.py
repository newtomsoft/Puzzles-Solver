from ortools.sat.python.cp_model import CpModel, CpSolver

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Island import Island
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Puzzles.GameSolver import GameSolver


class ShingokiSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.input_grid = grid
        self._island_grid: IslandGrid | None = None
        self._init_island_grid()
        self._model = CpModel()
        self._solver = CpSolver()
        self._island_bridges_ortools: dict[Position, dict[Direction, any]] = {}
        self._previous_solution: IslandGrid | None = None

    def _init_island_grid(self):
        self._island_grid = IslandGrid([[Island(Position(r, c), 2) for c in range(self.input_grid.columns_number)] for r in range(self.input_grid.rows_number)])

    def _init_solver(self):
        self._model = CpModel()
        self._island_bridges_ortools = {
            island.position: {
                direction: self._model.new_bool_var(f"{island.position}_{direction}")
                for direction in Direction.orthogonal_directions()
            }
            for island in self._island_grid.islands.values()
        }
        self._add_constraints()

    def get_solution(self) -> IslandGrid:
        self._init_solver()
        solution, _ = self._ensure_all_islands_connected()
        return solution

    def _ensure_all_islands_connected(self) -> tuple[IslandGrid, int]:
        proposition_count = 0
        orthogonal_dirs = Direction.orthogonal_directions()
        
        while True:
            status = self._solver.solve(self._model)
            if status != 4 and status != 2: # 4 = OPTIMAL, 2 = FEASIBLE
                break
                
            proposition_count += 1
            # Mise à jour de _island_grid avec les valeurs du modèle
            for position, direction_bridges in self._island_bridges_ortools.items():
                island = self._island_grid[position]
                for direction, bridges in direction_bridges.items():
                    if position.after(direction) not in self._island_bridges_ortools:
                        continue
                    bridges_number = self._solver.value(bridges)
                    target_pos, _ = island.direction_position_bridges[direction]
                    island.set_bridge_to_position(target_pos, bridges_number)
                island.set_bridges_count_according_to_directions_bridges()

            connected_components = self._island_grid.get_connected_positions(exclude_without_bridge=True)
            if len(connected_components) == 1:
                self._previous_solution = self._island_grid
                return self._island_grid, proposition_count
            
            if len(connected_components) == 0: # Devrait être impossible s'il y a des cercles
                return IslandGrid.empty(), proposition_count

            # Ajout de contraintes pour éliminer les sous-tours (Cuts)
            for component_positions in connected_components:
                # Pour chaque composante S, on identifie les ponts sortants (frontière)
                boundary_bridges = []
                for pos in component_positions:
                    for direction in orthogonal_dirs:
                        neighbor_pos = pos.after(direction)
                        if neighbor_pos in self._island_bridges_ortools and neighbor_pos not in component_positions:
                            boundary_bridges.append(self._island_bridges_ortools[pos][direction])
                
                if boundary_bridges:
                    # Si S est actif, il doit y avoir au moins 2 ponts sortants
                    # On utilise sum(boundary_bridges) >= 2
                    self._model.add(sum(boundary_bridges) >= 2)
        
        return IslandGrid.empty(), proposition_count

    def get_other_solution(self):
        if not self._previous_solution:
            return IslandGrid.empty()
            
        previous_solution_constraints = []
        for island in self._previous_solution.islands.values():
            for direction in [Direction.right(), Direction.down()]:
                # On ne prend que right et down pour éviter la redondance (Opposite constraint)
                if direction in island.direction_position_bridges:
                    _, bridges_count = island.direction_position_bridges[direction]
                    if bridges_count > 0:
                        previous_solution_constraints.append(self._island_bridges_ortools[island.position][direction])
                    else:
                        previous_solution_constraints.append(self._island_bridges_ortools[island.position][direction].negated())
        
        if previous_solution_constraints:
            self._model.add_bool_or([var.negated() for var in previous_solution_constraints])
        
        self._init_island_grid()
        return self._ensure_all_islands_connected()[0]

    def _add_constraints(self):
        self._add_initial_constraints()
        self._add_opposite_bridges_constraints()
        self._add_bridges_sum_constraints()
        self._add_dots_count_constraints()

    def _add_initial_constraints(self):
        # Optimization: track if a position has a circle to avoid repeated calls
        has_circle = {}
        for position, cell_value in self.input_grid:
            color, _ = self._convert_cell_value_to_color_and_segments_count(cell_value)
            has_circle[position] = (color != ' ')

        for position in self._island_bridges_ortools:
            r, c = position.r, position.c
            if r == 0:
                self._model.add(self._island_bridges_ortools[position][Direction.up()] == 0)
            if r == self._island_grid.rows_number - 1:
                self._model.add(self._island_bridges_ortools[position][Direction.down()] == 0)
            if c == 0:
                self._model.add(self._island_bridges_ortools[position][Direction.left()] == 0)
            if c == self._island_grid.columns_number - 1:
                self._model.add(self._island_bridges_ortools[position][Direction.right()] == 0)
            
            # Optimization: Pre-calculate neighbors to avoid Direction calls in loop
            orthogonal_dirs = Direction.orthogonal_directions()
            
            # Le chemin doit passer par tous les cercles
            if has_circle.get(position, False):
                sum_bridges = sum([self._island_bridges_ortools[position][direction] for direction in orthogonal_dirs])
                self._model.add(sum_bridges == 2)

    def _add_opposite_bridges_constraints(self):
        orthogonal_dirs = Direction.orthogonal_directions()
        for island in self._island_grid.islands.values():
            for direction in orthogonal_dirs:
                if direction in island.direction_position_bridges:
                    neighbor_pos, _ = island.direction_position_bridges[direction]
                    # Optimization: only add constraint once per bridge
                    if island.position < neighbor_pos:
                        self._model.add(self._island_bridges_ortools[island.position][direction] == self._island_bridges_ortools[neighbor_pos][direction.opposite])
                else:
                    self._model.add(self._island_bridges_ortools[island.position][direction] == 0)

    def _add_bridges_sum_constraints(self):
        for position in self._island_bridges_ortools:
            sum_bridges = sum(self._island_bridges_ortools[position].values())
            # sum_bridges must be 0 or 2
            self._model.add_linear_constraint(sum_bridges, 0, 4)
            self._model.add(sum_bridges != 1)
            self._model.add(sum_bridges != 3)
            # sum_bridges can't be 4 in Shingoki (max 2) but actually 4 is possible in grid, but Shingoki says 0 or 2
            self._model.add(sum_bridges != 4)

    def _add_dots_count_constraints(self):
        for position, cell_value in self.input_grid:
            color, segments_count = self._convert_cell_value_to_color_and_segments_count(cell_value)
            if color == ' ':
                continue
                
            constraints = []
            if color == 'b':
                if segments_count == 0:
                    constraints = self._black_constraints_when_no_segment_len_constraint(position)
                else:
                    constraints = self._black_constraints(position, segments_count)
                self._model.add_bool_or(constraints)
                self._not_loop_black2_constraint(position)
            elif color == 'w':
                if segments_count == 0:
                    constraints = self._white_constraints_when_no_segment_len_constraint(position)
                else:
                    constraints = self._white_constraints(position, segments_count)
                self._model.add_bool_or(constraints)
            elif color == 'g':
                if segments_count == 0:
                    constraints = self._black_and_white_constraints_when_no_segment_len_constraint(position)
                else:
                    constraints = self._black_and_white_constraints(position, segments_count)
                self._model.add_bool_or(constraints)
                self._not_loop_black2_constraint(position)

    def _white_constraints_when_no_segment_len_constraint(self, position: Position):
        vertical = self._white_vertical_constraint_when_no_segment_len_constraint(position)
        horizontal = self._white_horizontal_constraint_when_no_segment_len_constraint(position)
        return [vertical, horizontal]

    def _white_vertical_constraint_when_no_segment_len_constraint(self, position):
        res = self._model.new_bool_var(f"white_v_{position}")
        self._model.add_bool_and([self._island_bridges_ortools[position][Direction.up()], self._island_bridges_ortools[position][Direction.down()]]).only_enforce_if(res)
        self._model.add_bool_or([self._island_bridges_ortools[position][Direction.up()].negated(), self._island_bridges_ortools[position][Direction.down()].negated()]).only_enforce_if(res.negated())
        return res

    def _white_horizontal_constraint_when_no_segment_len_constraint(self, position):
        res = self._model.new_bool_var(f"white_h_{position}")
        self._model.add_bool_and([self._island_bridges_ortools[position][Direction.left()], self._island_bridges_ortools[position][Direction.right()]]).only_enforce_if(res)
        self._model.add_bool_or([self._island_bridges_ortools[position][Direction.left()].negated(), self._island_bridges_ortools[position][Direction.right()].negated()]).only_enforce_if(res.negated())
        return res

    def _white_constraints(self, position: Position, segments_count: int):
        white_constraints = []
        for first_part_count in range(1, segments_count):
            second_part_count = segments_count - first_part_count
            
            v_constraints = self._white_vertical_constraints(position, first_part_count, second_part_count)
            h_constraints = self._white_horizontal_constraints(position, first_part_count, second_part_count)
            
            for c in v_constraints:
                white_constraints.append(c)
            for c in h_constraints:
                white_constraints.append(c)
        return white_constraints

    def _white_vertical_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        vertical_positions = (
                [position.after(Direction.up(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.down(), count) for count in range(1, second_part_count + 1)]
        )
        if not all(p in self._island_bridges_ortools for p in vertical_positions):
            return []
            
        res = self._model.new_bool_var(f"white_v_{position}_{first_part_count}_{second_part_count}")
        
        # first_constraint_vertical
        parts = []
        parts.extend([self._island_bridges_ortools[p][Direction.up()] for p in vertical_positions[1:first_part_count + 1]])
        parts.extend([self._island_bridges_ortools[p][Direction.down()] for p in vertical_positions[first_part_count:-1]])
        
        for p in parts:
            self._model.add(p == 1).only_enforce_if(res)
        
        # turn_up
        up_vars = []
        for d in [Direction.left(), Direction.right()]:
            v = self._island_bridges_ortools[vertical_positions[0]].get(d, 0)
            if not isinstance(v, int): up_vars.append(v)
            
        if up_vars:
            self._model.add_bool_or(up_vars).only_enforce_if(res)
        else:
            self._model.add(res == 0)

        # turn_down
        down_vars = []
        for d in [Direction.left(), Direction.right()]:
            v = self._island_bridges_ortools[vertical_positions[-1]].get(d, 0)
            if not isinstance(v, int): down_vars.append(v)
            
        if down_vars:
            self._model.add_bool_or(down_vars).only_enforce_if(res)
        else:
            self._model.add(res == 0)

        return [res]

    def _white_horizontal_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        horizontal_positions = (
                [position.after(Direction.left(), count) for count in reversed(range(1, first_part_count + 1))] +
                [position] +
                [position.after(Direction.right(), count) for count in range(1, second_part_count + 1)]
        )
        if not all(p in self._island_bridges_ortools for p in horizontal_positions):
            return []
            
        res = self._model.new_bool_var(f"white_h_{position}_{first_part_count}_{second_part_count}")
        
        parts = []
        parts.extend([self._island_bridges_ortools[p][Direction.left()] for p in horizontal_positions[1:first_part_count + 1]])
        parts.extend([self._island_bridges_ortools[p][Direction.right()] for p in horizontal_positions[first_part_count:-1]])
        
        for p in parts:
            self._model.add(p == 1).only_enforce_if(res)
            
        # turn_left
        left_vars = []
        for d in [Direction.up(), Direction.down()]:
            v = self._island_bridges_ortools[horizontal_positions[0]].get(d, 0)
            if not isinstance(v, int): left_vars.append(v)
            
        if left_vars:
            self._model.add_bool_or(left_vars).only_enforce_if(res)
        else:
            self._model.add(res == 0)

        # turn_right
        right_vars = []
        for d in [Direction.up(), Direction.down()]:
            v = self._island_bridges_ortools[horizontal_positions[-1]].get(d, 0)
            if not isinstance(v, int): right_vars.append(v)
            
        if right_vars:
            self._model.add_bool_or(right_vars).only_enforce_if(res)
        else:
            self._model.add(res == 0)

        return [res]

    def _black_constraints_when_no_segment_len_constraint(self, position: Position):
        return [
            self._black_right_down_constraint_when_no_segment_len_constraint(position),
            self._black_right_up_constraint_when_no_segment_len_constraint(position),
            self._black_left_down_constraint_when_no_segment_len_constraint(position),
            self._black_left_up_constraint_when_no_segment_len_constraint(position)
        ]

    def _black_right_down_constraint_when_no_segment_len_constraint(self, position):
        res = self._model.new_bool_var(f"black_rd_{position}")
        self._model.add_bool_and([self._island_bridges_ortools[position][Direction.right()], self._island_bridges_ortools[position][Direction.down()]]).only_enforce_if(res)
        return res

    def _black_right_up_constraint_when_no_segment_len_constraint(self, position):
        res = self._model.new_bool_var(f"black_ru_{position}")
        self._model.add_bool_and([self._island_bridges_ortools[position][Direction.right()], self._island_bridges_ortools[position][Direction.up()]]).only_enforce_if(res)
        return res

    def _black_left_down_constraint_when_no_segment_len_constraint(self, position):
        res = self._model.new_bool_var(f"black_ld_{position}")
        self._model.add_bool_and([self._island_bridges_ortools[position][Direction.left()], self._island_bridges_ortools[position][Direction.down()]]).only_enforce_if(res)
        return res

    def _black_left_up_constraint_when_no_segment_len_constraint(self, position):
        res = self._model.new_bool_var(f"black_lu_{position}")
        self._model.add_bool_and([self._island_bridges_ortools[position][Direction.left()], self._island_bridges_ortools[position][Direction.up()]]).only_enforce_if(res)
        return res

    def _black_constraints(self, position: Position, segments_count: int):
        black_constraints = []
        for first_part_count in range(1, segments_count):
            second_part_count = segments_count - first_part_count
            black_constraints.extend(self._black_right_down_constraints(position, first_part_count, second_part_count))
            black_constraints.extend(self._black_right_up_constraints(position, first_part_count, second_part_count))
            black_constraints.extend(self._black_left_down_constraints(position, first_part_count, second_part_count))
            black_constraints.extend(self._black_left_up_constraints(position, first_part_count, second_part_count))
        return black_constraints

    def _black_right_down_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        h_pos = [position.after(Direction.right(), i) for i in range(1, first_part_count + 1)]
        v_pos = [position.after(Direction.down(), i) for i in range(1, second_part_count + 1)]
        if not all(p in self._island_bridges_ortools for p in h_pos + v_pos): return []
        
        res = self._model.new_bool_var(f"black_rd_{position}_{first_part_count}_{second_part_count}")
        self._model.add(self._island_bridges_ortools[position][Direction.right()] == 1).only_enforce_if(res)
        self._model.add(self._island_bridges_ortools[position][Direction.down()] == 1).only_enforce_if(res)
        for i in range(len(h_pos)-1):
            self._model.add(self._island_bridges_ortools[h_pos[i]][Direction.right()] == 1).only_enforce_if(res)
        for i in range(len(v_pos)-1):
            self._model.add(self._island_bridges_ortools[v_pos[i]][Direction.down()] == 1).only_enforce_if(res)
            
        # turn_h
        vars_h = []
        for d in [Direction.up(), Direction.down()]:
            v = self._island_bridges_ortools[h_pos[-1]].get(d, 0)
            if not isinstance(v, int): vars_h.append(v)
        if vars_h: self._model.add_bool_or(vars_h).only_enforce_if(res)
        else: self._model.add(res == 0)
        
        # turn_v
        vars_v = []
        for d in [Direction.left(), Direction.right()]:
            v = self._island_bridges_ortools[v_pos[-1]].get(d, 0)
            if not isinstance(v, int): vars_v.append(v)
        if vars_v: self._model.add_bool_or(vars_v).only_enforce_if(res)
        else: self._model.add(res == 0)
        
        return [res]

    def _black_right_up_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        h_pos = [position.after(Direction.right(), i) for i in range(1, first_part_count + 1)]
        v_pos = [position.after(Direction.up(), i) for i in range(1, second_part_count + 1)]
        if not all(p in self._island_bridges_ortools for p in h_pos + v_pos): return []
        res = self._model.new_bool_var(f"black_ru_{position}_{first_part_count}_{second_part_count}")
        self._model.add(self._island_bridges_ortools[position][Direction.right()] == 1).only_enforce_if(res)
        self._model.add(self._island_bridges_ortools[position][Direction.up()] == 1).only_enforce_if(res)
        for i in range(len(h_pos)-1): self._model.add(self._island_bridges_ortools[h_pos[i]][Direction.right()] == 1).only_enforce_if(res)
        for i in range(len(v_pos)-1): self._model.add(self._island_bridges_ortools[v_pos[i]][Direction.up()] == 1).only_enforce_if(res)
        
        # turn_h
        vars_h = []
        for d in [Direction.up(), Direction.down()]:
            v = self._island_bridges_ortools[h_pos[-1]].get(d, 0)
            if not isinstance(v, int): vars_h.append(v)
        if vars_h: self._model.add_bool_or(vars_h).only_enforce_if(res)
        else: self._model.add(res == 0)
        
        # turn_v
        vars_v = []
        for d in [Direction.left(), Direction.right()]:
            v = self._island_bridges_ortools[v_pos[-1]].get(d, 0)
            if not isinstance(v, int): vars_v.append(v)
        if vars_v: self._model.add_bool_or(vars_v).only_enforce_if(res)
        else: self._model.add(res == 0)
        
        return [res]

    def _black_left_down_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        h_pos = [position.after(Direction.left(), i) for i in range(1, first_part_count + 1)]
        v_pos = [position.after(Direction.down(), i) for i in range(1, second_part_count + 1)]
        if not all(p in self._island_bridges_ortools for p in h_pos + v_pos): return []
        res = self._model.new_bool_var(f"black_ld_{position}_{first_part_count}_{second_part_count}")
        self._model.add(self._island_bridges_ortools[position][Direction.left()] == 1).only_enforce_if(res)
        self._model.add(self._island_bridges_ortools[position][Direction.down()] == 1).only_enforce_if(res)
        for i in range(len(h_pos)-1): self._model.add(self._island_bridges_ortools[h_pos[i]][Direction.left()] == 1).only_enforce_if(res)
        for i in range(len(v_pos)-1): self._model.add(self._island_bridges_ortools[v_pos[i]][Direction.down()] == 1).only_enforce_if(res)
        
        # turn_h
        vars_h = []
        for d in [Direction.up(), Direction.down()]:
            v = self._island_bridges_ortools[h_pos[-1]].get(d, 0)
            if not isinstance(v, int): vars_h.append(v)
        if vars_h: self._model.add_bool_or(vars_h).only_enforce_if(res)
        else: self._model.add(res == 0)
        
        # turn_v
        vars_v = []
        for d in [Direction.left(), Direction.right()]:
            v = self._island_bridges_ortools[v_pos[-1]].get(d, 0)
            if not isinstance(v, int): vars_v.append(v)
        if vars_v: self._model.add_bool_or(vars_v).only_enforce_if(res)
        else: self._model.add(res == 0)
        
        return [res]

    def _black_left_up_constraints(self, position: Position, first_part_count: int, second_part_count: int):
        h_pos = [position.after(Direction.left(), i) for i in range(1, first_part_count + 1)]
        v_pos = [position.after(Direction.up(), i) for i in range(1, second_part_count + 1)]
        if not all(p in self._island_bridges_ortools for p in h_pos + v_pos): return []
        res = self._model.new_bool_var(f"black_lu_{position}_{first_part_count}_{second_part_count}")
        self._model.add(self._island_bridges_ortools[position][Direction.left()] == 1).only_enforce_if(res)
        self._model.add(self._island_bridges_ortools[position][Direction.up()] == 1).only_enforce_if(res)
        for i in range(len(h_pos)-1): self._model.add(self._island_bridges_ortools[h_pos[i]][Direction.left()] == 1).only_enforce_if(res)
        for i in range(len(v_pos)-1): self._model.add(self._island_bridges_ortools[v_pos[i]][Direction.up()] == 1).only_enforce_if(res)
        
        # turn_h
        vars_h = []
        for d in [Direction.up(), Direction.down()]:
            v = self._island_bridges_ortools[h_pos[-1]].get(d, 0)
            if not isinstance(v, int): vars_h.append(v)
        if vars_h: self._model.add_bool_or(vars_h).only_enforce_if(res)
        else: self._model.add(res == 0)
        
        # turn_v
        vars_v = []
        for d in [Direction.left(), Direction.right()]:
            v = self._island_bridges_ortools[v_pos[-1]].get(d, 0)
            if not isinstance(v, int): vars_v.append(v)
        if vars_v: self._model.add_bool_or(vars_v).only_enforce_if(res)
        else: self._model.add(res == 0)
        
        return [res]

    def _black_and_white_constraints_when_no_segment_len_constraint(self, position):
        return self._white_constraints_when_no_segment_len_constraint(position) + self._black_constraints_when_no_segment_len_constraint(position)

    def _black_and_white_constraints(self, position: Position, segments_count: int):
        return self._white_constraints(position, segments_count) + self._black_constraints(position, segments_count)

    @staticmethod
    def _convert_cell_value_to_color_and_segments_count(cell_value: str):
        if cell_value == ' ':
            return ' ', 0
        color = cell_value[0]
        segments_count = int(cell_value[1:])
        return color, segments_count

    def _not_loop_black2_constraint(self, position: Position):
        # En Shingoki, un cercle noir avec un 2 ne peut pas former un petit carré 2x2 avec le chemin.
        # En fait, c'est vrai pour n'importe quel point, mais particulièrement pour les noirs 2.
        # On simplifie en interdisant tout cycle de longueur 4 (carré 2x2 de cellules).
        
        # Carré en haut à droite : points (r,c), (r-1,c), (r,c+1), (r-1,c+1)
        if position.up in self._island_bridges_ortools and \
           position.right in self._island_bridges_ortools and \
           position.up_right in self._island_bridges_ortools:
            b1 = self._island_bridges_ortools[position][Direction.right()]
            b2 = self._island_bridges_ortools[position.up][Direction.right()]
            b3 = self._island_bridges_ortools[position][Direction.up()]
            b4 = self._island_bridges_ortools[position.right][Direction.up()]
            self._model.add_bool_or([b1.negated(), b2.negated(), b3.negated(), b4.negated()])

        # Carré en bas à droite
        if position.down in self._island_bridges_ortools and \
           position.right in self._island_bridges_ortools and \
           position.down_right in self._island_bridges_ortools:
            b1 = self._island_bridges_ortools[position][Direction.right()]
            b2 = self._island_bridges_ortools[position.down][Direction.right()]
            b3 = self._island_bridges_ortools[position][Direction.down()]
            b4 = self._island_bridges_ortools[position.right][Direction.down()]
            self._model.add_bool_or([b1.negated(), b2.negated(), b3.negated(), b4.negated()])

        # Note: on ne fait que up_right et down_right pour chaque position, 
        # car les autres carrés seront couverts par d'autres positions (leurs coins respectifs).
