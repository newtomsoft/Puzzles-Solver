
import json
from collections import defaultdict

from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class VuqqKakuroGridProvider(PlaywrightGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        if len(browser.pages) > 0:
            page = browser.pages[0]
        else:
            page = await browser.new_page()

        await page.goto(url)
        await page.wait_for_load_state('networkidle')

        # Inject hook to capture fillText and fillRect
        await page.evaluate("""
            (() => {
                window.capturedOps = [];
                const originalFillText = CanvasRenderingContext2D.prototype.fillText;
                const originalFillRect = CanvasRenderingContext2D.prototype.fillRect;

                CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
                    window.capturedOps.push({
                        op: 'text',
                        text: text,
                        x: x,
                        y: y,
                        style: this.fillStyle
                    });
                    return originalFillText.apply(this, arguments);
                };

                CanvasRenderingContext2D.prototype.fillRect = function(x, y, w, h) {
                    window.capturedOps.push({
                        op: 'rect',
                        x: x,
                        y: y,
                        w: w,
                        h: h,
                        style: this.fillStyle
                    });
                    return originalFillRect.apply(this, arguments);
                };
            })();
        """)

        # Trigger a redraw/clean state
        if await page.is_visible('.game-new'):
            await page.click('.game-new')
        elif await page.is_visible('.game-restart'):
            await page.click('.game-restart')

        # Wait for canvas to be redrawn
        await page.wait_for_timeout(1000)

        captured_data = await page.evaluate("window.capturedOps")

        if not captured_data:
            # Try forcing a resize to trigger redraw if no text found
            await page.set_viewport_size({"width": 1000, "height": 1000})
            await page.wait_for_timeout(500)
            captured_data = await page.evaluate("window.capturedOps")

        if not captured_data:
            raise Exception("No drawing operations captured from canvas.")

        # Get canvas screen metrics for coordinate conversion
        canvas_metrics = await page.evaluate("""
            (() => {
                const canvas = document.querySelector('canvas');
                if (!canvas) return null;
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

        if not canvas_metrics:
             raise Exception("Canvas element not found.")

        # Calculate grid cell centers for the player
        grid, unique_xs, unique_ys = self._parse_captured_data(captured_data)

        # Convert internal coordinates to screen coordinates
        scale_x = canvas_metrics['client_width'] / canvas_metrics['internal_width']
        scale_y = canvas_metrics['client_height'] / canvas_metrics['internal_height']
        offset_x = canvas_metrics['client_left']
        offset_y = canvas_metrics['client_top']

        # Calculate center points for clicks
        screen_xs = []
        for i in range(len(unique_xs) - 1):
            center_x = (unique_xs[i] + unique_xs[i+1]) / 2
            screen_xs.append(center_x * scale_x + offset_x)

        screen_ys = []
        for i in range(len(unique_ys) - 1):
            center_y = (unique_ys[i] + unique_ys[i+1]) / 2
            screen_ys.append(center_y * scale_y + offset_y)

        metadata = {'cx': screen_xs, 'cy': screen_ys}

        # Inject metadata for the Player
        await page.evaluate(f"window.vuqq_meta = {json.dumps(metadata)}")

        return grid

    @staticmethod
    def _parse_captured_data(ops):
        # Extract coordinates to determine grid lines
        xs_candidates = []
        ys_candidates = []

        texts = [op for op in ops if op['op'] == 'text']
        rects = [op for op in ops if op['op'] == 'rect']

        # Use rects to define grid primarily, as they represent cells/backgrounds
        for r in rects:
            # We assume rects align with grid lines
            xs_candidates.append(r['x'])
            xs_candidates.append(r['x'] + r['w'])
            ys_candidates.append(r['y'])
            ys_candidates.append(r['y'] + r['h'])

        # Use texts as well (centers or corners?) Text coords are usually baseline/start.
        for t in texts:
            xs_candidates.append(t['x'])
            ys_candidates.append(t['y'])

        if not xs_candidates or not ys_candidates:
            raise Exception("No coordinates found to reconstruct grid.")

        # Cluster coordinates
        def get_clusters(values, tolerance=5):
            values = sorted(values)
            clusters = []
            if not values: return clusters

            current_cluster = [values[0]]
            for v in values[1:]:
                if v - current_cluster[-1] < tolerance:
                    current_cluster.append(v)
                else:
                    clusters.append(sum(current_cluster) / len(current_cluster))
                    current_cluster = [v]
            clusters.append(sum(current_cluster) / len(current_cluster))
            return clusters

        unique_xs = get_clusters(xs_candidates)
        unique_ys = get_clusters(ys_candidates)

        # Filter out clusters that are too close (noise) or try to find a consistent step
        # Assuming a regular grid
        if len(unique_xs) < 2 or len(unique_ys) < 2:
            raise Exception(f"Not enough grid lines found. xs: {len(unique_xs)}, ys: {len(unique_ys)}")

        # Refine clusters: calculate gaps and filter
        # ... logic to find the median gap and rebuild grid lines ...
        # For simplicity, let's assume the clustering worked and we just use them.
        # But we might need to filter boundaries.

        cols_count = len(unique_xs) - 1
        rows_count = len(unique_ys) - 1

        matrix = [[0 for _ in range(cols_count)] for _ in range(rows_count)]

        # Helper to find cell index
        def get_cell_index(x, y, xs, ys):
            c = -1
            r = -1
            for i in range(len(xs) - 1):
                if xs[i] <= x <= xs[i+1] + 1: # +1 tolerance
                    c = i
                    break
            for i in range(len(ys) - 1):
                if ys[i] <= y <= ys[i+1] + 1:
                    r = i
                    break
            return r, c

        # Analyze cells
        # We need to distinguish:
        # 1. White Cell (Empty, no clue) -> 0
        # 2. Black Cell (Empty, no clue) -> [0, 0]
        # 3. Clue Cell -> [h_sum, v_sum]

        # Initialize all as White (0)
        # Then iterate rects to find Black cells

        black_cells = set() # (r, c)

        for r_op in rects:
            # Check color. If it's dark/grey, it's a black cell.
            # Vuqq likely uses specific colors. Let's assume non-white is black.
            style = str(r_op.get('style', '')).lower()
            if 'fff' in style or 'white' in style or style == '#ffffff':
                continue # It's a white cell background or clear

            # Find which cell this rect covers
            # Rect center
            cx = r_op['x'] + r_op['w'] / 2
            cy = r_op['y'] + r_op['h'] / 2

            r_idx, c_idx = get_cell_index(cx, cy, unique_xs, unique_ys)
            if r_idx != -1 and c_idx != -1:
                black_cells.add((r_idx, c_idx))
                # Initialise as empty black
                matrix[r_idx][c_idx] = [0, 0]

        # Analyze texts for clues
        for t_op in texts:
            if not t_op['text'].strip():
                continue
            try:
                val = int(t_op['text'])
            except ValueError:
                continue

            x = t_op['x']
            y = t_op['y']

            # Find cell
            r_idx, c_idx = get_cell_index(x, y, unique_xs, unique_ys)

            if r_idx != -1 and c_idx != -1:
                # Ensure it's marked as black/clue cell
                if (r_idx, c_idx) not in black_cells:
                    black_cells.add((r_idx, c_idx))
                    matrix[r_idx][c_idx] = [0, 0]

                # Determine position within cell for Horizontal vs Vertical
                cell_x_start = unique_xs[c_idx]
                cell_x_end = unique_xs[c_idx+1]
                cell_y_start = unique_ys[r_idx]
                cell_y_end = unique_ys[r_idx+1]

                cell_w = cell_x_end - cell_x_start
                cell_h = cell_y_end - cell_y_start

                # Relative pos
                rel_x = (x - cell_x_start) / cell_w
                rel_y = (y - cell_y_start) / cell_h

                # Top-Right -> Horizontal Sum -> index 0
                # Bottom-Left -> Vertical Sum -> index 1
                # Usually Horizontal sum (for the row) is in top-right corner
                # Vertical sum (for the column) is in bottom-left corner

                if rel_x > 0.5 and rel_y < 0.5:
                    matrix[r_idx][c_idx][0] = val
                elif rel_x < 0.5 and rel_y > 0.5:
                    matrix[r_idx][c_idx][1] = val
                else:
                    # Fallback or center? Maybe just assign based on x/y
                    if rel_x > rel_y: # Top-Right half
                         matrix[r_idx][c_idx][0] = val
                    else:
                         matrix[r_idx][c_idx][1] = val

        return Grid(matrix), unique_xs, unique_ys
