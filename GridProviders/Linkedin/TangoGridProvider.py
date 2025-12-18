from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class TangoGridProvider(PlaywrightGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        await page.goto(url)
        frame = page.frames[1]
        start_game_button = await frame.wait_for_selector('button:has-text("Commencer une partie")')
        await start_game_button.click()
        board = await frame.wait_for_selector('div.grid-board')
        cells_divs = await board.query_selector_all('div.lotka-cell')
        grid_size = int(len(cells_divs) ** 0.5)
        content = []
        suns = 0
        moons = 0
        for cell_div in cells_divs:
            svg = await cell_div.query_selector('svg')
            value = -1
            if (await svg.get_attribute('aria-label')) in ['Soleil', 'Sara Blakely']:
                value = 1
                suns += 1
            elif (await svg.get_attribute('aria-label')) in ['Lune', 'Talons']:
                value = 0
                moons += 1

            content.append(value)

        if suns + moons == 0:
            raise ValueError("No suns or moons found in the grid")

        matrix = [[content[int(i * grid_size + j)] for j in range(int(grid_size))] for i in range(int(grid_size))]

        comparisons_positions = {
            'equal': [],
            'non_equal': []
        }

        cells_divs_operators = await board.query_selector_all('div.lotka-cell-edge')
        for cell_div_operator in cells_divs_operators:
            if 'lotka-cell-edge--right' in (await cell_div_operator.get_attribute('class')):
                edge_type = 'right'
            elif 'lotka-cell-edge--down' in (await cell_div_operator.get_attribute('class')):
                edge_type = 'down'
            else:
                raise ValueError("Unknown edge type")

            svg = await cell_div_operator.query_selector('svg')
            if (await svg.get_attribute('aria-label')) == 'Égal':
                edge_value = 'equal'
            elif (await svg.get_attribute('aria-label')) == 'Cross':
                edge_value = 'non_equal'
            else:
                raise ValueError("Unknown edge value")
            previous_div = await cell_div_operator.evaluate_handle('node => node.parentElement')
            index = int(await previous_div.get_attribute('data-cell-idx'))
            position = Position(index // grid_size, index % grid_size)
            comparisons_positions[edge_value].append(
                (position, position.right if edge_type == 'right' else position.down)
            )

        return Grid(matrix), comparisons_positions
