from playwright.async_api import BrowserContext

from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleSeeThroughPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    game_name = "see_through"
    def __init__(self, browser: BrowserContext):
        super().__init__(browser)
        self._island_grid_solution: IslandGrid | None = None

    async def play(self, solution: IslandGrid):
        self._island_grid_solution = solution
        columns_number, rows_number = solution.columns_number - 1, solution.rows_number - 1
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(columns_number, rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        pairs_positions = self._find_unique_different_pairs_positions()
        await self._draw_regions(cell_height, cell_width, page, pairs_positions, x0, y0)

        await self.close()
        self._process_video(video, rectangle)

    def _find_unique_different_pairs_positions(self) -> list[tuple[Position, Position]]:
        pairs: list[tuple[Position, Position]] = list()
        
        islands = self._island_grid_solution.islands
        for island, position in [(island, position) for position, island in islands.items() if not island.has_no_bridge()]:
            if Direction.right() in island.direction_position_bridges.keys() and island.direction_position_bridges[Direction.right()][1] == 1 and position not in self._island_grid_solution.edge_up_positions() + self._island_grid_solution.edge_down_positions() + self._island_grid_solution.edge_right_positions():
                pairs.append((position.up, position))
            if Direction.down() in island.direction_position_bridges.keys() and island.direction_position_bridges[Direction.down()][1] == 1 and position not in self._island_grid_solution.edge_left_positions() + self._island_grid_solution.edge_right_positions() + self._island_grid_solution.edge_down_positions():
                pairs.append((position.left, position))

        return pairs

    async def _draw_regions(self, cell_height, cell_width, page, pairs_positions: list[tuple[Position, Position]], x0, y0):
        for position0, position1 in pairs_positions:
            await self._click(position0.direction_to(position1), position0, page, cell_width, cell_height, x0, y0)

    @staticmethod
    async def _click(direction: Direction, position, page, cell_width, cell_height, x0, y0):
        if direction == Direction.right():
            await page.mouse.move(x0 + cell_width + position.c * cell_width, y0 + cell_height / 2 + position.r * cell_height)
            await page.mouse.down()
            await page.mouse.up()
            return
        if direction == Direction.down():
            await page.mouse.move(x0 + cell_width / 2 + position.c * cell_width, y0 + cell_height + position.r * cell_height)
            await page.mouse.down()
            await page.mouse.up()
            return
        raise ValueError(f"unexpected direction: {direction}")