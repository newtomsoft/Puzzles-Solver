from time import sleep

from GridPlayers.GridPlayer import GridPlayer


class PuzzleBaronCalcudokuGridPlayer(GridPlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        grid_box_divs = page.query_selector_all('div.gridbox')

        for position, digit in solution:
            index = solution.get_index_from_position(position)
            grid_box_divs[index].click()
            page.keyboard.press(str(digit))

        sleep(20)
