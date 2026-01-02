import { ShirokuroCell } from '../../Domain/Shirokuro/shirokuro-constants.js';
import { Position } from '../../Domain/Base/position.js';

import { BaseSolver } from '../Base/solver.js';

export class ShirokuroSolver extends BaseSolver<string[][], any> {
    h: any[][];
    v: any[][];

    constructor(ctx: any, grid: string[][]) {
        super(ctx, grid);
        this.h = [];
        this.v = [];
    }

    protected initVars(): void {
        for (let r = 0; r < this.rows; r++) {
            this.h[r] = [];
            for (let c = 0; c < this.cols - 1; c++) {
                const name = `h_${r}_${c}`;
                const v = this.ctx.Int.const(name);
                this.h[r][c] = v;
                this.solver.add(v.ge(0), v.le(1));
            }
        }

        for (let r = 0; r < this.rows - 1; r++) {
            this.v[r] = [];
            for (let c = 0; c < this.cols; c++) {
                const name = `v_${r}_${c}`;
                const v = this.ctx.Int.const(name);
                this.v[r][c] = v;
                this.solver.add(v.ge(0), v.le(1));
            }
        }
    }

    // 0: Up, 1: Right, 2: Down, 3: Left
    getEdge(r: number, c: number, dir: number): any {
        if (dir === 0) {
            if (r === 0) return null;
            return this.v[r - 1][c];
        }
        if (dir === 1) {
            if (c === this.cols - 1) return null;
            return this.h[r][c];
        }
        if (dir === 2) {
            if (r === this.rows - 1) return null;
            return this.v[r][c];
        }
        if (dir === 3) {
            if (c === 0) return null;
            return this.h[r][c - 1];
        }
        return null;
    }

