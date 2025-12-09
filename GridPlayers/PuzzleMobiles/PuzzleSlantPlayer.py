from time import sleep

from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleSlantPlayer(PuzzlesMobilePlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        cell_elements = page.query_selector_all('div.cell')

        for r in range(solution.rows_number):
            for c in range(solution.columns_number):
                target_val = solution[r][c]

                idx = r * solution.columns_number + c
                element = cell_elements[idx]

                element.click(button="left") if target_val == 1 else element.click(button="right")


        self.submit_score(page)
        sleep(3)
