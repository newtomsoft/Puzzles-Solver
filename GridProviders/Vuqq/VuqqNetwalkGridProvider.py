from playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.Pipe import Pipe
from Domain.Board.PipesGrid import PipesGrid
from Domain.Board.Position import Position
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class VuqqNetwalkGridProvider(PlaywrightGridProvider):
    async def get_grid(self, url: str) -> PipesGrid:
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url: str) -> PipesGrid:
        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = await browser.new_page()

        await page.goto(url)
        # await page.wait_for_load_state('networkidle') # Flaky
        await page.wait_for_selector('.grid')
        await page.wait_for_selector('.grid__cell')

        # Locate the grid cells
        cells = await page.locator('.grid__cell').all()

        # Determine grid size (assuming square grid for now based on Vuqq's "size" param)
        # But we can infer it from the number of cells
        total_cells = len(cells)
        size = int(total_cells**0.5)

        # Double check if it's square
        if size * size != total_cells:
            # Fallback to counting based on CSS grid style if possible, or assume square
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

            # Parse Rotation
            rotation = 0
            if style_attr and 'rotate:' in style_attr:
                # style="rotate: 90deg;"
                try:
                    # Extract number between 'rotate:' and 'deg'
                    part = style_attr.split('rotate:')[1].split('deg')[0].strip()
                    rotation = int(part)
                except (IndexError, ValueError):
                    rotation = 0

            # Normalize rotation (0, 90, 180, 270)
            rotation = rotation % 360

            # Parse Shape and Get Base Connections (at 0 deg)
            classes = class_attr.split()
            base_connections = set()

            if 'line' in classes and 'halfline' not in classes: # Straight (I)
                # Base I (line): 0deg is Horizontal (Left-Right) based on CSS analysis
                # Wait, my CSS analysis said:
                # .path.line::after top 40% bottom 40% left 0 right 0 -> Horizontal
                # So 0 deg = Left, Right
                base_connections = {Direction.left(), Direction.right()}
            elif 'corner' in classes: # Elbow (L)
                # Base L (corner): 0deg is Up-Left based on CSS analysis
                # .path.corner::after (left arm), ::before (up arm)
                base_connections = {Direction.up(), Direction.left()}
            elif 'bead' in classes: # Tee (T) or some 3-way
                # Base T (bead): 0deg is Up-Left-Right based on CSS analysis
                # .path.bead::after (horizontal bar), ::before (up bar)
                base_connections = {Direction.up(), Direction.left(), Direction.right()}
            elif 'halfline' in classes: # End (E)
                # Base E (halfline): 0deg is Left based on CSS analysis
                # .path.halfline::after (left arm)
                base_connections = {Direction.left()}
            else:
                # Unknown shape, default to empty or maybe Cross?
                # Vuqq Netwalk standard usually doesn't have cross, but if it did...
                # Let's assume empty/none if unknown, or raise error.
                # But for robustness, let's log or assume isolated?
                pass

            # Apply Rotation
            # Clockwise rotation: Up->Right->Down->Left->Up

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
