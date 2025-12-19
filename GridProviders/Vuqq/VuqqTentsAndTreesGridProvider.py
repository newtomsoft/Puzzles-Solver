import asyncio

from Domain.Board.Grid import Grid
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class VuqqTentsAndTreesGridProvider(PlaywrightGridProvider):
    async def scrap_grid(self, browser, url):
        page = await browser.new_page()

        # Inject drawing hook to capture canvas operations
        await page.route(lambda u: "drawing.js" in u, self._handle_drawing_js)
        await page.goto(url)

        try:
            # Wait for canvas
            await page.wait_for_selector("canvas", timeout=30000)

            # Poll for frames until we have a populated one
            logs = None
            for _ in range(40):
                # Check if we have frames with content
                # We look for a frame with > 10 items
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

            # Persist logs for Player
            await page.evaluate("logs => window.vuqq_logs = logs", logs)

            return self._parse_grid(logs)

        except Exception as e:
            await page.close()
            raise e

    async def _handle_drawing_js(self, route, request):
        try:
            response = await route.fetch()
            body = await response.text()
            # Initialize frames storage
            new_body = "window.vuqq_frames = []; window.current_frame = [];\n" + body

            # Inject hooks at start of function bodies
            hooks = [
                (
                    "start_draw: function() {",
                    "window.current_frame = []; window.vuqq_frames.push(window.current_frame);",
                ),
                (
                    "set_palette_entry: function(index, r, g, b) {",
                    "try { window.current_frame.push({type:'palette', index:index, rgb:[r,g,b]}); } catch(e) {}",
                ),
                (
                    "draw_text: function(x, y, fonttype, fontsize, align, colour, text) {",
                    "try { window.current_frame.push({type:'text', x:x, y:y, text:text, colour:colour}); } catch(e) {}",
                ),
                (
                    "draw_circle: function(cx, cy, radius, fillcolour, outlinecolour) {",
                    "try { window.current_frame.push({type:'circle', x:cx, y:cy, r:radius, fill:fillcolour}); } catch(e) {}",
                ),
                (
                    "draw_rect: function(x, y, w, h, colour) {",
                    "try { window.current_frame.push({type:'rect', x:x, y:y, w:w, h:h, colour:colour}); } catch(e) {}",
                ),
                (
                    "draw_poly: function(/* int* */coords, npoints, fillcolour, outlinecolour) {",
                    "try { var dc = Module.c_to_js_array(coords, npoints*2, 'i32'); window.current_frame.push({type:'poly', coords:dc, fill:fillcolour}); } catch(e){}",
                ),
            ]

            for signature, injection in hooks:
                new_body = new_body.replace(signature, signature + " " + injection)
            
            await route.fulfill(
                body=new_body,
                content_type='application/javascript'
            )
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

        # Initialize matrix with 0 (Grass/Empty)
        matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        
        # Prepare cues dict
        tents_numbers_by_column_row = {
            'row': [int(t["text"]) for t in row_clues],
            'column': [int(t["text"]) for t in col_clues]
        }

        row_ys = [t["y"] for t in row_clues]
        col_xs = [t["x"] for t in col_clues]

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

            matrix[r][c] = -1 # Tree value for Solver
            
        grid = Grid(matrix)

        return grid, tents_numbers_by_column_row
