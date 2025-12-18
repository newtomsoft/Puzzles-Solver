from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleKakurasuGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        await page.goto(url)
        await self.new_game(page, 'div.cell')
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        counters_side = soup.find('div', class_='side-counters')
        numbers_side = self._get_numbers(counters_side)
        counters_top = soup.find('div', class_='top-counters')
        numbers_top = self._get_numbers(counters_top)
        return {'side': numbers_side, 'top': numbers_top}

    @staticmethod
    def _get_numbers(counters) -> list[int]:
        numbers: list[int] = []
        for sc in counters.find_all('span', class_='sc2'):
            numbers.append(int(sc.get_text()))
        return numbers
