import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { DetourGridProvider } from './detour-grid-provider.js';
import { ExtractionResult } from '../Base/puzzle-handler.js';

export class DetourHandler extends BasePuzzleHandler {
    constructor() {
        super('detour', 'detour');
    }

    extract(html: string, url: string): ExtractionResult {
        const res = DetourGridProvider.getGridFromHTML(html);
        return { grid: res.clues, url, clues: res.clues, regions: res.regions };
    }

    getOrderedPath(solver: any, solution: any): any[] | null {
        return super.getOrderedPath(null, solution);
    }
}
