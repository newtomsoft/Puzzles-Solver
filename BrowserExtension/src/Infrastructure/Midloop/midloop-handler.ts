import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { MidloopGridProvider } from './midloop-grid-provider.js';
import { MidLoopSolver } from '../../Application/Midloop/midloop-solver.js';

export class MidloopHandler extends BasePuzzleHandler {
    constructor() {
        super('mid-loop', 'mid-loop');
    }

    detect(url: string, html: string): boolean {
        const u = url.toLowerCase();
        const h = html.toLowerCase();
        return u.includes('mid-loop') || u.includes('midloop') || u.includes('mid_loop') ||
            h.includes('mid-loop') || h.includes('midloop') || h.includes('mid_loop');
    }

    extract(html: string, url: string): any {
        return { grid: MidloopGridProvider.getGridFromHTML(html) };
    }

    async solve(ctx: any, extractionResult: any): Promise<any> {
        const solver = new MidLoopSolver(ctx, extractionResult.grid);
        extractionResult.solverInstance = solver;
        return await solver.solve();
    }
}
