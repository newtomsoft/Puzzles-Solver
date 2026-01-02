import { DetourCell } from '../../Domain/Detour/detour-constants.js';
import { Position } from '../../Domain/Base/position.js';
import { BaseSolver } from '../Base/solver.js';

export interface DetourSolution {
    h: boolean[][];
    v: boolean[][];
}

export interface DetourProblem {
    clues: number[][];
    regions: number[][];
}

export class DetourSolver extends BaseSolver<DetourProblem, DetourSolution> {
    private h_vars: any[][];
    private v_vars: any[][];

    constructor(ctx: any, problem: DetourProblem) {
        super(ctx, problem);
        this.h_vars = [];
        this.v_vars = [];
    }

    protected initVars(): void {
        for (let r = 0; r < this.rows; r++) {
            this.h_vars[r] = [];
            for (let c = 0; c < this.cols - 1; c++) {
                const v = this.ctx.Int.const(`h_${r}_${c}`);
                this.h_vars[r][c] = v;
                this.solver.add(v.ge(0), v.le(1));
            }
        }

        for (let r = 0; r < this.rows - 1; r++) {
            this.v_vars[r] = [];
            for (let c = 0; c < this.cols; c++) {
                const v = this.ctx.Int.const(`v_${r}_${c}`);
                this.v_vars[r][c] = v;
                this.solver.add(v.ge(0), v.le(1));
            }
        }
    }

    private getEdges(r: number, c: number) {
        const edges = [];
        if (c > 0) edges.push(this.h_vars[r][c - 1]); // Left
        if (c < this.cols - 1) edges.push(this.h_vars[r][c]); // Right
        if (r > 0) edges.push(this.v_vars[r - 1][c]); // Up
        if (r < this.rows - 1) edges.push(this.v_vars[r][c]); // Down
        return edges;
    }

