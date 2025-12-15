from time import sleep

from Domain.Board.Grid import Grid
from Domain.Puzzles.Pipes.PipeShapeTransition import PipeShapeTransition
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzlePipesPlayer(PuzzlesMobilePlayer):
    def play(self, solution: Grid[PipeShapeTransition]):
        page = self.browser.pages[0]
        cells = page.query_selector_all("div.selectable")
        for position, pipe_shape_transition in solution:
            index = position.r * solution.columns_number + position.c
            cells[index].click(click_count=pipe_shape_transition.clockwise_rotation)

        sleep(2)
        self.submit_score(page)
        sleep(3)
