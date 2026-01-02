import { Position } from '../../Domain/Base/position.js';

export function getOrderedPath(h: boolean[][], v: boolean[][]): Position[] {
    const rows = h.length;
    if (rows === 0) return [];
    const cols = v[0].length;
    let startR = -1, startC = -1;
    outer: for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if ((c < cols - 1 && h[r][c]) || (r < rows - 1 && v[r][c])) {
                startR = r; startC = c;
                break outer;
            }
        }
    }
    if (startR === -1) return [];

    const path: Position[] = [];
    let currR = startR, currC = startC;
    const visitedEdges = new Set<string>();

    while (true) {
        path.push(new Position(currR, currC));
        let nextR = -1, nextC = -1, edgeKey = "";

        if (currC < cols - 1 && h[currR][currC] && !visitedEdges.has(`h_${currR}_${currC}`)) {
            nextR = currR; nextC = currC + 1; edgeKey = `h_${currR}_${currC}`;
        } else if (currC > 0 && h[currR][currC - 1] && !visitedEdges.has(`h_${currR}_${currC - 1}`)) {
            nextR = currR; nextC = currC - 1; edgeKey = `h_${currR}_${currC - 1}`;
        } else if (currR < rows - 1 && v[currR][currC] && !visitedEdges.has(`v_${currR}_${currC}`)) {
            nextR = currR + 1; nextC = currC; edgeKey = `v_${currR}_${currC}`;
        } else if (currR > 0 && v[currR - 1][currC] && !visitedEdges.has(`v_${currR - 1}_${currC}`)) {
            nextR = currR - 1; nextC = currC; edgeKey = `v_${currR - 1}_${currC}`;
        }

        if (nextR === -1) break;
        visitedEdges.add(edgeKey);
        currR = nextR;
        currC = nextC;
        if (currR === startR && currC === startC) {
            path.push(new Position(currR, currC));
            break;
        }
    }
    return path;
}
