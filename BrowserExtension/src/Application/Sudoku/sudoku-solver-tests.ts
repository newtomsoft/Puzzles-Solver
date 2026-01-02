import { SudokuSolver } from './sudoku-solver.js';
import { SudokuProblem } from '../../Domain/Sudoku/sudoku-constants.js';
import { Position } from '../../Domain/Base/position.js';
import { jest } from '@jest/globals';

declare const global: any;
// @ts-ignore
const initZ3 = await import('../../../libs/z3-built.js');
(global as any).initZ3 = initZ3.default || initZ3;
// @ts-ignore
await import('../../../libs/z3-bundle.js');

describe('SudokuSolver', () => {
    let ctx: any;

    beforeAll(async () => {
        // Increase timeout for Z3 initialization
        jest.setTimeout(60000);
        const z3 = await (global as any).Z3();
        ctx = new z3.Context('main');
    });

    it('solves a standard 9x9 sudoku', async () => {
        // A simple valid sudoku (top left corner)
        // 5 3 . | . 7 . | . . .
        // 6 . . | 1 9 5 | . . .
        // . 9 8 | . . . | . 6 .

        const grid: (number | null)[][] = Array.from({ length: 9 }, () => Array(9).fill(null));
        grid[0][0] = 5; grid[0][1] = 3; grid[0][4] = 7;
        grid[1][0] = 6; grid[1][3] = 1; grid[1][4] = 9; grid[1][5] = 5;
        grid[2][1] = 9; grid[2][2] = 8; grid[2][7] = 6;
        grid[3][0] = 8; grid[3][4] = 6; grid[3][8] = 3;
        grid[4][0] = 4; grid[4][3] = 8; grid[4][5] = 3; grid[4][8] = 1;
        grid[5][0] = 7; grid[5][4] = 2; grid[5][8] = 6;
        grid[6][1] = 6; grid[6][6] = 2; grid[6][7] = 8;
        grid[7][3] = 4; grid[7][4] = 1; grid[7][5] = 9; grid[7][8] = 5;
        grid[8][4] = 8; grid[8][7] = 7; grid[8][8] = 9;

        const problem: SudokuProblem = {
            type: 'standard',
            grid: grid
        };

        const solver = new SudokuSolver(ctx, problem);
        const solution = await solver.solve();

        expect(solution).not.toBeNull();
        if (solution) {
            // Check few values
            expect(solution[0][0]).toBe(5);
            expect(solution[0][1]).toBe(3);
            // expect(solution[0][2]).toBe(4); // Inferred
            expect(solution[8][8]).toBe(9);

            // Check distinctness in row 0
            const row0 = new Set(solution[0]);
            expect(row0.size).toBe(9);
        }
    });

    it('solves a small killer sudoku cage', async () => {
        // Use 4x4 to be faster
        const grid: (number | null)[][] = Array.from({ length: 4 }, () => Array(4).fill(null));

        const problem: SudokuProblem = {
            type: 'killer',
            grid: grid,
            cages: [
                { sum: 3, cells: [new Position(0, 0), new Position(0, 1)] } // 1+2 or 2+1
            ]
        };

        const solver = new SudokuSolver(ctx, problem);
        const solution = await solver.solve();

        expect(solution).not.toBeNull();
        if (solution) {
            const val1 = solution[0][0];
            const val2 = solution[0][1];
            expect(val1 + val2).toBe(3);
            expect(val1).not.toBe(val2);
            expect([1, 2]).toContain(val1);
            expect([1, 2]).toContain(val2);
        }
    });
});
