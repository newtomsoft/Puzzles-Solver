from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer, Point, Rectangle


class PuzzLinkRomaPlayer(PlaywrightPlayer):
    game_name = "roma"

    _DIR_TO_DELTA = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1),
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
        await page.wait_for_selector("#divques svg", state="visible", timeout=30000)
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

        for r in range(rows):
            for c in range(cols):
                value = solution.value(r, c)
                if not isinstance(value, str) or value not in self._DIR_TO_DELTA:
                    continue

                dr, dc = self._DIR_TO_DELTA[value]
                nr, nc = r + dr, c + dc

                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue

                start = self._cell_center(painter_info, r, c)
                end = self._cell_center(painter_info, nr, nc)

                await page.mouse.move(start[0], start[1])
                await page.mouse.down()
                await page.mouse.move(end[0], end[1], steps=5)
                await page.mouse.up()

        await self.close()
        await self._process_video(video, video_rect, 0)
        return PlayStatus.SUCCESS
