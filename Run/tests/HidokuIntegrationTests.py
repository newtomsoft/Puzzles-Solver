import unittest
import sys
from unittest.mock import MagicMock

# Mock modules if necessary, though we will run a real integration test if possible.
# But since the sandbox might restrict internet or browser, I should rely on the Playwright setup.
# The user already provided a script inspect_hidoku.py which worked.

from GridProviders.GridGames.HidokuGridProvider import HidokuGridProvider
from playwright.async_api import async_playwright
import asyncio

class HidokuIntegrationTests(unittest.TestCase):
    def test_scrap_grid(self):
        async def run_test(url, expected_rows, expected_cols):
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                provider = HidokuGridProvider()

                print(f"Scraping {url}...")
                grid = await provider.scrap_grid(browser, url)

                print(f"Grid scraped ({expected_rows}x{expected_cols}):")
                print(str(grid))

                self.assertIsNotNone(grid)
                self.assertEqual(grid.rows_number, expected_rows)
                self.assertEqual(grid.columns_number, expected_cols)

                # Verify some numbers are filled
                filled_count = 0
                for r in range(grid.rows_number):
                    for c in range(grid.columns_number):
                        val = grid[r, c]
                        if val is not None:
                            filled_count += 1
                            self.assertIsInstance(val, int)

                print(f"Found {filled_count} numbers.")
                self.assertGreater(filled_count, 0, "Should have found some numbers")

                await browser.close()

        # Run async tests
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Easy
        loop.run_until_complete(run_test("https://gridgames.app/hidoku/?d=Easy", 5, 5))
        # Medium
        loop.run_until_complete(run_test("https://gridgames.app/hidoku/?d=Medium", 6, 6))
        # Hard
        loop.run_until_complete(run_test("https://gridgames.app/hidoku/?d=Hard", 7, 7))
        # Extreme
        loop.run_until_complete(run_test("https://gridgames.app/hidoku/?d=Extreme", 8, 8))

        loop.close()

if __name__ == "__main__":
    unittest.main()
