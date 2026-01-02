import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { LinesweeperGridProvider } from './linesweeper-grid-provider.js';
import { LinesweeperSolver } from '../../Application/Linesweeper/linesweeper-solver.js';

export class LinesweeperHandler extends BasePuzzleHandler {
    constructor() {
        super('linesweeper', 'linesweeper');
    }

    extract(html: string, url: string): any {
        return { grid: LinesweeperGridProvider.getGridFromHTML(html) };
    }

    async solve(ctx: any, extractionResult: any): Promise<any> {
        const solver = new LinesweeperSolver(ctx, extractionResult.grid);
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

                let char = grid[r][c] >= 0 ? grid[r][c].toString() : getBoxDrawingChar(up, down, left, right);
                line += char;
                if (c < cols - 1) line += (right ? "─" : " ");
            }
            s += line + "\n";
        }
        return s;
    }
}

function getBoxDrawingChar(up: boolean, down: boolean, left: boolean, right: boolean): string {
    const symbols = {
        vertical: "│",
        horizontal: "─",
        topLeft: "┌",
        topRight: "┐",
        bottomLeft: "└",
        bottomRight: "┘",
    };
    if (up && down) return symbols.vertical;
    if (left && right) return symbols.horizontal;
    if (down && right) return symbols.topLeft;
    if (down && left) return symbols.topRight;
    if (up && right) return symbols.bottomLeft;
    if (up && left) return symbols.bottomRight;
    return "·";
}
