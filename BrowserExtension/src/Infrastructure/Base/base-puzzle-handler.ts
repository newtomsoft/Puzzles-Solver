import { PuzzleHandler, ExtractionResult } from './puzzle-handler.js';
import { MasyuGridProvider } from '../Masyu/masyu-grid-provider.js';

export class BasePuzzleHandler implements PuzzleHandler {
    constructor(
        private type: string,
        private urlKeyword: string,
        private provider: MasyuGridProvider | any | null = null
    ) { }

    getType(): string {
        return this.type;
    }

    detect(url: string, html: string): boolean {
        return url.includes(this.urlKeyword);
    }

    extract(html: string, url: string): ExtractionResult {
        if (this.provider && this.provider.extract) {
            return { grid: this.provider.extract(html), url };
        }
        return { grid: MasyuGridProvider.getGridFromHTML(html), url };
    }

    async solve(extractionResult: ExtractionResult): Promise<any> {
        const body: any = {
            url: extractionResult.url,
            grid: extractionResult.grid,
            data: extractionResult.data,
            html: (extractionResult as any).html
        };

        // Handle extra data if present (e.g. for Detour)
        if (extractionResult.regions) {
            body.extra_data = [extractionResult.regions];
        } else if (extractionResult.extra) {
            body.extra_data = Array.isArray(extractionResult.extra) ? extractionResult.extra : [extractionResult.extra];
        }

        const response = await fetch('http://localhost:5000/api/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });

        const result = await response.json();
        if (result.status === 'solved') {
            return result.solution;
        } else {
            throw new Error(result.error || result.status || 'Failed to solve');
        }
    }

    getSolutionDisplay(puzzleType: string, extractionResult: ExtractionResult, solution: any): string {
        const matrix = solution.matrix || (Array.isArray(solution) && Array.isArray(solution[0]) ? solution : null);

        let rows = 0;
        let cols = 0;

        if (extractionResult.grid) {
            rows = extractionResult.grid.length;
            cols = extractionResult.grid[0].length;
        } else if (matrix) {
            rows = matrix.length;
            cols = matrix[0].length;
        } else if (solution.h) {
            rows = solution.h.length;
            cols = solution.h[0].length + 1;
        }

        if (rows === 0) return "Solution obtained (no visual preview available)";

        let s = "";
        for (let r = 0; r < rows; r++) {
            let line = " ";
            for (let c = 0; c < cols; c++) {
                if (matrix) {
                    line += matrix[r][c] + " ";
                } else {
                    const up = (r > 0) && solution.v?.[r - 1]?.[c];
                    const down = (r < rows - 1) && solution.v?.[r]?.[c];
                    const left = (c > 0) && solution.h?.[r]?.[c - 1];
                    const right = (c < cols - 1) && solution.h?.[r]?.[c];

                    let char = getBoxDrawingChar(up, down, left, right);
                    if (solution.black?.[r]?.[c]) char = "■";
                    line += char;
                    if (c < cols - 1) line += (right ? "─" : " ");
                }
            }
            s += line + "\n";
        }
        return s;
    }

    getOrderedPath(solver: any, solution: any): any[] | null {
        if (!solution || !solution.h || !solution.v) return null;
        return getOrderedPath(solution.h, solution.v);
    }

    getBlackCells(solution: any): any[] | null {
        if (solution && solution.black) {
            const blackCells: any[] = [];
            for (let r = 0; r < solution.black.length; r++) {
                for (let c = 0; c < solution.black[r].length; c++) {
                    if (solution.black[r][c]) {
                        blackCells.push({ r, c });
                    }
                }
            }
            return blackCells;
        }

        const matrix = solution.matrix || (Array.isArray(solution) && Array.isArray(solution[0]) ? solution : null);
        if (matrix) {
            const cells: any[] = [];
            for (let r = 0; r < matrix.length; r++) {
                for (let c = 0; c < matrix[r].length; c++) {
                    const val = matrix[r][c];
                    // For Akari, 1 means a bulb. For other puzzles, we might need different logic.
                    // But usually 1 or true means "fill" in these types of puzzles.
                    if (val === 1 || val === '1' || val === true) {
                        cells.push({ r, c });
                    }
                }
            }
            return cells;
        }
        return null;
    }
}

import { getOrderedPath } from '../../Application/Base/loop-utils.js';

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
