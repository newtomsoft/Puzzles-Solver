import { BasePuzzleHandler } from '../Base/base-puzzle-handler.js';
import { MidloopGridProvider } from './midloop-grid-provider.js';
import { ExtractionResult } from '../Base/puzzle-handler.js';

export class MidloopHandler extends BasePuzzleHandler {
    constructor() {
        super('mid-loop', 'mid-loop');
    }

    detect(url: string, html: string): boolean {
        const u = url.toLowerCase();
        return u.includes('mid-loop') || u.includes('midloop') || u.includes('mid_loop');
    }

    extract(html: string, url: string): ExtractionResult {
        return { grid: MidloopGridProvider.getGridFromHTML(html), url };
    }
}
