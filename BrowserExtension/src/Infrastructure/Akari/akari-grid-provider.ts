export class AkariGridProvider {
    static getGridFromHTML(html: string): any {
        const sizeMatch = html.match(/(?:gpl\.)?([Ss]ize)\s*=\s*(\d+);/);
        if (!sizeMatch) {
            throw new Error("Could not find grid size.");
        }
        const size = parseInt(sizeMatch[2], 10);

        const pqqMatch = html.match(/(?:gpl\.)?pq{1,2}\s*=\s*"(.*?)";/);
        if (!pqqMatch) {
            throw new Error("Could not find grid data (pq/pqq).");
        }
        let pqq = pqqMatch[1];

        // Custom base64 decoding if applicable
        if (pqq.length >= 4 && /^[A-Za-z0-9+/]*={0,2}$/.test(pqq.slice(3))) {
            try {
                pqq = atob(pqq.slice(3));
            } catch (e) {
                console.warn("Base64 decode failed, using raw string", e);
            }
        }

        let pqqList: string[];
        const splitPipe = pqq.split('|');
        if (splitPipe.length === size || splitPipe.length === size * size) {
            pqqList = splitPipe;
        } else {
            pqqList = pqq.split('');
        }

        const black_cells: [number, number][] = [];
        const number_constraints: { [key: string]: number } = {};

        for (let i = 0; i < pqqList.length; i++) {
            const r = Math.floor(i / size);
            const c = i % size;
            const char = pqqList[i];

            if (char === '.') {
                // White cell
            } else if ("01234".includes(char)) {
                black_cells.push([r, c]);
                number_constraints[`(${r}, ${c})`] = parseInt(char, 10);
            } else if (char === '5') {
                black_cells.push([r, c]);
            }
        }

        return {
            columns_number: size,
            rows_number: size,
            black_cells: black_cells,
            number_constraints: number_constraints
        };
    }
}
