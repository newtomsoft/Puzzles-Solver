from time import sleep

from Domain.Board.Direction import Direction
from GridPlayers.PuzzleMobiles.PuzzlesMobilePlayer import PuzzlesMobilePlayer


class PuzzleThermometersPlayer(PuzzlesMobilePlayer):
    def play(self, solution):
        page = self.browser.pages[0]
        cells = page.locator(".cell:not(.task)")
        cells_all = cells.all()
        matrix_cells = sorted(
            [cell_div for cell_div in cells_all if 'selectable' in cell_div.get_attribute('class')],
            key=lambda div: (int(div.get_attribute('style').split('top:')[1].split('px')[0]), int(div.get_attribute('style').split('left:')[1].split('px')[0]))
        )
        for position, value in solution:
            index = position.r * solution.columns_number + position.c
            box = matrix_cells[index].bounding_box()
            if value == Direction.down():
                page.mouse.move(box['x'] + box['width'] // 2, box['y'] + box['height'])
                page.mouse.down()
                page.mouse.up()
            elif value == Direction.right():
                page.mouse.move(box['x'] + box['width'], box['y'] + box['height'] // 2)
                page.mouse.down()
                page.mouse.up()
        self.submit_score(page)
        sleep(3)
