import asyncio

from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class VuqqSudokuPlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = self.browser.pages[0]

        # Ensure we are on the page
        await page.wait_for_selector('.grid__cell')

        cells = await page.query_selector_all('.grid__cell')
        if len(cells) != 81:
            raise Exception("Grid cells not found during playback")

        # Numpad buttons
        # The DOM shows <span ... ng-click="$ctrl.keyPress(item)">1</span> inside .game__controls-numpad
        numpad_buttons = await page.query_selector_all('.game__controls-numpad span')

        # Create a map for numpad buttons by text
        numpad_map = {}
        for btn in numpad_buttons:
            text = await btn.inner_text()
            text = text.strip()
            if text.isdigit():
                numpad_map[int(text)] = btn

        for position, value in solution:
            if not value:
                continue

            idx = position.r * 9 + position.c
            cell = cells[idx]

            # Check if cell is already filled (has a number that is not empty)
            number_span = await cell.query_selector('.number')
            existing_text = ""
            if number_span:
                existing_text = await number_span.inner_text()

            # If cell is already filled, skip (assuming it's a clue or already correct)
            if existing_text.strip():
                continue

            # Click cell
            await cell.click()
            # Small delay might be needed for selection to register
            # await asyncio.sleep(0.05)

            # Click number
            if value in numpad_map:
                await numpad_map[value].click()
            else:
                print(f"Warning: Numpad button for {value} not found")

        # Wait a bit after finishing
        await asyncio.sleep(1)
