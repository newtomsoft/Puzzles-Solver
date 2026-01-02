import assert from 'node:assert/strict';
import { KuroshiroGridProvider } from './kuroshiro-grid-provider.js';
import { KuroshiroCell } from '../../Domain/Kuroshiro/kuroshiro-constants.js';

const W = KuroshiroCell.WHITE;
const B = KuroshiroCell.BLACK;
const _ = KuroshiroCell.EMPTY;

describe('KuroshiroGridProvider Tests', () => {

    it('should extract grid from HTML correctly', () => {
        const rawData = ".2.1.1.2.";
        const b64 = Buffer.from(rawData).toString('base64');
        const pqq = "###" + b64;

        const html = `
            <script>
            gpl.Size = 3;
            gpl.pqq = "${pqq}";
            </script>
        `;

        const grid = KuroshiroGridProvider.getGridFromHTML(html);

        const expected = [
            [_, B, _],
            [W, _, W],
            [_, B, _]
        ];

        assert.deepStrictEqual(grid, expected);
    });
});
