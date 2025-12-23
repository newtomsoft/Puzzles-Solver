from playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Pipe import Pipe
from Domain.Board.PipesGrid import PipesGrid
from GridProviders.Vuqq.Base.VuqqGridProvider import VuqqGridProvider


class VuqqNetwalkGridProvider(VuqqGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url: str) -> PipesGrid:
        page = await self.open_page(browser, url, ".grid__cell")

        await page.wait_for_selector('.grid')
        await page.wait_for_selector('.grid__cell')

        cells = await page.locator('.grid__cell').all()

        total_cells = len(cells)
        size = int(total_cells**0.5)

        if size * size != total_cells:
            raise ValueError(f"Grid is not square: {total_cells} cells found.")

        rows_number = size
        columns_number = size

        matrix = [[None for _ in range(columns_number)] for _ in range(rows_number)]

        for idx, cell in enumerate(cells):
            r = idx // columns_number
            c = idx % columns_number

            path_el = cell.locator('.path')
            class_attr = await path_el.get_attribute('class')
            style_attr = await path_el.get_attribute('style')

            rotation = 0
            if style_attr and 'rotate:' in style_attr:
                try:
                    part = style_attr.split('rotate:')[1].split('deg')[0].strip()
                    rotation = int(part)
                except (IndexError, ValueError):
                    rotation = 0

            rotation = rotation % 360

            classes = class_attr.split()
            base_connections = set()

            if 'line' in classes and 'halfline' not in classes: # Straight (I)
                base_connections = {Direction.left(), Direction.right()}
            elif 'corner' in classes: # Elbow (L)
                base_connections = {Direction.up(), Direction.left()}
            elif 'bead' in classes: # Tee (T) or some 3-way
                base_connections = {Direction.up(), Direction.left(), Direction.right()}
            elif 'halfline' in classes: # End (E)
                base_connections = {Direction.left()}
            else:
                pass

            final_connections = set()
            steps = rotation // 90

            for d in base_connections:
                new_d = d
                for _ in range(steps):
                    new_d = self._rotate_direction_cw(new_d)
                final_connections.add(new_d)

            matrix[r][c] = Pipe.from_connection(frozenset(final_connections))

        return PipesGrid(matrix)

    def _rotate_direction_cw(self, direction: Direction) -> Direction:
        if direction == Direction.up():
            return Direction.right()
        if direction == Direction.right():
            return Direction.down()
        if direction == Direction.down():
            return Direction.left()
        if direction == Direction.left():
            return Direction.up()
        return direction
