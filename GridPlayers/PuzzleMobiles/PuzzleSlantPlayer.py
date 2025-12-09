from playwright.sync_api import Page

from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleSlantPlayer(PuzzlesMobilePlayer):
    def play(self, solution):
        page = self.browser.pages[0]

        # Get all cell elements
        cell_elements = page.query_selector_all('div.cell')

        # Verify count
        if len(cell_elements) != solution.rows_number * solution.columns_number:
            # If mismatch, we can't reliably play.
            # We'll log or just return.
            return

        for r in range(solution.rows_number):
            for c in range(solution.columns_number):
                target_val = solution[r][c] # '\' or '/'

                # Index in flat list (assuming row-major order)
                idx = r * solution.columns_number + c
                if idx >= len(cell_elements):
                    break

                element = cell_elements[idx]

                # Assume board starts empty.
                # Standard PuzzlesMobile behavior for Slant/Gokigen:
                # Click 1 -> / (Right slant)
                # Click 2 -> \ (Left slant)
                # Click 3 -> Empty

                if target_val == '/':
                    element.click()
                elif target_val == '\\':
                    element.click()
                    element.click()
