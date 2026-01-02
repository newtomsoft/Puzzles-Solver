import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { SudokuGridProvider } from './sudoku-grid-provider.js';
import { SudokuSolver } from '../../Application/Sudoku/sudoku-solver.js';

export class SudokuHandler extends BasePuzzleHandler {
    constructor() {
        super('sudoku', 'sudoku');
    }

    detect(url: string, html: string): boolean {
        return url.includes('sudoku') || url.includes('jigsaw') || url.includes('killer');
    }

    extract(html: string, url: string): any {
        const problem = SudokuGridProvider.getGridFromHTML(html, url);
        return { grid: problem.grid, problem };
    }

    async solve(ctx: any, extractionResult: any): Promise<any> {
        const solver = new SudokuSolver(ctx, extractionResult.problem);
        return await solver.solve();
    }

    getSolutionDisplay(puzzleType: string, extractionResult: any, solution: any): string {
        const grid = extractionResult.grid;
        const rows = grid.length;
        const cols = grid[0].length;
        let s = "";
        for (let r = 0; r < rows; r++) {
            let line = " ";
            for (let c = 0; c < cols; c++) {
                line += solution[r][c].toString();
                if (c < cols - 1) line += " ";
            }
            s += line + "\n";
        }
        return s;
    }

    getOrderedPath(): any[] | null {
        return null;
    }
}
