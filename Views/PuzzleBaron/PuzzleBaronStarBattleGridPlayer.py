from time import sleep

from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class PuzzleBaronStarBattlePlayer(PlaywrightPlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        grid_box_divs = page.query_selector_all('div.box')

        for position, _ in [(position, value) for position, value in solution if value]:
            index = solution.get_index_from_position(position)
            grid_box_divs[index].click(click_count=2)

        sleep(20)
