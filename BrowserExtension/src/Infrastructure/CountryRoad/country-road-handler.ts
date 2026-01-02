import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { CountryRoadGridProvider } from './country-road-grid-provider.js';
import { CountryRoadSolver } from '../../Application/CountryRoad/country-road-solver.js';

export class CountryRoadHandler extends BasePuzzleHandler {
    constructor() {
        super('countryroad', 'country');
    }

    extract(html: string, url: string): any {
        const res = CountryRoadGridProvider.getGridFromHTML(html);
        return { grid: res.clues, clues: res.clues, regions: res.regions };
    }

    async solve(ctx: any, extractionResult: any): Promise<any> {
        const solver = new CountryRoadSolver(ctx, { clues: extractionResult.clues, regions: extractionResult.regions });
        extractionResult.solverInstance = solver;
        return await solver.solve();
    }

    getOrderedPath(solver: any, solution: any): any[] | null {
        return solver.getOrderedPath(solution);
    }
}
