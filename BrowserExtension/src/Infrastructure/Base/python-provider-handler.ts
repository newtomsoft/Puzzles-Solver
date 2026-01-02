import { BasePuzzleHandler } from './base-puzzle-handler.js';
import { ExtractionResult } from './puzzle-handler.js';

/**
 * A generic handler that delegates grid extraction to the Python backend.
 * Used for puzzles where the Python provider is already implemented and robust.
 */
export class PythonProviderHandler extends BasePuzzleHandler {
    constructor(type: string, urlKeyword: string) {
        super(type, urlKeyword);
    }

    extract(html: string, url: string): ExtractionResult {
        // We pass the HTML to the backend so the Python provider can extract the grid.
        return { grid: null, url, html } as any;
    }
}
