from abc import abstractmethod

from playwright.async_api import Page

from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class PuzzlesMobilePlayer(PlaywrightPlayer):
    @abstractmethod
    async def play(self, solution):
        pass

    @staticmethod
    async def submit_score(page: Page):
        await page.wait_for_selector('.succ')
        score_submit_button = page.locator("#btnHallSubmit")
        if (await score_submit_button.count()) > 0:
            await score_submit_button.first.click()
