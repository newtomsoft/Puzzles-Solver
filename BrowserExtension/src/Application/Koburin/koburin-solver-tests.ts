import assert from 'assert';
import { KoburinSolver } from './koburin-solver.js';
import { KoburinCell } from '../../Domain/Koburin/koburin-constants.js';

declare const global: any;
// @ts-ignore
const initZ3 = await import('../../../libs/z3-built.js');
global.initZ3 = initZ3.default || initZ3;
// @ts-ignore
await import('../../../libs/z3-bundle.js');

const _ = KoburinCell.EMPTY;

import { drawGridSolution, normalizeGridString } from '../Base/test-utils.js';

function solutionToString(solution: any, grid: number[][]): string {
    return drawGridSolution(solution, grid.length, grid[0].length, (r, c) => {
        const val = grid[r][c];
        if (val >= 0) {
            return val.toString();
        } else if (solution.black[r][c]) {
            return '■';
        }
        return null;
    });
}

describe('KoburinSolver Tests', () => {
    let z3: any;

    beforeAll(async () => {
        z3 = await (global as any).Z3();
    });

    const testCases = [
        {
            name: 'test_solution_3x3_digit_0',
            grid: [
                [_, _, _],
                [_, 0, _],
                [_, _, _],
            ],
            expected:
                ' ┌─────┐ \n' +
                ' │  0  │ \n' +
                ' └─────┘ '
        },
        {
            name: 'test_solution_4x3_digit_1',
            grid: [
                [_, 1, _, _],
                [_, _, _, _],
                [_, _, _, _],
            ],
            expected:
                ' ■  1  ┌──┐ \n' +
                ' ┌─────┘  │ \n' +
                ' └────────┘ '
        },
        {
            name: 'test_solution_5x5',
            grid: [
                [_, _, 0, _, _],
                [_, _, _, _, _],
                [_, 1, _, 1, _],
                [_, _, _, _, _],
                [_, _, _, _, 0],
            ],
            expected:
                ' ┌──┐  0  ┌──┐ \n' +
                ' │  └─────┘  │ \n' +
                ' │  1  ■  1  │ \n' +
                ' │  ┌──┐  ┌──┘ \n' +
                ' └──┘  └──┘  0 '
        },
        {
            name: 'test_solution_8x8',
            grid: [
                [_, _, 0, _, _, 1, _, _],
                [_, _, _, _, _, _, _, _],
                [_, _, 3, _, _, _, _, _],
                [_, _, _, _, _, 0, _, _],
                [0, _, _, _, _, _, _, 0],
                [_, _, _, 1, _, _, _, _],
                [_, _, _, _, _, _, _, _],
                [0, _, _, _, _, 0, _, _],
            ],
            expected:
                ' ┌──┐  0  ┌──┐  1  ┌──┐ \n' +
                ' │  └─────┘  │  ■  │  │ \n' +
                ' │  ■  3  ■  └─────┘  │ \n' +
                ' └──┐  ■  ┌──┐  0  ┌──┘ \n' +
                ' 0  │  ┌──┘  └──┐  │  0 \n' +
                ' ┌──┘  │  1  ■  │  └──┐ \n' +
                ' └──┐  └─────┐  └──┐  │ \n' +
                ' 0  └────────┘  0  └──┘ ',
        },
        {
            name: 'test_solution_12x12_evil_6r695',
            grid: [
                [0, _, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, 0, _, _, _, _],
                [_, _, 3, _, _, 0, _, _, 0, _, _, 0],
                [_, _, _, _, _, _, _, _, _, _, _, _],
                [_, 1, _, _, _, _, _, _, _, _, 0, _],
                [_, _, _, _, _, _, _, _, _, _, _, _],
                [_, _, 1, _, 0, _, 1, _, _, 0, _, _],
                [_, _, _, _, _, _, _, 1, _, _, _, _],
                [_, _, _, _, _, 1, _, _, _, 0, _, _],
                [_, _, _, _, _, _, _, _, _, _, 1, _],
                [_, 1, _, _, 1, _, _, 2, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _, _],
            ],
            multiple: 6,
            expected:
                ' 0  ┌─────┐  ■  ┌────────┐  ┌─────┐ \n' +
                ' ┌──┘  ■  └──┐  └──┐  0  └──┘  ┌──┘ \n' +
                ' │  ■  3  ■  │  0  └──┐  0  ┌──┘  0 \n' +
                ' └─────┐  ┌──┘  ┌──┐  └──┐  └─────┐ \n' +
                ' ■  1  │  │  ┌──┘  │  ■  └──┐  0  │ \n' +
                ' ┌─────┘  │  └──┐  └──┐  ┌──┘  ┌──┘ \n' +
                ' └──┐  1  │  0  │  1  └──┘  0  └──┐ \n' +
                ' ■  │  ■  └─────┘  ■  1  ┌─────┐  │ \n' +
                ' ┌──┘  ┌──┐  ■  1  ┌─────┘  0  └──┘ \n' +
                ' │  ■  │  └─────┐  └────────┐  1  ■ \n' +
                ' │  1  └──┐  1  │  ■  2  ■  └─────┐ \n' +
                ' └────────┘  ■  └─────────────────┘ ',
            skip: true
        }
    ];

    for (const t of (testCases as any[])) {
        const testFn = t.skip ? it.skip : it;
        testFn(t.name, async () => {
            const ctx = new z3.Context('main');
            const solver = new KoburinSolver(ctx, t.grid);
            const solution = await solver.solve();

            assert.ok(solution, "Expected solution but got null");

            if (t.multiple) {
                let count = 1;
                while (count < t.multiple) {
                    const currentSol = await solver.getOtherSolution();
                    assert.ok(currentSol, `Expected solution #${count + 1} but got null`);
                    count++;
                }
                const noMore = await solver.getOtherSolution();
                assert.strictEqual(noMore, null, "Expected no more solutions");
            } else {
                const actual = solutionToString(solution, t.grid);
                assert.strictEqual(normalizeGridString(actual), normalizeGridString(t.expected!));

                const other = await solver.getOtherSolution();
                assert.strictEqual(other, null, "Expected exactly one solution");
            }
        });
    }
});
