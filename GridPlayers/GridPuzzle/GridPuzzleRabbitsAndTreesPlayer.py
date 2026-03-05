from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from Domain.Puzzles.RabbitsAndTrees.RabbitsAndTreesSolver import RabbitsAndTreesSolver


class GridPuzzleRabbitsAndTreesPlayer(PlaywrightPlayer):
    game_name = "rabbits-and-trees"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")

        for position, value in solution:
            if value == RabbitsAndTreesSolver.NOTHING:
                continue

            # Sur gridpuzzle.com pour Rabbits and Trees:
            # 2 clics -> Lapin (1)
            # 3 clics -> Arbre (2)
            
            index = position.r * solution.columns_number + position.c
            
            num_clicks = 0
            if value == RabbitsAndTreesSolver.RABBIT:
                num_clicks = 2
            elif value == RabbitsAndTreesSolver.TREE:
                num_clicks = 3
            
            for _ in range(num_clicks):
                await cells[index].click()

        await self.close()
        await self._process_video(video, rectangle)
