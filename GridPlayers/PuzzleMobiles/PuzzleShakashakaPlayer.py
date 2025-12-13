from time import sleep

from Domain.Board.Grid import Grid
from Domain.Puzzles.Shakashaka.ShakashakaSolver import ShakashakaCellType
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleShakashakaPlayer(PuzzlesMobilePlayer):
    def play(self, solution: Grid):
        page = self.browser.pages[0]

        cells = page.locator('div.cell, div.shakashaka-task-cell')
        box = cells.nth(0).bounding_box()
        w = box["width"]
        h = box["height"]

        for position, value in [(pos, val) for pos, val in solution if val not in {ShakashakaCellType.BLACK_FULL, ShakashakaCellType.WHITE_FULL}]:
            idx = position.r * solution.columns_number + position.c
            cell = cells.nth(idx)
            if value == ShakashakaCellType.WHITE_BR:
                cell.click(position={"x": w * 0.15, "y": h * 0.15})
                continue
            if value == ShakashakaCellType.WHITE_BL:
                cell.click(position={"x": w * 0.85, "y": h * 0.15})
                continue
            if value == ShakashakaCellType.WHITE_TL:
                cell.click(position={"x": w * 0.85, "y": h * 0.85})
                continue
            cell.click(position={"x": w * 0.15, "y": h * 0.85})

        self.submit_score(page)
        sleep(3)
