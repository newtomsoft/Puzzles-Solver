from Domain.Board.IslandsGrid import IslandGrid
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer

class GridPuzzleSheepAndWolvesPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    game_name = "sheep-and-wolves"

    async def play(self, solution: IslandGrid):
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        await self._draw_loop(cell_height, cell_width, page, solution, x0, y0)

        await self.close()
        await self._process_video(video, rectangle)
