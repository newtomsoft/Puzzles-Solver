import asyncio

from Domain.Board.Direction import Direction
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleThermometersPlayer(PuzzlesMobilePlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        cells = page.locator(".cell:not(.task)")
        cells_all = await cells.all()
        matrix_cells = sorted(
            [cell_div for cell_div in cells_all if 'selectable' in await cell_div.get_attribute('class')],
            key=lambda div: (div, 0)
        )
        
        # We need to sort asynchronously because get_attribute is async
        matrix_cells_with_pos = []
        for cell_div in cells_all:
             if 'selectable' in await cell_div.get_attribute('class'):
                 style = await cell_div.get_attribute('style')
                 top = int(style.split('top:')[1].split('px')[0])
                 left = int(style.split('left:')[1].split('px')[0])
                 matrix_cells_with_pos.append((cell_div, top, left))
        
        matrix_cells_with_pos.sort(key=lambda x: (x[1], x[2]))
        matrix_cells = [x[0] for x in matrix_cells_with_pos]

        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            box = await matrix_cells[index].bounding_box()
            if value == Direction.down():
                await page.mouse.move(box['x'] + box['width'] // 2, box['y'] + box['height'])
                await page.mouse.down()
                await page.mouse.up()
            elif value == Direction.right():
                await page.mouse.move(box['x'] + box['width'], box['y'] + box['height'] // 2)
                await page.mouse.down()
                await page.mouse.up()
        await self.submit_score(page)
        await asyncio.sleep(3)
