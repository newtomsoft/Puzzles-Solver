import '../../libs/z3-built.js';
import '../../libs/z3-bundle.js';
import { MasyuGridProvider } from '../Masyu/masyu-grid-provider.js';
import { KoburinGridProvider } from '../Koburin/koburin-grid-provider.js';
import { DetourGridProvider } from '../Detour/detour-grid-provider.js';
import { MasyuSolver } from '../../Application/Masyu/masyu-solver.js';
import { KoburinSolver } from '../../Application/Koburin/koburin-solver.js';
import { DetourSolver, DetourProblem } from '../../Application/Detour/detour-solver.js';

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'SOLVE') {
        solvePuzzle(message.html, message.url)
            .then(result => sendResponse(result))
            .catch(err => sendResponse({ success: false, error: err.message }));
        return true; // Keep channel open
    }
});

async function solvePuzzle(html: string, url: string) {
    let puzzleType = 'masyu';
    if (url.includes('koburin')) {
        puzzleType = 'koburin';
    } else if (url.includes('detour')) {
        puzzleType = 'detour';
    }

    let grid: any;
    let detourData: { clues: number[][], regions: number[][] } | null = null;

    if (puzzleType === 'koburin') {
        grid = KoburinGridProvider.getGridFromHTML(html);
    } else if (puzzleType === 'detour') {
        detourData = DetourGridProvider.getGridFromHTML(html);
        grid = detourData.clues; // Use clues for size reference
    } else {
        grid = MasyuGridProvider.getGridFromHTML(html);
    }

    if (!(globalThis as any).Z3) {
        throw new Error("Z3 library not loaded.");
    }
    const z3 = await (globalThis as any).Z3();
    try {
        z3.setParam('parallel.enable', 'false');
    } catch (e) {
        console.warn("Could not set global parallel.enable", e);
    }
    const { Context } = z3;

    if (z3.em && typeof z3.em.ccall === 'function') {
        const intArrayToByteArr = (ints: number[]) => new Uint8Array(new Uint32Array(ints).buffer);
        z3.Z3.solver_check = function (c: number, s: number) {
            return z3.em.ccall("Z3_solver_check", "number", ["number", "number"], [c, s]);
        };
        z3.Z3.solver_check_assumptions = function (c: number, s: number, assumptions: number[]) {
            return z3.em.ccall("Z3_solver_check_assumptions", "number", ["number", "number", "number", "array"], [
                c, s, assumptions.length, intArrayToByteArr(assumptions)
            ]);
        };
    }

    const ctx = new Context('main');

    let solution: any;
    let solver: any;
    if (puzzleType === 'koburin') {
        solver = new KoburinSolver(ctx, grid);
        solution = await solver.solve();
    } else if (puzzleType === 'detour') {
        const detourProblem: DetourProblem = { clues: detourData!.clues, regions: detourData!.regions };
        solver = new DetourSolver(ctx, detourProblem);
        solution = await solver.solve();
    } else {
        solver = new MasyuSolver(ctx, grid);
        solution = await solver.solve();
    }

    if (solution) {
        const rows = grid.length;
        const orderedPath = solver.getOrderedPath(solution);
        const blackCells = puzzleType === 'koburin' ?
            solution.black.flatMap((row: boolean[], r: number) =>
                row.map((active, c) => active ? { r, c } : null).filter((x: any) => x !== null)
            ) : [];

        return { success: true, solutionPath: orderedPath, blackCells, rows };
    } else {
        return { success: false, error: "No solution found." };
    }
}
