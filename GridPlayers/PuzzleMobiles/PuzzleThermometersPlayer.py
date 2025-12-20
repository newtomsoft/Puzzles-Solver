import asyncio

from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleThermometersPlayer(PuzzlesMobilePlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        sorted_cells = await self._get_cells_sorted_by_position(page)

        for position in (position for position, value in solution if value):
            index = position.r * solution.columns_number + position.c
            await sorted_cells[index].click()

        await self.submit_score(page)
        await asyncio.sleep(3)

    @staticmethod
    async def _get_cells_sorted_by_position(page):
        all_cells = await page.query_selector_all(".cell.selectable:not(.task)")
        styles = await asyncio.gather(*[cell.get_attribute('style') for cell in all_cells])

        cells_with_pos = []
        for i, style in enumerate(styles):
            top = int(style.split('top:')[1].split('px')[0])
            left = int(style.split('left:')[1].split('px')[0])
            cells_with_pos.append((all_cells[i], top, left))

        cells_with_pos.sort(key=lambda x: (x[1], x[2]))
        return [cell for cell, _, _ in cells_with_pos]
