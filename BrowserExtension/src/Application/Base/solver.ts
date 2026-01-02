export interface Solver<T> {
    solve(): Promise<T | null>;
}

export abstract class BaseSolver<TProblem, TSolution> implements Solver<TSolution> {
    protected ctx: any;
    protected solver: any;
    protected problem: TProblem;
    protected rows: number = 0;
    protected cols: number = 0;

    constructor(ctx: any, problem: TProblem) {
        this.ctx = ctx;
        this.problem = problem;
        this.solver = new ctx.Solver();
        
        if (Array.isArray(problem)) {
            this.rows = problem.length;
            if (this.rows > 0 && Array.isArray(problem[0])) {
                this.cols = problem[0].length;
            }
        } else if (problem && typeof problem === 'object') {
             // Try to find grid in common problem objects
             const p = problem as any;
             const grid = p.grid || p.clues;
             if (Array.isArray(grid)) {
                 this.rows = grid.length;
                 if (this.rows > 0 && Array.isArray(grid[0])) {
                     this.cols = grid[0].length;
                 }
             }
        }
    }

    abstract solve(): Promise<TSolution | null>;

    protected abstract initVars(): void;
    protected abstract addConstraints(): void;

    /**
     * Helper to add a sum constraint to the solver.
     */
    protected addSumConstraint(vars: any[], targetSum: number | any) {
        if (vars.length === 0) {
            if (typeof targetSum === 'number') {
                if (targetSum !== 0) {
                    // This should ideally not happen if logic is correct, 
                    // but we add it for completeness.
                    this.solver.add(this.ctx.False());
                }
            }
            return;
        }

        let sum = vars[0];
        for (let i = 1; i < vars.length; i++) {
            sum = sum.add(vars[i]);
        }
        this.solver.add(sum.eq(targetSum));
    }
}
