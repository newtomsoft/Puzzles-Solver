from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleHakoiriPlayer(PlaywrightPlayer):
    game_name = "hakoiri"

    def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = self._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")
        for position_index, shape in [(position.r * solution.columns_number + position.c, self._convert_to_shape(value)) for position, value in solution if value > 0]:
            if cells[position_index].text_content() == '.':
                continue
            cells[position_index].click()
            keyboard_div = page.locator('#keyboard')
            if keyboard_div is None:
                continue
            shape_div = keyboard_div.locator(f'div.{shape}').first
            shape_div.click()

        self.close()
        self._process_video(video, rectangle, 0)

    @staticmethod
    def _convert_to_shape(value: int):
        if value == 1:
            return 'circle'
        elif value == 2:
            return 'square'
        else:
            return 'triangle'
