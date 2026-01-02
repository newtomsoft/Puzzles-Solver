import { Position } from '../../Domain/Base/position.js';
import { CanvasPlayer } from '../Base/canvas-player.js';

export class DetourPlayer {
    static async play(path: Position[], size: number): Promise<void> {
        await CanvasPlayer.drawPath(path, size, size);
    }
}
