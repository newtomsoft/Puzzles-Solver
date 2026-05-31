from PuzzleSolver.Board.Grid import Grid
from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleNorinoriPlayer(PlaywrightPlayer):
    game_name = "norinori"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        
        black_positions = [p for p, v in solution if v]
        played = set()
        
        for pos in black_positions:
            if pos in played:
                continue

            # Norinori rules: black cells always form dominoes (2x1 or 1x2)
            # Find its neighbor in the solution
            neighbors = [n for n in solution.neighbors_positions(pos) if solution[n]]
            if neighbors:
                neighbor = neighbors[0]
                
                # Click both cells of the domino
                for p in [pos, neighbor]:
                    index = p.r * solution.columns_number + p.c
                    await cells[index].click()
                    played.add(p)

        await self.close()
        await self._process_video(video, rectangle, 0)
        return PlayStatus.SUCCESS
