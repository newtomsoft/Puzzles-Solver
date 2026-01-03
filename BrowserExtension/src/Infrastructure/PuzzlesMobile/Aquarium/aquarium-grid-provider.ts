import { PuzzlesMobileGridProvider } from "../Base/puzzles-mobile-grid-provider";

export class AquariumGridProvider extends PuzzlesMobileGridProvider {
    protected parseDocument(doc: Document): { grid: any[][], regions?: any[][], extra?: any } {
        const baseResult = super.parseDocument(doc);
        const grid = baseResult.grid; // In base this might contain 0s or text
        const size = grid.length;

        // Aquarium structure:
        // Regions are defined by borders.
        // Clues are in .taskTop and .taskLeft

        // Extract Clues
        const topClues = Array.from(doc.querySelectorAll('.taskTop .taskCell')).map(el => parseInt(el.textContent || "0"));
        const leftClues = Array.from(doc.querySelectorAll('.taskLeft .taskCell')).map(el => parseInt(el.textContent || "0"));

        // Extract Regions
        // We need to build a region map based on 'b-r', 'b-b' classes on .cell.selectable
        // We can do a BFS/DFS on the grid.

        const regions = Array.from({ length: size }, () => Array(size).fill(-1));
        const cells = Array.from(doc.querySelectorAll('.cell.selectable'));

        let currentRegionId = 1;

        for (let r = 0; r < size; r++) {
            for (let c = 0; c < size; c++) {
                if (regions[r][c] === -1) {
                    this.floodFillRegions(r, c, currentRegionId, regions, cells, size);
                    currentRegionId++;
                }
            }
        }

        // Prepare result
        // The API likely expects:
        // grid: regions (ID matrix)
        // extra_data: clues (concatenated top then left, or specifically formatted)

        // The .bru file shows "grid" as region IDs.
        // "extra_data" as array of numbers.

        // Let's replace 'grid' content with 'regions'.
        const regionGrid = regions;

        // Clues: The API .bru for Aquarium has "extra_data": [[5, 2, 3...]]
        // It seems to be Top Clues then Left Clues flattened?
        // Or Left then Top?
        // Standard PuzzlesMobile order for extra_data usually matches the Python implementation.
        // Python typically sends [col_clues, row_clues] flat?
        // Or specific structure.

        // Let's assume standard concatenated: [...col_clues, ...row_clues]
        const extra_data = [...topClues, ...leftClues];

        return {
            grid: regionGrid,
            extra: [extra_data] // The API expects list of lists usually for extra_data
        };
    }

    private floodFillRegions(startR: number, startC: number, id: number, regions: number[][], cells: Element[], size: number) {
        const stack = [[startR, startC]];
        regions[startR][startC] = id;

        while (stack.length > 0) {
            const [r, c] = stack.pop()!;
            const index = r * size + c;
            const cell = cells[index];
            const classes = cell.classList;

            // Check neighbors

            // Right
            if (c < size - 1 && !classes.contains('b-r')) {
                if (regions[r][c + 1] === -1) {
                    regions[r][c + 1] = id;
                    stack.push([r, c + 1]);
                }
            }

            // Down
            if (r < size - 1 && !classes.contains('b-b')) {
                if (regions[r + 1][c] === -1) {
                    regions[r + 1][c] = id;
                    stack.push([r + 1, c]);
                }
            }

            // Left (check neighbor's right border)
            if (c > 0) {
                const leftIndex = r * size + (c - 1);
                const leftCell = cells[leftIndex];
                if (!leftCell.classList.contains('b-r')) {
                     if (regions[r][c - 1] === -1) {
                        regions[r][c - 1] = id;
                        stack.push([r, c - 1]);
                    }
                }
            }

            // Up (check neighbor's bottom border)
            if (r > 0) {
                const upIndex = (r - 1) * size + c;
                const upCell = cells[upIndex];
                if (!upCell.classList.contains('b-b')) {
                     if (regions[r - 1][c] === -1) {
                        regions[r - 1][c] = id;
                        stack.push([r - 1, c]);
                    }
                }
            }
        }
    }

    protected parseCell(cell: Element, r: number, c: number, doc: Document): any {
        return 0; // We compute regions separately
    }
}
