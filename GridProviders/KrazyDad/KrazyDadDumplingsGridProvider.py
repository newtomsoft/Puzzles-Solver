from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import (
    PuzzlesMobileGridProvider,
)


class KrazyDadDumplingsGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        await page.goto(url)
        await self.new_game(page)
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        canvas = soup.find('canvas', id='puzzlecontainer')
        #save canvas to image
        with(open('canvas.png', 'wb')) as file:
            file.write(await page.screenshot())
        pass

grid_provider = KrazyDadDumplingsGridProvider()
grid_provider.get_grid("https://krazydad.com/play/dumplings/?kind=6x6_dumps&volumeNumber=1&bookNumber=1&puzzleNumber=1")