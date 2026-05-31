from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Board.Position import Position
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleShimaguniPlayer(PlaywrightPlayer):
    game_name = "shimaguni"

    async def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")
        
        # Identify blocks of connected black cells (1s)
        visited = set()
        for r in range(solution.rows_number):
            for c in range(solution.columns_number):
                pos = Position(r, c)
                if solution[pos] == 1 and pos not in visited:
                    # Found a new block, traverse it
                    block = self._get_connected_black_cells(solution, pos, visited)
                    # Process the entire block
                    for p in block:
                        index = p.r * solution.columns_number + p.c
                        await cells[index].click()

        await self.close()
        await self._process_video(video, rectangle, 0)

    def _get_connected_black_cells(self, solution: Grid, start_pos: Position, visited: set) -> set[Position]:
        block = set()
        stack = [start_pos]
        while stack:
            pos = stack.pop()
            if pos in visited:
                continue
            visited.add(pos)
            block.add(pos)
            for neighbor in solution.neighbors_positions(pos):
                if solution[neighbor] == 1 and neighbor not in visited:
                    stack.append(neighbor)
        return block
