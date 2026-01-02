
export function drawGridSolution(
    solution: { v: any[][], h: any[][], black?: any[][] },
    rows: number,
    cols: number,
    renderCell: (r: number, c: number) => string | null,
    defaultChar: string = " ",
    startChar: string = " "
): string {
    if (!solution) return '';
    let s = "";
    for (let r = 0; r < rows; r++) {
        let line = startChar;
        for (let c = 0; c < cols; c++) {
            const cellContent = renderCell(r, c);
            if (cellContent !== null) {
                line += cellContent;
            } else {
                const up = (r > 0) && solution.v[r - 1][c];
                const down = (r < rows - 1) && solution.v[r][c];
                const left = (c > 0) && solution.h[r][c - 1];
                const right = (c < cols - 1) && solution.h[r][c];

                let char = defaultChar;
                if (up && down && left && right) char = "┼";
                else if (up && down && left) char = "┤";
                else if (up && down && right) char = "├";
                else if (up && left && right) char = "┴";
                else if (down && left && right) char = "┬";
                else if (up && down) char = "│";
                else if (left && right) char = "─";
                else if (down && right) char = "┌";
                else if (down && left) char = "┐";
                else if (up && right) char = "└";
                else if (up && left) char = "┘";

                line += char;
            }

            if (c < cols - 1) {
                const right = (c < cols - 1) && solution.h[r][c];
                line += (right ? "──" : "  ");
            }
        }
        s += line + (defaultChar === " " ? " " : ""); // Original Masyu code didn't add trailing space, check Purenrupu
        if (r < rows - 1) s += "\n";
    }
    return s;
}

export function normalizeGridString(s: string): string {
    return s.trim().split(/\r?\n/).map(l => l.trimEnd()).join('\n');
}
