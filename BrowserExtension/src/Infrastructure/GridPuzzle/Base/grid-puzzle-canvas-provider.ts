export class GridPuzzleCanvasProvider {
    static getCanvasData(html: string): { pqqList: string[], size: number } {
        const sizeMatch = html.match(/(?:gpl\.)?([Ss]ize)\s*=\s*(\d+);/);
        if (!sizeMatch) {
            throw new Error("Could not find grid size.");
        }
        const size = parseInt(sizeMatch[2], 10);

        const pqqMatch = html.match(/(?:gpl\.)?pq{1,2}\s*=\s*"(.*?)";/);
        if (!pqqMatch) {
            throw new Error("Could not find grid data (pq/pqq).");
        }
        const pqqRaw = pqqMatch[1];
        const pqqString = this.decodeIfCustomBase64(pqqRaw);
        const pqqList = this.splitToList(pqqString, size);

        return { pqqList, size };
    }

    static getCanvasDataExtended(html: string): { pqqList: string[], arList: string[], abList: string[], size: number } {
        const { pqqList, size } = this.getCanvasData(html);

        const arMatch = html.match(/ar_data\s*=\s*"(.*?)";/);
        if (!arMatch) throw new Error("Could not find ar_data.");
        const arString = this.decodeIfCustomBase64(arMatch[1]);
        const arList = this.splitToList(arString, size);

        const abMatch = html.match(/ab_data\s*=\s*"(.*?)";/);
        if (!abMatch) throw new Error("Could not find ab_data.");
        const abString = this.decodeIfCustomBase64(abMatch[1]);
        const abList = this.splitToList(abString, size);

        return { pqqList, arList, abList, size };
    }

    static decodeIfCustomBase64(str: string): string {
        if (str.length < 4 || !this.isValidBase64(str.slice(3))) {
            return str;
        }
        try {
            return atob(str.slice(3));
        } catch (e) {
            console.warn("Base64 decode failed, returning original string", e);
            return str;
        }
    }

    static isValidBase64(str: string): boolean {
        return str.length % 4 === 0 && /^[A-Za-z0-9+/]*={0,2}$/.test(str);
    }

    static splitToList(str: string, size: number): string[] {
        const splitPipe = str.split('|');
        if (splitPipe.length === size || splitPipe.length === size * size) {
            return splitPipe;
        }
        return str.split('');
    }
}
