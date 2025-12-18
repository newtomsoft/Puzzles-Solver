from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.GridPuzzle.Base.GridPuzzleTagByBlockPlayer import GridPuzzleTagByBlockPlayer


class GridPuzzleTilePaintPlayer(GridPuzzleTagByBlockPlayer):
    game_name = "tile_paint"
    async def play(self, data: tuple[Grid, dict[int, frozenset[Position]]]):
        grid_solution = data[0]
        tiles = data[1]

        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        for position in [next(iter(positions)) for positions in tiles.values()]:
            if grid_solution[position]:
                index = position.r * grid_solution.columns_number + position.c
                await cells[index].click()

        await self.close()
        self._process_video(video, rectangle, 0)
