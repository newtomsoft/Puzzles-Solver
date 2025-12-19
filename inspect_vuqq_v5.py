import asyncio
from playwright.async_api import async_playwright
import json

async def handle_drawing_js(route, request):
    try:
        response = await route.fetch()
        body = await response.text()

        # Inject logs
        new_body = body

        # Init logs array
        new_body = "window.vuqq_logs = [];\n" + new_body

        # Palette
        new_body = new_body.replace(
            "set_palette_entry: function(index, r, g, b) {",
            "set_palette_entry: function(index, r, g, b) { window.vuqq_logs.push({type:'palette', index:index, rgb:[r,g,b]});"
        )

        # Text
        new_body = new_body.replace(
            "draw_text: function(x, y, fonttype, fontsize, align, colour, text) {",
            "draw_text: function(x, y, fonttype, fontsize, align, colour, text) { window.vuqq_logs.push({type:'text', x:x, y:y, text:text, colour:colour});"
        )

        # Circle
        new_body = new_body.replace(
            "draw_circle: function(cx, cy, radius, fillcolour, outlinecolour) {",
            "draw_circle: function(cx, cy, radius, fillcolour, outlinecolour) { window.vuqq_logs.push({type:'circle', x:cx, y:cy, r:radius, fill:fillcolour});"
        )

        # Rect
        new_body = new_body.replace(
            "draw_rect: function(x, y, w, h, colour) {",
            "draw_rect: function(x, y, w, h, colour) { window.vuqq_logs.push({type:'rect', x:x, y:y, w:w, h:h, colour:colour});"
        )

        # Poly
        # Note: we need to decode coords using Module.c_to_js_array which is global or needs access
        # In drawing.js Module is global? Yes.
        new_body = new_body.replace(
            "draw_poly: function(/* int* */coords, npoints, fillcolour, outlinecolour) {",
            "draw_poly: function(coords, npoints, fillcolour, outlinecolour) { try { var dc = Module.c_to_js_array(coords, npoints*2, 'i32'); window.vuqq_logs.push({type:'poly', coords:dc, fill:fillcolour}); } catch(e){} "
        )

        await route.fulfill(response=response, body=new_body)
    except Exception as e:
        print(f"Error handling route: {e}")
        await route.continue_()

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.route("**/drawing.js", handle_drawing_js)

        await page.goto("https://vuqq.com/fr/tents-and-trees/")

        try:
            await page.wait_for_selector("canvas", timeout=10000)
            await asyncio.sleep(5)

            logs = await page.evaluate("window.vuqq_logs")
            with open("vuqq_logs.json", "w") as f:
                json.dump(logs, f, indent=2)

            print(f"Captured {len(logs)} logs.")

        except Exception as e:
            print(f"Error: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
