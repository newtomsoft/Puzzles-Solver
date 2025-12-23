from playwright.async_api import BrowserContext, Page

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class VuqqGridProvider(PlaywrightGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        pass

    @staticmethod
    async def open_page(browser: BrowserContext, url: str, selector:str) -> Page:
        page = browser.pages[0]
        await page.route(lambda u: "drawing.js" in u, VuqqGridProvider._handle_drawing_js)
        await page.goto(url, wait_until='domcontentloaded')
        await page.wait_for_selector(selector, timeout=3000)
        return page

    @staticmethod
    async def _handle_drawing_js(route):
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
