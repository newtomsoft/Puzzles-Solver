import re
from typing import Any


class PuzzLinkLightupGridEditor:
    _puzzlink_url = "https://puzz.link/p?{game}/{width}/{height}/{body}"

    def __init__(self, data_game: dict[str, Any]):
        self._data_game = data_game
        self._rows = data_game['rows_number']
        self._cols = data_game['columns_number']

        number_constraints = {}
        for k, v in data_game.get('number_constraints', {}).items():
            if isinstance(k, str):
                match = re.search(r'\(?(\d+),\s*(\d+)\)?', k)
                if match:
                    pos = (int(match.group(1)), int(match.group(2)))
                    number_constraints[pos] = v
            else:
                number_constraints[(k[0], k[1])] = v

        self._number_constraints = number_constraints

    def get_url(self) -> str:
        qnum_values = [-1] * (self._rows * self._cols)
        for (r, c), val in self._number_constraints.items():
            qnum_values[r * self._cols + c] = val

        body = self._encode4cell(qnum_values, self._rows * self._cols)
        return self._puzzlink_url.format(game="akari", width=self._cols, height=self._rows, body=body)

    @staticmethod
    def _encode4cell(qnum_values: list[int], total_cells: int) -> str:
        result = ""
        skip_acc = 0
        d = 0
        while d < total_cells:
            e = ""
            val = qnum_values[d]

            if val >= 0:
                if d + 1 < total_cells and qnum_values[d + 1] != -1:
                    e = format(val, 'x')
                elif d + 2 < total_cells and qnum_values[d + 2] != -1:
                    e = format(5 + val, 'x')
                    d += 1
                else:
                    e = format(10 + val, 'x')
                    d += 2
            elif val == -2:
                e = "."
            else:
                skip_acc += 1

            if skip_acc == 0:
                result += e
            elif e or skip_acc == 20:
                result += PuzzLinkLightupGridEditor._to_base36(skip_acc + 15) + e
                skip_acc = 0

            d += 1

        if skip_acc > 0:
            result += PuzzLinkLightupGridEditor._to_base36(skip_acc + 15)

        return result

    @staticmethod
    def _to_base36(n: int) -> str:
        digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        if n == 0:
            return "0"
        result = ""
        while n > 0:
            result = digits[n % 36] + result
            n //= 36
        return result
