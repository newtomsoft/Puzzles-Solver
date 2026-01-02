export class Grid<T> {
    constructor(public readonly cells: T[][]) { }

    get rows(): number {
        return this.cells.length;
    }

    get cols(): number {
        return this.cells[0].length;
    }

    get(r: number, c: number): T {
        return this.cells[r][c];
    }

    solutionToString(solution: { h: boolean[][], v: boolean[][], black?: boolean[][] }): string {
        if (!solution) return '';
        const rows = this.rows;
        const cols = this.cols;
        let s = "";
        for (let r = 0; r < rows; r++) {
            let line = " ";
            for (let c = 0; c < cols; c++) {
                const up = (r > 0) && solution.v[r - 1][c];
                const down = (r < rows - 1) && solution.v[r][c];
                const left = (c > 0) && solution.h[r][c - 1];
                const right = (c < cols - 1) && solution.h[r][c];

                let char = " ";
                if (up && down && left && right) char = "┼";
                else if (up && down && left) char = "┤";
                else if (up && down && right) char = "├";
                else if (left && right && up) char = "┴";
                else if (left && right && down) char = "┬";
                else if (up && down) char = "│";
                else if (left && right) char = "─";
                else if (down && right) char = "┌";
                else if (down && left) char = "┐";
                else if (up && right) char = "└";
                else if (up && left) char = "┘";

                if (char === " ") {
                    if (!up && !down && !left && !right) {
                        char = "·";
                    }
                }

                if (solution.black && solution.black[r][c]) {
                    char = '■';
                }

                line += char;

                if (c < cols - 1) {
                    const rightEdge = (c < cols - 1) && solution.h[r][c];
                    line += (rightEdge ? "──" : "  ");
                }
            }
            s += line + " ";
            if (r < rows - 1) s += "\n";
        }
        return s;
    }
}
