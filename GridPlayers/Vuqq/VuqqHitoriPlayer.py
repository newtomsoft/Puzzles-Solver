from Domain.Board.Grid import Grid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer

class VuqqHitoriPlayer(PlaywrightPlayer):
    async def play(self, grid: Grid) -> None:
        page = self.browser.pages[0]

        # We assume the page is already open and on the grid
        cells = page.locator('.grid__cell')

        for r in range(grid.rows_number):
            for c in range(grid.columns_number):
                val = grid[r, c]
                # Index in flat list
                idx = r * grid.columns_number + c
                cell = cells.nth(idx)

                # Determine target state
                target_is_black = (val is False)
                # target_is_green = (isinstance(val, int)) # Not used currently

                # Determine current state
                classes = await cell.get_attribute('class')
                classes_list = classes.split()
                is_black = 'black' in classes_list
                is_green = 'green' in classes_list

                # Strategy:
                # Left Click Cycle: Empty -> Black -> Green -> Empty
                # Right Click: Toggle Green (Empty->Green, Green->Empty) or Reset?
                #
                # Based on analysis:
                # To set Black:
                # - If Empty: Click Left (-> Black)
                # - If Green: Click Left twice (Green->Empty->Black) or Right (Green->Empty) then Left (Empty->Black)
                # - If Black: Do nothing
                #
                # To set Green (for White cells):
                # - If Empty: Right Click (-> Green)
                # - If Black: Click Left (Black -> Green)
                # - If Green: Do nothing

                if target_is_black:
                    if is_black:
                        continue
                    elif is_green:
                        # Green -> Empty -> Black
                        await cell.click() # to Empty
                        await cell.click() # to Black
                    else: # Empty
                        # Empty -> Black
                        await cell.click()

                else: # Target is White (Number) -> We can mark Green or leave Empty
                    # Let's mark it Green to be consistent with visualization
                    if is_green:
                        continue
                    elif is_black:
                        # Black -> Green
                        await cell.click()
                    else: # Empty
                        # Empty -> Green via Right Click (safest shortcut)
                        await cell.click(button='right')
