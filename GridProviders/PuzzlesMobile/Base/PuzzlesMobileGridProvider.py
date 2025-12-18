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
        await PuzzlesMobileGridProvider._handle_consent_modals(page)
        await PuzzlesMobileGridProvider._update_robot_value(page)

        url_object = urlparse(page.url)
        if 'specid=' in url_object.query:
            return

        new_game_button = page.locator("#btnNew")
        await new_game_button.click(force=True)
        await page.wait_for_selector(selector_to_waite)

        await PuzzlesMobileGridProvider._handle_consent_modals(page)

    @staticmethod
    async def _update_robot_value(page: Page):
        await page.evaluate("""() => {
            const robot = document.getElementById('robot');
            if (robot) {
                robot.value = '1';
            }
        }""")

    @staticmethod
    async def _handle_consent_modals(page: Page):
        await page.add_style_tag(content="""
            #qc-cmp2-container, #snigel-cmp-framework, .snigel-cmp-framework, .robot-animation, #robot, .fc-ab-root {
                display: none !important;
                visibility: hidden !important;
                pointer-events: none !important;
                z-index: -10000 !important;
            }
        """)
