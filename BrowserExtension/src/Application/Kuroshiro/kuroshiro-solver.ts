import { KuroshiroCell } from '../../Domain/Kuroshiro/kuroshiro-constants.js';
import { Position } from '../../Domain/Base/position.js';

import { BaseSolver } from '../Base/solver.js';

export class KuroshiroSolver extends BaseSolver<string[][], any> {
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

    // Returns the edge variable for the edge leaving (r,c) in direction dir.
    // For Up, it is v[r-1][c].
    // For Down, it is v[r][c].
    // For Left, it is h[r][c-1].
    // For Right, it is h[r][c].
    getEdgeVar(r: number, c: number, dir: number): any {
        return this.getEdge(r, c, dir);
    }

    protected addConstraints() {
        this.addInitialConstraints();
        this.addLinksConstraints();
    }

    protected addInitialConstraints() {
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

                const isCircle = val === KuroshiroCell.WHITE || val === KuroshiroCell.BLACK;

                if (isCircle) {
                    this.addSumConstraint(edges, 2);
                } else {
                    this.solver.add(this.ctx.Or(sumEdges.eq(2), sumEdges.eq(0)));
                }
            }
        }
    }

    addLinksConstraints() {
        const circles: { r: number, c: number, val: string }[] = [];
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                if (this.problem[r][c] === KuroshiroCell.WHITE || this.problem[r][c] === KuroshiroCell.BLACK) {
                    circles.push({ r, c, val: this.problem[r][c] });
                }
            }
        }

        for (const circle of circles) {
            const sameColorLinks = this.getSameColorCirclesLinkedConstraints(circle.r, circle.c, circle.val);
            const otherColorLinks = this.getOtherColorCirclesLinkedConstraints(circle.r, circle.c, circle.val);

            const allLinks = [...sameColorLinks, ...otherColorLinks];

            // Sum(If(link, 1, 0)) == 2
            let sumLinks = this.ctx.Int.val(0);
            for (const link of allLinks) {
                sumLinks = sumLinks.add(this.ctx.If(link, this.ctx.Int.val(1), this.ctx.Int.val(0)));
            }
            this.solver.add(sumLinks.eq(2));
        }
    }

    getSameColorCirclesLinkedConstraints(r: number, c: number, val: string): any[] {
        // it must have no turn between two circles of the same color
        const constraints: any[] = [];
        const directions = [0, 1, 2, 3]; // Up, Right, Down, Left

        for (const d of directions) {
            const pathConditions: any[] = [];
            let found = false;

            // Check immediate edge
            const edge = this.getEdgeVar(r, c, d);
            if (!edge) continue;
            pathConditions.push(edge.eq(1));

            let currR = r;
            let currC = c;

            // Move one step
            if (d === 0) currR--;
            else if (d === 1) currC++;
            else if (d === 2) currR++;
            else if (d === 3) currC--;

            while (currR >= 0 && currR < this.rows && currC >= 0 && currC < this.cols) {
                const cellVal = this.problem[currR][currC];
                if (cellVal === val) {
                    found = true;
                    break;
                }

                // If not found yet, we must continue straight, so we need the edge in the same direction
                // However, the python code says:
                // constraints.append(self._island_bridges_z3[current_position][direction] == 1)
                // This means the edge LEAVING the current position in the same direction.

                const nextEdge = this.getEdgeVar(currR, currC, d);
                if (!nextEdge) break; // Hit wall

                pathConditions.push(nextEdge.eq(1));

                if (d === 0) currR--;
                else if (d === 1) currC++;
                else if (d === 2) currR++;
                else if (d === 3) currC--;
            }

            if (found) {
                if (pathConditions.length > 1) {
                    constraints.push(this.ctx.And(...pathConditions));
                } else if (pathConditions.length === 1) {
                    constraints.push(pathConditions[0]);
                }
            }
        }
        return constraints;
    }

    getOtherColorCirclesLinkedConstraints(r: number, c: number, val: string): any[] {
        // it must have exactly 1 turn between two circles of different colors
        const constraints: any[] = [];
        const otherColor = val === KuroshiroCell.WHITE ? KuroshiroCell.BLACK : KuroshiroCell.WHITE;

        const otherCircles: { r: number, c: number }[] = [];
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                if (this.problem[row][col] === otherColor) {
                    if (row !== r || col !== c) { // Should always be true since color diff
                        otherCircles.push({ r: row, c: col });
                    }
                }
            }
        }

        for (const other of otherCircles) {
            // Horizontal turn pos: (r, other.c) -> same row as start, same col as end
            const horTurnPos = { r: r, c: other.c };
            // Vertical turn pos: (other.r, c) -> same row as end, same col as start
            const vertTurnPos = { r: other.r, c: c };

            // Directions
            const horDir = other.c > c ? 1 : 3; // Right or Left
            const vertDir = other.r > r ? 2 : 0; // Down or Up

            // Path 1: Move Horizontally first, then Vertically
            const horFirstConstraint = this.getToOtherCircleConstraint(r, c, other.r, other.c, horTurnPos.r, horTurnPos.c, horDir, vertDir);

            // Path 2: Move Vertically first, then Horizontally
            const vertFirstConstraint = this.getToOtherCircleConstraint(r, c, other.r, other.c, vertTurnPos.r, vertTurnPos.c, vertDir, horDir);

            // The python code ORs them if both are possible, but Python appends to constraints list.
            // Wait, Python: constraints.append(Or(hor_first, vert_first))
            // BUT: if one of them is False (invalid path due to obstacles), it handles it.

            const paths = [];
            if (horFirstConstraint) paths.push(horFirstConstraint);
            if (vertFirstConstraint) paths.push(vertFirstConstraint);

            if (paths.length > 0) {
                constraints.push(this.ctx.Or(...paths));
            }
        }
        return constraints;
    }

    getToOtherCircleConstraint(startR: number, startC: number, endR: number, endC: number, turnR: number, turnC: number, firstDir: number, secondDir: number): any {
        const constraints: any[] = [];

        // From Start to Turn
        let currR = startR;
        let currC = startC;

        // Edge leaving start
        const firstEdge = this.getEdgeVar(currR, currC, firstDir);
        if (!firstEdge) return null;
        constraints.push(firstEdge.eq(1));

        // Move
        if (firstDir === 0) currR--;
        else if (firstDir === 1) currC++;
        else if (firstDir === 2) currR++;
        else if (firstDir === 3) currC--;

        // Loop until Turn
        while ((currR !== turnR || currC !== turnC)) {
            // Must be empty
            if (this.problem[currR][currC] !== KuroshiroCell.EMPTY) return null;

            const edge = this.getEdgeVar(currR, currC, firstDir);
            if (!edge) return null;
            constraints.push(edge.eq(1));

            if (firstDir === 0) currR--;
            else if (firstDir === 1) currC++;
            else if (firstDir === 2) currR++;
            else if (firstDir === 3) currC--;
        }

        // Check if we hit a wall or something at Turn position?
        // Python: if self._input_grid[current_position] != '': return False
        // This check happens AFTER the loop. The loop condition is `while grid[pos] == '' and pos != turn`.
        // My loop condition is just `!= turn`.
        // So I need to check the cell at the current position (which is now == turn position).
        // Wait, the turn position CAN have a circle?
        // Python:
        // while self._input_grid[current_position] == '' and current_position != turn_position: ...
        // if self._input_grid[current_position] != '': return False
        // This implies the turn position MUST be empty.

        if (this.problem[currR][currC] !== KuroshiroCell.EMPTY) return null;

        // From Turn to End
        // Edge leaving Turn in secondDir
        const secondEdge = this.getEdgeVar(currR, currC, secondDir);
        if (!secondEdge) return null;
        constraints.push(secondEdge.eq(1));

        if (secondDir === 0) currR--;
        else if (secondDir === 1) currC++;
        else if (secondDir === 2) currR++;
        else if (secondDir === 3) currC--;

        // Loop until End
        while (currR !== endR || currC !== endC) {
            // Must be empty
            if (this.problem[currR][currC] !== KuroshiroCell.EMPTY) return null;

            const edge = this.getEdgeVar(currR, currC, secondDir);
            if (!edge) return null;
            constraints.push(edge.eq(1));

            if (secondDir === 0) currR--;
            else if (secondDir === 1) currC++;
            else if (secondDir === 2) currR++;
            else if (secondDir === 3) currC--;
        }

        // We reached End. The cell at End is guaranteed to be the other circle by the caller logic.

        if (constraints.length > 1) {
            return this.ctx.And(...constraints);
        }
        return constraints[0];
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

            // Logic:
            // 1. If only 1 loop and covers all used cells -> Good.
            // 2. If multiple loops -> Bad (Add constraint to break loops).
            // 3. If no loops? (Should not happen if there are circles, as they need degree 2).

            // Check coverage: All "used" cells must be in the single loop.
            // A cell is used if it has edges connected to it.

            if (loops.length === 1) {
                // Check if there are any edges NOT in this loop.
                const loopEdgesCount = loops[0].edges.length;
                let totalEdges = 0;
                for (let r = 0; r < this.rows; r++) {
                    for (let c = 0; c < this.cols - 1; c++) {
                        if (solution.h[r][c]) totalEdges++;
                    }
                }
                for (let r = 0; r < this.rows - 1; r++) {
                    for (let c = 0; c < this.cols; c++) {
                        if (solution.v[r][c]) totalEdges++;
                    }
                }

                if (totalEdges === loopEdgesCount) {
                    this.lastSolution = solution;
                    return solution;
                }
                // If extra edges exist (disconnected components), we need to ban this state?
                // The python code says: "connected_positions = get_connected_positions... if len == 1 return"
                // It treats disconnected components as invalid.
            }

            if (loops.length === 0) {
                // Might happen if grid is empty?
                // But if circles exist, loops > 0.
                // If no circles, empty solution is valid?
                // Python: if len(connected_positions) == 1...
                // If empty grid, connected_positions might be 0?
                // Assuming non-trivial puzzles.
            }

            // Add constraints to ban these specific loops/components
            for (const comp of components) {
                if (comp.edges.length > 0) {
                    const litNot = [];
                    for (const edge of comp.edges) {
                        const z3Var = edge.type === 'h' ? this.h[edge.r][edge.c] : this.v[edge.r][edge.c];
                        litNot.push(z3Var.eq(0)); // At least one edge must be 0
                        // Python logic:
                        // cell_constraints = [edge == val for edge in component]
                        // not_loop = Not(And(cell_constraints))
                        // So: Or(edge != val)
                        // Since val is 1 (it is an edge in the solution), edge != 1 means edge == 0.
                        // So Or(edge == 0 for all edges in loop).
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

                // Only interested in cells that are part of a path
                // Check if any edge is connected to this cell
                const up = (r > 0) && sol.v[r - 1][c];
                const down = (r < this.rows - 1) && sol.v[r][c];
                const left = (c > 0) && sol.h[r][c - 1];
                const right = (c < this.cols - 1) && sol.h[r][c];

                if (!up && !down && !left && !right) continue;

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
