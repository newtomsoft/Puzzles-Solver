import assert from 'assert';
import { DetourSolver } from './detour-solver.js';
import { DetourCell } from '../../Domain/Detour/detour-constants.js';

declare const global: any;
// @ts-ignore
const initZ3 = await import('../../../libs/z3-built.js');
global.initZ3 = initZ3.default || initZ3;
// @ts-ignore
await import('../../../libs/z3-bundle.js');

import { drawGridSolution, normalizeGridString } from '../Base/test-utils.js';

function solutionToString(solution: any, grid: number[][]): string {
    return drawGridSolution(solution, grid.length, grid[0].length, () => null);
}

const _ = DetourCell.EMPTY;
const [a, b, c, d, e, f, g, h, i, j] = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19];

describe('DetourSolver Tests', () => {
    let z3: any;

    beforeAll(async () => {
        z3 = await (global as any).Z3();
    });

    const cases = [
        {
            name: 'test_4x4_easy_l9wxr',
            regions: [
                [1, 2, 2, 3],
                [1, 2, 4, 3],
                [5, 5, 4, 6],
                [7, 5, 4, 6],
            ],
            clues: [
                [1, 1, _, 1],
                [_, _, 2, _],
                [1, _, _, 1],
                [1, _, _, _],
            ],
            expected:
                ' ┌────────┐ \n' +
                ' │  ┌──┐  │ \n' +
                ' │  │  │  │ \n' +
                ' └──┘  └──┘ '
        },
        {
            name: 'test_6x6_evil_kd80m',
            regions: [
                [1, 1, 1, 2, 2, 2],
                [3, 3, 1, 2, 3, 3],
                [3, 3, 3, 3, 3, 3],
                [3, 4, 4, 4, 4, 3],
                [3, 4, 5, 6, 4, 3],
                [7, 7, 5, 6, 8, 8],
            ],
            clues: [
                [3, _, _, _, _, _],
                [7, _, _, _, _, _],
                [_, _, _, _, _, _],
                [_, _, _, _, _, _],
                [_, _, 2, 0, _, _],
                [_, _, _, _, _, _],
            ],
            expected:
                ' ┌─────┐  ┌─────┐ \n' +
                ' │  ┌──┘  │  ┌──┘ \n' +
                ' │  └─────┘  └──┐ \n' +
                ' │  ┌────────┐  │ \n' +
                ' │  │  ┌─────┘  │ \n' +
                ' └──┘  └────────┘ '
        },
        {
            name: 'test_8x8_evil_e5j72',
            skip: true,
            regions: [
                [1, 1, 2, 2, 2, 3, 3, 3],
                [1, 1, 4, 2, 3, 3, 5, 3],
                [6, 1, 4, 2, 5, 5, 5, 3],
                [6, 6, 4, 2, 7, 7, 7, 7],
                [8, 6, 6, 6, 9, 7, 7, 7],
                [8, 8, a, 9, 9, 7, b, b],
                [8, a, a, 9, 9, c, c, c],
                [8, 8, 8, 9, 9, c, c, c],
            ],
            clues: [
                [4, _, 5, _, _, 3, _, _],
                [_, _, 1, _, _, _, _, _],
                [_, _, _, _, _, _, _, _],
                [_, _, _, _, 2, _, _, _],
                [6, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _],
                [_, _, _, _, _, 5, _, _],
                [_, _, _, _, _, _, _, _],
            ],
            expected:
                ' ┌────────┐  ┌──┐  ┌──┐ \n' +
                ' └──┐  ┌──┘  │  │  │  │ \n' +
                ' ┌──┘  │  ┌──┘  │  │  │ \n' +
                ' └──┐  │  └──┐  │  │  │ \n' +
                ' ┌──┘  └─────┘  │  │  │ \n' +
                ' └──┐  ┌─────┐  └──┘  │ \n' +
                ' ┌──┘  │  ┌──┘  ┌──┐  │ \n' +
                ' └─────┘  └─────┘  └──┘ '
        },
        {
            name: 'test_10x10_evil_65wjq',
            skip: true,
            regions: [
                [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
                [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
                [6, 1, 2, 7, 7, 7, 7, 4, 5, 8],
                [6, 1, 9, a, a, a, a, b, 5, 8],
                [6, 9, 9, 9, a, a, b, b, b, 8],
                [6, 9, c, c, a, a, d, d, b, 8],
                [e, e, c, c, a, a, d, d, f, f],
                [e, e, e, g, g, g, g, f, f, f],
                [e, e, h, h, i, i, j, j, f, f],
                [h, h, h, h, i, i, j, j, j, j],
            ],
            clues: [
                [5, _, 4, _, 0, _, 1, _, 4, _],
                [_, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, 1],
                [_, _, 2, 7, _, _, _, 3, _, _],
                [_, _, _, _, _, _, _, _, _, _],
                [_, _, 2, _, _, _, 2, _, _, _],
                [4, _, _, _, _, _, _, _, 3, _],
                [_, _, _, 2, _, _, _, _, _, _],
                [_, _, 3, _, 0, _, 1, _, _, _],
                [_, _, _, _, _, _, _, _, _, _],
            ],
            expected:
                ' ┌──┐  ┌────────────────────┐ \n' +
                ' │  └──┘  ┌─────────────────┘ \n' +
                ' └──┐  ┌──┘  ┌────────┐  ┌──┐ \n' +
                ' ┌──┘  └─────┘  ┌──┐  └──┘  │ \n' +
                ' │  ┌───────────┘  │  ┌──┐  │ \n' +
                ' │  │  ┌────────┐  └──┘  │  │ \n' +
                ' │  │  └─────┐  └────────┘  │ \n' +
                ' └──┘  ┌──┐  └───────────┐  │ \n' +
                ' ┌─────┘  └──────────────┘  │ \n' +
                ' └──────────────────────────┘ ',
        }
    ];

    for (const t of cases) {
        const testFn = (t as any).skip ? it.skip : it;
        testFn(t.name, async () => {
            const ctx = new z3.Context('main');
            const solver = new DetourSolver(ctx, { clues: t.clues, regions: t.regions });
            const solution = await solver.solve();

            assert.ok(solution);
            const actual = solutionToString(solution, t.clues);
            assert.strictEqual(normalizeGridString(actual), normalizeGridString(t.expected));

            const other = await solver.getOtherSolution();
            assert.strictEqual(other, null, "Expected exactly one solution");
        });
    }
});
