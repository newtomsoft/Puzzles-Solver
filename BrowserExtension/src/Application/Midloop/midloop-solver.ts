import { BaseSolver } from '../Base/solver.js';
import { Position } from '../../Domain/Base/position.js';

export class MidLoopSolver extends BaseSolver<(number | null)[][], any> {
    h: any[][];
    v: any[][];
    dots: { r: number, c: number }[];

    constructor(ctx: any, grid: (number | null)[][]) {
        super(ctx, grid);
        // Input grid size includes edges.
        // Python: rows_number = (input_grid.rows_number + 1) // 2
        this.rows = Math.ceil(grid.length / 2);
        this.cols = Math.ceil(grid[0].length / 2);

        this.dots = [];
        for (let r = 0; r < grid.length; r++) {
            for (let c = 0; c < grid[r].length; c++) {
                if (grid[r][c] === 1) {
                    // Store as solver coordinates (floating point allowed like Python)
                    this.dots.push({ r: r / 2.0, c: c / 2.0 });
                }
            }
        }

        this.h = [];
        this.v = [];
    }

    protected initVars() {
        this.h = [];
        this.v = [];
        // Horizontal edges: h[r][c] exists for r in 0..rows-1, c in 0..cols-2
        for (let r = 0; r < this.rows; r++) {
            this.h[r] = [];
            for (let c = 0; c < this.cols - 1; c++) {
                const name = `h_${r}_${c}`;
                const v = this.ctx.Int.const(name);
                this.h[r][c] = v;
                this.solver.add(v.ge(0), v.le(1));
            }
        }

        // Vertical edges: v[r][c] exists for r in 0..rows-2, c in 0..cols-1
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

    // Helper to get edge variable in a direction
    // 0: Up, 1: Right, 2: Down, 3: Left
    getEdge(r: number, c: number, dir: number): any {
        if (dir === 0) { // Up
            if (r > 0 && this.v[r - 1]) return this.v[r - 1][c];
        } else if (dir === 1) { // Right
            if (c < this.cols - 1 && this.h[r]) return this.h[r][c];
        } else if (dir === 2) { // Down
            if (r < this.rows - 1 && this.v[r]) return this.v[r][c];
        } else if (dir === 3) { // Left
            if (c > 0 && this.h[r]) return this.h[r][c - 1];
        }
        return this.ctx.Int.val(0);
    }

    protected addConstraints() {
        this.addInitialConstraints();
        this.addMinimalEdgeSegmentsConstraints();
        this.addMinimalInsideSegmentsConstraints();
        this.addSymmetryConstraints();
    }

    addInitialConstraints() {
        // Each node must have degree 0 or 2
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

                this.solver.add(this.ctx.Or(sum.eq(0), sum.eq(2)));
            }
        }
    }

    isOnRow(pos: { r: number, c: number }) {
        return Number.isInteger(pos.r);
    }

    isOnCol(pos: { r: number, c: number }) {
        return Number.isInteger(pos.c);
    }

    // Python: _add_minimal_edge_segments_constraints
    addMinimalEdgeSegmentsConstraints() {
        for (const dot of this.dots) {
            // Check if dot is on edge of the INPUT grid?
            // Python: `_input_grid.is_position_in_edge_up(position)`
            // Input grid size is `inputGrid.length`.
            // Dot coords in input grid are `2 * dot.r`, `2 * dot.c`.
            const ir = dot.r * 2;
            const ic = dot.c * 2;
            const maxIr = this.problem.length - 1;
            const maxIc = this.problem[0].length - 1;

            const isEdgeUp = (ir === 0);
            const isEdgeDown = (ir === maxIr);
            const isEdgeLeft = (ic === 0);
            const isEdgeRight = (ic === maxIc);

            if (isEdgeUp || isEdgeDown) {
                this.solver.add(this.minimalHorizontalSegmentsConstraints(dot));
            }
            if (isEdgeLeft || isEdgeRight) {
                this.solver.add(this.minimalVerticalSegmentsConstraints(dot));
            }
        }
    }

    // Python: _add_minimal_inside_segments_constraints
    addMinimalInsideSegmentsConstraints() {
        for (const dot of this.dots) {
            const ir = dot.r * 2;
            const ic = dot.c * 2;
            const maxIr = this.problem.length - 1;
            const maxIc = this.problem[0].length - 1;

            const isEdgeUp = (ir === 0);
            const isEdgeDown = (ir === maxIr);
            const isEdgeLeft = (ic === 0);
            const isEdgeRight = (ic === maxIc);

            if (!isEdgeUp && !isEdgeDown && !isEdgeLeft && !isEdgeRight) {
                this.solver.add(this.ctx.Or(
                    this.minimalHorizontalSegmentsConstraints(dot),
                    this.minimalVerticalSegmentsConstraints(dot)
                ));
            }
        }
    }

    minimalHorizontalSegmentsConstraints(dot: { r: number, c: number }) {
        // if not dot_position.is_on_row(): return False
        if (!this.isOnRow(dot)) return this.ctx.Bool.val(false);

        const r = dot.r;
        const c = dot.c;

        if (!this.isOnCol(dot)) {
            // Dot is on horizontal edge (between columns)
            // position_left = Position(r, int(c))
            // position_right = right
            // In TS/Solver coords: dot is at (r, c_int + 0.5).
            // It corresponds to h[r][floor(c)].
            const c_left = Math.floor(c);
            // Constraint: left->right == 1 and right->left == 1.
            // This just means h[r][c_left] == 1.
            const edge = this.h[r][c_left];
            return edge.eq(1); // Simplification: Since h is undirected in Z3 (just a number), 1 means used.
        }

        // Dot is on node
        // Left=1, Right=1, Up=0, Down=0
        const left = this.getEdge(r, c, 3);
        const right = this.getEdge(r, c, 1);
        const up = this.getEdge(r, c, 0);
        const down = this.getEdge(r, c, 2);

        const constraints = [];
        if (left) constraints.push(left.eq(1));
        if (right) constraints.push(right.eq(1));
        if (up) constraints.push(up.eq(0));
        if (down) constraints.push(down.eq(0));

        return this.ctx.And(...constraints);
    }

    minimalVerticalSegmentsConstraints(dot: { r: number, c: number }) {
        if (!this.isOnCol(dot)) return this.ctx.Bool.val(false);

        const r = dot.r;
        const c = dot.c;

        if (!this.isOnRow(dot)) {
            // Dot is on vertical edge
            const r_up = Math.floor(r);
            const edge = this.v[r_up][c];
            return edge.eq(1);
        }

        // Dot is on node
        const left = this.getEdge(r, c, 3);
        const right = this.getEdge(r, c, 1);
        const up = this.getEdge(r, c, 0);
        const down = this.getEdge(r, c, 2);

        const constraints = [];
        if (up) constraints.push(up.eq(1));
        if (down) constraints.push(down.eq(1));
        if (left) constraints.push(left.eq(0));
        if (right) constraints.push(right.eq(0));

        return this.ctx.And(...constraints);
    }

    addSymmetryConstraints() {
        for (const dot of this.dots) {
            const ir = dot.r * 2;
            const ic = dot.c * 2;
            const maxIr = this.problem.length - 1;
            const maxIc = this.problem[0].length - 1;

            const onRow = this.isOnRow(dot);
            const onCol = this.isOnCol(dot);

            if (onRow && onCol) {
                // Node: Needs either vertical or horizontal symmetry
                const vert = this.symmetryVerticalSegmentConstraint(dot);
                const horiz = this.symmetryHorizontalSegmentConstraint(dot);
                this.solver.add(this.ctx.Or(vert, horiz));
            } else if (onRow) {
                // Between columns: must have horizontal symmetry
                if (ic > 0 && ic < maxIc) {
                    this.solver.add(this.symmetryHorizontalSegmentConstraint(dot));
                }
            } else if (onCol) {
                // Between rows: must have vertical symmetry
                if (ir > 0 && ir < maxIr) {
                    this.solver.add(this.symmetryVerticalSegmentConstraint(dot));
                }
            }
        }
    }

    symmetryVerticalSegmentConstraint(dot: { r: number, c: number }) {
        const ir = dot.r * 2;
        const maxIr = this.problem.length - 1;
        if (ir === 0 || ir === maxIr) return this.ctx.Bool.val(false);

        const constraints = [];
        const r = dot.r;
        const c = dot.c;

        if (this.isOnRow(dot)) {
            // Dot is on Node (r, c)
            const up = this.getEdge(r, c, 0); // v[r-1][c]
            const down = this.getEdge(r, c, 2); // v[r][c]
            const left = this.getEdge(r, c, 3);
            const right = this.getEdge(r, c, 1);
            if (up) constraints.push(up.eq(1));
            if (down) constraints.push(down.eq(1));
            if (left) constraints.push(left.eq(0));
            if (right) constraints.push(right.eq(0));

            let r_up = r - 1;
            let r_down = r + 1;
            let all_straight = this.ctx.Bool.val(true);

            while (r_up >= 0 && r_down < this.rows) {
                const u_in = this.v[r_up] ? this.v[r_up][c] : null;
                const d_in = this.v[r_down - 1] ? this.v[r_down - 1][c] : null;

                if (!u_in || !d_in) break;

                const u_out = (r_up > 0) ? this.v[r_up - 1][c] : this.ctx.Int.val(0);
                const d_out = (r_down < this.rows - 1) ? this.v[r_down][c] : this.ctx.Int.val(0);

                const up_go_down = u_in.eq(1);
                const down_go_up = d_in.eq(1);
                const both_go_in = this.ctx.And(up_go_down, down_go_up);
                all_straight = this.ctx.And(all_straight, both_go_in);

                // Turn condition: if one turns, both must turn
                constraints.push(this.ctx.Implies(all_straight, u_out.eq(d_out)));

                r_up--;
                r_down++;
            }
        } else {
            // Dot on vertical edge
            const r_floor = Math.floor(r);
            if (this.v[r_floor]) constraints.push(this.v[r_floor][c].eq(1));

            let r_up = r_floor;
            let r_down = r_floor + 1;
            let all_straight = this.ctx.Bool.val(true);

            while (r_up >= 0 && r_down < this.rows) {
                const u_in = this.v[r_up] ? this.v[r_up][c] : null;
                const d_in = this.v[r_down - 1] ? this.v[r_down - 1][c] : null;
                if (!u_in || !d_in) break;

                const u_out = (r_up > 0) ? this.v[r_up - 1][c] : this.ctx.Int.val(0);
                const d_out = (r_down < this.rows - 1) ? this.v[r_down][c] : this.ctx.Int.val(0);

                const up_go_down = u_in.eq(1);
                const down_go_up = d_in.eq(1);
                const both_go_in = this.ctx.And(up_go_down, down_go_up);
                all_straight = this.ctx.And(all_straight, both_go_in);

                constraints.push(this.ctx.Implies(all_straight, u_out.eq(d_out)));

                r_up--;
                r_down++;
            }
        }
        return this.ctx.And(...constraints);
    }

    symmetryHorizontalSegmentConstraint(dot: { r: number, c: number }) {
        const ic = dot.c * 2;
        const maxIc = this.problem[0].length - 1;
        if (ic === 0 || ic === maxIc) return this.ctx.Bool.val(false);

        const constraints = [];
        const r = dot.r;
        const c = dot.c;

        if (this.isOnCol(dot)) {
            // Dot is on Node (r, c)
            const left = this.getEdge(r, c, 3);
            const right = this.getEdge(r, c, 1);
            const up = this.getEdge(r, c, 0);
            const down = this.getEdge(r, c, 2);
            if (left) constraints.push(left.eq(1));
            if (right) constraints.push(right.eq(1));
            if (up) constraints.push(up.eq(0));
            if (down) constraints.push(down.eq(0));

            let c_left = c - 1;
            let c_right = c + 1;
            let all_straight = this.ctx.Bool.val(true);

            while (c_left >= 0 && c_right < this.cols) {
                const l_in = this.h[r] ? this.h[r][c_left] : null;
                const r_in = this.h[r] ? this.h[r][c_right - 1] : null;
                if (!l_in || !r_in) break;

                const l_out = (c_left > 0) ? this.h[r][c_left - 1] : this.ctx.Int.val(0);
                const r_out = (c_right < this.cols - 1) ? this.h[r][c_right] : this.ctx.Int.val(0);

                const left_go_right = l_in.eq(1);
                const right_go_left = r_in.eq(1);
                const both_go_in = this.ctx.And(left_go_right, right_go_left);
                all_straight = this.ctx.And(all_straight, both_go_in);

                constraints.push(this.ctx.Implies(all_straight, l_out.eq(r_out)));

                c_left--;
                c_right++;
            }
        } else {
            // Dot on horizontal edge
            const c_floor = Math.floor(c);
            if (this.h[r]) constraints.push(this.h[r][c_floor].eq(1));

            let c_left = c_floor;
            let c_right = c_floor + 1;
            let all_straight = this.ctx.Bool.val(true);

            while (c_left >= 0 && c_right < this.cols) {
                const l_in = this.h[r] ? this.h[r][c_left] : null;
                const r_in = this.h[r] ? this.h[r][c_right - 1] : null;
                if (!l_in || !r_in) break;

                const l_out = (c_left > 0) ? this.h[r][c_left - 1] : this.ctx.Int.val(0);
                const r_out = (c_right < this.cols - 1) ? this.h[r][c_right] : this.ctx.Int.val(0);

                const left_go_right = l_in.eq(1);
                const right_go_left = r_in.eq(1);
                const both_go_in = this.ctx.And(left_go_right, right_go_left);
                all_straight = this.ctx.And(all_straight, both_go_in);

                constraints.push(this.ctx.Implies(all_straight, l_out.eq(r_out)));

                c_left--;
                c_right++;
            }
        }
        return this.ctx.And(...constraints);
    }

    async solve(previousSolution: any = null) {
        if (!this.h || this.h.length === 0) {
            this.initVars();
            this.addConstraints();
        }

        if (previousSolution) {
            // Block previous solution
            const constraints = [];
            for (let r = 0; r < this.rows; r++) {
                for (let c = 0; c < this.cols - 1; c++) {
                    const val = previousSolution.h[r][c] ? 1 : 0;
                    constraints.push(this.h[r][c].eq(val));
                }
            }
            for (let r = 0; r < this.rows - 1; r++) {
                for (let c = 0; c < this.cols; c++) {
                    const val = previousSolution.v[r][c] ? 1 : 0;
                    constraints.push(this.v[r][c].eq(val));
                }
            }
            this.solver.add(this.ctx.Not(this.ctx.And(...constraints)));
        }

        while (true) {
            const result = await this.solver.check();
            if (result !== 'sat') {
                return null;
            }

            const model = this.solver.model();
            const solution = this.extractSolution(model);

            const components = this.findComponents(solution);
            // Connected components logic
            // We want exactly 1 connected component that contains all active edges.
            // But `findComponents` returns all connected graphs.
            // We filter for those with edges.
            const loops = components.filter(comp => comp.edges.length > 0);

            if (loops.length === 0) {
                // Empty solution? Allowed?
                // If input has dots, it must not be empty (constraints force edges).
                // If input has no dots, empty is valid?
                // Python: `get_solution` returns `IslandGrid.empty()` if unsolvable.
                // If solvable, it returns the solution.
                return solution;
            }

            if (loops.length === 1) {
                return solution;
            }

            // If multiple loops, ban this combination
            const blocking = [];
            for (const loop of loops) {
                // For each loop, at least one edge must be removed (or rather, the whole set of loops is invalid)
                // Standard sub-tour elimination:
                // Block ALL loops?
                // Python: `not_loop_constraints.append(Not(And(cell_constraints)))` for EACH loop.
                // "For positions in connected_positions ... cell_constraints ... Not(And(...))"

                const loopConstraints = [];
                for (const edge of loop.edges) {
                    const z3Var = edge.type === 'h' ? this.h[edge.r][edge.c] : this.v[edge.r][edge.c];
                    // We want to say: It's NOT the case that (ALL these edges are 1)
                    // Wait, Python code: `self._island_bridges_z3[position][direction] == value`
                    // Value is from the model (bridges_number).
                    // So it blocks the EXACT configuration of that loop.
                    loopConstraints.push(z3Var.eq(1));
                }
                blocking.push(this.ctx.Not(this.ctx.And(...loopConstraints)));
            }
            this.solver.add(this.ctx.And(...blocking));
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

    // Copy-paste adaptation from MasyuSolver
    findComponents(sol: { h: boolean[][], v: boolean[][] }) {
        const visited = new Set();
        const components: { edges: { type: string, r: number, c: number }[] }[] = [];
        const key = (r: number, c: number) => `${r},${c}`;

        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                if (visited.has(key(r, c))) continue;

                // Check if this node has any edges
                const hasEdges =
                    (c < this.cols - 1 && sol.h[r][c]) ||
                    (c > 0 && sol.h[r][c - 1]) ||
                    (r < this.rows - 1 && sol.v[r][c]) ||
                    (r > 0 && sol.v[r - 1][c]);

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
                    // Right
                    if (curr.c < this.cols - 1 && sol.h[curr.r][curr.c]) neighbors.push({ ...new Position(curr.r, curr.c + 1), edge: { type: 'h', r: curr.r, c: curr.c } });
                    // Left
                    if (curr.c > 0 && sol.h[curr.r][curr.c - 1]) neighbors.push({ ...new Position(curr.r, curr.c - 1), edge: { type: 'h', r: curr.r, c: curr.c - 1 } });
                    // Down
                    if (curr.r < this.rows - 1 && sol.v[curr.r][curr.c]) neighbors.push({ ...new Position(curr.r + 1, curr.c), edge: { type: 'v', r: curr.r, c: curr.c } });
                    // Up
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
