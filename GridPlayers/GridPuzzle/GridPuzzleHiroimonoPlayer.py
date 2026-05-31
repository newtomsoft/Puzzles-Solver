from PuzzleSolver.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
import math


class GridPuzzleHiroimonoPlayer(PlaywrightPlayer):
    game_name = "hiroimono"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        visual_size = int(math.sqrt(len(cells)))

        steps = {}
        for pos, val in solution:
            if val is not None:
                steps[val] = pos

        dom_stones = []
        for i, cell in enumerate(cells):
            if await cell.query_selector(".q_cell"):
                r = i // visual_size
                c = i % visual_size
                dom_stones.append((r, c))
        
        min_r = min(s[0] for s in dom_stones)
        min_c = min(s[1] for s in dom_stones)

        for step_num in sorted(steps.keys()):
            pos = steps[step_num]
            abs_r = pos.r + min_r
            abs_c = pos.c + min_c
            
            index = abs_r * visual_size + abs_c
            if index < len(cells):
                q_cell = await cells[index].query_selector(".q_cell")
                await q_cell.click(force=True)
                await page.keyboard.type(str(step_num))
                
        await self.close()
        await self._process_video(video, rectangle, 0)
