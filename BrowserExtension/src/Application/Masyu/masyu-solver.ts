import { MasyuCell } from '../../Domain/Masyu/masyu-constants.js';
import { Position } from '../../Domain/Base/position.js';
import { BaseSolver } from '../Base/solver.js';

export class MasyuSolver extends BaseSolver<(string | null)[][], any> {
    rows: number;
    cols: number;
    clues: Record<string, string>;
    h: any[][];
    v: any[][];

    /**
     * @param ctx - Z3 Context
     * @param grid - 2D array representing the puzzle. 'W'/'w' for White, 'B'/'b' for Black, others as empty.
     */
    constructor(ctx: any, grid: (string | null)[][]) {
        super(ctx, grid);
        this.rows = grid.length;
        this.cols = grid[0].length;
        this.clues = {};

        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const val = grid[r][c];
                if (val === 'W' || val === 'w' || val === MasyuCell.WHITE) {
                    this.clues[`${r},${c}`] = MasyuCell.WHITE;
                } else if (val === 'B' || val === 'b' || val === MasyuCell.BLACK) {
                    this.clues[`${r},${c}`] = MasyuCell.BLACK;
                }
            }
        }

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

    protected addConstraints() {
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const edges = [];
                for (let d = 0; d < 4; d++) {
                    const e = this.getEdge(r, c, d);
                    if (e) edges.push(e);
                }

                if (edges.length === 0) continue;

                if (this.clues[`${r},${c}`]) {
                    this.addSumConstraint(edges, 2);
                    this.addClueLogic(r, c, this.clues[`${r},${c}`]);
                } else {
                    let sum = edges[0];
                    for (let i = 1; i < edges.length; i++) {
                        sum = sum.add(edges[i]);
                    }
                    this.solver.add(this.ctx.Or(sum.eq(0), sum.eq(2)));
                }
            }
        }
    }


    addClueLogic(r: number, c: number, type: string) {
        const left = this.getEdge(r, c, 3);
        const right = this.getEdge(r, c, 1);
        const up = this.getEdge(r, c, 0);
        const down = this.getEdge(r, c, 2);

        if (type === MasyuCell.WHITE) {
            let hPossible = null;
            let vPossible = null;

            if (left && right) {
                const leftOfLeft = this.getEdge(r, c - 1, 3);
                const rightOfRight = this.getEdge(r, c + 1, 1);

                const turns = [];
                if (leftOfLeft) turns.push(leftOfLeft.eq(0));
                else turns.push(this.ctx.Bool.val(true));

                if (rightOfRight) turns.push(rightOfRight.eq(0));
                else turns.push(this.ctx.Bool.val(true));

                hPossible = this.ctx.And(left.eq(1), right.eq(1), this.ctx.Or(...turns));
            }

            if (up && down) {
                const upOfUp = this.getEdge(r - 1, c, 0);
                const downOfDown = this.getEdge(r + 1, c, 2);

                const turns = [];
                if (upOfUp) turns.push(upOfUp.eq(0));
                else turns.push(this.ctx.Bool.val(true));

                if (downOfDown) turns.push(downOfDown.eq(0));
                else turns.push(this.ctx.Bool.val(true));

                vPossible = this.ctx.And(up.eq(1), down.eq(1), this.ctx.Or(...turns));
            }

            if (hPossible && vPossible) {
                this.solver.add(this.ctx.Or(hPossible, vPossible));
            } else if (hPossible) {
                this.solver.add(hPossible);
            } else if (vPossible) {
                this.solver.add(vPossible);
            } else {
                this.solver.add(this.ctx.Bool.val(false));
            }

        } else if (type === MasyuCell.BLACK) {
            const patterns = [];

            if (up && right) {
                const upLeg = this.getEdge(r - 1, c, 0);
                const rightLeg = this.getEdge(r, c + 1, 1);

                if (upLeg && rightLeg) {
                    patterns.push(this.ctx.And(
                        up.eq(1), right.eq(1),
                        upLeg.eq(1), rightLeg.eq(1)
                    ));
                }
            }

            if (up && left) {
                const upLeg = this.getEdge(r - 1, c, 0);
                const leftLeg = this.getEdge(r, c - 1, 3);
                if (upLeg && leftLeg) {
                    patterns.push(this.ctx.And(
                        up.eq(1), left.eq(1),
                        upLeg.eq(1), leftLeg.eq(1)
                    ));
                }
            }

            if (down && right) {
                const downLeg = this.getEdge(r + 1, c, 2);
                const rightLeg = this.getEdge(r, c + 1, 1);
                if (downLeg && rightLeg) {
                    patterns.push(this.ctx.And(
                        down.eq(1), right.eq(1),
                        downLeg.eq(1), rightLeg.eq(1)
                    ));
                }
            }

            if (down && left) {
                const downLeg = this.getEdge(r + 1, c, 2);
                const leftLeg = this.getEdge(r, c - 1, 3);
                if (downLeg && leftLeg) {
                    patterns.push(this.ctx.And(
                        down.eq(1), left.eq(1),
                        downLeg.eq(1), leftLeg.eq(1)
                    ));
                }
            }

            if (patterns.length > 0) {
                this.solver.add(this.ctx.Or(...patterns));
            } else {
                this.solver.add(this.ctx.Bool.val(false));
            }
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
                if (Object.keys(this.clues).length > 0) {
                    console.error("No loops found despite clues.");
                    return null;
                }
                return solution;
            }

            if (loops.length === 1) {
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

                const activeEdges = [];
                if (c < this.cols - 1 && sol.h[r][c]) activeEdges.push({ type: 'h', r, c, nr: r, nc: c + 1 });
                if (c > 0 && sol.h[r][c - 1]) activeEdges.push({ type: 'h', r: r, c: c - 1, nr: r, nc: c - 1 }); // Edge is identified by top-left coord
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


