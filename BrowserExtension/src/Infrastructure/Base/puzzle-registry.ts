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
import { YajikabeHandler } from '../Yajikabe/yajikabe-handler.js';
import { AquariumGridProvider } from '../PuzzlesMobile/Aquarium/aquarium-grid-provider.js';
import { TapaGridProvider } from '../PuzzlesMobile/Tapa/tapa-grid-provider.js';

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

        // Puzzles Mobile Implementations
        registry.register(new BasePuzzleHandler('aquarium', 'puzzle-aquarium.com', new AquariumGridProvider()));
        registry.register(new BasePuzzleHandler('tapa', 'puzzle-tapa.com', new TapaGridProvider()));
        registry.register(new BasePuzzleHandler('nurikabe', 'puzzle-nurikabe.com', new TapaGridProvider()));
        registry.register(new BasePuzzleHandler('hitori', 'puzzle-hitori.com', new TapaGridProvider()));
        registry.register(new BasePuzzleHandler('heyawake', 'puzzle-heyawake.com', new TapaGridProvider()));
        registry.register(new BasePuzzleHandler('minesweeper', 'puzzle-minesweeper.com', new TapaGridProvider()));
        registry.register(new BasePuzzleHandler('binairo', 'puzzle-binairo.com', new TapaGridProvider()));
        registry.register(new BasePuzzleHandler('fillomino', 'puzzle-fillomino.com', new TapaGridProvider()));
        registry.register(new BasePuzzleHandler('shakashaka', 'puzzle-shakashaka.com', new TapaGridProvider()));
        // registry.register(new BasePuzzleHandler('tents', 'puzzle-tents.com', new TapaGridProvider())); // Tents usually has outside clues but TapaProvider might extract grid if clues are in grid? No, Tents has outside clues.
        // Tents needs Aquarium-like provider (Outside clues + Grid).
        registry.register(new BasePuzzleHandler('norinori', 'puzzle-norinori.com', new AquariumGridProvider())); // Regions
        registry.register(new BasePuzzleHandler('starbattle', 'puzzle-star-battle.com', new AquariumGridProvider())); // Regions
        registry.register(new BasePuzzleHandler('renkatsu', 'puzzle-renkatsu.com', new AquariumGridProvider())); // Regions

        // Existing handlers
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
        registry.register(new YajikabeHandler());

        // Default masyu handler last as it has broadest detection or fallback
        registry.register(new BasePuzzleHandler('masyu', 'masyu'));
        return registry;
    }
}
