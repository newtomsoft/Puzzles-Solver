import { CanvasPlayer } from '../Base/canvas-player.js';

export class ShirokuroPlayer {
    static async play(solution: { h: boolean[][], v: boolean[][] }, rows: number, cols: number): Promise<void> {
        const path = CanvasPlayer.edgesToPath(solution.h, solution.v, rows, cols);
        await CanvasPlayer.drawPath(path, rows, cols);
    }
}
