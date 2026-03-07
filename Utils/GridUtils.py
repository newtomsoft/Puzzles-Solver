from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


def region_grid_to_string(grid: Grid) -> str:
    rows = grid.rows_number
    cols = grid.columns_number

    char_map = {
        (False, False, False, False): ' ',
        (False, False, False, True): '╶',
        (False, False, True, False): '╴',
        (False, False, True, True): '─',
        (False, True, False, False): '╷',
        (False, True, False, True): '┌',
        (False, True, True, False): '┐',
        (False, True, True, True): '┬',
        (True, False, False, False): '╵',
        (True, False, False, True): '└',
        (True, False, True, False): '┘',
        (True, False, True, True): '┴',
        (True, True, False, False): '│',
        (True, True, False, True): '├',
        (True, True, True, False): '┤',
        (True, True, True, True): '┼',
    }

    def get_val(r, c):
        if 0 <= r < rows and 0 <= c < cols:
            return grid[r][c]
        return -1

    result = []
    for r in range(rows + 1):
        line_chars = ['']
        for c in range(cols + 1):
            tl = get_val(r - 1, c - 1)
            tr = get_val(r - 1, c)
            bl = get_val(r, c - 1)
            br = get_val(r, c)

            up = (tl != tr)
            down = (bl != br)
            left = (tl != bl)
            right = (tr != br)

            line_chars.append(char_map[(up, down, left, right)])

            if c < cols:
                val_above = get_val(r - 1, c)
                val_below = get_val(r, c)
                if val_above != val_below:
                    line_chars.append('─')
                else:
                    line_chars.append(' ')

        line_chars.append('\n')
        result.append("".join(line_chars))

    return "".join(result)
