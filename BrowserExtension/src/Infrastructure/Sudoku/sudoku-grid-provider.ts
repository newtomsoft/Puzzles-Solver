import { SudokuProblem, KillerCage } from '../../Domain/Sudoku/sudoku-constants.js';
import { Position } from '../../Domain/Base/position.js';

export class SudokuGridProvider {
    static getGridFromHTML(html: string, url: string = ""): SudokuProblem {
        let type: 'standard' | 'jigsaw' | 'killer' = 'standard';
        if (url.includes('jigsaw') || html.includes('jigsaw')) type = 'jigsaw';
        if (url.includes('killer') || html.includes('killer')) type = 'killer';

        const sizeMatch = html.match(/gpl\.([Ss]ize)\s*=\s*(\d+);/);
        let size = 9;
        if (sizeMatch) {
            size = parseInt(sizeMatch[2], 10);
        }

        const grid: (number | null)[][] = Array.from({ length: size }, () => Array(size).fill(null));

        const pqqMatch = html.match(/gpl\.pq{1,2}\s*=\s*"(.*?)";/);
        if (pqqMatch) {
            let pqq = pqqMatch[1];
            if (pqq.length >= 4 && /^[A-Za-z0-9+/]*={0,2}$/.test(pqq.slice(3))) {
                try {
                    pqq = atob(pqq.slice(3));
                } catch (e) {
                    // Ignore
                }
            }

            let index = 0;
            for (let i = 0; i < pqq.length && index < size * size; i++) {
                const char = pqq[i];
                const val = parseInt(char);
                if (!isNaN(val) && val >= 1 && val <= 9) {
                    const r = Math.floor(index / size);
                    const c = index % size;
                    grid[r][c] = val;
                    index++;
                } else if (char === '.') {
                    index++;
                }
            }
        }

        return {
            type,
            grid,
            regions: [],
            cages: []
        };
    }
}