    protected addConstraints() {
        // 1. Every cell has exactly degree 2 (loop passes through all squares)
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const edges = this.getEdges(r, c);
                this.addSumConstraint(edges, 2);
            }
        }

        // 2. Region turn clues
        const regionToPositions = new Map<number, { r: number, c: number }[]>();
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const rid = this.problem.regions[r][c];
                if (!regionToPositions.has(rid)) regionToPositions.set(rid, []);
                regionToPositions.get(rid)!.push({ r, c });
            }
        }

        const regionToClue = new Map<number, number>();
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const clue = this.problem.clues[r][c];
                if (clue !== DetourCell.EMPTY) {
                    const rid = this.problem.regions[r][c];
                    const existing = regionToClue.get(rid) || -1;
                    if (clue > existing) regionToClue.set(rid, clue);
                }
            }
        }

        for (const [rid, clue] of regionToClue.entries()) {
            const positions = regionToPositions.get(rid)!;
            const turnIndicators = positions.map(p => {
                const r = p.r, c = p.c;
                const left = c > 0 ? this.h_vars[r][c - 1] : this.ctx.Int.val(0);
                const right = c < this.cols - 1 ? this.h_vars[r][c] : this.ctx.Int.val(0);
                const up = r > 0 ? this.v_vars[r - 1][c] : this.ctx.Int.val(0);
                const down = r < this.rows - 1 ? this.v_vars[r][c] : this.ctx.Int.val(0);

                // A turn happens if (left+right == 1) and (up+down == 1)
                // Since deg=2, if either is 1, the other must be 1 to make total 2.
                const turn = this.ctx.If(
                    this.ctx.And(
                        left.add(right).eq(1),
                        up.add(down).eq(1)
                    ),
                    1, 0
                );
                return turn;
            });

            this.solver.add(this.ctx.Sum(...turnIndicators).eq(clue));
        }
    }

    async solve(): Promise<DetourSolution | null> {
        this.initVars();
        this.addConstraints();

        while (true) {
            const res = await this.solver.check();
            if (res !== 'sat') return null;

            const model = this.solver.model();
            const h = this.h_vars.map(row => row.map(v => model.eval(v).toString() === '1'));
            const v = this.v_vars.map(row => row.map(v => model.eval(v).toString() === '1'));

            const solution: DetourSolution = { h, v };
            const components = this.findComponents(solution);

            if (components.length === 1) {
                return solution;
            }

            // Sub-tour elimination
            for (const component of components) {
                const lits = [];
                for (const edge of component.edges) {
                    const z3Var = edge.type === 'h' ? this.h_vars[edge.r][edge.c] : this.v_vars[edge.r][edge.c];
                    lits.push(z3Var.eq(0));
                }
                this.solver.add(this.ctx.Or(...lits));
            }
        }
    }

    private findComponents(sol: DetourSolution) {
        const visited = new Set<string>();
        const components: { edges: { type: string, r: number, c: number }[] }[] = [];
        const key = (r: number, c: number) => `${r},${c}`;

        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                if (visited.has(key(r, c))) continue;

                // Check if cell is part of any loop (it should be in Detour)
                const hasEdge = (c < this.cols - 1 && sol.h[r][c]) ||
                    (c > 0 && sol.h[r][c - 1]) ||
                    (r < this.rows - 1 && sol.v[r][c]) ||
                    (r > 0 && sol.v[r - 1][c]);

                if (!hasEdge) continue;

                const componentEdges = new Set<string>();
                const queue: { r: number, c: number }[] = [{ r, c }];
                visited.add(key(r, c));

                while (queue.length > 0) {
                    const curr = queue.shift()!;
                    const neighbors: { r: number, c: number, type: string, er: number, ec: number }[] = [];

                    if (curr.c < this.cols - 1 && sol.h[curr.r][curr.c])
                        neighbors.push({ r: curr.r, c: curr.c + 1, type: 'h', er: curr.r, ec: curr.c });
                    if (curr.c > 0 && sol.h[curr.r][curr.c - 1])
                        neighbors.push({ r: curr.r, c: curr.c - 1, type: 'h', er: curr.r, ec: curr.c - 1 });
                    if (curr.r < this.rows - 1 && sol.v[curr.r][curr.c])
                        neighbors.push({ r: curr.r + 1, c: curr.c, type: 'v', er: curr.r, ec: curr.c });
                    if (curr.r > 0 && sol.v[curr.r - 1][curr.c])
                        neighbors.push({ r: curr.r - 1, c: curr.c, type: 'v', er: curr.r - 1, ec: curr.c });

                    for (const n of neighbors) {
                        componentEdges.add(`${n.type}_${n.er}_${n.ec}`);
                        const k = key(n.r, n.c);
                        if (!visited.has(k)) {
                            visited.add(k);
                            queue.push({ r: n.r, c: n.c });
                        }
                    }
                }

                components.push({
                    edges: Array.from(componentEdges).map(k => {
                        const [type, er, ec] = k.split('_');
                        return { type, r: parseInt(er), c: parseInt(ec) };
                    })
                });
            }
        }
        return components;
    }

    getOrderedPath(sol: DetourSolution): Position[] {
        let startR = -1, startC = -1;
        outer: for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                if ((c < this.cols - 1 && sol.h[r][c]) || (r < this.rows - 1 && sol.v[r][c])) {
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
            currR = nextR; currC = nextC;
            if (currR === startR && currC === startC) {
                path.push(new Position(currR, currC));
                break;
            }
        }
        return path;
    }

    async getOtherSolution(): Promise<DetourSolution | null> {
        // Not used by the extension but for tests
        const model = this.solver.model();
        const lits = [];
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols - 1; c++) {
                const val = model.eval(this.h_vars[r][c]).toString();
                lits.push(this.h_vars[r][c].eq(parseInt(val)));
            }
        }
        for (let r = 0; r < this.rows - 1; r++) {
            for (let c = 0; c < this.cols; c++) {
                const val = model.eval(this.v_vars[r][c]).toString();
                lits.push(this.v_vars[r][c].eq(parseInt(val)));
            }
        }
        this.solver.add(this.ctx.Not(this.ctx.And(...lits)));
        return this.solve();
    }
}
