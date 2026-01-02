import { KoburinCell } from '../../Domain/Koburin/koburin-constants.js';

export class KoburinGridProvider {
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
        const pqqBase64 = pqqMatch[1];

        let decodedData: string;
        try {
            decodedData = atob(pqqBase64.substring(3));
        } catch (e) {
            console.warn("Base64 decode failed for Koburin pqq", e);
            throw new Error("Failed to decode Koburin grid data.");
        }

        const grid: number[][] = [];
        for (let r = 0; r < size; r++) {
            const row: number[] = [];
            for (let c = 0; c < size; c++) {
                const char = decodedData[r * size + c] || '.';
                let val = KoburinCell.EMPTY;

                if (char >= '0' && char <= '9') {
                    val = parseInt(char, 10);
                }

                row.push(val);
            }
            grid.push(row);
        }

        return grid;
    }
}
