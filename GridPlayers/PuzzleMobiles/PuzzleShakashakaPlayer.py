from time import sleep

from Domain.Board.Grid import Grid
from Domain.Puzzles.Shakashaka.ShakashakaSolver import ShakashakaSolver
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleShakashakaPlayer(PuzzlesMobilePlayer):
    def play(self, solution: Grid):
        page = self.browser.pages[0]

        cells = page.locator('div.cell, div.shakashaka-task-cell')
        box = cells.nth(0).bounding_box()
        w = box["width"]
        h = box["height"]

        for position, value in [(pos, val) for pos, val in solution if val not in {ShakashakaSolver.full_black, ShakashakaSolver.full_white}]:
            idx = position.r * solution.columns_number + position.c
            cell = cells.nth(idx)
            if value == 1:
                cell.click(position={"x": w * 0.15, "y": h * 0.15})
                continue
            if value == 2:
                cell.click(position={"x": w * 0.85, "y": h * 0.15})
                continue
            if value == 3:
                cell.click(position={"x": w * 0.85, "y": h * 0.85})
                continue
            cell.click(position={"x": w * 0.15, "y": h * 0.85})

        self.submit_score(page)
        sleep(3)
