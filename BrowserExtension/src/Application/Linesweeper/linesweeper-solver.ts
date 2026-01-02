import { Position } from '../../Domain/Base/position.js';
import { BaseSolver } from '../Base/solver.js';

export class LinesweeperSolver extends BaseSolver<number[][], any> {
    h: any[][];
    v: any[][];

    constructor(ctx: any, grid: number[][]) {
        super(ctx, grid);
        this.h = [];
        this.v = [];
    }

    protected initVars(): void {
        for (let r = 0; r < this.rows; r++) {
            this.h[r] = [];
            for (let c = 0; c < this.cols - 1; c++) {
                const v = this.ctx.Int.const(`h_${r}_${c}`);
                this.h[r][c] = v;
                this.solver.add(v.ge(0), v.le(1));
            }
        }

        for (let r = 0; r < this.rows - 1; r++) {
            this.v[r] = [];
            for (let c = 0; c < this.cols; c++) {
                const v = this.ctx.Int.const(`v_${r}_${c}`);
                this.v[r][c] = v;
                this.solver.add(v.ge(0), v.le(1));
            }
        }
    }

    getEdge(r: number, c: number, dir: number): any {
        if (dir === 0) { // Up
            if (r === 0) return null;
            return this.v[r - 1][c];
        }
        if (dir === 1) { // Right
            if (c === this.cols - 1) return null;
            return this.h[r][c];
        }
        if (dir === 2) { // Down
            if (r === this.rows - 1) return null;
            return this.v[r][c];
        }
        if (dir === 3) { // Left
            if (c === 0) return null;
            return this.h[r][c - 1];
        }
        return null;
    }

    protected addConstraints() {
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const val = this.problem[r][c];
                const edges = [];
                for (let d = 0; d < 4; d++) {
                    const e = this.getEdge(r, c, d);
                    if (e) edges.push(e);
                }

                let sumEdges = edges.length > 0 ? edges[0] : this.ctx.Int.val(0);
                for (let i = 1; i < edges.length; i++) {
                    sumEdges = sumEdges.add(edges[i]);
                }

                if (val >= 0) {
                    // Clue cell: no bridges pass through it
                    this.solver.add(sumEdges.eq(0));

                    // Count 8 neighbors that are part of the loop
                    const neighborsSum = [];
                    for (let nr = r - 1; nr <= r + 1; nr++) {
                        for (let nc = c - 1; nc <= c + 1; nc++) {
                            if (nr === r && nc === c) continue;
                            if (nr >= 0 && nr < this.rows && nc >= 0 && nc < this.cols) {
                                // Neighbor is in loop if its sum of edges is 2 (or > 0, since it's 0 or 2)
                                // We can sum the degrees of neighbors.
                                // Total sum of degrees of occupied neighbors = 2 * (number of occupied neighbors)
                                // So we want: sum(degrees of neighbors) == val * 2
                                const nEdges = [];
                                for (let d = 0; d < 4; d++) {
                                    const e = this.getEdge(nr, nc, d);
                                    if (e) nEdges.push(e);
                                }
                                if (nEdges.length > 0) {
                                    let nSum = nEdges[0];
                                    for (let i = 1; i < nEdges.length; i++) nSum = nSum.add(nEdges[i]);
                                    neighborsSum.push(nSum);
                                }
                            }
                        }
                    }

                    if (neighborsSum.length > 0) {
                        this.addSumConstraint(neighborsSum, val * 2);
                    } else {
                        if (val > 0) {
                            this.solver.add(this.ctx.Bool.val(false));
                        }
                    }

                } else {
                    // Empty cell: 0 or 2 bridges
                    this.solver.add(this.ctx.Or(sumEdges.eq(0), sumEdges.eq(2)));
                }
            }
        }
    }

    private lastSolution: any = null;

    async solve() {
        this.initVars();
        this.addConstraints();
        return await this.getSolution();
    }

    private async getSolution() {
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
                this.lastSolution = solution;
                return solution;
            }

            if (loops.length === 1) {
                this.lastSolution = solution;
                return solution;
            }

            for (const comp of components) {
                if (comp.edges.length > 0) {
                    const litNot = [];
                    for (const edge of comp.edges) {
                        const z3Var = edge.type === 'h' ? this.h[edge.r][edge.c] : this.v[edge.r][edge.c];
                        litNot.push(z3Var.eq(0));
                    }
                    this.solver.add(this.ctx.Or(...litNot));
                }
            }
        }
    }

    async getOtherSolution() {
        if (!this.lastSolution) return null;

        const clauses = [];
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols - 1; c++) {
                clauses.push(this.h[r][c].eq(this.lastSolution.h[r][c] ? 1 : 0));
            }
        }
        for (let r = 0; r < this.rows - 1; r++) {
            for (let c = 0; c < this.cols; c++) {
                clauses.push(this.v[r][c].eq(this.lastSolution.v[r][c] ? 1 : 0));
            }
        }

        if (clauses.length > 0) {
            this.solver.add(this.ctx.Not(this.ctx.And(...clauses)));
        }

        return await this.getSolution();
    }

    extractSolution(model: any) {
        const sol: { h: boolean[][], v: boolean[][] } = { h: [], v: [] };
        for (let r = 0; r < this.rows; r++) {
            sol.h[r] = [];
            for (let c = 0; c < this.cols - 1; c++) {
                sol.h[r][c] = model.eval(this.h[r][c]).toString() === '1';
            }
        }
        for (let r = 0; r < this.rows - 1; r++) {
            sol.v[r] = [];
            for (let c = 0; c < this.cols; c++) {
                sol.v[r][c] = model.eval(this.v[r][c]).toString() === '1';
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

                const activeEdges = [];
                if (c < this.cols - 1 && sol.h[r][c]) activeEdges.push({ type: 'h', r, c, nr: r, nc: c + 1 });
                if (c > 0 && sol.h[r][c - 1]) activeEdges.push({ type: 'h', r: r, c: c - 1, nr: r, nc: c - 1 });
                if (r < this.rows - 1 && sol.v[r][c]) activeEdges.push({ type: 'v', r, c, nr: r + 1, nc: c });
                if (r > 0 && sol.v[r - 1][c]) activeEdges.push({ type: 'v', r: r - 1, c: c, nr: r - 1, nc: c });

                if (activeEdges.length === 0) continue;

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