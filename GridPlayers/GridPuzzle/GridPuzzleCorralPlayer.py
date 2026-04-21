from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.GridPuzzle.Base.GridPuzzleRegionBorderPlayer import GridPuzzleRegionBorderPlayer


class GridPuzzleCorralPlayer(GridPuzzleRegionBorderPlayer):
    game_name = "cave"

    async def play(self, solution: Grid) -> PlayStatus:
        self._solution = solution
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        pairs_positions = self._find_unique_different_pairs_positions()
        await self._draw_regions(cell_height, cell_width, page, pairs_positions, x0, y0)

        await self.close()
        await self._process_video(video, rectangle)
        return PlayStatus.SUCCESS

    def _find_unique_different_pairs_positions(self) -> list[tuple[Position, Position]]:
        if self._solution is None:
            return []

        pairs: list[tuple[Position, Position]] = []
        rows_number = self._solution.rows_number
        columns_number = self._solution.columns_number

        for r in range(rows_number):
            for c in range(columns_number):
                position = Position(r, c)
                is_current_zero = self._solution.value(position) == 0

                if c + 1 < columns_number:
                    right = Position(r, c + 1)
                    if is_current_zero != (self._solution.value(right) == 0):
                        pairs.append((position, right))

                if r + 1 < rows_number:
                    down = Position(r + 1, c)
                    if is_current_zero != (self._solution.value(down) == 0):
                        pairs.append((position, down))

        return pairs
