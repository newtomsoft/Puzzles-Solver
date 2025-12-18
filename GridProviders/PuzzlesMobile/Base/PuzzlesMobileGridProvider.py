import math
from urllib.parse import urlparse

from bs4 import BeautifulSoup, ResultSet, Tag
from playwright.async_api import BrowserContext, Page


class PuzzlesMobileGridProvider:
    @staticmethod
    async def get_new_html_page(browser: BrowserContext, url) -> str:
        page = browser.pages[0]
        await page.goto(url)
        await PuzzlesMobileGridProvider.new_game(page)
        html_page = await page.content()
        return html_page

    @staticmethod
    def get_puzzle_info_text(soup):
        puzzle_info = soup.find('div', class_='puzzleInfo')
        puzzle_info_text = puzzle_info.text
        return puzzle_info_text

    @staticmethod
    def _scrap_grid_data(html_page: str) -> tuple[ResultSet[Tag], int, BeautifulSoup]:
        soup = BeautifulSoup(html_page, 'html.parser')
        cell_divs = soup.find_all('div', class_='cell')
        matrix_cells = [cell_div for cell_div in cell_divs if 'selectable' in cell_div.get('class', [])]
        cells_count = len(matrix_cells)
        row_count = int(math.sqrt(cells_count))
        return cell_divs, row_count, soup

    @staticmethod
    async def new_game(page: Page, selector_to_waite='div.cell'):
        url_object = urlparse(page.url)
        if 'specid=' in url_object.query:
            return
        new_game_button = page.locator("#btnNew")
        if (await new_game_button.count()) > 0:
            consent_dialog = page.locator("#snigel-cmp-framework")
            if await consent_dialog.count() > 0 and await (accept_button := page.locator("#accept-choices")).count() > 0:
                await accept_button.click()

            agree_button = page.get_by_role("button", name="AGREE", exact=True)
            if await agree_button.count() > 0:
                await agree_button.first.click()

            await new_game_button.click()
            await page.wait_for_selector(selector_to_waite)