import assert from 'assert';
import { MidloopHandler } from './midloop-handler.js';

describe('MidloopHandler Detection', () => {
    it('should detect mid-loop puzzles by URL', () => {
        const handler = new MidloopHandler();
        assert.strictEqual(handler.detect('https://fr.gridpuzzle.com/mid-loop', ''), true);
        assert.strictEqual(handler.detect('https://fr.gridpuzzle.com/mid-loop?size=3', ''), true);
        assert.strictEqual(handler.detect('https://fr.gridpuzzle.com/masyu', ''), false);
    });
});
