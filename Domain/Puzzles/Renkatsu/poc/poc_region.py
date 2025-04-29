from z3 import *


def configure_single_region_constraints(solver, matrix, step, n, m, region_size):

    solver.add(z3.Sum([matrix[i][j] for i in range(n) for j in range(m)]) == region_size)

    for i in range(n):
        for j in range(m):
            solver.add(If(matrix[i][j], step[i][j] >= 1, step[i][j] == 0))
    roots = []
    for i in range(n):
        for j in range(m):
            roots.append(And(matrix[i][j], step[i][j] == 1))
    solver.add(Or(roots))
    for i in range(len(roots)):
        for j in range(i + 1, len(roots)):
            solver.add(Not(And(roots[i], roots[j])))
    for i in range(n):
        for j in range(m):
            current_step = step[i][j]
            adjacents = []
            if i > 0:
                adjacents.append(And(matrix[i - 1][j], step[i - 1][j] == current_step - 1))
            if i < n - 1:
                adjacents.append(And(matrix[i + 1][j], step[i + 1][j] == current_step - 1))
            if j > 0:
                adjacents.append(And(matrix[i][j - 1], step[i][j - 1] == current_step - 1))
            if j < m - 1:
                adjacents.append(And(matrix[i][j + 1], step[i][j + 1] == current_step - 1))

            solver.add(Implies(And(matrix[i][j], current_step > 1), Or(adjacents)))


def print_solved(matrix, n, m):
    for i in range(n):
        row = []
        for j in range(m):
            row.append('X' if matrix[i][j] else '.')
        print(' '.join(row))
    print()


def print_step_solved(matrix, n, m):
    for i in range(n):
        row = []
        for j in range(m):
            row.append(str(matrix[i][j]) if matrix[i][j] > 0 else '.')
        print(' '.join(row))
    print()


def exclude(solver, matrix, matrix_solved, n, m):
    solver.add(Not(And([matrix[i][j] == matrix_solved[i][j] for j in range(m) for i in range(n)])))


def solve_connected_region(n, m):
    solver = Solver()
    matrix_z3 = [[Bool(f'cell_{i}_{j}') for j in range(m)] for i in range(n)]
    step = [[Int(f'step_{i}_{j}') for j in range(m)] for i in range(n)]
    size = 4
    configure_single_region_constraints(solver, matrix_z3, step, n, m, size)

    count = 0
    while solver.check() == sat:
        count += 1
        model = solver.model()
        matrix_solved = [[model.evaluate(matrix_z3[i][j]) for j in range(m)] for i in range(n)]
        step_solved = [[(model.evaluate(step[i][j])).as_long() for j in range(m)] for i in range(n)]
        # print_solved(matrix_solved, n, m)
        # print_step_solved(step_solved, n, m)
        exclude(solver, matrix_z3, matrix_solved, n, m)
        # input("Press ENTER to continue...")
    print("solutions count", count)


solve_connected_region(4, 4)
