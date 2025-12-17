
from Domain.Board.Island import Island
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleCanvasMultiLoopsPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    async def play(self, solution: IslandGrid):
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        await self._draw_multi_loop(cell_height, cell_width, page, solution, x0, y0)

        await self.close()
        self._process_video(video, rectangle)


    async def _draw_multi_loop(self, cell_height, cell_width, page, solution: IslandGrid, x0, y0):
        loops_cells = solution.compute_linear_connected_cells(exclude_without_bridge=False)
        for loop_cells in loops_cells:
            cell_up_left = min(loop_cells, key=lambda cell: (cell.position.r, cell.position.c))
            path_positions = self._path_loop(loop_cells, cell_up_left)
            for index, position in enumerate(path_positions[:-1]):
                next_position = path_positions[index + 1]
                direction = position.direction_to(next_position)
                await self._trace_direction_from_position(position, direction, page, cell_width, cell_height, x0, y0)

    @staticmethod
    def _path_loop(cells: set[Island], start_cell: Island) -> list[Position]:
        cells_by_positions = {cell.position: cell for cell in cells}
        positions = [start_cell.position]
        current_cell = start_cell
        previous_position = None

        while True:
            # Find all connected neighbors that are in the loop
            connected_neighbors = []
            for direction, (neighbor_pos, bridge_count) in current_cell.direction_position_bridges.items():
                if bridge_count > 0 and neighbor_pos in cells_by_positions:
                    connected_neighbors.append((direction, neighbor_pos))

            # Filter out the one we just came from
            valid_moves = []
            for direction, pos in connected_neighbors:
                if previous_position is None or pos != previous_position:
                    valid_moves.append((direction, pos))

            if not valid_moves:
                break

            next_move = None
            if len(valid_moves) == 1:
                next_move = valid_moves[0]
            else:
                # Multiple choices, try to go straight
                if previous_position:
                    arrival_direction = previous_position.direction_to(current_cell.position)
                    # We want to leave in the same direction
                    for direction, pos in valid_moves:
                        if direction == arrival_direction:
                            next_move = (direction, pos)
                            break

                # Fallback if no straight path found or start
                if next_move is None:
                    next_move = valid_moves[0]

            direction, next_pos = next_move

            # Check if we closed the loop
            if next_pos == start_cell.position:
                positions.append(next_pos)
                break

            # Move
            positions.append(next_pos)
            previous_position = current_cell.position
            current_cell = cells_by_positions[next_pos]

        return positions
