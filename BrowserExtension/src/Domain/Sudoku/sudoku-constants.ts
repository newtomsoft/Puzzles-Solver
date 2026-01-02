import { Position } from '../Base/position.js';

export interface KillerCage {
    sum: number;
    cells: Position[];
}

export interface SudokuProblem {
    type: 'standard' | 'jigsaw' | 'killer';
    grid: (number | null)[][];
    regions?: Position[][]; // For Jigsaw (and Standard, explicitly)
    cages?: KillerCage[]; // For Killer
}
