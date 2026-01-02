import assert from 'node:assert/strict';
import { ShirokuroGridProvider } from './shirokuro-grid-provider.js';
import { ShirokuroCell } from '../../Domain/Shirokuro/shirokuro-constants.js';

const W = ShirokuroCell.WHITE;
const B = ShirokuroCell.BLACK;
const _ = ShirokuroCell.EMPTY;

describe('ShirokuroGridProvider Tests', () => {

    it('should extract grid from HTML correctly with numeric encoding', () => {
        const pqqPayload = Buffer.from("12.").toString('base64');
        const html = `
            <script>
            gpl.Size = 3;
            gpl.pqq = "xxx${pqqPayload}.........."; // Padding for size 3x3=9 chars
            </script>
        `;

        const rawData = "12.......";
        const b64 = Buffer.from(rawData).toString('base64');
        const pqq = "###" + b64; // Prefix

        const html2 = `
            <script>
            gpl.Size = 3;
            gpl.pqq = "${pqq}";
            </script>
        `;

        const grid = ShirokuroGridProvider.getGridFromHTML(html2);

        const expected = [
            [W, B, _],
            [_, _, _],
            [_, _, _]
        ];

        assert.deepStrictEqual(grid, expected);
    });
});
