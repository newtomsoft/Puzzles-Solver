import assert from 'assert';
import { KoburinPlayer } from './koburin-player.js';
import { Position } from '../../Domain/Base/position.js';

describe('KoburinPlayer Tests', () => {
    it('should simulate events for black cells and path', async () => {
        const capturedEvents: { type: string; x: number; y: number; buttons: number }[] = [];

        (globalThis as any).window = {
            setTimeout: (fn: Function) => fn()
        };
        (globalThis as any).document = {
            querySelector: (selector: string) => {
                if (selector === 'canvas') {
                    return {
                        getBoundingClientRect: () => ({ left: 10, top: 10, width: 70, height: 70 }),
                        dispatchEvent: (event: any) => {
                            capturedEvents.push({
                                type: event.type,
                                x: event.clientX,
                                y: event.clientY,
                                buttons: event.buttons
                            });
                        }
                    };
                }
                return null;
            }
        };

        const MockEvent = class {
            type: string;
            clientX: number;
            clientY: number;
            buttons: number;
            constructor(type: string, options: any) {
                this.type = type;
                this.clientX = options.clientX;
                this.clientY = options.clientY;
                this.buttons = options.buttons || 0;
            }
        };
        (globalThis as any).MouseEvent = MockEvent;
        (globalThis as any).PointerEvent = MockEvent;

        const path = [new Position(0, 0), new Position(0, 1)];
        const blackCells = [new Position(1, 1)];
        const size = 7;

        await KoburinPlayer.play(path, blackCells, size);

        // Black cell: 2 events (down, up) * 2 types = 4 events
        // Path: 3 events (down, move, up) * 2 types = 6 events
        // Total = 10 events
        assert.strictEqual(capturedEvents.length, 10, "Should have 10 events");

        // First 4 events are for the black cell at (1,1)
        // Cell width = 70/7 = 10. Center of (1,1) is left+10/2 + 1*10 = 10+5+10 = 25. Same for Y.
        assert.strictEqual(capturedEvents[0].type, 'pointerdown');
        assert.strictEqual(capturedEvents[0].x, 25);
        assert.strictEqual(capturedEvents[0].y, 25);
        assert.strictEqual(capturedEvents[1].type, 'mousedown');

        assert.strictEqual(capturedEvents[2].type, 'pointerup');
        assert.strictEqual(capturedEvents[3].type, 'mouseup');

        // Next 6 events are for the path (0,0) -> (0,1)
        // Cell center of (0,0) is 10+5+0 = 15
        assert.strictEqual(capturedEvents[4].type, 'pointerdown');
        assert.strictEqual(capturedEvents[4].x, 15);
        assert.strictEqual(capturedEvents[4].y, 15);

        // (0,1) center is x=10+5+10=25, y=15
        assert.strictEqual(capturedEvents[6].type, 'pointermove');
        assert.strictEqual(capturedEvents[6].x, 25);
        assert.strictEqual(capturedEvents[6].y, 15);

        assert.strictEqual(capturedEvents[8].type, 'pointerup');

        // Cleanup
        delete (globalThis as any).window;
        delete (globalThis as any).document;
        delete (globalThis as any).MouseEvent;
        delete (globalThis as any).PointerEvent;
    });
});
