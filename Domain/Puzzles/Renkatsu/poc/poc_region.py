from unittest import TestCase

from z3 import *


def add_single_regions_constraints(solver, matrix, steps: list, regions_size: list, n, m):
    for i in range(n):
        for j in range(m):
            solver.add(matrix[i][j] >= 1)
            solver.add(matrix[i][j] <= len(steps))

    for index, step in enumerate(steps):
        region_id = index + 1
        add_connected_cells_in_region_constraints(solver, matrix, step, regions_size[index], n, m, region_id)


def add_connected_cells_in_region_constraints(solver, matrix, step, region_size: int, n, m, region_id):
    solver.add(z3.Sum([matrix[i][j] == region_id for i in range(n) for j in range(m)]) == region_size)

    for i in range(n):
        for j in range(m):
            solver.add(If(matrix[i][j] == region_id, step[i][j] >= 1, step[i][j] == 0))
    roots = []
    for i in range(n):
        for j in range(m):
            roots.append(And(matrix[i][j] == region_id, step[i][j] == 1))
    solver.add(Or(roots))
    for i in range(len(roots)):
        for j in range(i + 1, len(roots)):
            solver.add(Not(And(roots[i], roots[j])))
    for i in range(n):
        for j in range(m):
            current_step = step[i][j]
            adjacents = []
            if i > 0:
                adjacents.append(And(matrix[i - 1][j] == region_id, step[i - 1][j] == current_step - 1))
            if i < n - 1:
                adjacents.append(And(matrix[i + 1][j] == region_id, step[i + 1][j] == current_step - 1))
            if j > 0:
                adjacents.append(And(matrix[i][j - 1] == region_id, step[i][j - 1] == current_step - 1))
            if j < m - 1:
                adjacents.append(And(matrix[i][j + 1] == region_id, step[i][j + 1] == current_step - 1))

            solver.add(Implies(And(matrix[i][j] == region_id, current_step > 1), Or(adjacents)))


def print_solved(matrix, n, m):
    for i in range(n):
        row = []
        for j in range(m):
            row.append(str(matrix[i][j]) if matrix[i][j] > 0 else '.')
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


def solve_connected_region(n, m) -> int:
    solver = Solver()
    matrix_z3 = [[Int(f'cell_{i}_{j}') for j in range(m)] for i in range(n)]
    step0 = [[Int(f'step0_{i}_{j}') for j in range(m)] for i in range(n)]
    step1 = [[Int(f'step1_{i}_{j}') for j in range(m)] for i in range(n)]
    step2 = [[Int(f'step2_{i}_{j}') for j in range(m)] for i in range(n)]
    step3 = [[Int(f'step3_{i}_{j}') for j in range(m)] for i in range(n)]
    steps = [step0, step1, step2, step3]
    sizes = [10, 3, 2, 1]
    add_single_regions_constraints(solver, matrix_z3, steps, sizes, n, m)

    count = 0
    while solver.check() == sat:
        count += 1
        model = solver.model()
        matrix_solved = [[(model.evaluate(matrix_z3[i][j])).as_long() for j in range(m)] for i in range(n)]
        print_solved(matrix_solved, n, m)
        # step_solved = [[(model.evaluate(steps[0][i][j])).as_long() for j in range(m)] for i in range(n)]
        # print_step_solved(step_solved, n, m)
        exclude(solver, matrix_z3, matrix_solved, n, m)
        # input("Press ENTER to continue...")
    # print("solutions count", count)
    return count


class GeneratorTest(TestCase):
    def test_Toto(self):
        count = solve_connected_region(4, 4)
        self.assertEqual(3400, count)
