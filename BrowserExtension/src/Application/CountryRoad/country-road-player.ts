import { CanvasPlayer } from '../Base/canvas-player.js';

export class CountryRoadPlayer {
    static async play(solution: { h: number[][], v: number[][] }, rows: number, cols: number): Promise<void> {
        const path = CanvasPlayer.edgesToPath(solution.h, solution.v, rows, cols);
        await CanvasPlayer.drawPath(path, rows, cols);
    }
}
