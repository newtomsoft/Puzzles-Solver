
import { BaseSolver } from '../Base/solver.js';

export interface CountryRoadProblem {
    clues: number[][];
    regions: number[][];
}

export class CountryRoadSolver extends BaseSolver<CountryRoadProblem, any> {
    private h_vars: any[][] = [];
    private v_vars: any[][] = [];

    constructor(ctx: any, problem: CountryRoadProblem) {
        super(ctx, problem);
        this.initVars();
        this.addConstraints();
    }

    protected initVars() {
        const rows = this.rows;
        const cols = this.cols;

        // Horizontal edges: h[r][c] is edge between (r,c) and (r,c+1)
        for (let r = 0; r < rows; r++) {
            const row: any[] = [];
            for (let c = 0; c < cols - 1; c++) {
                row.push(this.ctx.Int.const(`h_${r}_${c}`));
            }
            this.h_vars.push(row);
        }

        // Vertical edges: v[r][c] is edge between (r,c) and (r+1,c)
        for (let r = 0; r < rows - 1; r++) {
            const row: any[] = [];
            for (let c = 0; c < cols; c++) {
                row.push(this.ctx.Int.const(`v_${r}_${c}`));
            }
            this.v_vars.push(row);
        }

        // Used vars: used[r][c] == 1 if cell is part of loop, 0 otherwise
        for (let r = 0; r < rows; r++) {
            const row: any[] = [];
            for (let c = 0; c < cols; c++) {
                // Derived from edges, but useful explicit variable for constraints
                // Actually we can compute it dynamically: sum(edges) == 2 => used=1, sum(edges) == 0 => used=0
                // but explicit variable might be cleaner?
                // Let's stick to edges first as primary variables.
            }
        }
    }

