import assert from 'assert';
import { ShirokuroSolver } from './ShirokuroSolver.js';
import { ShirokuroCell } from '../../Domain/Shirokuro/shirokuro-constants.js';
import { drawGridSolution, normalizeGridString } from '../Base/test-utils.js';


declare const global: any;
// @ts-ignore
const initZ3 = await import('../../../libs/z3-built.js');
(global as any).initZ3 = initZ3.default || initZ3;
// @ts-ignore
await import('../../../libs/z3-bundle.js');

// Helper to create string representation of solution
function solutionToString(solution: any, rows: number, cols: number): string {
    return drawGridSolution(solution, rows, cols, (r, c) => null, "\u00b7");
}

const W = ShirokuroCell.WHITE;
const B = ShirokuroCell.BLACK;
const _ = ShirokuroCell.EMPTY;

describe('ShirokuroSolver Tests', () => {
    let z3: any;

    beforeAll(async () => {
        z3 = await (global as any).Z3();
        try {
            z3.setParam('parallel.enable', 'false');
        } catch (e) {
            console.warn("Could not set global parallel.enable in tests", e);
        }
    });

    const testCases = [
        {
            name: 'test_solution_3x3_black_cells',
            grid: [
                [B, _, B],
                [_, _, _],
                [B, _, B],
            ],
            expected:
                ' ┌─────┐ \n' +
                ' │  ·  │ \n' +
                ' └─────┘ '
        },
        {
            name: 'test_solution_5x5_black_cells',
            grid: [
                [B, _, _, B, _],
                [_, _, _, B, B],
                [_, _, _, B, B],
                [B, B, _, _, _],
                [_, B, _, B, _],
            ],
            expected:
                ' ┌────────┐  · \n' +
                ' │  ·  ·  └──┐ \n' +
                ' │  ·  ·  ┌──┘ \n' +
                ' └──┐  ·  │  · \n' +
                ' ·  └─────┘  · '
        },
        {
            name: 'test_solution_5x5_white_cells',
            grid: [
                [W, _, _, W, _],
                [_, _, _, W, W],
                [_, _, _, W, W],
                [W, W, _, _, _],
                [_, W, _, W, _],
            ],
            expected:
                ' ┌────────┐  · \n' +
                ' │  ·  ·  └──┐ \n' +
                ' │  ·  ·  ┌──┘ \n' +
                ' └──┐  ·  │  · \n' +
                ' ·  └─────┘  · '
        },
        {
            name: 'test_solution_3x3_black_n_white_cells',
            grid: [
                [W, _, W],
                [_, _, _],
                [_, B, _],
            ],
            expected:
                ' ┌─────┐ \n' +
                ' │  ·  │ \n' +
                ' └─────┘ '
        },
        {
            name: 'test_solution_4x4_black_n_white_cells',
            grid: [
                [W, _, B, _],
                [_, B, B, W],
                [W, W, B, _],
                [_, _, B, _],
            ],
            expected:
                ' ┌──┐  ┌──┐ \n' +
                ' │  └──┘  │ \n' +
                ' └──┐  ┌──┘ \n' +
                ' ·  └──┘  · '
        },
        {
            name: 'test_solution_10x10_black_cells',
            skip: true,
            grid: [
                [_, B, B, _, _, B, _, B, _, _],
                [_, B, B, _, B, _, _, B, _, B],
                [_, _, _, _, _, _, _, _, _, _],
                [_, B, _, B, B, B, _, B, _, B],
                [_, _, _, _, _, _, _, _, _, _],
                [B, _, _, B, _, _, _, _, B, B],
                [_, _, _, _, _, _, _, B, B, _],
                [B, _, B, _, _, B, _, B, _, _],
                [_, B, B, _, _, _, _, B, _, B],
                [_, B, _, _, _, B, _, _, _, _],
            ],
            expected:
                ' ·  ┌──┐  ·  ·  ┌─────┐  ·  · \n' +
                ' ·  │  └─────┐  │  ·  └─────┐ \n' +
                ' ·  │  ·  ·  │  │  ·  ·  ·  │ \n' +
                ' ·  └─────┐  └──┘  ·  ┌─────┘ \n' +
                ' ·  ·  ·  │  ·  ·  ·  │  ·  · \n' +
                ' ┌────────┘  ·  ·  ·  │  ┌──┐ \n' +
                ' │  ·  ·  ·  ·  ·  ·  └──┘  │ \n' +
                ' └─────┐  ·  ·  ┌─────┐  ·  │ \n' +
                ' ·  ┌──┘  ·  ·  │  ·  └─────┘ \n' +
                ' ·  └───────────┘  ·  ·  ·  · '
        },
        {
            name: 'test_solution_5x5_292p8',
            grid: [
                [B, B, B, _, B],
                [_, W, _, B, B],
                [_, W, W, B, B],
                [_, _, W, W, W],
                [B, B, _, _, _],
            ],
            expected:
                ' ┌───────────┐ \n' +
                ' └──┐  ┌──┐  │ \n' +
                ' ┌──┘  │  └──┘ \n' +
                ' │  ·  └─────┐ \n' +
                ' └───────────┘ '
        },
        {
            name: 'test_solution_10x10_292p8',
            skip: true,
            grid: [
                [_, _, _, W, _, _, W, B, _, _],
                [B, B, B, _, _, W, _, B, B, W],
                [B, _, B, _, B, _, W, W, B, _],
                [_, _, _, B, _, _, W, _, B, _],
                [_, W, B, _, B, _, _, W, _, W],
                [W, W, _, B, _, _, _, _, W, _],
                [_, W, _, _, W, B, _, B, _, _],
                [_, _, W, _, _, B, W, _, _, B],
                [_, B, W, _, W, W, _, B, W, W],
                [_, _, W, B, _, _, _, _, B, _],
            ],
            expected:
                ' ┌─────────────────┐  ┌─────┐ \n' +
                ' └─────┐  ┌─────┐  │  └──┐  │ \n' +
                ' ┌─────┘  │  ┌──┘  └──┐  │  │ \n' +
                ' │  ┌─────┘  └─────┐  └──┘  │ \n' +
                ' └──┘  ┌───────────┘  ┌─────┘ \n' +
                ' ┌──┐  │  ┌───────────┘  ┌──┐ \n' +
                ' │  └──┘  └──┐  ┌──┐  ┌──┘  │ \n' +
                ' │  ·  ┌──┐  └──┘  │  │  ┌──┘ \n' +
                ' └──┐  │  │  ┌──┐  └──┘  └──┐ \n' +
                ' ·  └──┘  └──┘  └───────────┘ '
        }
    ];

    for (const t of testCases) {
        const testFn = (t as any).skip ? it.skip : it;
        testFn(t.name, async () => {
            const ctx = new z3.Context('main');
            const solver = new ShirokuroSolver(ctx, t.grid);
            const solution = await solver.solve();

            assert.ok(solution, "Expected solution but got null");

            const actual = solutionToString(solution, t.grid.length, t.grid[0].length);

            const expectedNorm = normalizeGridString(t.expected);
            const actualNorm = normalizeGridString(actual);

            assert.strictEqual(actualNorm, expectedNorm);
        });
    }
});
