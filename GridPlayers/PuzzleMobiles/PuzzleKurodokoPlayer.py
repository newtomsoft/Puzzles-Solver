from time import sleep

from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from Domain.Board.Position import Position

class PuzzleKurodokoPlayer(PuzzlesMobilePlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        # Assuming Kurodoko cells are toggled by clicking.
        # Typically one click = Black, two clicks = White (or flagged), etc.
        # Or click to cycle.
        # In Nurikabe, clicking toggles black/white/dot.
        # In Kurodoko, we need to mark Black cells.
        # The logic in Solver returns: 0 for Black, >0 for White/Number.

        # We need to target cells that are Black in the solution.
        # But wait, original grid had 0 for unknown.
        # The solution has 0 for Black.

        # We need to find all cells.
        cells = page.query_selector_all("div.cell")

        if not cells:
            print("No cells found for playing!")
            return

        # Double check we have the right number of cells
        if len(cells) != solution.rows_number * solution.columns_number:
             # Try filtering like in provider
             filtered = [c for c in cells if 'top:' in c.get_attribute('style') and 'left:' in c.get_attribute('style')]
             if len(filtered) == solution.rows_number * solution.columns_number:
                 cells = filtered
             else:
                 print(f"Warning: Cell count mismatch. Found {len(cells)}, expected {solution.rows_number * solution.columns_number}")

        for r in range(solution.rows_number):
            for c in range(solution.columns_number):
                val = solution.value(Position(r, c))
                # If val == 0, it means Black.
                # We should click it.
                if val == 0:
                    index = r * solution.columns_number + c
                    if index < len(cells):
                        # Use bounding box click which is safer than element click sometimes
                        box = cells[index].bounding_box()
                        if box:
                            x = box['x'] + box['width'] / 2
                            y = box['y'] + box['height'] / 2
                            page.mouse.click(x, y)
                        else:
                             cells[index].click()

                        # Note: If multiple clicks are needed (e.g. cycle empty -> black -> white),
                        # we assume 1 click makes it Black.
                        # If not, we might need to adjust.
                        # Usually on puzzles-mobile:
                        # Tap 1: Black
                        # Tap 2: Dot (White/Marked)
                        # Tap 3: Empty

        sleep(1)
        self.submit_score(page)
        # sleep(60) # Keeping it but maybe reducing for dev/testing if I could run it.
