import assert from 'assert';
import { MidloopGridProvider } from './midloop-grid-provider.js';
import { MidloopCell } from '../../Domain/Midloop/midloop-constants.js';

describe('MidloopGridProvider', () => {
    it('should extract 3x3 grid (internal 5x5) correctly', () => {
        const html = `
            <script>
                var gpl = {};
                gpl.Size = 3;
                gpl.pqq = "0000000000001000000000001";
            </script>
        `;
        const grid = MidloopGridProvider.getGridFromHTML(html);
        assert.strictEqual(grid.length, 5);
        assert.strictEqual(grid[0].length, 5);
        // "0000000000001000000000001"
        // Index 12 is (2,2)
        assert.strictEqual(grid[2][2], MidloopCell.DOT);
        assert.strictEqual(grid[0][0], MidloopCell.EMPTY);
    });

    it('should handle single quotes and Base64 encoded pqq', () => {
        const html = `
            <script>
                var gpl = {};
                gpl.Size = 3;
                // Base64 for "100000001" is "MTAwMDAwMDAx"
                gpl.pqq = 'MTAwMDAwMDAx';
            </script>
        `;
        const grid = MidloopGridProvider.getGridFromHTML(html);
        assert.strictEqual(grid.length, 5);
        // Dots at (0,0) and (2,2) in puzzle coords -> (0,0) and (4,4) in internal coords
        assert.strictEqual(grid[0][0], MidloopCell.DOT);
        assert.strictEqual(grid[4][4], MidloopCell.DOT);
    });

    it('should handle binary 1 dot representation', () => {
        const html = `
            <script>
                var gpl = {};
                gpl.Size = 2;
                gpl.pqq = "\x01\x00\x00\x01";
            </script>
        `;
        const grid = MidloopGridProvider.getGridFromHTML(html);
        assert.strictEqual(grid.length, 3);
        assert.strictEqual(grid[0][0], MidloopCell.DOT);
        assert.strictEqual(grid[2][2], MidloopCell.DOT);
    });
});
