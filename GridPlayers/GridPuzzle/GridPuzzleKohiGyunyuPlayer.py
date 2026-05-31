from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer

class GridPuzzleKohiGyunyuPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    game_name = "kohi-gyunyu"

    async def play(self, solution: IslandGrid):
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        groups = getattr(solution, 'groups', {})
        for g_idx in sorted(groups.keys()):
            group = groups[g_idx]
            
            for p1, p2 in group['gray_connections']:
                await self._draw_connection(p1, p2, page, cell_width, cell_height, x0, y0)

            for p1, p2 in group['other_connections']:
                await self._draw_connection(p1, p2, page, cell_width, cell_height, x0, y0)

        await self.close()
        await self._process_video(video, rectangle)

    async def _draw_connection(self, p1, p2, page, cell_width, cell_height, x0, y0):
        direction = p1.direction_to(p2)
        if direction != Direction.none():
            dist = abs(p1.r - p2.r) + abs(p1.c - p2.c)
            curr = p1
            for _ in range(dist):
                await self._trace_direction_from_position(curr, direction, page, cell_width, cell_height, x0, y0)
                curr = curr.after(direction)
