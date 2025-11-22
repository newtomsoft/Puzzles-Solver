from abc import abstractmethod

from playwright.sync_api import Page

from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class PuzzlesMobilePlayer(PlaywrightPlayer):
    @abstractmethod
    def play(self, solution):
        pass

    @staticmethod
    def submit_score(page: Page):
        page.wait_for_selector('.succ')
        score_submit_button = page.locator("#btnHallSubmit")
        if score_submit_button.count() > 0:
            score_submit_button.first.click()
