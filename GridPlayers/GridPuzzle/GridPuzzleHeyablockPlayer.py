from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleHeyablockPlayer(PlaywrightPlayer):
    game_name = "heyablock"

    async def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")

        black_positions = [pos for pos, value in solution if not value]
        black_set = set(black_positions)
        visited = set()
        blocks = []
        for pos in black_positions:
            if pos in visited:
                continue
            block = []
            queue = [pos]
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                block.append(current)
                for neighbor in solution.neighbors_positions(current):
                    if neighbor in black_set and neighbor not in visited:
                        queue.append(neighbor)
            blocks.append(block)

        for block in blocks:
            for pos in block:
                index = pos.r * solution.columns_number + pos.c
                await cells[index].click(click_count=2)

        await self.close()
        await self._process_video(video, rectangle, 0)
