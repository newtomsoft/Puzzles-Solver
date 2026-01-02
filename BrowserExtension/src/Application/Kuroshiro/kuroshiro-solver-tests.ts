import assert from 'assert';
import { KuroshiroSolver } from './kuroshiro-solver.js';
import { KuroshiroCell } from '../../Domain/Kuroshiro/kuroshiro-constants.js';
import { Grid } from '../../Domain/Base/grid.js';

declare const global: any;
// @ts-ignore
const initZ3 = await import('../../../libs/z3-built.js');
global.initZ3 = initZ3.default || initZ3;
// @ts-ignore
await import('../../../libs/z3-bundle.js');

const _ = KuroshiroCell.EMPTY;
const B = KuroshiroCell.BLACK;
const W = KuroshiroCell.WHITE;

describe('KuroshiroSolver Tests', () => {
    let z3: any;

    beforeAll(async () => {
        z3 = await (global as any).Z3();
    }, 20000);

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

    for (const t of (testCases as any[])) {
        const testFn = t.skip ? it.skip : it;
        testFn(t.name, async () => {
            const ctx = new z3.Context('main');
            const solver = new KuroshiroSolver(ctx, t.grid);
            const solution = await solver.solve();

            assert.ok(solution, "Expected solution but got null");

            const grid = new Grid(t.grid);
            const actual = grid.solutionToString(solution);
            const normalize = (s: string) => s.split(/\r?\n/).map(l => l.trimEnd()).join('\n');
            assert.strictEqual(normalize(actual), normalize(t.expected));

            const other = await solver.getOtherSolution();
            assert.strictEqual(other, null, "Expected exactly one solution");
        }, 10000);
    }
});
