from bs4 import BeautifulSoup
from playwright.sync_api import BrowserContext

from GridProviders.GridProvider import GridProvider
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from GridProviders.PuzzlesMobileGridProvider import PuzzlesMobileGridProvider


class PuzzleNonogramGridProvider(GridProvider, PlaywrightGridProvider, PuzzlesMobileGridProvider):
    def get_grid(self, url: str):
        return self.with_playwright(self.scrap_grid, url)

    def scrap_grid(self, browser: BrowserContext, url):
        page = browser.pages[0]
        page.goto(url)
        self.new_game(page, 'div.task-cell')
        html_page = page.content()
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
