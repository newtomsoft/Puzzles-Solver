from PuzzleSolver.Board.Direction import Direction
from PuzzleSolver.Board.IslandsGrid import IslandGrid
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer

class GridPuzzleMirukutiTeasePlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    game_name = "mirukuti-tease"

    async def play(self, solution: IslandGrid):
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        for biscuit_info in getattr(solution, 'biscuits', []):
            junction = biscuit_info['junction']
            for end_pos in [biscuit_info['stem_end'], biscuit_info['bar_end1'], biscuit_info['bar_end2']]:
                if end_pos == junction: continue
                
                direction = junction.direction_to(end_pos)
                if direction != Direction.none():
                    dist = abs(junction.r - end_pos.r) + abs(junction.c - end_pos.c)
                    curr = junction
                    for _ in range(dist):
                        await self._trace_direction_from_position(curr, direction, page, cell_width, cell_height, x0, y0)
                        curr = curr.after(direction)

        await self.close()
        await self._process_video(video, rectangle)
