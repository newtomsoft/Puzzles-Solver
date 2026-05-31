from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleMirukutiPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    game_name = "mirukuti"

    async def play(self, solution: IslandGrid):
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        # Draw all milk bars first
        for biscuit_info in getattr(solution, 'biscuits', []):
            junction = biscuit_info['junction']
            for milk_pos in biscuit_info['milks']:
                if milk_pos.r == junction.r: # horizontal
                    start = milk_pos if milk_pos.c < junction.c else junction
                    end = junction if milk_pos.c < junction.c else milk_pos
                else: # vertical
                    start = milk_pos if milk_pos.r < junction.r else junction
                    end = junction if milk_pos.r < junction.r else milk_pos
                
                direction = start.direction_to(end)
                if direction != Direction.none():
                    dist = abs(start.r - end.r) + abs(start.c - end.c)
                    curr = start
                    for _ in range(dist):
                        await self._trace_direction_from_position(curr, direction, page, cell_width, cell_height, x0, y0)
                        curr = curr.after(direction)

        # Draw all biscuit stems second
        for biscuit_info in getattr(solution, 'biscuits', []):
            biscuit_pos = biscuit_info['pos']
            junction = biscuit_info['junction']
            direction = biscuit_pos.direction_to(junction)
            if direction != Direction.none():
                dist = abs(biscuit_pos.r - junction.r) + abs(biscuit_pos.c - junction.c)
                curr = biscuit_pos
                for _ in range(dist):
                    await self._trace_direction_from_position(curr, direction, page, cell_width, cell_height, x0, y0)
                    curr = curr.after(direction)

        await self.close()
        await self._process_video(video, rectangle)
