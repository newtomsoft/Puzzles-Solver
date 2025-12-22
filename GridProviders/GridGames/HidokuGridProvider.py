import asyncio
import logging
from urllib.parse import parse_qs, urlparse

from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class HidokuGridProvider(PlaywrightGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url: str) -> Grid:
        page = browser.pages[0]

        await page.add_init_script("""
            window.canvas_logs = [];
            const proto = CanvasRenderingContext2D.prototype;

            const originalFillText = proto.fillText;
            proto.fillText = function(text, x, y, maxWidth) {
                window.canvas_logs.push({type: 'fillText', text: String(text), x: x, y: y, style: this.fillStyle, font: this.font});
                return originalFillText.call(this, text, x, y, maxWidth);
            };

            const originalStrokeText = proto.strokeText;
            proto.strokeText = function(text, x, y, maxWidth) {
                window.canvas_logs.push({type: 'strokeText', text: String(text), x: x, y: y, style: this.strokeStyle, font: this.font});
                return originalStrokeText.call(this, text, x, y, maxWidth);
            };
        """)

        await page.goto(url)
        try:
            await page.wait_for_selector("div#snigel-cmp-framework", timeout=5000)
            await page.evaluate("""
                () => {
                    const banner = document.getElementById('snigel-cmp-framework');
                    if (banner) {
                        banner.remove();
                    }
                }
            """)
            await asyncio.sleep(1)
        except Exception:
            logging.debug("Cookie banner not found or interaction failed.")


        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        difficulty_param = query_params.get('d', query_params.get('difficulty', ['easy']))[0]

        difficulty_map = {
            'easy': ('Easy', 5),
            'medium': ('Medium', 6),
            'hard': ('Hard', 7),
            'extreme': ('Extreme', 8),
        }

        target_diff_key = difficulty_param.lower()
        if target_diff_key not in difficulty_map:
            logging.warning(f"Unknown difficulty '{difficulty_param}', defaulting to Easy.")
            target_diff_key = 'easy'

        diff_label, grid_size = difficulty_map[target_diff_key]

        start_button = page.locator("button:has-text('Let\\'s Go!'), button:has-text('C\\'est parti')").first
        if await start_button.is_visible():
            await start_button.click()

        row_locator = page.locator(f"div[class*='_gameRow_']:has-text('{diff_label}')")
        diff_button = row_locator.locator("div[class*='_playButton_']").first

        if await diff_button.is_visible():
             await diff_button.click()
        else:
             logging.warning(f"Could not find specific play button for {diff_label}, trying text click.")
             await page.get_by_text(diff_label, exact=True).first.click()

        await page.wait_for_function("window.canvas_logs.length > 10", timeout=3000)

        logs = await page.evaluate("window.canvas_logs")

        return self._parse_logs_to_grid(logs, grid_size, grid_size)

    @staticmethod
    def _parse_logs_to_grid(logs: list, rows: int, cols: int) -> Grid:
        text_events = [log for log in logs if log['type'] in ('fillText', 'strokeText')]

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
