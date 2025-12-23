from abc import abstractmethod

from playwright.async_api import Page

from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.Base.PlayStatus import PlayStatus


class VuqqPlayer(PlaywrightPlayer):
    @abstractmethod
    async def play(self, solution) -> PlayStatus:
        pass

    # noinspection PyBroadException
    @staticmethod
    async def get_play_status(page: Page, *, success_message: str = None, success_selector: str = None) -> PlayStatus:
        try:
            await page.wait_for_selector(f"text={success_message}", timeout=1000)
            await page.locator('alert-comp button:has-text("Nouvelle partie")').click()
            return PlayStatus.SUCCESS
        except Exception:
            pass

        try:
            await page.wait_for_selector(success_selector, timeout=1000)
            return PlayStatus.SUCCESS
        except Exception:
            return PlayStatus.FAILED_NO_SUCCESS_SELECTOR
