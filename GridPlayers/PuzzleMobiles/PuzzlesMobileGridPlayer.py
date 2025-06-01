from abc import abstractmethod

from playwright.sync_api import Page

from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class PuzzlesMobileGridPlayer(PlaywrightGridPlayer):
    @abstractmethod
    def play(self, solution):
        pass

    def submit_score(self, page: Page):
        page.wait_for_selector('.succ')
        score_submit_button = page.locator("#btnHallSubmit")
        if score_submit_button.count() > 0:
            score_submit_button.first.click()
