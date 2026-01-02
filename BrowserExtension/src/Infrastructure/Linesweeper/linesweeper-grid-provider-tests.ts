import assert from 'node:assert/strict';
import { LinesweeperGridProvider } from './linesweeper-grid-provider.js';

describe('LinesweeperGridProvider Tests', () => {

    it('should extract grid from HTML correctly', () => {
        const rawData = "0.2.4.1.3";
        const b64 = Buffer.from(rawData).toString('base64');
        const pqq = "###" + b64;

        const html = `
            <script>
            gpl.Size = 3;
            gpl.pqq = "${pqq}";
            </script>
        `;

        const grid = LinesweeperGridProvider.getGridFromHTML(html);

        const expected = [
            [0, -1, 2],
            [-1, 4, -1],
            [1, -1, 3]
        ];

        assert.deepStrictEqual(grid, expected);
    });
});
