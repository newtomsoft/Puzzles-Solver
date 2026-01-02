import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { KuroshiroGridProvider } from './kuroshiro-grid-provider.js';
import { KuroshiroSolver } from '../../Application/Kuroshiro/kuroshiro-solver.js';

export class KuroshiroHandler extends BasePuzzleHandler {
    constructor() {
        super('kuroshiro', 'kuroshiro');
    }

    extract(html: string, url: string): any {
        return { grid: KuroshiroGridProvider.getGridFromHTML(html) };
    }

    async solve(ctx: any, extractionResult: any): Promise<any> {
        const solver = new KuroshiroSolver(ctx, extractionResult.grid);
        extractionResult.solverInstance = solver;
        return await solver.solve();
    }
}
