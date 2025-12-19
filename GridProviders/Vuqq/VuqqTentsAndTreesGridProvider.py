import asyncio
from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class VuqqTentsAndTreesGridProvider(PlaywrightGridProvider):
    async def get_grid(self, browser, url):
        page = await browser.new_page()
        # Inject drawing hook to capture canvas operations
        await page.route("**/drawing.js", self._handle_drawing_js)
        await page.goto(url)

        try:
            # Wait for canvas
            await page.wait_for_selector("canvas", timeout=30000)

            # Poll for logs until populated
            for _ in range(40):
                logs_len = await page.evaluate("window.vuqq_logs ? window.vuqq_logs.length : 0")
                if logs_len > 50:
                    await asyncio.sleep(0.5)  # Wait for stability
                    break
                await asyncio.sleep(0.5)

            logs = await page.evaluate("window.vuqq_logs")
            if not logs:
                raise Exception("No logs captured from drawing.js")

            return self._parse_grid(logs)

        except Exception as e:
            await page.close()
            raise e

    async def _handle_drawing_js(self, route, request):
        try:
            response = await route.fetch()
            body = await response.text()
            new_body = "window.vuqq_logs = [];\n" + body

            # Inject hooks at start of function bodies
            hooks = [
                (
                    "start_draw: function() {",
                    "window.vuqq_logs = [];",
                ),
                (
                    "set_palette_entry: function(index, r, g, b) {",
                    "window.vuqq_logs.push({type:'palette', index:index, rgb:[r,g,b]});",
                ),
                (
                    "draw_text: function(x, y, fonttype, fontsize, align, colour, text) {",
                    "window.vuqq_logs.push({type:'text', x:x, y:y, text:text, colour:colour});",
                ),
                (
                    "draw_circle: function(cx, cy, radius, fillcolour, outlinecolour) {",
                    "window.vuqq_logs.push({type:'circle', x:cx, y:cy, r:radius, fill:fillcolour});",
                ),
                (
                    "draw_rect: function(x, y, w, h, colour) {",
                    "window.vuqq_logs.push({type:'rect', x:x, y:y, w:w, h:h, colour:colour});",
                ),
                (
                    "draw_poly: function(/* int* */coords, npoints, fillcolour, outlinecolour) {",
                    "try { var dc = Module.c_to_js_array(coords, npoints*2, 'i32'); window.vuqq_logs.push({type:'poly', coords:dc, fill:fillcolour}); } catch(e){}",
                ),
            ]

            for signature, injection in hooks:
                new_body = new_body.replace(signature, signature + " " + injection)

            await route.fulfill(response=response, body=new_body)
        except Exception as e:
            print(f"Error injecting hooks: {e}")
            await route.continue_()

    def _parse_grid(self, logs):
        texts = [l for l in logs if l["type"] == "text"]
        rects = [l for l in logs if l["type"] == "rect"]

        # Identify clues
        xs = [t["x"] for t in texts]
        ys = [t["y"] for t in texts]

        if not xs or not ys:
            raise Exception("No clues found in logs")

        max_x = max(xs)
        max_y = max(ys)

        # Row clues are on the right (high x)
        row_clues = sorted([t for t in texts if abs(t["x"] - max_x) < 5], key=lambda t: t["y"])
        # Column clues are at the bottom (high y)
        col_clues = sorted([t for t in texts if abs(t["y"] - max_y) < 5], key=lambda t: t["x"])

        rows = len(row_clues)
        cols = len(col_clues)

        grid = Grid(rows, cols)
        # Store clues in grid attributes for the solver
        grid.row_clues = [int(t["text"]) for t in row_clues]
        grid.col_clues = [int(t["text"]) for t in col_clues]

        # Store coordinate mapping for Player
        row_ys = [t["y"] for t in row_clues]
        col_xs = [t["x"] for t in col_clues]

        # We assume the clues are aligned with the grid cells

        # Find Trees
        # Palette index 3 is trunk (brown), 4 is leaves (green)
        trunks = [r for r in rects if r.get("colour") == 3]

        for trunk in trunks:
            tx, ty = trunk["x"], trunk["y"]
            trunk_cx = tx + trunk["w"] / 2
            trunk_cy = ty + trunk["h"] / 2

            # Find closest cell
            c = min(range(cols), key=lambda i: abs(col_xs[i] - trunk_cx))
            r = min(range(rows), key=lambda i: abs(row_ys[i] - trunk_cy))

            grid[r][c] = "TREE"

        return grid
