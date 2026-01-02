export class CountryRoadGridProvider {
    static getGridFromHTML(html: string): { clues: (number | null)[][], regions: number[][] } {
        const sizeMatch = html.match(/gpl\.([Ss]ize)\s*=\s*(\d+);/);
        if (!sizeMatch) throw new Error("Could not find gpl.Size");
        const size = parseInt(sizeMatch[2], 10);

        const pqqMatch = html.match(/gpl\.pq{1,2}\s*=\s*"(.*?)";/);
        if (!pqqMatch) throw new Error("Could not find gpl.pqq");
        let pqq = pqqMatch[1];

        if (pqq.length >= 4 && /^[A-Za-z0-9+/]*={0,2}$/.test(pqq.slice(3))) {
            try {
                pqq = atob(pqq.slice(3));
            } catch (e) {
                console.warn("Base64 decode failed, using raw string", e);
            }
        }

        // Try to find ar_data and ab_data first (Detour style)
        const arMatch = html.match(/gpl\.ar_data\s*=\s*"(.*?)";/);
        const abMatch = html.match(/gpl\.ab_data\s*=\s*"(.*?)";/);

        // If not found, try paa (Masyu/Koburin style region data?)
        // Wait, Masyu doesn't use regions. Koburin does?
        // Koburin uses `paa`.
        // If `ar_data` is missing but `paa` exists, we should probably try to parse `paa`.
        // But for now, let's implement the Detour style (ar/ab) as primary since it was explicitly used in DetourGridProvider.
        // And if we encounter a puzzle with `paa` only, we might need a parser for that.
        // Since I don't have a `paa` parser ready and `Detour` provider uses `ar/ab`, I will stick to `ar/ab`.
        // However, looking at the grep results, `Koburin` and `Detour` have `paa` in the HTML files in `toMigrate`.
        // This strongly suggests `paa` is the standard and `ar/ab` might be specific to the site version `DetourGridProvider` was built for.
        // But without a `paa` parser logic (which is non-trivial bitstream decoding), I can't implement it reliably.
        // Except if I can find `paa` parsing logic in the codebase?
        // I searched for `gpl.paa` and found it only in HTML files and tests, not in logic (except `MasyuGridProviderTests` mocking it).

        // Let's assume for now that if `ar_data` is missing, we can't solve it.
        // Or if `ar_data` is missing, check if `paa` is there and throw a specific error.

        if (!arMatch || !abMatch) {
            // Fallback or error?
            // If `paa` is present, maybe we can decode it?
            // Since I don't have the spec, I'll error out for now.
            throw new Error("Could not find gpl.ar_data or gpl.ab_data (paa not supported yet).");
        }

        const ar = atob(arMatch[1].substring(3));
        const ab = atob(abMatch[1].substring(3));

        const clues: (number | null)[][] = [];
        let pqqList: string[];
        const splitPipe = pqq.split('|');
        pqqList = splitPipe.length === size || splitPipe.length === size * size ? splitPipe : pqq.split('');

        for (let r = 0; r < size; r++) {
            const row: (number | null)[] = [];
            for (let c = 0; c < size; c++) {
                const index = r * size + c;
                let valStr = "";
                if (index < pqqList.length) {
                    valStr = pqqList[index];
                }

                let val: number | null = null; // Empty/No Clue
                if (valStr >= '0' && valStr <= '9') {
                    val = parseInt(valStr, 10);
                } else if (valStr === '.') {
                    val = null;
                }
                row.push(val);
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

            // Try Right
            if (curr.c < size - 1 && ar[curr.r * size + curr.c] === '0' && regions[curr.r][curr.c + 1] === -1) {
                regions[curr.r][curr.c + 1] = regionId;
                queue.push({ r: curr.r, c: curr.c + 1 });
            }
            // Try Left
            if (curr.c > 0 && ar[curr.r * size + curr.c - 1] === '0' && regions[curr.r][curr.c - 1] === -1) {
                regions[curr.r][curr.c - 1] = regionId;
                queue.push({ r: curr.r, c: curr.c - 1 });
            }
            // Try Down
            if (curr.r < size - 1 && ab[curr.r * size + curr.c] === '0' && regions[curr.r + 1][curr.c] === -1) {
                regions[curr.r + 1][curr.c] = regionId;
                queue.push({ r: curr.r + 1, c: curr.c });
            }
            // Try Up
            if (curr.r > 0 && ab[(curr.r - 1) * size + curr.c] === '0' && regions[curr.r - 1][curr.c] === -1) {
                regions[curr.r - 1][curr.c] = regionId;
                queue.push({ r: curr.r - 1, c: curr.c });
            }
        }
    }
}