    protected addConstraints() {
        const rows = this.rows;
        const cols = this.cols;

        // Edges must be 0 or 1
        const allEdges: any[] = [];
        this.h_vars.forEach(row => row.forEach(v => allEdges.push(v)));
        this.v_vars.forEach(row => row.forEach(v => allEdges.push(v)));

        allEdges.forEach(e => {
            this.solver.add(this.ctx.And(e.ge(0), e.le(1)));
        });

        // Cell Constraints
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                const edges = this.getEdges(r, c);
                // Degree must be 0 or 2
                // sum(edges) == 2 OR sum(edges) == 0
                let sumEdges: any = edges[0];
                for (let i = 1; i < edges.length; i++) sumEdges = sumEdges.add(edges[i]);
                this.solver.add(this.ctx.Or(sumEdges.eq(2), sumEdges.eq(0)));
            }
        }

        // Region Constraints
        const regionsMap = new Map<number, { r: number, c: number }[]>();
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                const rid = this.problem.regions[r][c];
                if (!regionsMap.has(rid)) regionsMap.set(rid, []);
                regionsMap.get(rid)!.push({ r, c });
            }
        }

        regionsMap.forEach((cells, rid) => {
            // 1. Clue constraint: If region has a number N, exactly N cells must be used.
            // Check if any cell in this region has a clue
            let clue = -1;
            for (const cell of cells) {
                if (this.problem.clues[cell.r][cell.c] > 0) {
                    clue = this.problem.clues[cell.r][cell.c];
                    break;
                }
            }

            if (clue > 0) {
                // Proper logic: Sum(edges touching all cells in region) == clue * 2
                // Each internal edge in region is counted twice (for both cells), each external edge once.
                // Wait, simpler: Sum(used_status_of_cells) == clue.
                // used_status = (sum(edges) == 2) ? 1 : 0.
                // Or: sum(edges per cell) = 2 * used?
                // Yes, Sum(sum(edges_of_cell) for cell in cells) == clue * 2

                const allCellEdgeSums = cells.flatMap(cell => this.getEdges(cell.r, cell.c));
                // Note: getEdges returns the variable reference. h[r][c] will appear twice if it connects two cells in the same region.
                // This is correct: we want to sum degrees of all nodes in the region.
                if (allCellEdgeSums.length > 0) {
                    this.addSumConstraint(allCellEdgeSums, clue * 2);
                }
            }

            // 2. Single Path Constraint: Sum of edges crossing region boundary == 2
            const boundaryEdges = [];
            for (const cell of cells) {
                // Check 4 neighbors. If neighbor is outside region, that edge is a boundary edge.
                // Up
                if (cell.r > 0 && this.problem.regions[cell.r - 1][cell.c] !== rid) {
                    boundaryEdges.push(this.v_vars[cell.r - 1][cell.c]);
                } else if (cell.r === 0) {
                    // Boundary of grid is conceptually boundary of region too? 
                    // No, path doesn't go off grid. Edges are 0.
                    // But strictly speaking, "entering/exiting region" implies connection to another region.
                    // The constraint applies to connections to OTHER regions.
                }

                // Down
                if (cell.r < rows - 1 && this.problem.regions[cell.r + 1][cell.c] !== rid) {
                    boundaryEdges.push(this.v_vars[cell.r][cell.c]);
                }

                // Left
                if (cell.c > 0 && this.problem.regions[cell.r][cell.c - 1] !== rid) {
                    boundaryEdges.push(this.h_vars[cell.r][cell.c - 1]);
                }

                // Right
                if (cell.c < cols - 1 && this.problem.regions[cell.r][cell.c + 1] !== rid) {
                    boundaryEdges.push(this.h_vars[cell.r][cell.c]);
                }
            }
            if (boundaryEdges.length > 0) {
                this.addSumConstraint(boundaryEdges, 2);
            }
        });

        // 3. No adjacent empty cells in different regions
        // For every cell (r,c), look at neighbors (nr, nc).
        // If regions are different:
        // NOT (isEmpty(r,c) AND isEmpty(nr,nc))
        // => NOT (sumEdges(r,c) == 0 AND sumEdges(nr,nc) == 0)
        // => sumEdges(r,c) > 0 OR sumEdges(nr,nc) > 0
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                const myEdges = this.getEdges(r, c);
                let myEdgesSum: any = myEdges[0];
                for (let i = 1; i < myEdges.length; i++) myEdgesSum = myEdgesSum.add(myEdges[i]);
                const neighbors = [
                    { r: r - 1, c: c }, { r: r + 1, c: c }, { r: r, c: c - 1 }, { r: r, c: c + 1 }
                ];

                for (const n of neighbors) {
                    if (n.r >= 0 && n.r < rows && n.c >= 0 && n.c < cols) {
                        if (this.problem.regions[r][c] !== this.problem.regions[n.r][n.c]) {
                            const nEdges = this.getEdges(n.r, n.c);
                            let nEdgesSum: any = nEdges[0];
                            for (let i = 1; i < nEdges.length; i++) nEdgesSum = nEdgesSum.add(nEdges[i]);

                            this.solver.add(this.ctx.Or(
                                myEdgesSum.gt(0),
                                nEdgesSum.gt(0)
                            ));
                        }
                    }
                }
            }
        }
    }

    protected getEdges(r: number, c: number): any[] {
        const edges = [];
        if (r > 0) edges.push(this.v_vars[r - 1][c]); // Up
        if (r < this.rows - 1) edges.push(this.v_vars[r][c]); // Down
        if (c > 0) edges.push(this.h_vars[r][c - 1]); // Left
        if (c < this.cols - 1) edges.push(this.h_vars[r][c]); // Right
        return edges;
    }

    private previousSolution: { h: number[][], v: number[][] } | null = null;

    public async solve(): Promise<{ h: number[][], v: number[][] } | null> {
        while ((await this.solver.check()) === 'sat') {
            const model = this.solver.model();
            const hRes = this.h_vars.map(row => row.map(v => parseInt(model.eval(v).toString())));
            const vRes = this.v_vars.map(row => row.map(v => parseInt(model.eval(v).toString())));

            // Detect multiple loops or empty solution
            // Empty solution (all edges 0) is valid per constraints, but usually ruled out by clues?
            // Actually, if clues exist, empty solution is impossible.
            // But if no clues, empty solution satisfies degree 0 everywhere.
            // Does Country Road allow empty grid? No, usually not.
            // Constraint: "Single loop". So must be non-empty.
            // Check for loop count.

            const components = this.findComponents(hRes, vRes);
            const activeComponents = components.filter(comp => comp.length > 1); // Single node components might be empty cells?
            // Actually findComponents returns sets of connected "used" cells.

            if (activeComponents.length === 0) {
                // No used cells. If grid has clues, this shouldn't happen due to constraints.
                // If no clues, maybe blank is solution? But usually puzzle implies a solution.
                // Force at least one edge?
                // Let's assume there must be at least one loop.
                const allEdges = [...this.h_vars.flat(), ...this.v_vars.flat()];
                this.solver.add(this.ctx.gt(this.ctx.Sum(...allEdges), 0));
                continue;
            }

            if (activeComponents.length === 1) {
                // One loop. Check disjoint "non-empty" components?
                // findComponents should only return components of connected edges.
                // If there is exactly 1 component of edges, we are good.
                this.previousSolution = { h: hRes, v: vRes };
                return this.previousSolution;
            }

            // Multiple components -> Subtour elimination
            for (const comp of activeComponents) {
                // Add constraint: NOT (all edges in this component are present)
                // Actually, standard subtour elimination:
                // Sum(edges leaving set of nodes) >= 2
                // Or simply: NOT (all active edges defined by this solution exist)

                const edgesInComp: any[] = [];
                // Re-identify active edges in this component from model
                // And disable that specific configuration?
                // Better: Pick the component. Sum of cuts >= 2?
                // Or: NOT (this specific subtour).
                // Let's rely on standard practice: Negate the current edges of the subtour?
                // Subtour is a set of vertices connected by edges.
                // Constraint: It shouldn't be a closed loop by itself if there are others.

                // Let's identify the edges that Form this component.
                const currentEdges: any[] = [];
                for (const pos of comp) {
                    // Check internal edges
                    if (pos.c < this.cols - 1 && hRes[pos.r][pos.c] === 1) {
                        currentEdges.push(this.h_vars[pos.r][pos.c]);
                    }
                    if (pos.r < this.rows - 1 && vRes[pos.r][pos.c] === 1) {
                        currentEdges.push(this.v_vars[pos.r][pos.c]);
                    }
                }

                // Removing duplicates (each edge added once or twice?)
                // In above loop, I only check Right and Down.
                // Just be careful: if (r,c) in comp, and (r,c+1) in comp, edge h[r][c] is internal.
                // Is it possible (r,c) in comp but (r,c+1) NOT in comp?
                // If h[r][c] == 1, then they are connected, so both must be in same comp.

                // Uniqueness: using Set of edge names or indices?
                // Simplified: Sum(all active edges in component) < sizes of edges.
                // This breaks THIS specific loop.
                const activeExprs = [];
                for (let r = 0; r < this.rows; r++) {
                    for (let c = 0; c < this.cols; c++) {
                        // Check Right
                        if (c < this.cols - 1 && hRes[r][c] === 1) {
                            if (comp.some(p => p.r === r && p.c === c) && comp.some(p => p.r === r && p.c === c + 1)) {
                                activeExprs.push(this.h_vars[r][c]);
                            }
                        }
                        // Check Down
                        if (r < this.rows - 1 && vRes[r][c] === 1) {
                            if (comp.some(p => p.r === r && p.c === c) && comp.some(p => p.r === r + 1 && p.c === c)) {
                                activeExprs.push(this.v_vars[r][c]);
                            }
                        }
                    }
                }
                this.solver.add(this.ctx.Not(this.ctx.And(...activeExprs.map(e => e.eq(1)))));
            }
        }
        return null; // No solution
    }

    public findComponents(h: number[][], v: number[][]): { r: number, c: number }[][] {
        const rows = this.rows;
        const cols = this.cols;
        const visited = Array.from({ length: rows }, () => Array(cols).fill(false));
        const components: { r: number, c: number }[][] = [];

        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                // If visited or NOT active (isolated node with degree 0)
                // Wait, Degree 0 nodes are "empty". We don't care about them?
                // Yes, finding loops implies traversing connected nodes. nodes with degree 0 don't participate.

                const degree = (r > 0 ? v[r - 1][c] : 0) + (r < rows - 1 ? v[r][c] : 0) +
                    (c > 0 ? h[r][c - 1] : 0) + (c < cols - 1 ? h[r][c] : 0);

                if (degree === 0) continue;

                if (!visited[r][c]) {
                    const comp = [];
                    const q = [{ r, c }];
                    visited[r][c] = true;
                    while (q.length > 0) {
                        const curr = q.pop()!;
                        comp.push(curr);

                        // Neighbors connected by edges
                        // Up
                        if (curr.r > 0 && v[curr.r - 1][curr.c] === 1 && !visited[curr.r - 1][curr.c]) {
                            visited[curr.r - 1][curr.c] = true;
                            q.push({ r: curr.r - 1, c: curr.c });
                        }
                        // Down
                        if (curr.r < rows - 1 && v[curr.r][curr.c] === 1 && !visited[curr.r + 1][curr.c]) {
                            visited[curr.r + 1][curr.c] = true;
                            q.push({ r: curr.r + 1, c: curr.c });
                        }
                        // Left
                        if (curr.c > 0 && h[curr.r][curr.c - 1] === 1 && !visited[curr.r][curr.c - 1]) {
                            visited[curr.r][curr.c - 1] = true;
                            q.push({ r: curr.r, c: curr.c - 1 });
                        }
                        // Right
                        if (curr.c < cols - 1 && h[curr.r][curr.c] === 1 && !visited[curr.r][curr.c + 1]) {
                            visited[curr.r][curr.c + 1] = true;
                            q.push({ r: curr.r, c: curr.c + 1 });
                        }
                    }
                    components.push(comp);
                }
            }
        }
        return components;
    }

    public async getOtherSolution(): Promise<{ h: number[][], v: number[][] } | null> {
        if (!this.previousSolution) return null;

        const { h, v } = this.previousSolution;
        const currentSolutionConstraints: any[] = [];

        // H edges
        for (let r = 0; r < this.h_vars.length; r++) {
            for (let c = 0; c < this.h_vars[0].length; c++) {
                if (h[r][c] === 1) {
                    currentSolutionConstraints.push(this.h_vars[r][c].eq(1));
                } else {
                    currentSolutionConstraints.push(this.h_vars[r][c].eq(0));
                }
            }
        }

        // V edges
        for (let r = 0; r < this.v_vars.length; r++) {
            for (let c = 0; c < this.v_vars[0].length; c++) {
                if (v[r][c] === 1) {
                    currentSolutionConstraints.push(this.v_vars[r][c].eq(1));
                } else {
                    currentSolutionConstraints.push(this.v_vars[r][c].eq(0));
                }
            }
        }

        this.solver.add(this.ctx.Not(this.ctx.And(...currentSolutionConstraints)));

        // Reset previous solution to avoid loop if called multiple times directly
        this.previousSolution = null;

        return this.solve();
    }

    public getOrderedPath(sol: { h: number[][], v: number[][] }): { r: number, c: number }[] {
        const rows = this.rows;
        const cols = this.cols;

        let startR = -1, startC = -1;
        outer: for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                if ((c < cols - 1 && sol.h[r][c] === 1) || (r < rows - 1 && sol.v[r][c] === 1)) {
                    startR = r;
                    startC = c;
                    break outer;
                }
            }
        }
        if (startR === -1) return [];

        const path: { r: number, c: number }[] = [];
        let currR = startR;
        let currC = startC;
        const visitedEdges = new Set<string>();

        while (true) {
            path.push({ r: currR, c: currC });

            let nextR = -1, nextC = -1;
            let edgeKey = "";

            // Check neighbors for connected edges
            // Right
            if (currC < cols - 1 && sol.h[currR][currC] === 1 && !visitedEdges.has(`h_${currR}_${currC}`)) {
                nextR = currR; nextC = currC + 1; edgeKey = `h_${currR}_${currC}`;
            }
            // Left (check edge to the left, which is h[currR][currC-1])
            else if (currC > 0 && sol.h[currR][currC - 1] === 1 && !visitedEdges.has(`h_${currR}_${currC - 1}`)) {
                nextR = currR; nextC = currC - 1; edgeKey = `h_${currR}_${currC - 1}`;
            }
            // Down
            else if (currR < rows - 1 && sol.v[currR][currC] === 1 && !visitedEdges.has(`v_${currR}_${currC}`)) {
                nextR = currR + 1; nextC = currC; edgeKey = `v_${currR}_${currC}`;
            }
            // Up (check edge above, which is v[currR-1][currC])
            else if (currR > 0 && sol.v[currR - 1][currC] === 1 && !visitedEdges.has(`v_${currR - 1}_${currC}`)) {
                nextR = currR - 1; nextC = currC; edgeKey = `v_${currR - 1}_${currC}`;
            }

            if (nextR === -1) break;

            visitedEdges.add(edgeKey);
            currR = nextR;
            currC = nextC;

            if (currR === startR && currC === startC) {
                path.push({ r: currR, c: currC }); // Close loop
                break;
            }
        }
        return path;
    }
}
