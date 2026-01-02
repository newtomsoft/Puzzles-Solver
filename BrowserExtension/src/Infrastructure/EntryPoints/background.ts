import { PuzzleRegistry } from '../Base/puzzle-registry.js';

const registry = PuzzleRegistry.createDefault();

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'SOLVE') {
        solvePuzzle(message.html, message.url)
            .then(result => sendResponse(result))
            .catch(err => {
                console.error('Solve error:', err);
                sendResponse({ success: false, error: err.message });
            });
        return true; // Keep channel open
    }
});

async function solvePuzzle(html: string, url: string) {
    const handler = registry.getHandler(url, html);
    if (!handler) {
        throw new Error("No handler found for this puzzle type.");
    }

    console.log(`Using handler for: ${handler.getType()}`);
    const extractionResult = handler.extract(html, url);
    const solution = await handler.solve(extractionResult);

    if (solution) {
        const orderedPath = handler.getOrderedPath(null, solution);
        const blackCells = handler.getBlackCells(solution) || [];
        const rows = (extractionResult.grid && extractionResult.grid.length) || 0;

        return { success: true, solutionPath: orderedPath, blackCells, rows };
    } else {
        return { success: false, error: "No solution found." };
    }
}
