import { DetourCell } from '../../Domain/Detour/detour-constants.js';

export class DetourGridProvider {
    static getGridFromHTML(html: string): { clues: number[][], regions: number[][] } {
        const sizeMatch = html.match(/gpl\.Size\s*=\s*(\d+);/);
        if (!sizeMatch) throw new Error("Could not find gpl.Size");
        const size = parseInt(sizeMatch[1], 10);

        const pqqMatch = html.match(/gpl\.pqq\s*=\s*"(.*?)";/);
        if (!pqqMatch) throw new Error("Could not find gpl.pqq");
        const pqqBase64 = pqqMatch[1];
        const pqq = atob(pqqBase64.substring(3));

        const arMatch = html.match(/gpl\.ar_data\s*=\s*"(.*?)";/);
        const abMatch = html.match(/gpl\.ab_data\s*=\s*"(.*?)";/);
        if (!arMatch || !abMatch) throw new Error("Could not find gpl.ar_data or gpl.ab_data");

        const ar = atob(arMatch[1].substring(3));
        const ab = atob(abMatch[1].substring(3));

        const clues: number[][] = [];
        for (let r = 0; r < size; r++) {
            const row: number[] = [];
            for (let c = 0; c < size; c++) {
                const char = pqq[r * size + c];
                if (char === '|') {
                    row.push(DetourCell.EMPTY);
                } else {
                    const val = parseInt(char, 10);
                    row.push(isNaN(val) ? DetourCell.EMPTY : val);
                }
            }
            clues.push(row);
        }

        const regions = this.computeRegions(size, ar, ab);

        return { clues, regions };
    }

    private static computeRegions(size: number, ar: string, ab: string): number[][] {
        const regions: number[][] = Array.from({ length: size }, () => Array(size).fill(-1));
        let regionCount = 0;

        for (let r = 0; r < size; r++) {
            for (let c = 0; c < size; c++) {
                if (regions[r][c] === -1) {
                    this.floodFill(r, c, size, ar, ab, regions, regionCount++);
                }
            }
        }

        return regions;
    }

    private static floodFill(r: number, c: number, size: number, ar: string, ab: string, regions: number[][], regionId: number) {
        const queue = [{ r, c }];
        regions[r][c] = regionId;

        while (queue.length > 0) {
            const curr = queue.shift()!;

            if (curr.c < size - 1 && ar[curr.r * size + curr.c] === '0' && regions[curr.r][curr.c + 1] === -1) {
                regions[curr.r][curr.c + 1] = regionId;
                queue.push({ r: curr.r, c: curr.c + 1 });
            }
            if (curr.c > 0 && ar[curr.r * size + curr.c - 1] === '0' && regions[curr.r][curr.c - 1] === -1) {
                regions[curr.r][curr.c - 1] = regionId;
                queue.push({ r: curr.r, c: curr.c - 1 });
            }
            if (curr.r < size - 1 && ab[curr.r * size + curr.c] === '0' && regions[curr.r + 1][curr.c] === -1) {
                regions[curr.r + 1][curr.c] = regionId;
                queue.push({ r: curr.r + 1, c: curr.c });
            }
            if (curr.r > 0 && ab[(curr.r - 1) * size + curr.c] === '0' && regions[curr.r - 1][curr.c] === -1) {
                regions[curr.r - 1][curr.c] = regionId;
                queue.push({ r: curr.r - 1, c: curr.c });
            }
        }
    }
}
