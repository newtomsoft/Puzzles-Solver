from time import sleep

from Domain.Board.Position import Position
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleChessRangerPlayer(PuzzlesMobilePlayer):
    def play(self, solution: list[tuple[Position, Position]]):
        for move in solution:
            start_pos, end_pos = move
            self.click_cell(start_pos)
            self.click_cell(end_pos)
            sleep(0.2) # Small delay for animation

    def click_cell(self, position: Position):
        # Calculate index
        # Usually cells are indexed 0 to N-1
        # Need to know columns number.
        # But we don't have grid dimensions here easily unless we store it or re-scrape.
        # However, Playwright locator can use nth(index).

        # We need the columns number.
        # PuzzlesMobilePlayer doesn't seem to store grid info.
        # But looking at other players, they usually assume standard indexing.
        # Let's check if we can click by coordinates or if we need to get cells first.

        # Re-fetching cells is safe.
        cells = self.page.locator('.cell')

        # We need to know columns count to calculate index.
        # Can we infer it?
        # Or we can click by pixel position if we knew it.

        # Better: get all cells and calculate row/col from styles or count.
        # But that's slow.

        # Assumption: The grid doesn't change dimensions.
        # We can count columns once.

        # Wait, `solution` contains positions.
        # If we just get all `.cell` elements, we can index them if we know `columns_number`.

        # Let's get columns number from the first row logic

        # Note: If this is called per move, it might be slow.
        # But for Playwright it's okay.

        # Get all cells
        all_cells = cells.all()
        if not all_cells:
            return

        # Determine columns number
        # We can assume the grid is rectangular and check `top` style of the first few cells.
        # Or count how many have same `top` as the first one.

        first_cell_top = all_cells[0].get_attribute('style')
        # Parse top value... simple heuristic: count until top changes?
        # But cells might be ordered by DOM, which usually follows row-major order.

        # Let's count how many cells have the same top offset as the first one.
        count = 0
        import re
        top_regex = re.compile(r'top:\s*(\d+)px')

        first_match = top_regex.search(first_cell_top)
        first_top = first_match.group(1) if first_match else None

        columns = 0
        if first_top:
            for cell in all_cells:
                style = cell.get_attribute('style')
                match = top_regex.search(style)
                if match and match.group(1) == first_top:
                    columns += 1
                else:
                    break
        else:
            # Fallback if style parsing fails
             columns = 1 # Should not happen

        index = position.r * columns + position.c
        if 0 <= index < len(all_cells):
            all_cells[index].click()

    def __init__(self, page, *args, **kwargs):
        super().__init__(page, *args, **kwargs)
        self.page = page
