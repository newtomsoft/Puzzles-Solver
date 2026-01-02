import { Position } from '../../Domain/Base/position.js';
import { BaseSolver } from '../Base/solver.js';

export class PurenrupuSolver extends BaseSolver<number[][], any> {
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

                if (val === 1) {
                    // Wall: sum of edges must be 0
                    this.solver.add(sumEdges.eq(0));
                } else {
                    // Empty: sum of edges must be 2
                    this.solver.add(sumEdges.eq(2));
                }
            }
        }
    }

    async solve() {
        this.initVars();
        this.addConstraints();
        return await this.getSolution();
    }

    private lastSolution: any = null;

    async getSolution() {
        while (true) {
            const result = await this.solver.check();
            if (result !== 'sat') {
                return null;
            }

            const model = this.solver.model();
            const solution = this.extractSolution(model);
            const components = this.findComponents(solution);
            const loops = components.filter(comp => comp.edges.length > 0);

            if (loops.length > 1) {
                 for (const comp of loops) {
                     const litNot = [];
                    for (const edge of comp.edges) {
                        const z3Var = edge.type === 'h' ? this.h[edge.r][edge.c] : this.v[edge.r][edge.c];
                        litNot.push(z3Var.eq(0));
                    }
                    this.solver.add(this.ctx.Or(...litNot));
                }
                continue;
            }

            this.lastSolution = solution;
            return solution;
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
        const sol: { h: boolean[][], v: boolean[][] } = {
            h: [], v: []
        };
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
        const components: { edges: { type: string, r: number, c: number }[], positions: Position[] }[] = [];

        const key = (r: number, c: number) => `${r},${c}`;

        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                if (visited.has(key(r, c))) continue;
                // Only traverse Empty cells (part of loop)
                if (this.problem[r][c] !== 0) continue;

                const componentEdges = new Set<string>();
                const componentPositions: Position[] = [];
                const queue: Position[] = [new Position(r, c)];
                visited.add(key(r, c));

                while (queue.length > 0) {
                    const curr = queue.shift()!;
                    componentPositions.push(curr);

                    const neighbors: { r: number, c: number, edge: { type: string, r: number, c: number } }[] = [];
                    if (curr.c < this.cols - 1 && sol.h[curr.r][curr.c]) neighbors.push({ r: curr.r, c: curr.c + 1, edge: { type: 'h', r: curr.r, c: curr.c } });
                    if (curr.c > 0 && sol.h[curr.r][curr.c - 1]) neighbors.push({ r: curr.r, c: curr.c - 1, edge: { type: 'h', r: curr.r, c: curr.c - 1 } });
                    if (curr.r < this.rows - 1 && sol.v[curr.r][curr.c]) neighbors.push({ r: curr.r + 1, c: curr.c, edge: { type: 'v', r: curr.r, c: curr.c } });
                    if (curr.r > 0 && sol.v[curr.r - 1][curr.c]) neighbors.push({ r: curr.r - 1, c: curr.c, edge: { type: 'v', r: curr.r - 1, c: curr.c } });

                    for (const n of neighbors) {
                        const edgeKey = `${n.edge.type}_${n.edge.r}_${n.edge.c}`;
                        componentEdges.add(edgeKey);

                        const k = key(n.r, n.c);
                        if (!visited.has(k)) {
                            visited.add(k);
                            queue.push(new Position(n.r, n.c));
                        }
                    }
                }

                const edgeList = Array.from(componentEdges).map(k => {
                    const parts = k.split('_');
                    return { type: parts[0], r: parseInt(parts[1]), c: parseInt(parts[2]) };
                });
                components.push({ edges: edgeList, positions: componentPositions });
            }
        }
        return components;
    }
}
