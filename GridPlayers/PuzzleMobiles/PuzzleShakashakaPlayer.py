from time import sleep

from Domain.Board.Grid import Grid
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleShakashakaPlayer(PuzzlesMobilePlayer):
    def play(self, solution: Grid):
        page = self.browser.pages[0]
        # Locate all cells
        cells = page.locator('div.cell')
        count = cells.count()

        # We assume cells are ordered row-major or we need to map them.
        # PuzzlesMobile usually orders them by DOM order which matches Grid order?
        # Verify via position logic if needed, but standard is index-based.

        cols = solution.columns_number
        rows = solution.rows_number

        for r in range(rows):
            for c in range(cols):
                val = solution[r][c]
                # val: 0(E), 1(TL), 2(TR), 3(BR), 4(BL), 5(B)
                # Skip Black cells (5) as they are immutable
                if val == 5:
                    continue

                # Input mechanism:
                # Usually click to cycle: Empty -> TL -> TR -> BR -> BL -> Empty
                # Or click corners.
                # Let's assume Cycle for now (Left click).

                # Determine how many clicks needed.
                # Current state is Empty (0).
                # 0 -> 0 clicks
                # 1 -> 1 click
                # 2 -> 2 clicks
                # 3 -> 3 clicks
                # 4 -> 4 clicks

                # Optimize: Right click might go backwards?

                idx = r * cols + c
                cell = cells.nth(idx)

                # Check current class to know state?
                # Assuming start from empty.

                clicks = 0
                if val == 1: clicks = 1
                elif val == 2: clicks = 2
                elif val == 3: clicks = 3
                elif val == 4: clicks = 4

                for _ in range(clicks):
                    cell.click(button="left")
                    # sleep(0.05) # Small delay if needed

        self.submit_score(page)
