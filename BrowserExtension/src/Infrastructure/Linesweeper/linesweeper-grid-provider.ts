export class LinesweeperGridProvider {
    static getGridFromHTML(html: string): number[][] {
        const sizeMatch = html.match(/gpl\.([Ss]ize)\s*=\s*(\d+);/);
        if (!sizeMatch) {
            throw new Error("Could not find grid size (gpl.Size or gpl.size).");
        }
        const size = parseInt(sizeMatch[2], 10);

        const pqqMatch = html.match(/gpl\.pq{1,2}\s*=\s*"(.*?)";/);
        if (!pqqMatch) {
            throw new Error("Could not find grid data (gpl.pqq or gpl.pq).");
        }
        let pqq = pqqMatch[1];

        if (pqq.length >= 4 && /^[A-Za-z0-9+/]*={0,2}$/.test(pqq.slice(3))) {
            try {
                pqq = atob(pqq.slice(3));
            } catch (e) {
                console.warn("Base64 decode failed, using raw string", e);
            }
        }

        let pqqList: string[];
        const splitPipe = pqq.split('|');
        pqqList = splitPipe.length === size || splitPipe.length === size * size ? splitPipe : pqq.split('');

        const grid: number[][] = [];

        for (let r = 0; r < size; r++) {
            const row: number[] = [];
            for (let c = 0; c < size; c++) {
                const index = r * size + c;
                let valStr = "";
                if (index < pqqList.length) {
                    valStr = pqqList[index];
                }

                let val = -1; // Empty
                if (valStr >= '0' && valStr <= '9') {
                    val = parseInt(valStr, 10);
                } else if (valStr === '.') {
                    val = -1;
                }

                row.push(val);
            }
            grid.push(row);
        }

        return grid;
    }
}
