import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { KuroshiroGridProvider } from './kuroshiro-grid-provider.js';
import { ExtractionResult } from '../Base/puzzle-handler.js';

export class KuroshiroHandler extends BasePuzzleHandler {
    constructor() {
        super('kuroshiro', 'kuroshiro');
    }

    extract(html: string, url: string): ExtractionResult {
        return { grid: KuroshiroGridProvider.getGridFromHTML(html), url };
    }
}
