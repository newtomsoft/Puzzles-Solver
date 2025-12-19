from bs4 import BeautifulSoup
from playwright.async_api import BrowserContext

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobile.Base.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleNonogramsGridProvider(PlaywrightGridProvider, PuzzlesMobileGridProvider):
    async def get_grid(self, url: str):
        return await self.with_playwright(self.scrap_grid, url)

    async def scrap_grid(self, browser: BrowserContext, url):
        page = await self.open_page(browser, url)
        await self.new_game(page, 'div.task-cell')
        html_page = await page.content()
        soup = BeautifulSoup(html_page, 'html.parser')
        task_top = soup.find('div', id='taskTop')
        numbers_top = self._get_numbers(task_top)
        task_left = soup.find('div', id='taskLeft')
        numbers_left = self._get_numbers(task_left)
        return {'top': numbers_top, 'left': numbers_left}

    @staticmethod
    def _get_numbers(task):
        numbers: list[list[int]] = []
        for task_group in task.find_all('div', class_='task-group'):
            numbers.append([])
            cells = task_group.find_all('div', class_='task-cell selectable')
            for cell in cells:
                numbers[-1].append(int(cell.get_text()))
        return numbers
