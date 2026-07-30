import asyncio

from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer, Point, Rectangle


class PuzzLinkHerugolfPlayer(PlaywrightPlayer):
    game_name = "herugolf"

    _ARROW_TO_DIR = {
        '↓': (1, 0),   # DOWN
        '→': (0, 1),   # RIGHT
        '↑': (-1, 0),  # UP
        '←': (0, -1),  # LEFT
    }

    @staticmethod
    async def _get_painter_info(page) -> dict:
        return await page.evaluate("""
            () => {
                const painter = ui.puzzle.painter;
                const rect = painter.context.canvas.getBoundingClientRect();
                return {
                    x0: painter.x0,
                    y0: painter.y0,
                    bw: painter.bw,
                    bh: painter.bh,
                    canvasX: rect.x,
                    canvasY: rect.y,
                    canvasW: rect.width,
                    canvasH: rect.height,
                    cols: ui.puzzle.board.cols,
                    rows: ui.puzzle.board.rows,
                };
            }
        """)

    def _cell_center(self, info, r, c):
        bx = c * 2 + 1
        by = r * 2 + 1
        return (
            info['canvasX'] + info['x0'] + bx * info['bw'],
            info['canvasY'] + info['y0'] + by * info['bh'],
        )

    async def play(self, solution) -> PlayStatus:
        page = self.browser.pages[0]
        await page.wait_for_selector("#divques svg", state="visible")
        await page.wait_for_function(
            "typeof ui !== 'undefined' && ui.puzzle && ui.puzzle.board"
        )

        video, viewport_rect = await self._get_data_video_viewport(page)
        video_rect = None

        painter_info = await self._get_painter_info(page)

        if viewport_rect is not None:
            board_left = painter_info['canvasX'] + painter_info['x0']
            board_right = board_left + (painter_info['cols'] * 2 + 1) * painter_info['bw']
            x1 = int(board_left - painter_info['bw'])
            x2 = int(board_right + painter_info['bw'])
            video_rect = Rectangle(Point(x1, viewport_rect.y1), Point(x2, viewport_rect.y2))

        rows = solution.rows_number
        cols = solution.columns_number

        paths = []
        visited = [[False] * cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                v = solution.value(r, c)
                if not isinstance(v, str) or v not in self._ARROW_TO_DIR:
                    continue
                if visited[r][c]:
                    continue
                path_cells = [(r, c)]
                visited[r][c] = True
                cr, cc = r, c
                while True:
                    arrow = solution.value(cr, cc)
                    dr, dc = self._ARROW_TO_DIR[arrow]
                    nr, nc = cr + dr, cc + dc
                    if not (0 <= nr < rows and 0 <= nc < cols):
                        break
                    path_cells.append((nr, nc))
                    visited[nr][nc] = True
                    next_val = solution.value(nr, nc)
                    if isinstance(next_val, str) and next_val in self._ARROW_TO_DIR:
                        cr, cc = nr, nc
                    else:
                        break
                paths.append(path_cells)

        if paths:
            for path_cells in paths:
                coords = [self._cell_center(painter_info, r, c) for r, c in path_cells]
                sx, sy = coords[0]
                await page.mouse.move(sx, sy)
                await page.mouse.down()
                for cx, cy in coords[1:]:
                    await page.mouse.move(cx, cy, steps=5)
                await page.mouse.up()

        await self.close()
        await self._process_video(video, video_rect, 0)
        return PlayStatus.SUCCESS
