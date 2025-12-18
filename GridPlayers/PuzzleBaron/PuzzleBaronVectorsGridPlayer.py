import asyncio

from Domain.Board.Direction import Direction
from Domain.Board.Position import Position
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class PuzzleBaronVectorsPlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        grid_box_divs = await page.query_selector_all('div.gridbox')
        numbers = []
        for number_div in grid_box_divs:
            inner_text = await number_div.inner_text()
            numbers.append(int(inner_text) if inner_text else 0)

        for start_position, value in solution:
            if numbers[solution.get_index_from_position(start_position)] == 0:
                continue
            for direction in Direction.orthogonal_directions():
                end_position = Position(start_position.r, start_position.c)
                while end_position in solution and solution[end_position] == value:
                    end_position = end_position.after(direction)
                end_position = end_position.before(direction)
                if end_position != start_position:
                    await self.drag_n_drop(page.mouse, solution, start_position, end_position, grid_box_divs)

        await asyncio.sleep(6)
