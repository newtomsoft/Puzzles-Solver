from time import sleep

from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class PuzzleBaronLaserGridsGridPlayer(PlaywrightGridPlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        grid_box_divs = page.query_selector_all('div.gridbox')

        for position, _ in [(position, value) for position, value in solution if value]:
            index = solution.get_index_from_position(position)
            grid_box_divs[index].click()

        sleep(20)
