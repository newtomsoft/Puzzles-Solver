from playwright.sync_api import Page


class PuzzlesMobileGridProvider:
    @staticmethod
    def get_puzzle_info_text(soup):
        puzzle_info = soup.find('div', class_='puzzleInfo')
        puzzle_info_text = puzzle_info.text
        return puzzle_info_text

    @staticmethod
    def new_game(page: Page, selector_to_waite='div.cell'):
        new_game_button = page.locator("#btnNew")
        if new_game_button.count() > 0:
            new_game_button.click()
            page.wait_for_selector(selector_to_waite)
