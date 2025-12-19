import asyncio
from playwright.async_api import async_playwright
import json

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://vuqq.com/fr/tents-and-trees/")

            # Wait for game to load
            try:
                await page.wait_for_selector("canvas", timeout=10000)
                await asyncio.sleep(2) # Wait for JS initialization
            except:
                print("Canvas not found")

            # 1. Try Angular Scope
            print("Checking Angular Scope...")
            angular_data = await page.evaluate("""
                (() => {
                    if (typeof angular === 'undefined') return 'Angular not defined';
                    const el = document.querySelector('game-tentsandtrees');
                    if (!el) return 'Game element not found';
                    const scope = angular.element(el).scope();
                    if (!scope) return 'Scope not found';

                    // config is passed as attribute, might be on scope
                    return {
                        config: scope.config,
                        ctrl_config: scope.$ctrl ? scope.$ctrl.config : null
                    };
                })()
            """)
            print(f"Angular Data: {json.dumps(angular_data, indent=2)}")

            # 2. Try C Module / Globals
            print("\nChecking C Module...")
            c_data = await page.evaluate("""
                (() => {
                    const info = {};
                    if (typeof Module !== 'undefined') {
                        info.module_exists = true;
                        // Try to get new game desc if it's a string pointer
                        if (typeof _new_game_desc !== 'undefined') {
                             try {
                                 info.new_game_desc_ptr = _new_game_desc;
                                 if (typeof Module.UTF8ToString === 'function') {
                                     info.desc_string = Module.UTF8ToString(_new_game_desc);
                                 }
                             } catch(e) { info.error_reading_desc = e.toString(); }
                        }
                    } else {
                        info.module_exists = false;
                    }
                    return info;
                })()
            """)
            print(f"C Data: {json.dumps(c_data, indent=2)}")

            # 3. Check for exposed Puzzle instance or other globals
            print("\nChecking globals again...")
            globals_check = await page.evaluate("""
                (() => {
                    // Sometimes puzzle instance is attached to window.puzzle or similar
                    return {
                        window_puzzle: typeof window.puzzle,
                        window_game: typeof window.game
                    };
                })()
            """)
            print(f"Globals Check: {json.dumps(globals_check, indent=2)}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