    addConstraints() {
        // Degree constraints
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const edges = [];
                for (let d = 0; d < 4; d++) {
                    const e = this.getEdge(r, c, d);
                    if (e) edges.push(e);
                }

                if (edges.length === 0) continue;

                let sum = edges[0];
                for (let i = 1; i < edges.length; i++) {
                    sum = sum.add(edges[i]);
                }

                const val = this.problem[r][c];
                const isCircle = val === ShirokuroCell.WHITE || val === ShirokuroCell.BLACK;

                if (isCircle) {
                    this.solver.add(sum.eq(2));
                } else {
                    this.solver.add(this.ctx.Or(sum.eq(0), sum.eq(2)));
                }
            }
        }

        this.addLinksConstraints();
    }

    addLinksConstraints() {
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const val = this.problem[r][c];
                if (val === ShirokuroCell.WHITE || val === ShirokuroCell.BLACK) {
                    const sameColorConstraints = this.getSameColorCirclesLinkedConstraints(r, c, val);
                    const otherColorConstraints = this.getOtherColorCirclesLinkedConstraints(r, c, val);

                    const allConstraints = [...sameColorConstraints, ...otherColorConstraints];

                    const constraintVars = allConstraints.map(cond => this.ctx.If(cond, this.ctx.Int.val(1), this.ctx.Int.val(0)));

                    if (constraintVars.length === 0) {
                        // Should not happen in a valid puzzle unless it's impossible
                        this.solver.add(this.ctx.Bool.val(false));
                        continue;
                    }

                    let sum = constraintVars[0];
                    for (let i = 1; i < constraintVars.length; i++) {
                        sum = sum.add(constraintVars[i]);
                    }
                    this.solver.add(sum.eq(2));
                }
            }
        }
    }

    // Helper for "next position"
    nextPos(r: number, c: number, dir: number): { r: number, c: number } | null {
        let nr = r, nc = c;
        if (dir === 0) nr--;
        else if (dir === 1) nc++;
        else if (dir === 2) nr++;
        else if (dir === 3) nc--;

        if (nr < 0 || nr >= this.rows || nc < 0 || nc >= this.cols) return null;
        return { r: nr, c: nc };
    }

    getSameColorCirclesLinkedConstraints(r: number, c: number, color: string): any[] {
        const constraints = [];

        for (let d = 0; d < 4; d++) {
            const pathConstraints = [];
            let currR = r, currC = c;
            let found = false;

            // First edge from (r,c) in direction d
            const edge = this.getEdge(currR, currC, d);
            if (!edge) continue;

            pathConstraints.push(edge.eq(1));

            let next = this.nextPos(currR, currC, d);
            if (!next) continue; // Should be covered by getEdge but safe check

            currR = next.r; currC = next.c;

            while (currR >= 0 && currR < this.rows && currC >= 0 && currC < this.cols) {
                if (this.problem[currR][currC] === color) {
                    found = true;
                    break;
                }

                // Add edge to next
                const e = this.getEdge(currR, currC, d);
                if (!e) break; // Wall hit
                pathConstraints.push(e.eq(1));

                next = this.nextPos(currR, currC, d);
                if (!next) break;
                currR = next.r; currC = next.c;
            }

            if (found && pathConstraints.length > 0) {
                if (pathConstraints.length > 1) {
                    constraints.push(this.ctx.And(...pathConstraints));
                } else {
                    constraints.push(pathConstraints[0]);
                }
            }
        }
        return constraints;
    }

    getOtherColorCirclesLinkedConstraints(r: number, c: number, color: string): any[] {
        const constraints = [];
        const otherColor = (color === ShirokuroCell.WHITE) ? ShirokuroCell.BLACK : ShirokuroCell.WHITE;

        // Find all other circles
        const otherCircles = [];
        for (let or = 0; or < this.rows; or++) {
            for (let oc = 0; oc < this.cols; oc++) {
                if (this.problem[or][oc] === otherColor) {
                    // Must be different row and col for L-shape
                    if (or !== r && oc !== c) {
                        otherCircles.push({ r: or, c: oc });
                    }
                }
            }
        }

        for (const other of otherCircles) {
            // L-shape turn points
            // Option 1: Horizontal then Vertical (Turn at r, other.c)
            // Option 2: Vertical then Horizontal (Turn at other.r, c)

            const turnPos1 = { r: r, c: other.c }; // Horz first
            const turnPos2 = { r: other.r, c: c }; // Vert first

            // Directions
            const horzDir = (other.c > c) ? 1 : 3;
            const vertDir = (other.r > r) ? 2 : 0;

            const path1 = this.getToOtherCircleConstraint(r, c, other.r, other.c, turnPos1, horzDir, vertDir);
            const path2 = this.getToOtherCircleConstraint(r, c, other.r, other.c, turnPos2, vertDir, horzDir);

            if (path1 && path2) {
                constraints.push(this.ctx.Or(path1, path2));
            } else if (path1) {
                constraints.push(path1);
            } else if (path2) {
                constraints.push(path2);
            }
        }

        return constraints;
    }

    getToOtherCircleConstraint(r: number, c: number, targetR: number, targetC: number, turnPos: { r: number, c: number }, dir1: number, dir2: number): any {
        const constraints = [];

        let currR = r, currC = c;

        // First leg
        // Edge out of start
        const e1 = this.getEdge(currR, currC, dir1);
        if (!e1) return null;
        constraints.push(e1.eq(1));

        let next = this.nextPos(currR, currC, dir1);
        if (!next) return null;
        currR = next.r; currC = next.c;

        while (!(currR === turnPos.r && currC === turnPos.c)) {
            if (this.problem[currR][currC] !== ShirokuroCell.EMPTY) return null; // Blocked by another circle

            const e = this.getEdge(currR, currC, dir1);
            if (!e) return null;
            constraints.push(e.eq(1));

            next = this.nextPos(currR, currC, dir1);
            if (!next) return null;
            currR = next.r; currC = next.c;
        }

        // At turn position. Check if it's empty? Python code says:
        // while grid[curr] == '' and curr != turnPos: ...
        // if grid[curr] != '': return False
        // This implies turnPos must be empty (or valid pass-through).
        // Python code: `if self._input_grid[current_position] != '': return False` where `current_position` is `turnPos` after loop.
        if (this.problem[currR][currC] !== ShirokuroCell.EMPTY) return null;

        // Second leg
        // Edge out of turnPos
        const e2 = this.getEdge(currR, currC, dir2);
        if (!e2) return null;
        constraints.push(e2.eq(1));

        next = this.nextPos(currR, currC, dir2);
        if (!next) return null;
        currR = next.r; currC = next.c;

        while (!(currR === targetR && currC === targetC)) {
            if (this.problem[currR][currC] !== ShirokuroCell.EMPTY) return null;

            const e = this.getEdge(currR, currC, dir2);
            if (!e) return null;
            constraints.push(e.eq(1));

            next = this.nextPos(currR, currC, dir2);
            if (!next) return null;
            currR = next.r; currC = next.c;
        }

        // Reached target
        if (constraints.length > 1) {
            return this.ctx.And(...constraints);
        } else {
            return constraints[0];
        }
    }

    async solve() {
        this.initVars();
        this.addConstraints();

        while (true) {
            const result = await this.solver.check();
            if (result !== 'sat') {
                return null;
            }

            const model = this.solver.model();
            const solution = this.extractSolution(model);

            const components = this.findComponents(solution);
            const loops = components.filter(comp => comp.edges.length > 0);

            if (loops.length === 0) {
                // No loops found, but maybe satisfied?
                // If the grid has circles, there MUST be edges.
                // If no edges, it's empty solution, which is only valid for empty grid.
                // For now, assume if we have constraints, we must have edges.
                return solution;
            }

            if (loops.length === 1) {
                // Check if all circles are visited?
                // The degree constraints ensure all circles have 2 edges.
                // Subtour elimination ensures single loop.
                // If single loop visits all circles, we are good.
                // Are there "stray" loops that don't touch circles?
                // Degree constraints say empty cells are 0 or 2.
                // So any component is a loop.
                // If we have > 1 loop, we must eliminate.
                // If we have 1 loop, is it the solution?
                // Yes, because all circles must be part of *some* loop (degree 2).
                // If there is only 1 loop, all circles must be in it.
                return solution;
            }

            for (const loop of loops) {
                const litNot = [];
                for (const edge of loop.edges) {
                    const z3Var = edge.type === 'h' ? this.h[edge.r][edge.c] : this.v[edge.r][edge.c];
                    litNot.push(z3Var.eq(0));
                }
                this.solver.add(this.ctx.Or(...litNot));
            }
        }
    }

    extractSolution(model: any) {
        const sol: { h: boolean[][], v: boolean[][] } = { h: [], v: [] };
        for (let r = 0; r < this.rows; r++) {
            sol.h[r] = [];
            for (let c = 0; c < this.cols - 1; c++) {
                const val = model.eval(this.h[r][c]);
                const s = val.toString();
                sol.h[r][c] = (s === '1');
            }
        }
        for (let r = 0; r < this.rows - 1; r++) {
            sol.v[r] = [];
            for (let c = 0; c < this.cols; c++) {
                const val = model.eval(this.v[r][c]);
                const s = val.toString();
                sol.v[r][c] = (s === '1');
            }
        }
        return sol;
    }

    findComponents(sol: { h: boolean[][], v: boolean[][] }) {
        const visited = new Set();
        const components: { edges: { type: string, r: number, c: number }[] }[] = [];

        const key = (r: number, c: number) => `${r},${c}`;

        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                if (visited.has(key(r, c))) continue;

                // Check if this node has any edges
                let hasEdges = false;
                if (c < this.cols - 1 && sol.h[r][c]) hasEdges = true;
                if (c > 0 && sol.h[r][c - 1]) hasEdges = true;
                if (r < this.rows - 1 && sol.v[r][c]) hasEdges = true;
                if (r > 0 && sol.v[r - 1][c]) hasEdges = true;

                if (!hasEdges) {
                    visited.add(key(r, c));
                    continue;
                }

                const componentEdges = new Set();
                const queue: Position[] = [new Position(r, c)];
                visited.add(key(r, c));

                while (queue.length > 0) {
                    const curr = queue.shift();
                    if (!curr) break;

                    const neighbors: (Position & { edge: { type: string, r: number, c: number } })[] = [];
                    if (curr.c < this.cols - 1 && sol.h[curr.r][curr.c]) neighbors.push({ ...new Position(curr.r, curr.c + 1), edge: { type: 'h', r: curr.r, c: curr.c } });
                    if (curr.c > 0 && sol.h[curr.r][curr.c - 1]) neighbors.push({ ...new Position(curr.r, curr.c - 1), edge: { type: 'h', r: curr.r, c: curr.c - 1 } });
                    if (curr.r < this.rows - 1 && sol.v[curr.r][curr.c]) neighbors.push({ ...new Position(curr.r + 1, curr.c), edge: { type: 'v', r: curr.r, c: curr.c } });
                    if (curr.r > 0 && sol.v[curr.r - 1][curr.c]) neighbors.push({ ...new Position(curr.r - 1, curr.c), edge: { type: 'v', r: curr.r - 1, c: curr.c } });

                    for (const n of neighbors) {
                        const edgeKey = `${n.edge.type}_${n.edge.r}_${n.edge.c}`;
                        if (!componentEdges.has(edgeKey)) {
                            componentEdges.add(edgeKey);
                        }

                        const k = key(n.r, n.c);
                        if (!visited.has(k)) {
                            visited.add(k);
                            queue.push(n);
                        }
                    }
                }


                const edgeList = Array.from(componentEdges).map(k => {
                    const parts = (k as string).split('_');
                    return { type: parts[0], r: parseInt(parts[1]), c: parseInt(parts[2]) };
                });
                components.push({ edges: edgeList });
            }
        }
        return components;
    }
    getOrderedPath(sol: { h: boolean[][], v: boolean[][] }): Position[] {
        let startR = -1, startC = -1;
        outer: for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                if ((c < this.cols - 1 && sol.h[r][c]) || (r < this.rows - 1 && sol.v[r][c])) {
                    startR = r;
                    startC = c;
                    break outer;
                }
            }
        }
        if (startR === -1) return [];

        const path: Position[] = [];
        let currR = startR;
        let currC = startC;
        const visitedEdges = new Set<string>();

        while (true) {
            path.push(new Position(currR, currC));

            let nextR = -1, nextC = -1;
            let edgeKey = "";

            if (currC < this.cols - 1 && sol.h[currR][currC] && !visitedEdges.has(`h_${currR}_${currC}`)) {
                nextR = currR; nextC = currC + 1; edgeKey = `h_${currR}_${currC}`;
            } else if (currC > 0 && sol.h[currR][currC - 1] && !visitedEdges.has(`h_${currR}_${currC - 1}`)) {
                nextR = currR; nextC = currC - 1; edgeKey = `h_${currR}_${currC - 1}`;
            } else if (currR < this.rows - 1 && sol.v[currR][currC] && !visitedEdges.has(`v_${currR}_${currC}`)) {
                nextR = currR + 1; nextC = currC; edgeKey = `v_${currR}_${currC}`;
            } else if (currR > 0 && sol.v[currR - 1][currC] && !visitedEdges.has(`v_${currR - 1}_${currC}`)) {
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
}
