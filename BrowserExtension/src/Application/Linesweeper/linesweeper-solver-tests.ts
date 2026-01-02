import { LinesweeperSolver } from './linesweeper-solver.js';

// @ts-ignore
const initZ3 = await import('../../../libs/z3-built.js');
(global as any).initZ3 = initZ3.default || initZ3;
// @ts-ignore
await import('../../../libs/z3-bundle.js');

import { drawGridSolution, normalizeGridString } from '../Base/test-utils.js';

function solutionToString(solution: any, grid: number[][]): string {
    return drawGridSolution(solution, grid.length, grid[0].length, (r, c) => {
        return null;
    }, "·", "");
}

const _ = -1;

describe('LinesweeperSolver Tests', () => {
    let z3: any;

    beforeAll(async () => {
        z3 = await (global as any).Z3();
    }, 30000);

    const testCases = [
        {
            name: 'test_solution_4x4_292p8',
            grid: [
                [_, 3, _, _],
                [_, _, _, _],
                [_, _, _, _],
                [3, _, _, 2]
            ],
            expected:
                '·  ·  ·  · \n' +
                '┌─────┐  · \n' +
                '└──┐  │  · \n' +
                '·  └──┘  · '
        },
        {
            name: 'test_solution_4x4_1n690',
            grid: [
                [_, _, 3, _],
                [_, _, _, _],
                [_, 8, _, _],
                [_, _, _, 3]
            ],
            expected:
                '·  ·  ·  · \n' +
                '┌────────┐ \n' +
                '│  ·  ┌──┘ \n' +
                '└─────┘  · '
        },
        {
            name: 'test_solution_4x4_21d85',
            grid: [
                [3, _, _, 3],
                [_, _, _, _],
                [_, _, _, _],
                [3, _, _, 3]
            ],
            expected:
                '·  ┌──┐  · \n' +
                '┌──┘  └──┐ \n' +
                '└──┐  ┌──┘ \n' +
                '·  └──┘  · '
        },
        {
            name: 'test_solution_8x8_0evdw',
            grid: [
                [_, _, _, _, 4, _, 3, _],
                [_, 6, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _],
                [_, _, _, _, 7, _, _, _],
                [_, _, 8, _, 5, _, _, 5],
                [4, _, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _],
                [2, _, _, _, 5, _, _, 3],
            ],
            expected:
                '┌────────┐  ·  ·  ·  · \n' +
                '│  ·  ·  └──┐  ┌─────┐ \n' +
                '│  ·  ┌──┐  └──┘  ·  │ \n' +
                '│  ┌──┘  │  ·  ┌─────┘ \n' +
                '└──┘  ·  │  ·  └──┐  · \n' +
                '·  ┌─────┘  ·  ·  └──┐ \n' +
                '·  │  ·  ┌─────┐  ┌──┘ \n' +
                '·  └─────┘  ·  └──┘  · '
        },
        {
            name: 'test_solution_10x10_0wn5r',
            grid: [
                [_, _, _, 5, _, _, _, 4, _, _],
                [3, _, _, _, _, 5, _, _, _, _],
                [4, _, _, _, 6, _, _, _, _, _],
                [_, _, 8, _, _, _, _, 4, _, _],
                [_, _, _, _, 6, _, _, _, _, _],
                [_, 7, _, _, 6, _, _, 8, _, _],
                [_, _, _, _, _, _, _, _, _, _],
                [4, _, _, _, _, _, _, _, _, _],
                [_, _, _, _, 7, _, _, 5, 6, _],
                [2, _, _, _, _, _, _, _, _, _],
            ],
            skip: true,
            expected:
                '·  ┌──┐  ·  ┌─────┐  ·  ·  · \n' +
                '·  │  └─────┘  ·  └────────┐ \n' +
                '·  └─────┐  ·  ·  ·  ·  ·  │ \n' +
                '┌──┐  ·  └────────┐  ·  ·  │ \n' +
                '│  └─────┐  ·  ·  └─────┐  │ \n' +
                '│  ·  ·  │  ·  ┌──┐  ·  │  │ \n' +
                '└─────┐  └─────┘  │  ┌──┘  │ \n' +
                '·  ┌──┘  ┌─────┐  └──┘  ·  │ \n' +
                '·  │  ·  │  ·  │  ·  ·  ·  │ \n' +
                '·  └─────┘  ·  └───────────┘ '
        },
        {
            name: 'test_solution_12x12_1kkr6',
            grid: [
                [_, _, _, _, _, _, _, 3, _, _, _, _],
                [_, _, _, _, _, _, _, _, 6, _, 8, _],
                [4, _, 3, _, _, 6, _, _, _, _, _, _],
                [_, _, _, _, _, _, _, _, _, _, _, 5],
                [_, _, _, _, _, _, _, _, _, 5, _, _],
                [_, _, _, _, _, _, 6, _, _, _, _, _],
                [_, 5, 6, _, 7, _, _, 6, _, 3, _, _],
                [_, _, _, _, _, 7, _, _, _, _, _, _],
                [_, 8, _, _, _, _, _, _, _, 5, _, _],
                [_, _, _, _, 8, _, 7, _, _, _, _, 5],
                [2, _, _, _, _, _, _, _, _, _, _, _],
                [_, _, _, 3, _, _, 3, _, _, _, _, _],
            ],
            skip: true,
            expected:
                '·  ┌────────┐  ┌──┐  ·  ·  ┌─────┐ \n' +
                '·  │  ·  ·  └──┘  └──┐  ·  │  ·  │ \n' +
                '·  │  ·  ·  ·  ·  ·  └──┐  │  ┌──┘ \n' +
                '┌──┘  ·  ·  ┌─────┐  ·  └──┘  │  · \n' +
                '│  ┌─────┐  │  ·  └──┐  ·  ·  └──┐ \n' +
                '└──┘  ·  │  └──┐  ·  └──┐  ·  ·  │ \n' +
                '·  ·  ·  │  ·  └──┐  ·  │  ·  ·  │ \n' +
                '┌─────┐  └──┐  ·  │  ·  │  ·  ·  │ \n' +
                '│  ·  └─────┘  ┌──┘  ┌──┘  ·  ┌──┘ \n' +
                '└────────┐  ·  │  ·  │  ·  ┌──┘  · \n' +
                '·  ·  ·  └──┐  │  ·  └──┐  └─────┐ \n' +
                '·  ·  ·  ·  └──┘  ·  ·  └────────┘ '
        }
    ];

    for (const t of testCases) {
        const testFn = (t as any).skip ? it.skip : it;
        testFn(t.name, async () => {
            const ctx = new z3.Context('main');
            const solver = new LinesweeperSolver(ctx, t.grid);
            const solution = await solver.solve();

            expect(solution).toBeTruthy();

            const actual = solutionToString(solution, t.grid);
            expect(normalizeGridString(actual)).toBe(normalizeGridString(t.expected));

            const other = await solver.getOtherSolution();
            expect(other).toBeNull();
        }, 30000);
    }
});