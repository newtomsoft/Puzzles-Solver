from playwright.async_api import Page


class PuzzleBaronGridProvider:
    @staticmethod
    async def new_game(page: Page, selector_to_wait='div.gridbox'):
        new_game_button = page.locator(".button_green")
        if await new_game_button.count() > 0:
            await new_game_button.click()
            await page.wait_for_selector(selector_to_wait)
        div_to_view = await page.query_selector('#container')
        if div_to_view:
            await div_to_view.scroll_into_view_if_needed()
