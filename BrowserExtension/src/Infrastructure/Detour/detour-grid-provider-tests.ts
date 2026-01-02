import assert from 'node:assert/strict';
import { DetourGridProvider } from './detour-grid-provider.js';
import * as fs from 'fs';
import * as path from 'path';

describe('DetourGridProvider Tests', () => {
    it.skip('should extract grid and regions from 8x8.html', () => {
        const htmlPath = path.resolve('toMigrate/Detour/8x8.html');
        if (!fs.existsSync(htmlPath)) {
            console.warn('8x8.html not found, skipping test');
            return;
        }
        const html = fs.readFileSync(htmlPath, 'utf-8');
        const { clues, regions } = DetourGridProvider.getGridFromHTML(html);

        assert.strictEqual(clues.length, 8);
        assert.strictEqual(clues[0].length, 8);
        assert.strictEqual(regions.length, 8);
        assert.strictEqual(regions[0].length, 8);

        assert.strictEqual(clues[0][0], 4);
        assert.strictEqual(clues[0][4], 5);
        assert.strictEqual(clues[1][3], 4);
        assert.strictEqual(clues[1][7], 3);
        assert.strictEqual(clues[2][5], 0);
        assert.strictEqual(clues[3][2], 6);
        assert.strictEqual(clues[5][0], 1);
        assert.strictEqual(clues[5][5], 6);

        for (let r = 0; r < 8; r++) {
            for (let c = 0; c < 8; c++) {
                assert.ok(regions[r][c] >= 0, `Cell (${r}, ${c}) has no region`);
            }
        }
    });
});
