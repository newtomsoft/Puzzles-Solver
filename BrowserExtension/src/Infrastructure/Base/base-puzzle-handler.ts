import { PuzzleHandler } from './puzzle-handler.js';
import { MasyuGridProvider } from '../Masyu/masyu-grid-provider.js';
import { MasyuSolver } from '../../Application/Masyu/masyu-solver.js';

export class BasePuzzleHandler implements PuzzleHandler {
    constructor(private type: string, private urlKeyword: string) { }

    getType(): string {
        return this.type;
    }

    detect(url: string, html: string): boolean {
        return url.includes(this.urlKeyword);
    }

    extract(html: string, url: string): any {
        return { grid: MasyuGridProvider.getGridFromHTML(html) };
    }

    async solve(ctx: any, extractionResult: any): Promise<any> {
        const solver = new MasyuSolver(ctx, extractionResult.grid);
        extractionResult.solverInstance = solver;
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
                const up = (r > 0) && solution.v?.[r - 1]?.[c];
                const down = (r < rows - 1) && solution.v?.[r]?.[c];
                const left = (c > 0) && solution.h?.[r]?.[c - 1];
                const right = (c < cols - 1) && solution.h?.[r]?.[c];

                let char = getBoxDrawingChar(up, down, left, right);
                line += char;
                if (c < cols - 1) line += (right ? "─" : " ");
            }
            s += line + "\n";
        }
        return s;
    }

    getOrderedPath(solver: any, solution: any): any[] | null {
        return solver.getOrderedPath(solution);
    }

    getBlackCells(solution: any): any[] | null {
        return null;
    }
}

const BOX_SYMBOLS = {
    vertical: "│",
    horizontal: "─",
    topLeft: "┌",
    topRight: "┐",
    bottomLeft: "└",
    bottomRight: "┘",
} as const;

function getBoxDrawingChar(up: boolean, down: boolean, left: boolean, right: boolean): string {
    if (up && down) return BOX_SYMBOLS.vertical;
    if (left && right) return BOX_SYMBOLS.horizontal;
    if (down && right) return BOX_SYMBOLS.topLeft;
    if (down && left) return BOX_SYMBOLS.topRight;
    if (up && right) return BOX_SYMBOLS.bottomLeft;
    if (up && left) return BOX_SYMBOLS.bottomRight;
    return "·";
}
