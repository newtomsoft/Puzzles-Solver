from Domain.Board.Direction import Direction
from Domain.Board.Pipe import Pipe
from Domain.Board.PipesGrid import PipesGrid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class VuqqNetwalkPlayer(PlaywrightPlayer):
    async def play(self, solution: PipesGrid):
        # Access the page from the browser context
        if len(self.browser.pages) > 0:
            page = self.browser.pages[0]
        else:
            # Should not happen if provider ran first, but safe fallback or raise
            raise Exception("No pages found in browser context")

        await self._play(page, solution)

    async def _play(self, page, solution: PipesGrid):
        # Locate the grid cells
        cells = await page.locator('.grid .grid__cell').all()

        columns_number = solution.columns_number

        for idx, cell in enumerate(cells):
            r = idx // columns_number
            c = idx % columns_number

            target_pipe: Pipe = solution[r][c]
            target_connections = target_pipe.get_connected_to()

            # Get current state from DOM
            path_el = cell.locator('.path')
            class_attr = await path_el.get_attribute('class')
            style_attr = await path_el.get_attribute('style')

            # Parse Rotation
            current_rotation = 0
            if style_attr and 'rotate:' in style_attr:
                try:
                    part = style_attr.split('rotate:')[1].split('deg')[0].strip()
                    current_rotation = int(part)
                except (IndexError, ValueError):
                    current_rotation = 0

            current_rotation = current_rotation % 360

            # Determine base connections
            classes = class_attr.split()
            base_connections = set()

            if 'line' in classes and 'halfline' not in classes:
                base_connections = {Direction.left(), Direction.right()}
            elif 'corner' in classes:
                base_connections = {Direction.up(), Direction.left()}
            elif 'bead' in classes:
                base_connections = {Direction.up(), Direction.left(), Direction.right()}
            elif 'halfline' in classes:
                base_connections = {Direction.left()}

            # Simulate rotations to find match
            clicks_needed = 0
            found = False

            for i in range(4):
                # Rotate base connections by (current_rotation/90 + i) steps
                rotation_steps = (current_rotation // 90 + i) % 4

                rotated_connections = set()
                for d in base_connections:
                    new_d = d
                    for _ in range(rotation_steps):
                        new_d = self._rotate_direction_cw(new_d)
                    rotated_connections.add(new_d)

                if rotated_connections == target_connections:
                    clicks_needed = i
                    found = True
                    break

            if found and clicks_needed > 0:
                for _ in range(clicks_needed):
                    await cell.click()
                    # Wait slightly to ensure UI updates or at least event is registered
                    await page.wait_for_timeout(50)
            elif not found:
                 print(f"Warning: Could not find rotation for cell {r},{c} to match target {target_connections} with base {base_connections}")

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
