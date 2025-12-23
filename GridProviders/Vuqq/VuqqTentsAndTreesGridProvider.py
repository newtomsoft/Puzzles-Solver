import asyncio
import json

from Domain.Board.Grid import Grid
from Domain.Puzzles.Tents.TentsSolver import TentsSolver
from GridProviders.Vuqq.Base.VuqqGridProvider import VuqqGridProvider


class VuqqTentsAndTreesGridProvider(VuqqGridProvider):
    async def scrap_grid(self, browser, url):
        page = await self.open_page(browser, url, "canvas")

        logs = None
        for _ in range(40):
            js_check = """
                (() => {
                    if (!window.vuqq_frames) return null;
                    for (let i = window.vuqq_frames.length - 1; i >= 0; i--) {
                        if (window.vuqq_frames[i].length > 10) {
                            return window.vuqq_frames[i];
                        }
                    }
                    return null;
                })()
            """
            logs = await page.evaluate(js_check)
            if logs:
                break
            await asyncio.sleep(0.5)

        if not logs:
            raise Exception("No populated frame captured from drawing.js")

        await page.evaluate("logs => window.vuqq_logs = logs", logs)

        canvas_metrics = await page.evaluate("""
            (() => {
                const canvas = document.querySelector('canvas');
                const rect = canvas.getBoundingClientRect();
                return {
                    internal_width: canvas.width,
                    internal_height: canvas.height,
                    client_left: rect.left,
                    client_top: rect.top,
                    client_width: rect.width,
                    client_height: rect.height
                };
            })()
        """)

        grid, tents_numbers, raw_coords = self._parse_grid(logs)

        scale_x = canvas_metrics['client_width'] / canvas_metrics['internal_width']
        scale_y = canvas_metrics['client_height'] / canvas_metrics['internal_height']
        offset_x = canvas_metrics['client_left']
        offset_y = canvas_metrics['client_top']

        screen_col_xs = [x * scale_x + offset_x for x in raw_coords['col_xs']]
        screen_row_ys = [y * scale_y + offset_y for y in raw_coords['row_ys']]

        meta = {
            'col_xs': screen_col_xs,
            'row_ys': screen_row_ys,
            'trees': raw_coords['trees']
        }
        await page.evaluate(f"window.vuqq_meta = {json.dumps(meta)}")

        return grid, tents_numbers

    @staticmethod
    def _parse_grid(logs):
        texts = [log for log in logs if log["type"] == "text"]
        rects = [log for log in logs if log["type"] == "rect"]

        xs = [t["x"] for t in texts]
        ys = [t["y"] for t in texts]

        if not xs or not ys:
            raise Exception("No clues found in logs")

        max_x = max(xs)
        max_y = max(ys)

        row_clues = sorted([t for t in texts if abs(t["x"] - max_x) < 5], key=lambda t: t["y"])
        col_clues = sorted([t for t in texts if abs(t["y"] - max_y) < 5], key=lambda t: t["x"])

        rows = len(row_clues)
        cols = len(col_clues)

        matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        
        tents_numbers_by_column_row = {
            'row': [int(t["text"]) for t in row_clues],
            'column': [int(t["text"]) for t in col_clues]
        }

        row_ys = [t["y"] for t in row_clues]
        col_xs = [t["x"] for t in col_clues]

        trunks = [r for r in rects if r.get("colour") == 3]
        trees = []

        for trunk in trunks:
            tx, ty = trunk["x"], trunk["y"]
            trunk_cx = tx + trunk["w"] / 2
            trunk_cy = ty + trunk["h"] / 2

            c = min(range(cols), key=lambda i: abs(col_xs[i] - trunk_cx))
            r = min(range(rows), key=lambda i: abs(row_ys[i] - trunk_cy))

            matrix[r][c] = TentsSolver.tree_value
            trees.append((r, c))
            
        grid = Grid(matrix)
        
        raw_coords = {
            'col_xs': col_xs,
            'row_ys': row_ys,
            'trees': trees
        }

        return grid, tents_numbers_by_column_row, raw_coords
