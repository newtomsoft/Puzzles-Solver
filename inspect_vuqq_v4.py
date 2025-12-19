import asyncio
from playwright.async_api import async_playwright
import json

async def handle_puzzle_js(route, request):
    try:
        response = await route.fetch()
        body = await response.text()
        # Inject hook
        if "midend = _midend;" in body:
            new_body = body.replace('midend = _midend;', 'midend = _midend; window.vuqq_midend = _midend; console.log("Hooked midend:", _midend);')
            print("Successfully injected midend hook.")
            await route.fulfill(response=response, body=new_body)
        else:
            print("Could not find insertion point in puzzle.js")
            await route.fulfill(response=response)
    except Exception as e:
        print(f"Error handling route: {e}")
        await route.continue_()

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.route("**/puzzle.js", handle_puzzle_js)

        await page.goto("https://vuqq.com/fr/tents-and-trees/")

        try:
            await page.wait_for_selector("canvas", timeout=10000)
            await asyncio.sleep(3)

            midend = await page.evaluate("window.vuqq_midend")
            print(f"Midend: {midend}")

            if midend:
                # Check available globals starting with _midend
                globals_midend = await page.evaluate("""
                    Object.keys(window).filter(k => k.startsWith('_midend'))
                """)
                print(f"Global midend functions: {globals_midend}")

                # Check if we can call any to get text
                # Try _midend_get_game_id if it exists
                if '_midend_get_game_id' in globals_midend:
                    game_id = await page.evaluate(f"Module.UTF8ToString(_midend_get_game_id({midend}))")
                    print(f"Game ID: {game_id}")
                else:
                    print("_midend_get_game_id not found.")

                # Try saving via midend_serialise?
                # or midend_get_current_params

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
