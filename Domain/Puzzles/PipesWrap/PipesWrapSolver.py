from Domain.Direction import Direction
from Domain.Grid.GridBase import GridBase
from Domain.Grid.WrappedGrid import WrappedGrid
from Domain.Grid.WrappedPipesGrid import WrappedPipesGrid
from Domain.Position import Position
from Pipes.Pipe import Pipe
from Pipes.PipeShapeTransition import PipeShapeTransition
from Pipes.PipesSolver import PipesSolver
from Ports.SolverEngine import SolverEngine

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
                self._create_pipe_from_model(model, Position(r, c))
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
                connected_to = current_grid[position].get_connected_to()
                constraints.append(self._grid_z3[position][Direction.up()] == (Direction.up() in connected_to))
                constraints.append(self._grid_z3[position][Direction.down()] == (Direction.down() in connected_to))
                constraints.append(self._grid_z3[position][Direction.left()] == (Direction.left() in connected_to))
                constraints.append(self._grid_z3[position][Direction.right()] == (Direction.right() in connected_to))
            self._solver.add(self._solver.Not(self._solver.And(constraints)))

        return WrappedGrid.empty(), proposition_count

    def _add_edges_constraints(self, position):
        pass  # no edges constraints in PipesWrap

    def _add_connected_constraints(self):
        for position, value in self._grid_z3:
            position_up = self._grid_z3.neighbor_up(position)
            position_down = self._grid_z3.neighbor_down(position)
            position_left = self._grid_z3.neighbor_left(position)
            position_right = self._grid_z3.neighbor_right(position)
            self._solver.add(self._grid_z3[position][Direction.up()] == self._grid_z3[position_up][Direction.down()])
            self._solver.add(self._grid_z3[position][Direction.down()] == self._grid_z3[position_down][Direction.up()])
            self._solver.add(self._grid_z3[position][Direction.left()] == self._grid_z3[position_left][Direction.right()])
            self._solver.add(self._grid_z3[position][Direction.right()] == self._grid_z3[position_right][Direction.left()])
