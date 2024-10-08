class ShapePrinter:
    @staticmethod
    def print_shape_with_background(shape):
        r = max(r for r, c in shape) + 1
        c = max(c for r, c in shape) + 1
        empty_cell = '   '
        full_cell = f'\033[47m{empty_cell}\033[0m'
        matrix = [[full_cell if (x, y) in shape else empty_cell for y in range(-1, c)] for x in range(-1, r)]
        for row in matrix:
            print(''.join(row))
        print()
