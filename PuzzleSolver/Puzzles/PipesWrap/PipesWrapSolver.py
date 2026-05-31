from ortools.sat.python import cp_model

from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.GridBase import GridBase
from PuzzleSolver.Board.Pipe import Pipe
from PuzzleSolver.Board.Position import Position
from PuzzleSolver.Board.WrappedGrid import WrappedGrid
from PuzzleSolver.Board.WrappedPipesGrid import WrappedPipesGrid
from PuzzleSolver.Board.PipeShapeTransition import PipeShapeTransition
from PuzzleSolver.Puzzles.Pipes.PipesSolver import PipesSolver


class PipesWrapSolver(PipesSolver):
    def __init__(self, grid: GridBase[Pipe]):
        super().__init__(grid)
        self._grid_vars: WrappedGrid | None = None
        self._previous_solution: WrappedGrid[Pipe] | None = None

    def _init_solver(self):
        self._grid_vars = WrappedGrid([
            [
                {
                    Direction.up(): self._model.new_bool_var(f"{r}_{c}_up"),
                    Direction.left(): self._model.new_bool_var(f"{r}_{c}_left"),
                    Direction.down(): self._model.new_bool_var(f"{r}_{c}_down"),
                    Direction.right(): self._model.new_bool_var(f"{r}_{c}_right"),
                }
                for c in range(self._columns_number)
            ]
            for r in range(self._rows_number)
        ])

        self._add_constraints()

    def get_solution_when_all_pipes_connected(self):
        proposition_count = 0
        status = self._solver.solve(self._model)

        while status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            proposition_count += 1
            current_grid = WrappedPipesGrid([[
                self._create_pipe_from_model(Position(r, c))
                for c in range(self._columns_number)]
                for r in range(self._rows_number)])

            connected_positions, is_loop = current_grid.get_connected_positions_and_is_loop()
            if len(connected_positions) == 1 and not is_loop:
                self._previous_solution = current_grid
                transition_grid = WrappedGrid([[
                    PipeShapeTransition(self._input_grid[Position(r, c)], current_grid[Position(r, c)])
                    for c in range(self._columns_number)]
                    for r in range(self._rows_number)])
                return transition_grid, proposition_count

            if len(connected_positions) > 1:
                max_connected_positions = max(connected_positions, key=len)
                connected_positions = [position for positions in connected_positions if positions != max_connected_positions for position in positions]

            exclusion_literals = []
            for position in connected_positions:
                connected_to = current_grid[position].get_connected_to()
                for direction, is_connected in [
                    (Direction.up(), Direction.up() in connected_to),
                    (Direction.down(), Direction.down() in connected_to),
                    (Direction.left(), Direction.left() in connected_to),
                    (Direction.right(), Direction.right() in connected_to)
                ]:
                    temp_var = self._model.new_bool_var(f"excl_{position}_{direction}")
                    self._model.add(self._grid_vars[position][direction] == is_connected).only_enforce_if(temp_var)
                    self._model.add(self._grid_vars[position][direction] != is_connected).only_enforce_if(temp_var.negated())
                    exclusion_literals.append(temp_var)

            if exclusion_literals:
                self._model.add_bool_or([lit.negated() for lit in exclusion_literals])

            status = self._solver.solve(self._model)

        return WrappedGrid.empty(), proposition_count

    def _add_edges_constraints(self, position):
        pass  # no edges constraints in PipesWrap

    def _add_connected_constraints(self):
        for position, value in self._grid_vars:
            position_up = self._grid_vars.neighbor_up(position)
            position_down = self._grid_vars.neighbor_down(position)
            position_left = self._grid_vars.neighbor_left(position)
            position_right = self._grid_vars.neighbor_right(position)
            self._model.add(self._grid_vars[position][Direction.up()] == self._grid_vars[position_up][Direction.down()])
            self._model.add(self._grid_vars[position][Direction.down()] == self._grid_vars[position_down][Direction.up()])
            self._model.add(self._grid_vars[position][Direction.left()] == self._grid_vars[position_left][Direction.right()])
            self._model.add(self._grid_vars[position][Direction.right()] == self._grid_vars[position_right][Direction.left()])
