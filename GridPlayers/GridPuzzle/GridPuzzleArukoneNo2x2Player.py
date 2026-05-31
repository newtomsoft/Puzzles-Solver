import asyncio

from PuzzleSolver.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer


class GridPuzzleArukoneNo2x2Player(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    game_name = "Arukone-no-2x2"

    async def play(self, solution: Grid):
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        await self._draw_paths(cell_height, cell_width, page, solution, x0, y0)

        await self.close()
        await self._process_video(video, rectangle)

    async def _draw_paths(self, cell_height, cell_width, page, solution, x0, y0):
        paths = self._find_paths(solution)
        for path in paths:
            if not path:
                continue

            # Move to start position
            start_pos = path[0]
            await page.mouse.move(x0 + cell_width / 2 + start_pos.c * cell_width, y0 + cell_height / 2 + start_pos.r * cell_height)
            await page.mouse.down()

            for i in range(1, len(path)):
                pos = path[i]
                await page.mouse.move(x0 + cell_width / 2 + pos.c * cell_width, y0 + cell_height / 2 + pos.r * cell_height)

            await page.mouse.up()

    def _find_paths(self, solution: Grid) -> list[list]:
        values = set()
        for _, val in solution:
            if val is not None and val >= 0:
                values.add(val)

        paths = []
        for val in values:
            val_positions = [p for p, v in solution if v == val]
            shapes = self._get_shapes_for_value(val_positions)
            for shape in shapes:
                path = self._order_path(list(shape))
                if path:
                    paths.append(path)
        return paths

    def _get_shapes_for_value(self, val_positions: list) -> list[set]:
        shapes = []
        remaining = set(val_positions)
        while remaining:
            pos = remaining.pop()
            current_shape = {pos}
            stack = [pos]
            while stack:
                curr = stack.pop()
                for neighbor in [p for p in val_positions if p in remaining and curr.distance_to(p) == 1]:
                    remaining.remove(neighbor)
                    current_shape.add(neighbor)
                    stack.append(neighbor)
            shapes.append(current_shape)
        return shapes

    def _order_path(self, positions: list) -> list:
        if not positions:
            return []
        
        # On cherche une extrémité (1 voisin du même chemin)
        endpoints = []
        for p in positions:
            neighbors_in_path = [n for n in positions if p.distance_to(n) == 1]
            if len(neighbors_in_path) <= 1:
                endpoints.append(p)
        
        start = endpoints[0] if endpoints else positions[0]
        ordered_path = [start]
        remaining = set(positions)
        remaining.remove(start)
        
        curr = start
        while remaining:
            next_p = next((n for n in remaining if curr.distance_to(n) == 1), None)
            if not next_p:
                break
            ordered_path.append(next_p)
            remaining.remove(next_p)
            curr = next_p
            
        return ordered_path
        
    