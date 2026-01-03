import { GridProvider } from "../../Base/grid-provider";
import { Grid } from "../../../Domain/grid";

export class PuzzlesMobileGridProvider implements GridProvider {
    public getGrid(): Grid {
        const html = document.documentElement.outerHTML;
        const data = this.extract(html);
        const gridData = data.grid || [];
        const size = gridData.length;
        const grid = new Grid(size, size);
        for(let r=0; r<size; r++) {
            for(let c=0; c<size; c++) {
                grid.setValue(r, c, gridData[r][c]);
            }
        }
        return grid;
    }

    public extract(html: string): { grid: any[][], regions?: any[][], extra?: any } {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        return this.parseDocument(doc);
    }

    protected parseDocument(doc: Document): { grid: any[][], regions?: any[][], extra?: any } {
        const cells = Array.from(doc.querySelectorAll('.cell'));
        const matrixCells = cells.filter(cell => cell.classList.contains('selectable'));

        if (matrixCells.length === 0) {
            return { grid: [] };
        }

        const size = Math.sqrt(matrixCells.length);
        const grid: any[][] = [];

        for (let r = 0; r < size; r++) {
            grid[r] = [];
            for (let c = 0; c < size; c++) {
                const index = r * size + c;
                if (index < matrixCells.length) {
                    const cell = matrixCells[index];
                    const value = this.parseCell(cell, r, c, doc);
                    grid[r][c] = value;
                } else {
                    grid[r][c] = null;
                }
            }
        }

        return { grid };
    }

    protected parseCell(cell: Element, r: number, c: number, doc: Document): any {
        const text = cell.textContent?.trim();
        if (text && !isNaN(parseInt(text))) {
            return parseInt(text);
        }
        return 0;
    }
}
