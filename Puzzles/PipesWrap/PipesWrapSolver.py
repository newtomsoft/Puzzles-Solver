from Pipes.Pipe import Pipe
from Pipes.PipeShapeTransition import PipeShapeTransition
from Pipes.PipesSolver import PipesSolver
from Ports.SolverEngine import SolverEngine
from Utils.Direction import Direction
from Utils.GridBase import GridBase
from Utils.Position import Position
from Utils.WrappedGrid import WrappedGrid
from Utils.WrappedPipesGrid import WrappedPipesGrid

FALSE = False


class PipesWrapSolver(PipesSolver):
    def __init__(self, grid: GridBase[Pipe], solver_engine: SolverEngine):
        super().__init__(grid, solver_engine)
        self._grid_z3: WrappedGrid | None = None
        self._previous_solution: WrappedGrid[Pipe] | None = None

    def _init_solver(self):
        self._grid_z3 = WrappedGrid([
            [
                {
                    Direction.up(): self._solver.bool(f"{r}_{c}_up"),
                    Direction.left(): self._solver.bool(f"{r}_{c}_left"),
                    Direction.down(): self._solver.bool(f"{r}_{c}_down"),
                    Direction.right(): self._solver.bool(f"{r}_{c}_right"),
                }
                for c in range(self._columns_number)
            ]
            for r in range(self._rows_number)
        ])

        self._add_constraints()

    def get_solution_when_all_pipes_connected(self):
        proposition_count = 0
        while self._solver.has_solution():
            model = self._solver.model()
            proposition_count += 1
            current_grid = WrappedPipesGrid([[
                Pipe.from_connection(
                    up=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)][Direction.up()])),
                    down=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)][Direction.down()])),
                    left=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)][Direction.left()])),
                    right=self._solver.is_true(model.eval(self._grid_z3[Position(r, c)][Direction.right()]))
                )
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

            constraints = []
            for position in connected_positions:
                open_to = current_grid[position].get_open_to()
                constraints.append(self._grid_z3[position][Direction.up()] == open_to[Direction.up()])
                constraints.append(self._grid_z3[position][Direction.down()] == open_to[Direction.down()])
                constraints.append(self._grid_z3[position][Direction.left()] == open_to[Direction.left()])
                constraints.append(self._grid_z3[position][Direction.right()] == open_to[Direction.right()])
            self._solver.add(self._solver.Not(self._solver.And(constraints)))

        return WrappedGrid.empty(), proposition_count

    def _add_edges_constraints(self, position):
        pass  # no edges constraints in PipesWrap

    def _add_connected_constraints(self):
        for position, value in self._grid_z3:
            position_up = self._grid_z3.neighbor_position_up(position)
            position_down = self._grid_z3.neighbor_position_down(position)
            position_left = self._grid_z3.neighbor_position_left(position)
            position_right = self._grid_z3.neighbor_position_right(position)
            self._solver.add(self._grid_z3[position][Direction.up()] == self._grid_z3[position_up][Direction.down()])
            self._solver.add(self._grid_z3[position][Direction.down()] == self._grid_z3[position_down][Direction.up()])
            self._solver.add(self._grid_z3[position][Direction.left()] == self._grid_z3[position_left][Direction.right()])
            self._solver.add(self._grid_z3[position][Direction.right()] == self._grid_z3[position_right][Direction.left()])
