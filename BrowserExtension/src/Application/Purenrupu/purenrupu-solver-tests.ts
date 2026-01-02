import assert from 'assert';
import { PurenrupuSolver } from './purenrupu-solver.js';

// @ts-ignore
import initZ3 from '../../../libs/z3-built.js';
// @ts-ignore
await import('../../../libs/z3-bundle.js');

declare const global: any;
global.initZ3 = initZ3.default || initZ3;

import { drawGridSolution, normalizeGridString } from '../Base/test-utils.js';

function solutionToString(solution: any, grid: number[][]): string {
    return drawGridSolution(solution, grid.length, grid[0].length, (r, c) => {
        return grid[r][c] === 1 ? '·' : null;
    });
}

const _ = 0;

describe('PurenrupuSolver Tests', () => {
    let z3: any;

    beforeAll(async () => {
        const z3Factory = (global as any).Z3;
        z3 = await z3Factory();
    });

    const testCases = [
        {
            name: 'test_solution_5x5',
            grid: [
                [_, _, _, _, 1],
                [_, _, _, _, _],
                [1, _, _, 1, _],
                [_, _, 1, 1, _],
                [_, _, _, _, _],
            ],
            expected:
                ' ┌────────┐  · \n' +
                ' └─────┐  └──┐ \n' +
                ' ·  ┌──┘  ·  │ \n' +
                ' ┌──┘  ·  ·  │ \n' +
                ' └───────────┘ '
        },
        {
            name: 'test_solution_6x6',
            grid: [
                [_, _, 1, _, _, _],
                [_, _, 1, _, _, _],
                [_, _, _, _, _, 1],
                [_, 1, 1, 1, _, _],
                [_, _, _, _, _, _],
                [1, _, _, 1, _, _],
            ],
            expected:
                ' ┌──┐  ·  ┌─────┐ \n' +
                ' │  │  ·  │  ┌──┘ \n' +
                ' │  └─────┘  │  · \n' +
                ' │  ·  ·  ·  └──┐ \n' +
                ' └──┐  ┌─────┐  │ \n' +
                ' ·  └──┘  ·  └──┘ '
        },
        {
            name: 'test_solution_7x7',
            grid: [
                [_, _, _, _, _, _, _],
                [_, _, _, _, 1, _, _],
                [_, _, 1, _, _, _, 1],
                [_, _, _, 1, 1, _, _],
                [_, 1, _, 1, _, _, _],
                [_, 1, _, _, _, 1, _],
                [_, _, _, _, _, _, _],
            ],
            expected:
                ' ┌─────────────────┐ \n' +
                ' │  ┌─────┐  ·  ┌──┘ \n' +
                ' │  │  ·  └─────┘  · \n' +
                ' │  └──┐  ·  ·  ┌──┐ \n' +
                ' │  ·  │  ·  ┌──┘  │ \n' +
                ' │  ·  └─────┘  ·  │ \n' +
                ' └─────────────────┘ '
        },
        {
            name: 'test_solution_8x8',
            grid: [
                [_, _, _, _, _, 1, _, _],
                [_, 1, _, _, _, _, _, _],
                [_, _, _, _, 1, _, _, _],
                [_, _, 1, _, _, _, 1, _],
                [_, 1, _, _, 1, _, 1, _],
                [_, _, _, 1, _, _, _, _],
                [_, _, 1, _, _, 1, _, _],
                [_, _, 1, _, _, _, _, _],
            ],
            expected:
                ' ┌─────┐  ┌──┐  ·  ┌──┐ \n' +
                ' │  ·  │  │  └──┐  │  │ \n' +
                ' └──┐  └──┘  ·  └──┘  │ \n' +
                ' ┌──┘  ·  ┌─────┐  ·  │ \n' +
                ' │  ·  ┌──┘  ·  │  ·  │ \n' +
                ' │  ┌──┘  ·  ┌──┘  ┌──┘ \n' +
                ' │  │  ·  ┌──┘  ·  └──┐ \n' +
                ' └──┘  ·  └───────────┘ '
        },
        {
            name: 'test_solution_10x10',
            skip: true,
            grid: [
                [1, _, _, _, 1, _, _, _, _, _],
                [_, _, _, _, 1, _, 1, _, _, _],
                [_, 1, _, 1, _, _, _, _, 1, _],
                [_, _, _, 1, _, 1, _, _, _, _],
                [_, _, 1, _, _, _, _, 1, _, _],
                [_, _, _, _, _, _, _, 1, _, _],
                [_, 1, _, 1, _, _, _, _, _, 1],
                [_, _, _, _, 1, _, 1, 1, _, _],
                [_, _, 1, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, 1],
            ],
            expected:
                ' ·  ┌─────┐  ·  ┌─────┐  ┌──┐ \n' +
                ' ┌──┘  ┌──┘  ·  │  ·  └──┘  │ \n' +
                ' │  ·  │  ·  ┌──┘  ┌──┐  ·  │ \n' +
                ' │  ┌──┘  ·  │  ·  │  └──┐  │ \n' +
                ' │  │  ·  ┌──┘  ┌──┘  ·  │  │ \n' +
                ' │  └──┐  └──┐  └──┐  ·  └──┘ \n' +
                ' │  ·  │  ·  └──┐  └─────┐  · \n' +
                ' └──┐  └──┐  ·  │  ·  ·  └──┐ \n' +
                ' ┌──┘  ·  └─────┘  ┌──┐  ┌──┘ \n' +
                ' └─────────────────┘  └──┘  · '
        },
        {
            name: 'test_solution_12x12',
            skip: true,
            grid: [
                [_, _, _, _, 1, _, _, _, _, _, _, 1],
                [_, _, _, _, 1, _, _, _, _, 1, _, _],
                [1, _, _, _, _, _, _, 1, _, _, 1, _],
                [_, _, _, _, 1, 1, _, _, _, _, 1, _],
                [_, _, _, 1, _, _, _, _, 1, _, _, _],
                [_, _, _, _, _, _, 1, _, _, _, _, 1],
                [_, _, 1, _, 1, _, 1, 1, _, 1, _, _],
                [1, _, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, 1, _, _, 1, _, 1, _, _, _],
                [_, 1, _, _, 1, _, _, _, _, 1, 1, _],
                [_, _, _, _, _, 1, _, _, _, _, _, _],
                [1, _, _, 1, _, _, _, _, 1, _, _, 1],
            ],
            expected:
                ' ┌────────┐  ·  ┌─────┐  ┌─────┐  · \n' +
                ' └──┐  ┌──┘  ·  └──┐  └──┘  ·  └──┐ \n' +
                ' ·  │  │  ┌────────┘  ·  ┌──┐  ·  │ \n' +
                ' ┌──┘  └──┘  ·  ·  ┌─────┘  │  ·  │ \n' +
                ' └─────┐  ·  ┌──┐  └──┐  ·  │  ┌──┘ \n' +
                ' ┌─────┘  ┌──┘  │  ·  └──┐  └──┘  · \n' +
                ' └──┐  ·  │  ·  │  ·  ·  │  ·  ┌──┐ \n' +
                ' ·  └──┐  └──┐  └─────┐  └──┐  │  │ \n' +
                ' ┌─────┘  ·  └──┐  ·  │  ·  └──┘  │ \n' +
                ' │  ·  ┌──┐  ·  └──┐  └──┐  ·  ·  │ \n' +
                ' └──┐  │  └──┐  ·  └──┐  └──┐  ┌──┘ \n' +
                ' ·  └──┘  ·  └────────┘  ·  └──┘  · '
        }
    ];

    for (const t of testCases) {
        const testFn = (t as any).skip ? it.skip : it;
        testFn(t.name, async () => {
            const ctx = new z3.Context('main');
            const solver = new PurenrupuSolver(ctx, t.grid);
            const solution = await solver.solve();

            assert.ok(solution, "Expected solution but got null");

            const actual = solutionToString(solution, t.grid);
            assert.strictEqual(normalizeGridString(actual), normalizeGridString(t.expected));

            const other = await solver.getOtherSolution();
            assert.strictEqual(other, null, "Expected exactly one solution");
        });
    }
});
