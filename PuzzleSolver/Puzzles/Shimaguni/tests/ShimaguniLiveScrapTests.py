import unittest
import asyncio
from rebrowser_playwright.async_api import async_playwright
from PuzzleSolver.Board.Grid import Grid
from GridProviders.GridPuzzle.GridPuzzleShimaguniGridProvider import GridPuzzleShimaguniGridProvider

class ShimaguniLiveScrapTests(unittest.IsolatedAsyncioTestCase):
    async def test_scrap_live_puzzles(self):
        puzzles_to_test = [
            ("https://gridpuzzle.com/shimaguni/20nw8", (6, 6)),  # 6x6 evil
            ("https://gridpuzzle.com/shimaguni/0zjjg", (7, 7)),  # 7x7 evil
            ("https://gridpuzzle.com/shimaguni/0m5xw", (10, 10)), # 10x10 evil
            ("https://gridpuzzle.com/shimaguni/0d1r1", (12, 12)), # 12x12 evil
        ]
        
        provider = GridPuzzleShimaguniGridProvider()

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            
            for url, expected_dims in puzzles_to_test:
                with self.subTest(url=url):
                    try:
                        print(f"Attempting to scrape: {url}") # Fixed print statement
                        grid, regions = await provider.scrap_grid(context, url)
                        
                        self.assertIsNotNone(grid, f"Scraping {url} returned None grid")
                        self.assertFalse(grid.is_empty(), f"Scraping {url} returned an empty grid")
                        self.assertEqual(grid.rows_number, expected_dims[0], f"Grid dimensions mismatch for {url}: expected {expected_dims[0]} rows, got {grid.rows_number}")
                        self.assertEqual(grid.columns_number, expected_dims[1], f"Grid dimensions mismatch for {url}: expected {expected_dims[1]} columns, got {grid.columns_number}")
                        print(f"Successfully scraped {url} with dimensions {expected_dims}")
                        
                    except Exception as e:
                        self.fail(f"Failed to scrape {url}: {e}")
            
            await browser.close()

if __name__ == '__main__':
    unittest.main()
