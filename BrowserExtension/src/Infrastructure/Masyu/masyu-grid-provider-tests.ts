import assert from 'node:assert/strict';
import { MasyuGridProvider } from './masyu-grid-provider.js';
import { MasyuCell } from '../../Domain/Masyu/masyu-constants.js';


const W = MasyuCell.WHITE;
const B = MasyuCell.BLACK;
const _ = MasyuCell.EMPTY;

describe('MasyuGridProvider Tests', () => {

    it('should extract grid from HTML correctly', () => {
        const html = `
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Expert 5x5 Masyu Puzzles</title>
</head>
<body>
<script type="text/javascript">
let _lang_akari_no_completed = 'There are some cells that need to be completed.';
// ... lots of code ...
gpl.slug = "masyu";
gpl.pid = "4n544";
gpl.hid = "4n544";
gpl.level = 4;
gpl.pztype = "masyu";
gpl.stage_width = 360;
gpl.stage_height = 360;
gpl.Size = 5;
gpl.pqq = "LkILi5XLkIuLi4uLi5XVy4uLi5XLi4uVy4uQg==";
gpl.paa = "cnxLnxkcnxscnxscnxsZHxkcnxsdXwufC58dWR8dXJ8bHJ8bHJ8bGR8dWR8ZHJ8bHJ8bHJ8bHV8dWR8dXJ8bHJ8bHJ8bHJ8bHU=";
gpl.init();
</script>
</body>
</html>
        `;

        const grid = MasyuGridProvider.getGridFromHTML(html);

        const expected = [
            [_, _, W, _, B],
            [_, _, _, _, _],
            [_, W, W, _, _],
            [_, _, W, _, _],
            [_, W, _, _, B]
        ];

        assert.deepStrictEqual(grid, expected);
    });
});
