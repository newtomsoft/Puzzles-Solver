import asyncio
import logging
from urllib.parse import parse_qs, urlparse

from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class HidokuGridProvider(PlaywrightGridProvider):
    def __init__(self):
        super().__init__()

    async def scrap_grid(self, browser: BrowserContext, url: str) -> Grid:
        page = await browser.new_page()

        await page.add_init_script("""
            window.canvas_logs = [];
            const originalFillText = CanvasRenderingContext2D.prototype.fillText;
            CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
                window.canvas_logs.push({type: 'fillText', text: text, x: x, y: y, style: this.fillStyle, font: this.font});
                return originalFillText.apply(this, arguments);
            };

            const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
            CanvasRenderingContext2D.prototype.strokeText = function(text, x, y, maxWidth) {
                window.canvas_logs.push({type: 'strokeText', text: text, x: x, y: y, style: this.strokeStyle, font: this.font});
                return originalStrokeText.apply(this, arguments);
            };
        """)

        await page.goto(url)

        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        difficulty_param = query_params.get('d', query_params.get('difficulty', ['Easy']))[0]

        difficulty_map = {
            'easy': ('Easy', 5),
            'medium': ('Medium', 6),
            'hard': ('Hard', 7),
            'extreme': ('Extreme', 8),
            'extrême': ('Extreme', 8)
        }

        target_diff_key = difficulty_param.lower()
        if target_diff_key not in difficulty_map:
            logging.warning(f"Unknown difficulty '{difficulty_param}', defaulting to Easy.")
            target_diff_key = 'easy'

        diff_label, grid_size = difficulty_map[target_diff_key]

        try:
            start_button = page.locator("button:has-text('Let\\'s Go!'), button:has-text('C\\'est parti')").first
            await start_button.wait_for(timeout=2000)
            await start_button.click()
        except Exception:
            logging.debug("Start button not found or already clicked.")

        try:
            if diff_label == 'Extreme':
                diff_button = page.locator("text=Extreme").or_(page.locator("text=Extrême")).first
            else:
                diff_button = page.locator(f"text={diff_label}").first

            await diff_button.wait_for(timeout=10000)
            await diff_button.click()
        except Exception as e:
            logging.error(f"Could not find difficulty button for '{diff_label}': {e}")
            raise

        await page.wait_for_function("window.canvas_logs.length > 10", timeout=10000)

        await asyncio.sleep(2)

        logs = await page.evaluate("window.canvas_logs")

        return self._parse_logs_to_grid(logs, grid_size, grid_size)

    @staticmethod
    def _parse_logs_to_grid(logs: list, rows: int, cols: int) -> Grid:
        text_events = [l for l in logs if l['type'] in ('fillText', 'strokeText')]

        canvas_width = 351.0
        canvas_height = 351.0

        stride_x = canvas_width / cols
        stride_y = canvas_height / rows

        start_x = stride_x / 2
        start_y = stride_y / 2

        def map_coord(val, start, stride):
            return int(round((val - start) / stride))

        matrix = [[None for _ in range(cols)] for _ in range(rows)]
        grid = Grid(matrix)


        for event in text_events:
            text = event['text']
            x = float(event['x'])
            y = float(event['y'])

            if not text.isdigit():
                continue

            c = map_coord(x, start_x, stride_x)
            r = map_coord(y, start_y, stride_y)

            if 0 <= r < rows and 0 <= c < cols:
                grid[r, c] = int(text)

        return grid
