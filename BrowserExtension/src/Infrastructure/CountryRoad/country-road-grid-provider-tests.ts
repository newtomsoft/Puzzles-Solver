import assert from 'node:assert/strict';
import { CountryRoadGridProvider } from './country-road-grid-provider.js';

describe('CountryRoadGridProvider Tests', () => {

    it('should extract grid and regions from HTML correctly', () => {
        const arRaw = "0101";
        const abRaw = "1111";
        const arB64 = Buffer.from(arRaw).toString('base64');
        const abB64 = Buffer.from(abRaw).toString('base64');

        const pqqRaw = "2..1";
        const pqqB64 = Buffer.from(pqqRaw).toString('base64');

        const html = `
            <script>
            gpl.Size = 2;
            gpl.pqq = "###${pqqB64}";
            gpl.ar_data = "###${arB64}";
            gpl.ab_data = "###${abB64}";
            </script>
        `;

        const { clues, regions } = CountryRoadGridProvider.getGridFromHTML(html);

        const expectedClues = [
            [2, 0],
            [0, 1]
        ];

        const expectedRegions = [
            [0, 0],
            [1, 1]
        ];

        assert.deepStrictEqual(clues, expectedClues);
        assert.deepStrictEqual(regions, expectedRegions);
    });
});
