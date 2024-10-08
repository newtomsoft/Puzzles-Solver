from z3 import *

from get_from_url import get_from_hitoriconquest
from propagation import propagation


def print_proposition():
    for r0 in range(rows_number):
        for c0 in range(columns_number):
            print("□" if proposition_grid[r0][c0] else "■", end=' ')
        print()
    print('')


def print_dot():
    print('.', end='')
    if proposition_count % 100 == 0:
        print()


if __name__ == '__main__':
    pass
else:
    exit(0)

is_print_dot = False
is_print_proposition = True
grid_txt = '''
8	8	3	8	7	2	7	6	4	7	6	1	4	5	3	2	4	3	2	3	1	4	7	8	7	2	6	5	8	7	6	2	5	7	4	8	2	3	4	7	2	8	6	7	5	5	4	3	3	7	1	3	6	8	2	5	6	1	5	3	4	3	8	2
'''
# url = input("url ?")
url = "https://hitoriconquest.com/?puzzle_id=14725"
# grid_txt = get_from_hitoriconquest(url)

if '\n' in grid_txt.strip():
    grid = [[int(cell) for cell in row] for row in grid_txt.strip().split("\n")]
else:
    # assuming grid is square
    grid_txt = grid_txt.strip().split()
    rows_number = int(len(grid_txt) ** 0.5)
    columns_number = rows_number
    grid = [[int(grid_txt[i * columns_number + j]) for j in range(columns_number)] for i in range(rows_number)]
rows_number = len(grid)
columns_number = len(grid[0])
grid_z3 = [[Bool(f"grid_{i}_{j}") for j in range(columns_number)] for i in range(rows_number)]
right_link_z3 = [[Bool(f"rl_{i}_{j}") for j in range(columns_number)] for i in range(rows_number)]
left_link_z3 = [[Bool(f"ll_{i}_{j}") for j in range(columns_number)] for i in range(rows_number)]
down_link_z3 = [[Bool(f"dl_{i}_{j}") for j in range(columns_number)] for i in range(rows_number)]
up_link_z3 = [[Bool(f"ul_{i}_{j}") for j in range(columns_number)] for i in range(rows_number)]

right_link = [[False for _ in range(columns_number)] for _ in range(rows_number)]
down_link = [[False for _ in range(columns_number)] for _ in range(rows_number)]
left_link = [[False for _ in range(columns_number)] for _ in range(rows_number)]
up_link = [[False for _ in range(columns_number)] for _ in range(rows_number)]

solver = Solver()

white_for_unique_in_row_and_column = []
for r0 in range(rows_number):
    for c0 in range(columns_number):
        unique_in_row = all(grid[r0][c0] != grid[r0][c1] for c1 in range(columns_number) if c1 != c0)
        unique_in_column = all(grid[r0][c0] != grid[r1][c0] for r1 in range(rows_number) if r1 != r0)
        if unique_in_row and unique_in_column:
            white_for_unique_in_row_and_column.append(grid_z3[r0][c0])
solver.add(white_for_unique_in_row_and_column)

black_if_white_for_same_number_in_row_and_column = []
for r0 in range(rows_number):
    for c0 in range(columns_number):
        for c1 in range(c0 + 1, columns_number):
            if grid[r0][c0] == grid[r0][c1]:
                black_if_white_for_same_number_in_row_and_column.append(Implies(grid_z3[r0][c0], Not(grid_z3[r0][c1])))
        for r1 in range(r0 + 1, rows_number):
            if grid[r0][c0] == grid[r1][c0]:
                black_if_white_for_same_number_in_row_and_column.append(Implies(grid_z3[r0][c0], Not(grid_z3[r1][c0])))
solver.add(black_if_white_for_same_number_in_row_and_column)

# for r in range(rows_number):
#     solver.add(Distinct([grid_z3[r][c] for c in range(columns_number)]))
# for c in range(columns_number):
#     solver.add(Distinct([grid_z3[r][c] for r in range(rows_number)]))

white_for_unique_in_row_and_column = []
for r in range(rows_number):
    for c in range(columns_number):
        if r > 0:
            white_for_unique_in_row_and_column.append(Implies(Not(grid_z3[r][c]), grid_z3[r - 1][c]))
        if r < rows_number - 1:
            white_for_unique_in_row_and_column.append(Implies(Not(grid_z3[r][c]), grid_z3[r + 1][c]))
        if c > 0:
            white_for_unique_in_row_and_column.append(Implies(Not(grid_z3[r][c]), grid_z3[r][c - 1]))
        if c < columns_number - 1:
            white_for_unique_in_row_and_column.append(Implies(Not(grid_z3[r][c]), grid_z3[r][c + 1]))
solver.add(white_for_unique_in_row_and_column)

proposition_count = 0
solution_found = False
while solver.check() == sat:
    model = solver.model()
    proposition_count += 1
    proposition_grid = [[is_true(model.eval(grid_z3[i][j])) for j in range(columns_number)] for i in range(rows_number)]
    proposition_grid_z3 = [[model.eval(grid_z3[i][j]) for j in range(columns_number)] for i in range(rows_number)]
    whites_not_separated, visited_cells = propagation(proposition_grid)

    if is_print_proposition:
        print_proposition()

    if whites_not_separated:
        solution_found = True
        break

    if is_print_dot:
        print_dot()

    constraints_to_add = [grid_z3[r][c] if proposition_grid[r][c] else Not(grid_z3[r][c])
                          for r in range(rows_number) for c in range(columns_number)]
    solver.add(Not(And(constraints_to_add)))

print('\n')
print("proposition count:", proposition_count)
if solution_found:
    print("Solution trouvée :")
    print_proposition()
