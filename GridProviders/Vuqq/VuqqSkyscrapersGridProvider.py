
import json

from playwright.async_api import BrowserContext

from Domain.Board.Grid import Grid
from GridProviders.Vuqq.Base.VuqqGridProvider import VuqqGridProvider


class VuqqSkyscrapersGridProvider(VuqqGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url, "#gameboard")

        await page.evaluate("""
            (() => {
                window.capturedTexts = [];
                const originalFillText = CanvasRenderingContext2D.prototype.fillText;
                
                CanvasRenderingContext2D.prototype.fillText = function(text, x, y, maxWidth) {
                    window.capturedTexts.push({text: text, x: x, y: y});
                    return originalFillText.apply(this, arguments);
                };
            })();
        """)

        if await page.is_visible('.game-new'):
            await page.click('.game-new')

        await page.wait_for_timeout(1000)
        
        captured_data = await page.evaluate("window.capturedTexts")
        
        if not captured_data:
            await page.set_viewport_size({"width": 1000, "height": 1000})
            await page.wait_for_timeout(500)
            captured_data = await page.evaluate("window.capturedTexts")

        if not captured_data:
            raise Exception("No text captured from canvas.")
            
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
            
        grid, visible, raw_meta = self._parse_captured_data(captured_data)
        
        scale_x = canvas_metrics['client_width'] / canvas_metrics['internal_width']
        scale_y = canvas_metrics['client_height'] / canvas_metrics['internal_height']
        offset_x = canvas_metrics['client_left']
        offset_y = canvas_metrics['client_top']
        
        screen_xs = [x * scale_x + offset_x for x in raw_meta['xs']]
        screen_ys = [y * scale_y + offset_y for y in raw_meta['ys']]
        
        metadata = {'xs': screen_xs, 'ys': screen_ys}
        
        await page.evaluate(f"window.vuqq_meta = {json.dumps(metadata)}")
        
        return grid, visible

    @staticmethod
    def _parse_captured_data(data):
        items = []
        for item in data:
            try:
                if not item['text'].strip():
                    continue
                val = int(item['text'])
                items.append({'val': val, 'x': item['x'], 'y': item['y']})
            except ValueError:
                pass 
                
        if not items:
            raise Exception("No numerical clues found.")
            
        def get_clusters(values, tolerance=10):
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

        xs = [i['x'] for i in items]
        ys = [i['y'] for i in items]
        
        unique_xs = get_clusters(xs)
        unique_ys = get_clusters(ys)

        n_cols = len(unique_xs) - 2
        n_rows = len(unique_ys) - 2
        
        if n_cols != n_rows or n_cols < 1:
            raise Exception(f"Could not determine valid grid size. Found xs={len(unique_xs)}, ys={len(unique_ys)}")
            
        n = n_cols
        
        top_clues = [0] * n
        bottom_clues = [0] * n
        left_clues = [0] * n
        right_clues = [0] * n
        matrix_vals = [[0 for _ in range(n)] for _ in range(n)]
        
        def get_index(val, clusters, tolerance=10):
            for i, c in enumerate(clusters):
                if abs(val - c) < tolerance:
                    return i
            return -1

        for item in items:
            xi = get_index(item['x'], unique_xs)
            yi = get_index(item['y'], unique_ys)
            
            val = item['val']
            
            if xi == 0: 
                if 1 <= yi <= n:
                    left_clues[yi - 1] = val
                    
            elif xi == len(unique_xs) - 1:
                if 1 <= yi <= n:
                    right_clues[yi - 1] = val
                    
            elif 1 <= xi <= n:
                col_idx = xi - 1
                
                if yi == 0:
                    top_clues[col_idx] = val
                elif yi == len(unique_ys) - 1:
                    bottom_clues[col_idx] = val
                elif 1 <= yi <= n:
                    row_idx = yi - 1
                    matrix_vals[row_idx][col_idx] = val
                    
        grid = Grid(matrix_vals)
        visible = {
            'by_north': top_clues,
            'by_south': bottom_clues,
            'by_west': left_clues,
            'by_east': right_clues
        }
        
        return grid, visible, {'xs': unique_xs, 'ys': unique_ys}


