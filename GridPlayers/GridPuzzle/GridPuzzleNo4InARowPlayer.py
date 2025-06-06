from GridPlayers.PlaywrightPlayer import PlaywrightPlayer
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class GridPuzzleNo4InARowPlayer(PuzzlesMobilePlayer, PlaywrightPlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = self._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")
        previous_value = False
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            class_attr = cells[index].get_attribute('class')
            if 'x1' in class_attr or 'o1' in class_attr:
                continue
            if value == previous_value:
                cells[index].click()
            else:
                cells[index].click(click_count=2)
            previous_value = value

        self.close()
        self._process_video(video, "no4InARow", rectangle, 0)
