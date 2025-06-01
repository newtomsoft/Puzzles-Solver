from time import sleep

from GridPlayers.GridPlayer import GridPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobileGridPlayer import PuzzlesMobileGridPlayer


class PuzzleHitoriGridPlayer(GridPlayer, PuzzlesMobileGridPlayer):
        def play(self, solution):
        page = self.browser.pages[0]
        cells = page.query_selector_all("div.cell.selectable")
        for index, _ in [(solution.get_index_from_position(position), value) for position, value in solution if not value]:
            cells[index].click()

        cls.submit_score(page)
        sleep(60)
