from Domain.Board.Grid import Grid
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleTraceNumbersPlayer(PlaywrightPlayer):
    game_name = "trace_numbers"

    async def play(self, solution: Grid):
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        # Find all paths
        paths_number = max(solution[r][c] for r in range(solution.rows_number) for c in range(solution.columns_number)) + 1

        for path_idx in range(paths_number):
            path_cells = [(r, c) for r in range(solution.rows_number) for c in range(solution.columns_number) if solution[r][c] == path_idx]

            # Find start (endpoint with degree 1)
            start = None
            for r, c in path_cells:
                degree = sum(1 for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                             if 0 <= r + dr < solution.rows_number and 0 <= c + dc < solution.columns_number
                             and solution[r + dr][c + dc] == path_idx)
                if degree == 1:
                    start = (r, c)
                    break

            if start is None:
                continue

            # Trace path
            await page.mouse.move(x0 + cell_width / 2 + start[1] * cell_width, y0 + cell_height / 2 + start[0] * cell_height)
            await page.mouse.down()

            current = start
            prev = None
            while True:
                r, c = current
                neighbors = [(r + dr, c + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                             if 0 <= r + dr < solution.rows_number and 0 <= c + dc < solution.columns_number
                             and solution[r + dr][c + dc] == path_idx and (r + dr, c + dc) != prev]
                if not neighbors:
                    break
                prev = current
                current = neighbors[0]
                await page.mouse.move(x0 + cell_width / 2 + current[1] * cell_width, y0 + cell_height / 2 + current[0] * cell_height)

            await page.mouse.up()

        await self.close()
        await self._process_video(video, rectangle)
