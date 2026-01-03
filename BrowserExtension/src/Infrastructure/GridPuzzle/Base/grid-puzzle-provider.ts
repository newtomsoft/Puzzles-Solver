import { Grid } from "../../../Domain/Base/grid";

export class GridPuzzleProvider {
    static makeOpenedGrid(rowCount: number, columnCount: number, matrixCells: Element[]): Grid<Set<string>> {
        const bordersDict: { [key: string]: string } = {
            'br': 'right',
            'bl': 'left',
            'bt': 'up',
            'bb': 'down'
        };

        const allBorders = new Set(['up', 'down', 'left', 'right']);
        const gridData: Set<string>[][] = [];

        for (let r = 0; r < rowCount; r++) {
            gridData[r] = [];
            for (let c = 0; c < columnCount; c++) {
                gridData[r][c] = new Set();
            }
        }

        for (let i = 0; i < matrixCells.length; i++) {
            const r = Math.floor(i / columnCount);
            const c = i % columnCount;
            const cell = matrixCells[i];

            if (r >= rowCount) break;

            const closedBorders = new Set<string>();

            // Check for explicit border classes
            cell.classList.forEach(cls => {
                if (bordersDict[cls]) {
                    closedBorders.add(bordersDict[cls]);
                }
            });

            // Add implicit boundary borders
            if (r === 0) closedBorders.add('up');
            if (r === rowCount - 1) closedBorders.add('down');
            if (c === 0) closedBorders.add('left');
            if (c === columnCount - 1) closedBorders.add('right');

            // Calculate open borders: All - Closed
            const openBorders = new Set<string>();
            allBorders.forEach(b => {
                if (!closedBorders.has(b)) {
                    openBorders.add(b);
                }
            });

            gridData[r][c] = openBorders;
        }

        return new Grid(gridData);
    }
}
