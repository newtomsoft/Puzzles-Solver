from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class KrazyDadDumplingsGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page)
        html_page = page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        canvas = soup.find('canvas', id='puzzlecontainer')
        #save canvas to image
        with(open('canvas.png', 'wb')) as file:
            file.write(page.screenshot())
        pass

grid_provider = KrazyDadDumplingsGridProvider()
grid_provider.get_grid("https://krazydad.com/play/dumplings/?kind=6x6_dumps&volumeNumber=1&bookNumber=1&puzzleNumber=1")