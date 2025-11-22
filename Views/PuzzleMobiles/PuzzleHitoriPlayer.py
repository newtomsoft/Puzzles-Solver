from time import sleep

from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleHitoriPlayer(PuzzlesMobilePlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        cells = page.query_selector_all("div.cell.selectable")
        for index, _ in [(solution.get_index_from_position(position), value) for position, value in solution if not value]:
            cells[index].click()

        self.submit_score(page)
        sleep(60)
