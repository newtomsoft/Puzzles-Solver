import json

from playwright.async_api import BrowserContext

from GridProviders.Vuqq.Base.VuqqGridProvider import VuqqGridProvider


class VuqqAkariGridProvider(VuqqGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url, "canvas")

        await page.goto(url)
        await page.wait_for_selector('canvas')

        await page.evaluate("""
            (() => {
                window.capturedTexts = [];
                window.capturedRects = [];
                const originalFillText = CanvasRenderingContext2D.prototype.fillText;
                const originalFillRect = CanvasRenderingContext2D.prototype.fillRect;

                CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
                    window.capturedTexts.push({text: text, x: x, y: y});
                    return originalFillText.apply(this, arguments);
                };

                CanvasRenderingContext2D.prototype.fillRect = function(x, y, w, h) {
                    window.capturedRects.push({x: x, y: y, w: w, h: h, style: this.fillStyle});
                    return originalFillRect.apply(this, arguments);
                };
            })();
        """)

        if await page.is_visible('.game-new'):
            await page.click('.game-new')
        elif await page.is_visible('.game-restart'):
            await page.click('.game-restart')

        await page.wait_for_timeout(1000)

        captured_texts = await page.evaluate("window.capturedTexts")
        captured_rects = await page.evaluate("window.capturedRects")

        if not captured_rects:
             await page.set_viewport_size({"width": 1000, "height": 1000})
             await page.wait_for_timeout(500)
             captured_texts = await page.evaluate("window.capturedTexts")
             captured_rects = await page.evaluate("window.capturedRects")

        if not captured_rects:
            raise Exception("No rects captured from canvas.")

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

        cells = [r for r in captured_rects if 40 <= r['w'] <= 120 and 40 <= r['h'] <= 120 and abs(r['w'] - r['h']) < 5]

        if not cells:
             raise Exception("No cell-sized rects found.")

        avg_cell_w = sum(c['w'] for c in cells) / len(cells)
        avg_cell_h = sum(c['h'] for c in cells) / len(cells)

        xs = sorted(list(set([c['x'] for c in cells])))
        ys = sorted(list(set([c['y'] for c in cells])))

        def cluster(values, tolerance=10):
            if not values: return []
            values = sorted(values)
            clusters = []
            curr = [values[0]]
            for v in values[1:]:
                if v - curr[-1] < tolerance:
                    curr.append(v)
                else:
                    clusters.append(sum(curr)/len(curr))
                    curr = [v]
            clusters.append(sum(curr)/len(curr))
            return clusters

        unique_xs = cluster([c['x'] for c in cells])
        unique_ys = cluster([c['y'] for c in cells])

        rows = len(unique_ys)
        cols = len(unique_xs)

        # Initialize Grid with -1 (White)
        matrix = [[-1 for _ in range(cols)] for _ in range(rows)]

        def get_index(val, clusters):
            for i, c in enumerate(clusters):
                if abs(val - c) < 20:
                    return i
            return -1

        for c in cells:
            r = get_index(c['y'], unique_ys)
            c_idx = get_index(c['x'], unique_xs)

            if r != -1 and c_idx != -1:
                style = str(c['style']).lower()
                if style != '#f3f4f8' and style != '#ffffff':
                    matrix[r][c_idx] = -2  # Black, potentially with number
                else:
                    matrix[r][c_idx] = -1 # White

        for t in captured_texts:
            try:
                val = int(t['text'])
                tx = t['x']
                ty = t['y']

                c_idx = get_index(tx - 50, unique_xs)
                r_idx = get_index(ty - 50, unique_ys)

                if c_idx != -1 and r_idx != -1:
                    matrix[r_idx][c_idx] = val
            except ValueError:
                pass

        black_cells = []
        number_constraints = {}
        
        for r in range(rows):
            for c in range(cols):
                val = matrix[r][c]
                if val == -1:
                    continue # White
                
                black_cells.append((r, c))
                
                if 0 <= val <= 4:
                    number_constraints[(r, c)] = val

        data_game = {
            'rows_number': rows,
            'columns_number': cols,
            'black_cells': black_cells,
            'number_constraints': number_constraints
        }

        scale_x = canvas_metrics['client_width'] / canvas_metrics['internal_width']
        scale_y = canvas_metrics['client_height'] / canvas_metrics['internal_height']
        offset_x = canvas_metrics['client_left']
        offset_y = canvas_metrics['client_top']

        screen_xs = [(x + avg_cell_w / 2) * scale_x + offset_x for x in unique_xs]
        screen_ys = [(y + avg_cell_h / 2) * scale_y + offset_y for y in unique_ys]

        metadata = {'xs': screen_xs, 'ys': screen_ys}
        await page.evaluate(f"window.vuqq_meta = {json.dumps(metadata)}")

        return data_game
