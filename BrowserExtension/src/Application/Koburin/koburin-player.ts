import { Position } from '../../Domain/Base/position.js';
import { CanvasPlayer } from '../Base/canvas-player.js';

export class KoburinPlayer {
    static async play(path: Position[], blackCells: Position[], size: number): Promise<void> {
        // 1. Mark black cells
        await CanvasPlayer.clickCells(blackCells, size, size);

        // 2. Draw loop
        await CanvasPlayer.drawPath(path, size, size);
    }
}
