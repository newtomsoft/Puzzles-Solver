import asyncio
import json

from Domain.Board.Grid import Grid
from Domain.Puzzles.Tents.TentsSolver import TentsSolver
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class VuqqTentsAndTreesGridProvider(PlaywrightGridProvider):
    async def scrap_grid(self, browser, url):
        page = await browser.new_page()
        await page.route(lambda u: "drawing.js" in u, self._handle_drawing_js)
        await page.goto(url)

        try:
            await page.wait_for_selector("canvas", timeout=30000)

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

        except Exception as e:
            await page.close()
            raise e

    @staticmethod
    async def _handle_drawing_js(route, request):
        try:
            response = await route.fetch()
            body = await response.text()
            new_body = "window.vuqq_frames = []; window.current_frame = [];\n" + body

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

    @staticmethod
    def _parse_grid(logs):
        texts = [l for l in logs if l["type"] == "text"]
        rects = [l for l in logs if l["type"] == "rect"]

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
