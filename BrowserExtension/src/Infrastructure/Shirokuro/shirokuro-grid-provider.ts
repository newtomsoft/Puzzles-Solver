import { ShirokuroCell } from '../../Domain/Shirokuro/shirokuro-constants.js';

export class ShirokuroGridProvider {
    static getGridFromHTML(html: string): (string | null)[][] {
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

        const grid: (string | null)[][] = [];

        for (let r = 0; r < size; r++) {
            const row: (string | null)[] = [];
            for (let c = 0; c < size; c++) {
                const index = r * size + c;
                let val = "";
                if (index < pqqList.length) {
                    val = pqqList[index];
                }

                let converted: string | null = null;
                if (val === '1') converted = ShirokuroCell.WHITE;
                else if (val === '2') converted = ShirokuroCell.BLACK;
                else if (val === 'W') converted = ShirokuroCell.WHITE;
                else if (val === 'B') converted = ShirokuroCell.BLACK;
                else if (val === '.') converted = ShirokuroCell.EMPTY;
                else converted = ShirokuroCell.EMPTY;

                row.push(converted);
            }
            grid.push(row);
        }

        return grid;
    }
}
