from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from GridPlayers.Base.PlayStatus import PlayStatus
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleMarutaringuPlayer(PlaywrightPlayer):
    game_name = "marutaringu"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")

        # Build the cycle path by following adjacent black cells
        path = self._build_path(solution)

        for position in path:
            index = position.r * solution.columns_number + position.c
            await cells[index].click()

        await self.close()
        await self._process_video(video, rectangle, 0)
        return PlayStatus.SUCCESS

    @staticmethod
    def _build_path(solution: Grid) -> list[Position]:
        black_cells = {position for position, value in solution if value == 1}
        if not black_cells:
            return []

        # Pick a starting cell
        start = next(iter(black_cells))
        path = [start]
        visited = {start}

        current = start
        while True:
            neighbors = []
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = current.r + dr, current.c + dc
                npos = Position(nr, nc)
                if npos in black_cells and npos not in visited:
                    neighbors.append(npos)

            if not neighbors:
                break

            next_pos = neighbors[0]
            path.append(next_pos)
            visited.add(next_pos)
            current = next_pos

        return path
