import { MidloopCell } from '../../Domain/Midloop/midloop-constants.js';

export class MidloopGridProvider {
    static getGridFromHTML(html: string): (number | null)[][] {
        const sizeMatch = html.match(/gpl\.([Ss]ize)\s*=\s*(\d+);/);
        if (!sizeMatch) {
            throw new Error("Could not find grid size (gpl.Size or gpl.size).");
        }
        const size = parseInt(sizeMatch[2], 10);

        const pqqMatch = html.match(/gpl\.pq{1,2}\s*=\s*(["'])(.*?)\1\s*;/);
        if (!pqqMatch) {
            throw new Error("Could not find grid data (gpl.pqq or gpl.pq).");
        }
        let rawPqq = pqqMatch[2];
        let pqq = rawPqq;

        const internalSize = 2 * size - 1;
        const targetLengths = [size * size, internalSize * internalSize];

        const isGoodLength = (s: string) => {
            for (const len of targetLengths) {
                if (Math.abs(s.length - len) <= 5) return true;
            }
            return false;
        };

        // Try decoding with slice(3) first (Standard GridPuzzle pattern)
        if (rawPqq.length >= 4) {
            try {
                const decoded = atob(rawPqq.slice(3));
                if (isGoodLength(decoded)) {
                    pqq = decoded;
                } else if (/[A-Za-z]/.test(rawPqq)) {
                    // If raw string has letters, it might be raw base64 without prefix
                    const decodedRaw = atob(rawPqq);
                    if (isGoodLength(decodedRaw)) {
                        pqq = decodedRaw;
                    }
                }
            } catch (e) {
                // Try raw decode as fallback if it didn't match sliced
                try {
                    const decodedRaw = atob(rawPqq);
                    if (isGoodLength(decodedRaw)) {
                        pqq = decodedRaw;
                    }
                } catch (e2) { }
            }
        }

        const grid: (number | null)[][] = Array.from({ length: internalSize }, () => Array(internalSize).fill(MidloopCell.EMPTY));

        let pqqList: string[];
        const splitPipe = pqq.split('|');
        if (splitPipe.length > 1 && (splitPipe.length >= size || splitPipe.length >= size * size || splitPipe.length >= internalSize * internalSize)) {
            pqqList = splitPipe;
        } else {
            pqqList = pqq.split('');
        }

        const isDot = (val: string) => {
            if (!val) return false;
            // Dots are typically '1', 'B', 'D', 'W'.
            // In case of binary data, it's byte 1.
            // DO NOT match other characters or high-bit metadata.
            return val === '1' || val === 'B' || val === 'D' || val === 'W' || val.charCodeAt(0) === 1;
        };

        let skip = 0;
        // Search for a matching length with small offsets (prefixes)
        for (let s = 0; s <= 5; s++) {
            if (pqqList.length === internalSize * internalSize + s) {
                skip = s;
                break;
            }
        }

        if (skip === 0) {
            for (let s = 0; s <= 5; s++) {
                if (pqqList.length === size * size + s) {
                    skip = s;
                    break;
                }
            }
        }

        // Apply mapping
        if (pqqList.length >= internalSize * internalSize + skip && internalSize * internalSize > 0 &&
            (pqqList.length === internalSize * internalSize + skip || pqqList.length > (size * size + skip + 5))) {
            for (let r = 0; r < internalSize; r++) {
                for (let c = 0; c < internalSize; c++) {
                    const valStr = pqqList[skip + r * internalSize + c];
                    if (isDot(valStr)) {
                        grid[r][c] = MidloopCell.DOT;
                    }
                }
            }
        } else if (pqqList.length >= size * size + skip) {
            for (let r = 0; r < size; r++) {
                for (let c = 0; c < size; c++) {
                    const valStr = pqqList[skip + r * size + c];
                    if (isDot(valStr)) {
                        grid[2 * r][2 * c] = MidloopCell.DOT;
                    }
                }
            }
        }

        return grid;
    }
}
