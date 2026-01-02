import assert from 'assert';
import { MasyuSolver } from './masyu-solver.js';
import { MasyuCell } from '../../Domain/Masyu/masyu-constants.js';


declare const global: any;
// @ts-ignore
const initZ3 = await import('../../../libs/z3-built.js');
global.initZ3 = initZ3.default || initZ3;
// @ts-ignore
await import('../../../libs/z3-bundle.js');

// Helper to create string representation of solution
import { drawGridSolution, normalizeGridString } from '../Base/test-utils.js';

function solutionToString(solution: any, rows: number, cols: number): string {
    return drawGridSolution(solution, rows, cols, () => null, "\u00b7");
}

const W = MasyuCell.WHITE;
const B = MasyuCell.BLACK;
const _ = MasyuCell.EMPTY;

describe('MasyuSolver Tests', () => {
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
            name: 'test_solution_white_0',
            grid: [
                [_, W, _],
                [_, W, _],
            ],
            expected:
                ' ┌─────┐ \n' +
                ' └─────┘ '
        },
        {
            name: 'test_solution_white_1',
            grid: [
                [_, W, _],
                [_, _, _],
                [_, W, _],
            ],
            expected:
                ' ┌─────┐ \n' +
                ' │  ·  │ \n' +
                ' └─────┘ '
        },
        {
            name: 'test_solution_white_2',
            grid: [
                [_, W, _, _],
                [W, _, _, W],
                [_, _, W, _],
            ],
            expected:
                ' ┌────────┐ \n' +
                ' │  ·  ·  │ \n' +
                ' └────────┘ '
        },
        {
            name: 'test_solution_black',
            grid: [
                [B, _, _],
                [_, _, _],
                [_, _, B],
            ],
            expected:
                ' ┌─────┐ \n' +
                ' │  ·  │ \n' +
                ' └─────┘ '
        },
        {
            name: 'test_solution_basic_grid',
            grid: [
                [B, _, W, _],
                [_, _, W, _],
                [_, _, _, _]
            ],
            expected:
                ' ┌────────┐ \n' +
                ' │  ┌─────┘ \n' +
                ' └──┘  ·  · '
        },
        {
            name: 'test_solution_6x6_0',
            grid: [
                [B, W, _, _, _, _],
                [W, _, _, W, W, _],
                [_, B, W, _, _, _],
                [_, W, _, _, _, B],
                [W, _, _, W, _, _],
                [B, _, _, W, _, _]
            ],
            expected:
                ' ┌─────┐  ·  ·  · \n' +
                ' │  ·  └────────┐ \n' +
                ' │  ┌─────┐  ·  │ \n' +
                ' │  │  ·  └─────┘ \n' +
                ' │  └────────┐  · \n' +
                ' └───────────┘  · '
        },
        {
            name: 'test_solution_6x6_1',
            grid: [
                [_, B, _, _, W, _],
                [_, _, _, _, _, _],
                [_, W, B, W, _, B],
                [_, _, _, _, _, B],
                [_, _, _, _, _, _],
                [B, _, _, _, W, _]
            ],
            expected:
                ' ·  ┌───────────┐ \n' +
                ' ·  │  ·  ·  ·  │ \n' +
                ' ·  │  ┌────────┘ \n' +
                ' ┌──┘  │  ┌─────┐ \n' +
                ' │  ·  └──┘  ·  │ \n' +
                ' └──────────────┘ '
        },
        {
            name: 'test_solution_8x8_0',
            grid: [
                [B, W, _, W, _, _, W, _],
                [W, _, _, _, _, _, _, W],
                [_, _, _, _, W, _, _, _],
                [_, W, W, _, _, _, _, _],
                [_, _, _, B, W, W, _, W],
                [_, _, W, _, _, _, _, _],
                [B, W, _, _, W, W, _, _],
                [_, _, _, _, W, _, W, B]
            ],
            expected:
                ' ┌───────────┐  ┌─────┐ \n' +
                ' │  ·  ·  ·  │  │  ·  │ \n' +
                ' └──┐  ┌──┐  │  │  ┌──┘ \n' +
                ' ·  │  │  │  └──┘  └──┐ \n' +
                ' ┌──┘  │  └────────┐  │ \n' +
                ' │  ·  │  ·  ·  ·  │  │ \n' +
                ' └─────┘  ┌────────┘  │ \n' +
                ' ·  ·  ·  └───────────┘ '
        },
        {
            name: 'test_solution_8x8_1',
            grid: [
                [_, _, _, _, _, _, _, B],
                [W, _, B, _, B, _, _, _],
                [W, _, _, _, _, W, _, _],
                [_, W, _, _, _, _, W, _],
                [_, _, _, _, _, _, _, _],
                [B, _, _, B, B, _, _, _],
                [_, _, _, _, _, _, _, _],
                [_, W, _, W, _, _, _, B]
            ],
            expected:
                ' ┌────────────────────┐ \n' +
                ' │  ·  ┌─────┐  ┌──┐  │ \n' +
                ' │  ·  │  ·  │  │  └──┘ \n' +
                ' └─────┘  ┌──┘  └─────┐ \n' +
                ' ·  ·  ·  │  ·  ·  ·  │ \n' +
                ' ┌────────┘  ┌─────┐  │ \n' +
                ' │  ·  ·  ·  │  ┌──┘  │ \n' +
                ' └───────────┘  └─────┘ '
        },
        {
            name: 'test_solution_10x10_0',
            skip: true,
            grid: [
                [_, _, B, W, _, _, _, _, _, B],
                [W, _, W, _, B, W, _, W, _, _],
                [_, _, _, _, _, _, _, _, _, _],
                [_, _, W, _, B, _, _, W, _, _],
                [_, W, B, W, _, _, _, W, _, _],
                [W, B, W, _, _, W, W, B, _, B],
                [_, _, _, _, _, _, _, _, B, _],
                [_, _, W, _, _, _, _, _, _, _],
                [W, _, _, _, B, W, W, _, _, _],
                [B, W, B, B, _, _, _, _, W, _]
            ],
            expected:
                ' ┌──┐  ┌────────────────────┐ \n' +
                ' │  │  │  ·  ┌───────────┐  │ \n' +
                ' │  │  │  ·  │  ·  ·  ┌──┘  │ \n' +
                ' │  │  │  ·  └─────┐  │  ·  │ \n' +
                ' │  │  └────────┐  │  │  ·  │ \n' +
                ' │  └────────┐  │  │  └─────┘ \n' +
                ' └──┐  ┌──┐  │  │  └─────┐  · \n' +
                ' ┌──┘  │  │  │  └─────┐  │  · \n' +
                ' │  ·  │  │  └────────┘  └──┐ \n' +
                ' └─────┘  └─────────────────┘ '
        },
        {
            name: 'test_solution_10x10_1',
            skip: true,
            grid: [
                [_, _, B, W, _, _, B, B, _, _],
                [_, _, W, _, _, _, W, W, _, W],
                [W, _, _, _, W, _, W, W, _, W],
                [_, W, W, _, W, W, _, _, _, _],
                [W, _, _, _, _, _, _, _, W, _],
                [_, _, B, W, B, _, _, _, W, _],
                [_, _, W, _, _, _, _, W, _, _],
                [_, W, W, _, _, W, _, _, _, W],
                [_, _, _, W, W, _, W, _, _, W],
                [_, _, _, B, _, W, _, _, W, B]
            ],
            expected:
                ' ·  ·  ┌───────────┐  ┌─────┐ \n' +
                ' ┌──┐  │  ·  ┌──┐  │  │  ·  │ \n' +
                ' │  │  │  ·  │  │  │  │  ·  │ \n' +
                ' │  │  │  ·  │  │  └──┘  ┌──┘ \n' +
                ' │  └──┘  ┌──┘  └─────┐  │  · \n' +
                ' └─────┐  │  ┌─────┐  │  │  · \n' +
                ' ┌──┐  │  │  │  ┌──┘  │  └──┐ \n' +
                ' │  │  │  │  │  │  ·  └──┐  │ \n' +
                ' │  └──┘  │  │  └────────┘  │ \n' +
                ' └────────┘  └──────────────┘ '
        },
        {
            name: 'test_solution_10x10_2',
            skip: true,
            grid: [
                [_, _, _, _, W, _, _, _, _, _],
                [_, _, _, _, _, _, _, W, _, _],
                [W, B, _, B, _, B, _, _, _, _],
                [_, _, _, _, _, _, B, W, _, _],
                [_, _, _, W, _, B, _, _, _, W],
                [_, B, _, B, _, W, _, _, _, _],
                [_, _, _, _, _, _, _, W, _, _],
                [_, _, _, _, W, _, _, _, _, _],
                [_, _, _, W, _, W, _, W, _, _],
                [_, _, B, _, _, _, W, _, W, _]
            ],
            expected:
                ' ┌──┐  ·  ┌─────┐  ┌────────┐ \n' +
                ' │  │  ·  │  ·  │  └─────┐  │ \n' +
                ' │  └─────┘  ·  └─────┐  │  │ \n' +
                ' └──┐  ┌───────────┐  │  │  │ \n' +
                ' ┌──┘  └────────┐  │  └──┘  │ \n' +
                ' │  ┌─────┐  ·  │  └──┐  ┌──┘ \n' +
                ' │  │  ·  │  ┌──┘  ·  │  └──┐ \n' +
                ' │  └──┐  │  │  ┌──┐  └──┐  │ \n' +
                ' │  ·  │  │  │  │  └─────┘  │ \n' +
                ' └─────┘  └──┘  └───────────┘ '
        },
        {
            name: 'test_solution_15x15',
            skip: true,
            grid: [
                [_, _, _, _, W, _, _, W, _, _, _, _, W, B, _],
                [_, W, _, W, _, _, _, _, W, W, B, _, _, W, _],
                [_, B, _, _, _, W, W, _, _, _, _, B, _, _, _],
                [_, _, B, W, _, _, W, _, _, _, B, _, B, _, B],
                [_, W, _, _, _, _, _, _, _, _, _, _, _, _, W],
                [_, W, _, _, _, W, _, _, W, W, _, W, _, _, _],
                [_, B, W, _, _, _, _, _, _, W, _, _, _, _, _],
                [_, W, W, _, W, W, W, _, _, _, _, _, W, B, W],
                [W, _, _, _, _, _, _, _, _, W, W, _, _, _, _],
                [_, _, _, W, W, _, _, B, _, B, _, W, _, _, W],
                [_, _, _, W, _, B, _, B, W, W, B, W, _, W, _],
                [B, W, _, W, B, W, W, _, _, _, _, _, _, W, _],
                [B, _, _, _, _, _, _, _, _, W, W, _, _, _, _],
                [W, _, _, W, _, _, W, W, _, W, _, _, W, W, W],
                [_, _, _, _, W, _, _, _, _, _, B, W, B, _, _]
            ],
            expected:
                ' ┌──┐  ·  ┌─────┐  ┌────────────────────┐  · \n' +
                ' │  │  ·  │  ·  └──┘  ┌────────┐  ·  ·  │  · \n' +
                ' │  └─────┘  ┌────────┘  ·  ·  │  ┌─────┘  · \n' +
                ' └──┐  ┌─────┘  ┌──────────────┘  │  ┌─────┐ \n' +
                ' ·  │  │  ·  ┌──┘  ┌──┐  ·  ·  ·  │  │  ·  │ \n' +
                ' ·  │  └──┐  └─────┘  └────────┐  │  │  ┌──┘ \n' +
                ' ·  └─────┘  ┌──┐  ┌──┐  ┌─────┘  └──┘  └──┐ \n' +
                ' ┌────────┐  │  │  │  │  └──┐  ┌────────┐  │ \n' +
                ' │  ·  ·  └──┘  │  │  │  ·  │  │  ┌──┐  │  │ \n' +
                ' │  ·  ┌────────┘  │  └─────┘  │  │  └──┘  │ \n' +
                ' │  ·  └────────┐  │  ┌────────┘  │  ┌─────┘ \n' +
                ' └───────────┐  │  │  │  ┌──┐  ┌──┘  └─────┐ \n' +
                ' ┌─────┐  ·  │  └──┘  └──┘  │  │  ·  ┌──┐  │ \n' +
                ' │  ·  └─────┘  ┌────────┐  │  │  ·  │  │  │ \n' +
                ' └──────────────┘  ·  ·  └──┘  └─────┘  └──┘ '
        }
    ];

    for (const t of testCases) {
        const testFn = (t as any).skip ? it.skip : it;
        testFn(t.name, async () => {
            const ctx = new z3.Context('main');
            const solver = new MasyuSolver(ctx, t.grid);
            const solution = await solver.solve();

            assert.ok(solution, "Expected solution but got null");

            const actual = solutionToString(solution, t.grid.length, t.grid[0].length);
            assert.strictEqual(normalizeGridString(actual), normalizeGridString(t.expected));
        });
    }
});
