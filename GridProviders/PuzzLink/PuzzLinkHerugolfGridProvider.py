from PuzzleSolver.Board.Grid import Grid
from PuzzleSolver.Puzzles.Herugolf.HerugolfSolver import HerugolfSolver
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider


class PuzzLinkHerugolfGridProvider(PlaywrightGridProvider):
    _BITS = [16, 8, 4, 2, 1]

    async def scrap_grid(self, browser, url):
        return self._parse_url(url)

    @staticmethod
    def _parse_url(url: str) -> Grid:
        if "?" in url:
            path = url.split("?", 1)[1]
        else:
            path = url
        path = path.split("&", 1)[0].split("#", 1)[0]
        parts = [p for p in path.split("/") if p]
        if len(parts) < 4:
            raise ValueError(f"Invalid puzz.link herugolf URL: {url}")
        cols = int(parts[1])
        rows = int(parts[2])
        body = parts[3]

        values = PuzzLinkHerugolfGridProvider._decode_body(body, rows * cols)
        grid_data = []
        for r in range(rows):
            row = []
            for c in range(cols):
                idx = r * cols + c
                row.append(values[idx] if idx < len(values) else None)
            grid_data.append(row)
        return Grid(grid_data)

    @staticmethod
    def _decode_body(body: str, max_cells: int) -> list:
        cells = [{"qnum": -1, "ques": 0} for _ in range(max_cells)]
        pos = 0

        pos = PuzzLinkHerugolfGridProvider._decode_ice(body, cells, max_cells, pos)
        PuzzLinkHerugolfGridProvider._decode_herugolf(body, cells, max_cells, pos)

        result = []
        for c in cells:
            if c["ques"] == 31:
                result.append(HerugolfSolver.cell_hole)
            elif c["qnum"] >= 0:
                result.append(c["qnum"])
            elif c["ques"] == 6:
                result.append(HerugolfSolver.cell_water)
            else:
                result.append(HerugolfSolver.cell_empty)
        return result

    @staticmethod
    def _decode_ice(body: str, cells: list, max_cells: int, pos: int) -> int:
        while pos < len(body):
            char = body[pos]
            val = int(char, 32)
            for bit_idx in range(5):
                cell_idx = pos * 5 + bit_idx
                if cell_idx >= max_cells:
                    return pos + 1
                if val & PuzzLinkHerugolfGridProvider._BITS[bit_idx]:
                    cells[cell_idx]["ques"] = 6
            pos += 1
        return pos

    @staticmethod
    def _decode_herugolf(body: str, cells: list, max_cells: int, pos: int) -> int:
        cell_idx = 0
        while pos < len(body) and cell_idx < max_cells:
            char = body[pos]
            if "0" <= char <= "9":
                cells[cell_idx]["qnum"] = int(char, 16)
                pos += 1
                cell_idx += 1
            elif "a" <= char <= "f":
                cells[cell_idx]["qnum"] = int(char, 16)
                pos += 1
                cell_idx += 1
            elif char == "-":
                if pos + 2 <= len(body):
                    cells[cell_idx]["qnum"] = int(body[pos + 1:pos + 3], 16)
                    pos += 3
                    cell_idx += 1
            elif char == "h":
                cells[cell_idx]["ques"] = 31
                pos += 1
                cell_idx += 1
            elif "i" <= char <= "z":
                cell_idx += int(char, 36) - 18
                pos += 1
                cell_idx += 1
            else:
                pos += 1
                cell_idx += 1
        return pos
