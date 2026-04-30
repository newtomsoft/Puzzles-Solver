from Domain.Board.Direction import Direction
from Domain.Board.IslandsGrid import IslandGrid
from Domain.Board.Position import Position
from GridPlayers.GridPuzzle.Base.GridPuzzleCanvasPlayer import GridPuzzleCanvasPlayer
from GridPlayers.Base.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleObitaruPlayer(PlaywrightPlayer, GridPuzzleCanvasPlayer):
    game_name = "obitaru"

    async def play(self, solution: IslandGrid):
        if solution.is_empty():
            return
        cell_height, cell_width, page, x0, y0 = await self._get_canvas_data(solution.columns_number, solution.rows_number)
        video, rectangle = await self._get_data_video_viewport(page)

        # Draw each rectangle clockwise: top → right → bottom → left
        drawn_segments = set()
        for r1, c1, r2, c2 in solution.rectangles:
            # Top edge: left to right
            for c in range(c1, c2):
                pos = Position(r1, c)
                seg = (pos, Direction.right())
                if seg not in drawn_segments:
                    drawn_segments.add(seg)
                    await self._trace_direction_from_position(pos, Direction.right(), page, cell_width, cell_height, x0, y0)

            # Right edge: top to bottom
            for r in range(r1, r2):
                pos = Position(r, c2)
                seg = (pos, Direction.down())
                if seg not in drawn_segments:
                    drawn_segments.add(seg)
                    await self._trace_direction_from_position(pos, Direction.down(), page, cell_width, cell_height, x0, y0)

            # Bottom edge: right to left
            for c in range(c2, c1, -1):
                pos = Position(r2, c)
                seg = (pos, Direction.left())
                if seg not in drawn_segments:
                    drawn_segments.add(seg)
                    await self._trace_direction_from_position(pos, Direction.left(), page, cell_width, cell_height, x0, y0)

            # Left edge: bottom to top
            for r in range(r2, r1, -1):
                pos = Position(r, c1)
                seg = (pos, Direction.up())
                if seg not in drawn_segments:
                    drawn_segments.add(seg)
                    await self._trace_direction_from_position(pos, Direction.up(), page, cell_width, cell_height, x0, y0)

        await self.close()
        await self._process_video(video, rectangle)
