import { GridProvider } from '../Base/grid-provider.js';

export class YajikabeGridProvider implements GridProvider {
    extract(html: string): any {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const container = doc.querySelector('#puzzle-main');
        if (!container) throw new Error("Could not find puzzle container");

        const cells = Array.from(container.querySelectorAll('.cell'));
        const size = Math.sqrt(cells.length);
        if (!Number.isInteger(size)) {
            throw new Error(`Grid is not square: ${cells.length} cells`);
        }

        const matrix: string[][] = [];
        const directionMap: { [key: string]: string } = {
            'r': '→',
            'd': '↓',
            'l': '←',
            'u': '↑'
        };

        for (let r = 0; r < size; r++) {
            const row: string[] = [];
            for (let c = 0; c < size; c++) {
                const cell = cells[r * size + c];
                const text = cell.textContent?.trim() || '';

                if (text) {
                    // Find arrow element
                    const arrowDiv = Array.from(cell.querySelectorAll('div')).find(div =>
                        Array.from(div.classList).some(cls => cls.startsWith('arrow_'))
                    );

                    let directionChar = '';
                    if (arrowDiv) {
                        const arrowClass = Array.from(arrowDiv.classList).find(cls => cls.startsWith('arrow_'));
                        if (arrowClass) {
                            const dirKey = arrowClass.replace('arrow_', '');
                            if (directionMap[dirKey]) {
                                directionChar = directionMap[dirKey];
                            }
                        }
                    }
                    row.push(text + directionChar);
                } else {
                    row.push('');
                }
            }
            matrix.push(row);
        }

        return matrix;
    }
}
