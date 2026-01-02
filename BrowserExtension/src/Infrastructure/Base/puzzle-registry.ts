import { PuzzleHandler } from './puzzle-handler.js';
import { BasePuzzleHandler } from './base-puzzle-handler.js';
import { SudokuHandler } from '../Sudoku/sudoku-handler.js';
import { DetourHandler } from '../Detour/detour-handler.js';
import { CountryRoadHandler } from '../CountryRoad/country-road-handler.js';
import { KoburinHandler } from '../Koburin/koburin-handler.js';
import { LinesweeperHandler } from '../Linesweeper/linesweeper-handler.js';
import { ShirokuroHandler } from '../Shirokuro/shirokuro-handler.js';
import { KuroshiroHandler } from '../Kuroshiro/kuroshiro-handler.js';
import { MidloopHandler } from '../Midloop/midloop-handler.js';
import { AkariHandler } from '../Akari/akari-handler.js';
import { PythonProviderHandler } from './python-provider-handler.js';

export class PuzzleRegistry {
    private handlers: PuzzleHandler[] = [];

    register(handler: PuzzleHandler) {
        this.handlers.push(handler);
    }

    getHandler(url: string, html: string): PuzzleHandler | null {
        for (const handler of this.handlers) {
            if (handler.detect(url, html)) {
                return handler;
            }
        }
        return null;
    }

    getAllHandlers(): PuzzleHandler[] {
        return this.handlers;
    }

    static createDefault(): PuzzleRegistry {
        const registry = new PuzzleRegistry();
        registry.register(new KoburinHandler());
        registry.register(new DetourHandler());
        registry.register(new LinesweeperHandler());
        registry.register(new CountryRoadHandler());
        registry.register(new ShirokuroHandler());
        registry.register(new KuroshiroHandler());
        registry.register(new SudokuHandler());
        registry.register(new MidloopHandler());
        registry.register(new AkariHandler());

        // Puzzles using Python-based extraction (Python providers)
        registry.register(new PythonProviderHandler('slitherlink', 'slitherlink'));
        registry.register(new PythonProviderHandler('yajilin', 'yajilin'));
        registry.register(new PythonProviderHandler('hashi', 'hashi'));
        registry.register(new PythonProviderHandler('galaxies', 'galaxies'));
        registry.register(new PythonProviderHandler('shingoki', 'shingoki'));

        // Default masyu handler last as it has broadest detection or fallback
        registry.register(new BasePuzzleHandler('masyu', 'masyu'));
        return registry;
    }
}
