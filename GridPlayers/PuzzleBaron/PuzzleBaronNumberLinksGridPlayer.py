from time import sleep

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.PlaywrightGridPlayer import PlaywrightGridPlayer


class PuzzleBaronNumberLinksGridPlayer(PlaywrightGridPlayer):
    def play(self, solution: Grid):
        page = self.browser.pages[0]
        grid_box_divs = page.query_selector_all('div.gridbox')
        numbers = [int(inner_text) if (inner_text := number_div.inner_text()) else -1 for number_div in grid_box_divs]

        numbers_processed = set()
        for start_position, start_value in solution:
            if numbers[solution.get_index_from_position(start_position)] == -1 or start_value in numbers_processed:
                continue
            numbers_processed.add(start_value)
            positions_processed = {start_position}
            self.mouse_move(page.mouse, solution, start_position, grid_box_divs)
            self.mouse_down(page.mouse)
            next_position = self._next_position(solution, start_position, start_value, positions_processed)
            while next_position:
                positions_processed.add(next_position)
                self.mouse_move(page.mouse, solution, next_position, grid_box_divs)
                next_position = self._next_position(solution, next_position, start_value, positions_processed)
        self.mouse_up(page.mouse)
        sleep(20)

    def _next_position(self, solution: Grid[int], start_position: Position, start_value: int, positions_processed: set[Position]) -> Position:
        return next((neighbor_position for neighbor_position in solution.neighbors_positions(start_position) if neighbor_position not in positions_processed and solution[neighbor_position] == start_value), None)
