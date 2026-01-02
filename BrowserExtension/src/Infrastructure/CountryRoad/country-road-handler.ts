import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { CountryRoadGridProvider } from './country-road-grid-provider.js';
import { ExtractionResult } from '../Base/puzzle-handler.js';

export class CountryRoadHandler extends BasePuzzleHandler {
    constructor() {
        super('countryroad', 'country');
    }

    extract(html: string, url: string): ExtractionResult {
        const res = CountryRoadGridProvider.getGridFromHTML(html);
        return { grid: res.clues, url, clues: res.clues, regions: res.regions };
    }

    getOrderedPath(solver: any, solution: any): any[] | null {
        return super.getOrderedPath(null, solution);
    }
}
