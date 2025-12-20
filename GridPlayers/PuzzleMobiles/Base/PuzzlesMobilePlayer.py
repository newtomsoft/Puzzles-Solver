from abc import abstractmethod

from playwright.async_api import Page

from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.PuzzleMobiles.Base.SubmissionStatus import SubmissionStatus


class PuzzlesMobilePlayer(PlaywrightPlayer):
    @abstractmethod
    async def play(self, solution) -> SubmissionStatus:
        pass

    @staticmethod
    async def submit_score(page: Page) -> SubmissionStatus:
        success_selector_visible = await page.query_selector('.succ') is not None

        if not success_selector_visible: return SubmissionStatus.FAILED_NO_SUCCESS_SELECTOR

        score_submit_button = page.locator("#btnHallSubmit")
        submit_button_exists = (await score_submit_button.count()) > 0

        if not submit_button_exists: return SubmissionStatus.FAILED_NO_SUBMIT_BUTTON

        await score_submit_button.first.click()
        return SubmissionStatus.SUCCESS
