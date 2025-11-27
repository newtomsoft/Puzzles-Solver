from Domain.Board.Grid import Grid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleSudokuPlayer(PlaywrightPlayer):
    game_name = "sudoku"

    def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = self._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")

        for position, solution_value in solution:
            index = position.r * solution.columns_number + position.c
            if index >= len(cells):
                break
                
            cell = cells[index]
            
            is_readonly = cell.get_attribute("data-readonly") == "1"
            if is_readonly:
                continue
                
            current_value = cell.get_attribute("data-val")
            if current_value == str(solution_value):
                continue

            cell.click()
            page.keyboard.press(str(solution_value))

        self.close()
        self._process_video(video, rectangle, 0)
