from Grid import Grid
from GridProviders.GridProvider import GridProvider


class StringGridProvider(GridProvider):
    def get_grid(self, source: str):
        if '|' and '_' in source:
            matrix = [[cell for cell in row.split('|')] for row in source.strip().split('_')]
            for r in range(len(matrix)):
                row = matrix[r]
                for c in range(len(row)):
                    if "\\" in row[c]:
                        row[c] = [int(part) for part in row[c].split("\\")][::-1]
                    else:
                        row[c] = int(row[c])
            return Grid(matrix)

        if '|' in source:
            matrix = [[row.strip()] for row in source.strip().split('|')]
            matrix_to_return = [[] for _ in range(len(matrix))]
            for r, index in enumerate(range(len(matrix))):
                row = matrix[r]
                row_split = ''.join(row).split()
                for c in row_split:
                    if "\\" in c:
                        row[c] = [int(part) for part in row[c].split("\\")][::-1]
                    else:
                        matrix_to_return[index].append(int(c))
            return Grid(matrix_to_return)

        grid_txt = source.strip().split()
        rows_number = int(len(grid_txt) ** 0.5)
        columns_number = rows_number
        if rows_number * columns_number != len(grid_txt):
            print("Warning: grid cropped to be square")

        matrix = [[int(grid_txt[r * columns_number + c]) if grid_txt[r * columns_number + c].lstrip('-').isnumeric() else grid_txt[r * columns_number + c] for c in range(columns_number)] for r in range(rows_number)]
        return Grid(matrix)
