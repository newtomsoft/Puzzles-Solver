import { SudokuProblem, KillerCage } from '../../Domain/Sudoku/sudoku-constants.js';
import { Position } from '../../Domain/Base/position.js';
import { BaseSolver } from '../Base/solver.js';

export class SudokuSolver extends BaseSolver<SudokuProblem, number[][]> {
    cells: any[][];

    constructor(ctx: any, problem: SudokuProblem) {
        super(ctx, problem);
        this.cells = [];
    }

    protected initVars(): void {
        const rows = this.problem.grid.length;
        const cols = this.problem.grid[0].length;

        for (let r = 0; r < rows; r++) {
            this.cells[r] = [];
            for (let c = 0; c < cols; c++) {
                const name = `cell_${r}_${c}`;
                const v = this.ctx.Int.const(name);
                this.cells[r][c] = v;
                this.solver.add(v.ge(1), v.le(Math.max(rows, cols)));

                // Fixed values
                if (this.problem.grid[r][c] !== null && this.problem.grid[r][c]! > 0) {
                     this.solver.add(v.eq(this.problem.grid[r][c]));
                }
            }
        }
    }

    protected addConstraints() {
        const rows = this.problem.grid.length;
        const cols = this.problem.grid[0].length;

        // Row Distinct
        for (let r = 0; r < rows; r++) {
            const rowVars = [];
            for (let c = 0; c < cols; c++) {
                rowVars.push(this.cells[r][c]);
            }
            this.solver.add(this.ctx.Distinct(...rowVars));
        }

        // Col Distinct
        for (let c = 0; c < cols; c++) {
            const colVars = [];
            for (let r = 0; r < rows; r++) {
                colVars.push(this.cells[r][c]);
            }
            this.solver.add(this.ctx.Distinct(...colVars));
        }

        // Regions
        if (this.problem.type === 'jigsaw' && this.problem.regions && this.problem.regions.length > 0) {
            for (const region of this.problem.regions) {
                const regionVars = region.map(p => this.cells[p.r][p.c]);
                if (regionVars.length > 0) {
                    this.solver.add(this.ctx.Distinct(...regionVars));
                }
            }
        } else if (this.problem.type === 'standard' || (this.problem.type === 'killer')) {
             // Standard 3x3 boxes (assuming 9x9)
             // Even killer sudoku usually has 3x3 box constraints unless specified otherwise
             if (rows === 9 && cols === 9) {
                 for (let br = 0; br < 3; br++) {
                     for (let bc = 0; bc < 3; bc++) {
                         const boxVars = [];
                         for (let r = 0; r < 3; r++) {
                             for (let c = 0; c < 3; c++) {
                                 boxVars.push(this.cells[br * 3 + r][bc * 3 + c]);
                             }
                         }
                         this.solver.add(this.ctx.Distinct(...boxVars));
                     }
                 }
             }
        }

        // Killer Cages
        if (this.problem.type === 'killer' && this.problem.cages) {
            for (const cage of this.problem.cages) {
                const cageVars = cage.cells.map(p => this.cells[p.r][p.c]);

                // Sum constraint
                this.addSumConstraint(cageVars, cage.sum);

                // Distinct constraint within cage
                this.solver.add(this.ctx.Distinct(...cageVars));
            }
        }
    }

    async solve(): Promise<number[][] | null> {
        this.initVars();
        this.addConstraints();

        const result = await this.solver.check();
        if (result !== 'sat') {
            return null;
        }

        const model = this.solver.model();
        const solution: number[][] = [];
        const rows = this.problem.grid.length;
        const cols = this.problem.grid[0].length;

        for (let r = 0; r < rows; r++) {
            solution[r] = [];
            for (let c = 0; c < cols; c++) {
                const val = model.eval(this.cells[r][c]);
                solution[r][c] = parseInt(val.toString());
            }
        }
        return solution;
    }
}
