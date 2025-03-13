from playwright.sync_api import Page


class PuzzleBaronGridProvider:
    @staticmethod
    def new_game(page: Page, selector_to_wait='div.gridbox'):
        new_game_button = page.locator(".button_green")
        if new_game_button.count() > 0:
            new_game_button.click()
            page.wait_for_selector(selector_to_wait)
