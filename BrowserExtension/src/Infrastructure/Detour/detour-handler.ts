import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { DetourGridProvider } from './detour-grid-provider.js';
import { DetourSolver } from '../../Application/Detour/detour-solver.js';

export class DetourHandler extends BasePuzzleHandler {
    constructor() {
        super('detour', 'detour');
    }

    extract(html: string, url: string): any {
        const res = DetourGridProvider.getGridFromHTML(html);
        return { grid: res.clues, clues: res.clues, regions: res.regions };
    }

    async solve(ctx: any, extractionResult: any): Promise<any> {
        const solver = new DetourSolver(ctx, { clues: extractionResult.clues, regions: extractionResult.regions });
        extractionResult.solverInstance = solver;
        return await solver.solve();
    }

    getOrderedPath(solver: any, solution: any): any[] | null {
        return solver.getOrderedPath(solution);
    }
}
