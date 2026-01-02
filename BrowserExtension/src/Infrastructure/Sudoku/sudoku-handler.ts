import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { SudokuGridProvider } from './sudoku-grid-provider.js';
import { ExtractionResult } from '../Base/puzzle-handler.js';

export class SudokuHandler extends BasePuzzleHandler {
    constructor() {
        super('sudoku', 'sudoku');
    }

    detect(url: string, html: string): boolean {
        return url.includes('sudoku') || url.includes('jigsaw') || url.includes('killer');
    }

    extract(html: string, url: string): ExtractionResult {
        const problem = SudokuGridProvider.getGridFromHTML(html, url);
        return {
            grid: problem.grid,
            url,
            regions: problem.regions,
            cages: problem.cages
        };
    }

    getSolutionDisplay(puzzleType: string, extractionResult: ExtractionResult, solution: any): string {
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
