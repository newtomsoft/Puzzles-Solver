from ortools.sat.python import cp_model
from typing import Optional
import re
from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Board.RegionsGrid import RegionsGrid
from PuzzleSolver.Puzzles.GameSolver import GameSolver
from PuzzleSolver.Board.Grid import Grid


class KinKonKanSolver(GameSolver):
    slash = "╱"
    backslash = "╲"
    _SLASH_MAP = {Direction.up(): Direction.right(), Direction.right(): Direction.up(), Direction.down(): Direction.left(), Direction.left(): Direction.down()}
    _BACKSLASH_MAP = {Direction.up(): Direction.left(), Direction.left(): Direction.up(), Direction.down(): Direction.right(), Direction.right(): Direction.down()}

    def __init__(self, regions: RegionsGrid, clues: dict[str, list[str]]):
        self.rows_number = regions.rows_number
        self.columns_number = regions.columns_number
        self.regions_grid = regions
        self.regions = [list(region) for region in regions.get_regions().values()]

        self.clues = self._process_clues(clues)
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._grid_var: Grid = Grid.empty()
        self._previous_solution: Grid = Grid.empty()

    def _build_model(self):
        if not self._grid_var.is_empty():
            return
        self._init_variables()
        self._add_constraints()

    def _init_variables(self):
        self._grid_var = Grid([[self._model.new_int_var(0, 2, f"g_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._is_empty = Grid([[self._model.new_bool_var(f"is_empty_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._is_slash = Grid([[self._model.new_bool_var(f"is_slash_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])
        self._is_backslash = Grid([[self._model.new_bool_var(f"is_backslash_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)])

        for p, var in self._grid_var:
            self._model.add(var == 0).only_enforce_if(self._is_empty[p])
            self._model.add(var != 0).only_enforce_if(self._is_empty[p].negated())
            self._model.add(var == 1).only_enforce_if(self._is_slash[p])
            self._model.add(var != 1).only_enforce_if(self._is_slash[p].negated())
            self._model.add(var == 2).only_enforce_if(self._is_backslash[p])
            self._model.add(var != 2).only_enforce_if(self._is_backslash[p].negated())

            self._model.add(self._is_empty[p] + self._is_slash[p] + self._is_backslash[p] == 1)

    def _add_constraints(self):
        self._add_region_constraints()
        all_has_in, all_p_in = self._add_clue_constraints()
        self._add_mirror_touch_constraints(all_has_in)
        self._add_mutual_exclusion_constraints(all_p_in)
        self._model.add_decision_strategy(
            [self._grid_var[p] for p, _ in self.regions_grid],
            cp_model.CHOOSE_FIRST, cp_model.SELECT_MIN_VALUE)

    def _add_region_constraints(self):
        for region in self.regions:
            mirrors = [self._is_empty[p].negated() for p in region]
            self._model.add(sum(mirrors) == 1)

    def _add_clue_constraints(self) -> tuple[list, list]:
        all_has_in = []
        all_p_in = []
        for path_idx, (label, pairs) in enumerate(self.clues.items()):
            match = re.search(r'\d+', label)
            expected_mirrors = int(match.group()) if match else None
            has_in, p_in = self._add_flow_constraint(path_idx, pairs, expected_mirrors)
            all_has_in.append(has_in)
            all_p_in.append(p_in)
        return all_has_in, all_p_in

    def _add_mutual_exclusion_constraints(self, all_p_in: list):
        for position, _ in self.regions_grid:
            r, c = position.r, position.c
            for d in Direction.orthogonal_directions():
                face_entries = [p_in[r][c][d] for p_in in all_p_in]
                self._model.add(sum(face_entries) <= 1)

    def _add_mirror_touch_constraints(self, all_has_in: list):
        for position, _ in self.regions_grid:
            r, c = position.r, position.c
            touches = [has_in[r][c] for has_in in all_has_in]
            self._model.add_bool_or(touches).only_enforce_if(self._is_empty[position].negated())

    def _add_flow_constraint(self, k: int, pairs: list[tuple[Position, Direction]], expected_count: Optional[int]):
        p_in = [[{d: self._model.new_bool_var(f"p_{k}_{r}_{c}_{d.value}") for d in Direction.orthogonal_directions()} for c in range(self.columns_number)] for r in range(self.rows_number)]
        has_in = [[self._model.new_bool_var(f"h_{k}_{r}_{c}") for c in range(self.columns_number)] for r in range(self.rows_number)]
        order = [[{d: self._model.new_int_var(0, self.rows_number * self.columns_number * 4, f"o_{k}_{r}_{c}_{d.value}") for d in Direction.orthogonal_directions()} for c in range(self.columns_number)] for r in range(self.rows_number)]

        pos1, dir1 = pairs[0]
        pos2, dir2 = pairs[1]
        exit_dir2 = dir2.opposite

        entry_from_outside = {(pos1.r, pos1.c, dir1)}
        exit_to_outside = {(pos2.r, pos2.c, exit_dir2)}

        for position, _ in self.regions_grid:
            r, c = position.r, position.c
            p_in_list = [p_in[r][c][d] for d in Direction.orthogonal_directions()]
            self._model.add_bool_or(p_in_list).only_enforce_if(has_in[r][c])
            self._model.add_bool_and([v.negated() for v in p_in_list]).only_enforce_if(has_in[r][c].negated())


            for d_out in Direction.orthogonal_directions():
                npos = position.after(d_out)
                d_slash_src = self._SLASH_MAP[d_out]
                d_bs_src = self._BACKSLASH_MAP[d_out]

                if npos in self.regions_grid:
                    self._model.add(p_in[npos.r][npos.c][d_out] == p_in[r][c][d_out]).only_enforce_if(self._is_empty[position])
                    self._model.add(p_in[npos.r][npos.c][d_out] == p_in[r][c][d_slash_src]).only_enforce_if(self._is_slash[position])
                    self._model.add(p_in[npos.r][npos.c][d_out] == p_in[r][c][d_bs_src]).only_enforce_if(self._is_backslash[position])

                    self._model.add(order[npos.r][npos.c][d_out] == order[r][c][d_out] + 1).only_enforce_if([p_in[npos.r][npos.c][d_out], self._is_empty[position]])
                    self._model.add(order[npos.r][npos.c][d_out] == order[r][c][d_slash_src] + 1).only_enforce_if([p_in[npos.r][npos.c][d_out], self._is_slash[position]])
                    self._model.add(order[npos.r][npos.c][d_out] == order[r][c][d_bs_src] + 1).only_enforce_if([p_in[npos.r][npos.c][d_out], self._is_backslash[position]])
                else:
                    if (r, c, d_out) in exit_to_outside:
                        pass
                    else:
                        self._model.add(p_in[r][c][d_out] == 0).only_enforce_if(self._is_empty[position])
                        self._model.add(p_in[r][c][d_slash_src] == 0).only_enforce_if(self._is_slash[position])
                        self._model.add(p_in[r][c][d_bs_src] == 0).only_enforce_if(self._is_backslash[position])

            for d_in in Direction.orthogonal_directions():
                prev_pos = position.after(d_in.opposite)
                if prev_pos not in self.regions_grid and (r, c, d_in) not in entry_from_outside:
                    self._model.add(p_in[r][c][d_in] == 0)

        self._model.add(p_in[pos1.r][pos1.c][dir1] == 1)
        self._model.add(order[pos1.r][pos1.c][dir1] == 1)

        exit_in_dir = dir2.opposite
        self._model.add(p_in[pos2.r][pos2.c][exit_in_dir] == 1).only_enforce_if(self._is_empty[Position(pos2.r, pos2.c)])
        self._model.add(p_in[pos2.r][pos2.c][self._SLASH_MAP[exit_in_dir]] == 1).only_enforce_if(self._is_slash[Position(pos2.r, pos2.c)])
        self._model.add(p_in[pos2.r][pos2.c][self._BACKSLASH_MAP[exit_in_dir]] == 1).only_enforce_if(self._is_backslash[Position(pos2.r, pos2.c)])

        if expected_count is not None:
            reflection_vars = []
            for position, _ in self.regions_grid:
                r, c = position.r, position.c
                for d in Direction.orthogonal_directions():
                    reflection = self._model.new_bool_var(f"refl_{k}_{r}_{c}_{d.value}")
                    self._model.add_bool_and([p_in[r][c][d], self._is_empty[position].negated()]).only_enforce_if(reflection)
                    self._model.add_bool_or([p_in[r][c][d].negated(), self._is_empty[position]]).only_enforce_if(reflection.negated())
                    reflection_vars.append(reflection)
            self._model.add(sum(reflection_vars) == expected_count)

        return has_in, p_in

    def _solve(self) -> Grid:
        status = self._solver.solve(self._model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            result = Grid([['.' for _ in range(self.columns_number)] for _ in range(self.rows_number)])
            for position, var in self._grid_var:
                val = self._solver.value(var)
                if val == 1:
                    result[position] = self.slash
                elif val == 2:
                    result[position] = self.backslash
            return result
        return Grid.empty()

    def get_solution(self) -> Grid:
        self._build_model()
        self._previous_solution = self._solve()
        return self._previous_solution

    def get_other_solution(self) -> Grid:
        if self._previous_solution.is_empty():
            return self.get_solution()

        diff_constraints = []
        for position, var in self._grid_var:
            val = self._solver.value(var)
            is_diff = self._model.new_bool_var(f"diff_{position.r}_{position.c}")
            self._model.add(var != val).only_enforce_if(is_diff)
            self._model.add(var == val).only_enforce_if(is_diff.negated())
            diff_constraints.append(is_diff)

        self._model.add_bool_or(diff_constraints)
        self._previous_solution = self._solve()
        return self._previous_solution

    def _process_clues(self, raw_clues: dict[str, list[str]]) -> dict[str, list[tuple[Position, Direction]]]:
        clue_index_map = {}

        if 'top' in raw_clues:
            for c, text in enumerate(raw_clues['top']):
                self._parse_clue(text, Position(0, c), Direction.down(), clue_index_map)
        if 'bottom' in raw_clues:
            for c, text in enumerate(raw_clues['bottom']):
                self._parse_clue(text, Position(self.rows_number - 1, c), Direction.up(), clue_index_map)
        if 'left' in raw_clues:
            for r, text in enumerate(raw_clues['left']):
                self._parse_clue(text, Position(r, 0), Direction.right(), clue_index_map)
        if 'right' in raw_clues:
            for r, text in enumerate(raw_clues['right']):
                self._parse_clue(text, Position(r, self.columns_number - 1), Direction.left(), clue_index_map)

        clues = {}
        for clue_key, data in clue_index_map.items():
            if len(data['pairs']) == 2:
                label = data['letter']
                if data['number'] is not None:
                    label += str(data['number'])
                clues[label] = data['pairs']

        return clues

    @staticmethod
    def _parse_clue(text, pos, entry_dir, temp):
        if not text:
            return
        match_letter = re.search(r'([A-Za-z]+)', text)
        match_num = re.search(r'(\d+)', text)

        letter = match_letter.group(1) if match_letter else text
        number = int(match_num.group(1)) if match_num else None

        clue_key = f"{letter}_{number}" if number is not None else letter

        if clue_key not in temp:
            temp[clue_key] = {'pairs': [], 'number': number, 'letter': letter}
        temp[clue_key]['pairs'].append((pos, entry_dir))
