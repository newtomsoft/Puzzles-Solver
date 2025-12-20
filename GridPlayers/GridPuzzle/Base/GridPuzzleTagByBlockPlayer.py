from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleTagByBlockPlayer(PlaywrightPlayer):
    async def play(self, solution):
        page = self.browser.pages[0]
        video, rectangle = await self._get_data_video_viewport(page)

        cells = await page.query_selector_all("div.g_cell")

        true_positions = {position for position, value in solution if value}

        visited = set()
        blocks = []

        def get_block(start_pos):
            result_block = []
            stack = [start_pos]

            while stack:
                pos = stack.pop()
                if pos in visited or pos not in true_positions:
                    continue

                visited.add(pos)
                result_block.append(pos)

                # Vérifier les 4 voisins adjacents (haut, bas, gauche, droite)
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    neighbor = type(pos)(pos.r + dr, pos.c + dc)
                    if neighbor in true_positions and neighbor not in visited:
                        stack.append(neighbor)

            return result_block

        # Identifier tous les blocs
        for position in true_positions:
            if position not in visited:
                block = get_block(position)
                blocks.append(block)

        # Traiter chaque bloc ligne par ligne
        for block in blocks:
            for position in block:
                index = position.r * solution.columns_number + position.c
                await cells[index].click()

        await self.close()
        self._process_video(video, rectangle, 0)
