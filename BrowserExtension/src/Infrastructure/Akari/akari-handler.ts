import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { AkariGridProvider } from './akari-grid-provider.js';
import { ExtractionResult } from '../Base/puzzle-handler.js';

export class AkariHandler extends BasePuzzleHandler {
    constructor() {
        super('akari', 'lightup');
    }

    detect(url: string, html: string): boolean {
        return url.includes('lightup') || url.includes('akari');
    }

    extract(html: string, url: string): ExtractionResult {
        const data = AkariGridProvider.getGridFromHTML(html);
        return { grid: null, data: data, url };
    }
}
