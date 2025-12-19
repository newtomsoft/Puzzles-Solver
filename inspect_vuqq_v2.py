import asyncio
from playwright.async_api import async_playwright
import json

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://vuqq.com/fr/tents-and-trees/")

            # Wait for any canvas
            try:
                await page.wait_for_selector("canvas", timeout=20000)
                print("Canvas found.")
            except:
                print("Canvas not found within timeout.")

            # Dump HTML
            content = await page.content()
            with open("page_dump.html", "w") as f:
                f.write(content)

            # Take screenshot
            await page.screenshot(path="page.png")

            # Check frames
            print(f"Frames: {len(page.frames)}")
            for frame in page.frames:
                print(f"Frame url: {frame.url}")

            # Check globals
            globals_js = """
            (() => {
                return Object.keys(window).filter(k => k.toLowerCase().includes('vuqq') || k.toLowerCase().includes('game'));
            })()
            """
            suspicious_globals = await page.evaluate(globals_js)
            print(f"Suspicious globals: {suspicious_globals}")

            # Check meta again
            meta = await page.evaluate("window.vuqq_meta")
            print(f"window.vuqq_meta: {meta}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
