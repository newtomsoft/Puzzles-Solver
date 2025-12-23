from abc import abstractmethod

from playwright.async_api import Page

from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class PuzzlesMobilePlayer(PlaywrightPlayer):
    @abstractmethod
    async def play(self, solution) -> PlayStatus:
        pass

    @staticmethod
    async def submit_score(page: Page) -> PlayStatus:
        success_selector_visible = await page.query_selector(".succ") is not None

        if not success_selector_visible:
            return PlayStatus.FAILED_NO_SUCCESS_SELECTOR

        score_submit_button = page.locator("#btnHallSubmit")
        submit_button_exists = (await score_submit_button.count()) > 0

        if not submit_button_exists:
            return PlayStatus.FAILED_NO_SUBMIT_BUTTON

        await score_submit_button.first.click()
        return PlayStatus.SUCCESS
