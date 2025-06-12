from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleHashiPlayer(PlaywrightPlayer):
    def play(self, solution: IslandGrid):
        page = self.browser.pages[0]
        video, rectangle = self._get_data_video_viewport(page)
        cells = page.locator(".islands")
        for index, island in enumerate(solution.islands.values()):
            box = cells.nth(index).bounding_box()
            for direction, (position, value) in island.direction_position_bridges.items():
                if direction == Direction.down():
                    page.mouse.move(box['x'] + box['width'] // 2, box['y'] + box['height'] + 5)
                    for _ in range(value):
                        page.mouse.down()
                        page.mouse.up()
                elif direction == Direction.right():
                    page.mouse.move(box['x'] + box['width'] + 5, box['y'] + box['height'] // 2)
                    for _ in range(value):
                        page.mouse.down()
                        page.mouse.up()

        self.close()
        self._process_video(video, "hashi", rectangle, 0)
