import assert from 'assert';
import { MasyuPlayer } from './masyu-player.js';
import { Position } from '../../Domain/Base/position.js';

describe('MasyuPlayer Tests', () => {
    it('should simulate Pointer and Mouse events for a path', async () => {
        const capturedEvents: { type: string; x: number; y: number; buttons: number }[] = [];

        (globalThis as any).window = {
            setTimeout: (fn: Function) => fn()
        };
        (globalThis as any).document = {
            querySelector: (selector: string) => {
                if (selector === 'canvas') {
                    return {
                        getBoundingClientRect: () => ({ left: 10, top: 10, width: 100, height: 100 }),
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

        const path = [new Position(0, 0), new Position(1, 0)];

        await MasyuPlayer.play(path, 5);

        // 3 steps (down, move, up) * 2 event types (Pointer, Mouse) = 6 events
        assert.strictEqual(capturedEvents.length, 6, "Should have 6 events");

        assert.strictEqual(capturedEvents[0].type, 'pointerdown');
        assert.strictEqual(capturedEvents[1].type, 'mousedown');
        assert.strictEqual(capturedEvents[0].x, 20);
        assert.strictEqual(capturedEvents[0].buttons, 1);

        assert.strictEqual(capturedEvents[2].type, 'pointermove');
        assert.strictEqual(capturedEvents[3].type, 'mousemove');
        assert.strictEqual(capturedEvents[2].y, 40);
        assert.strictEqual(capturedEvents[2].buttons, 1);

        assert.strictEqual(capturedEvents[4].type, 'pointerup');
        assert.strictEqual(capturedEvents[5].type, 'mouseup');
        assert.strictEqual(capturedEvents[4].buttons, 0);

        // Cleanup
        delete (globalThis as any).window;
        delete (globalThis as any).document;
        delete (globalThis as any).MouseEvent;
        delete (globalThis as any).PointerEvent;
    });
});
