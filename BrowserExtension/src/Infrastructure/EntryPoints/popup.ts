import { PuzzleRegistry } from '../Base/puzzle-registry.js';
import { PuzzleHandler } from '../Base/puzzle-handler.js';

const registry = PuzzleRegistry.createDefault();

document.getElementById('solveBtn')!.onclick = async () => {
    const output = document.getElementById('output') as HTMLDivElement;
    const container = document.getElementById('solutionContainer') as HTMLDivElement;

    container.style.display = 'block';
    updateStatus('Analyzing page...', output);

    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!tab || !tab.id) {
            updateStatus('No active tab found.', output);
            return;
        }

        const injectionResults = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => document.documentElement.outerHTML
        });

        if (!injectionResults || injectionResults.length === 0 || !injectionResults[0].result) {
            updateStatus('Failed to retrieve page content.', output);
            return;
        }

        const html = injectionResults[0].result;
        const url = tab.url || "";

        const handler = registry.getHandler(url, html);
        if (!handler) {
            updateStatus('Puzzle type not supported.', output);
            return;
        }

        const puzzleType = handler.getType();
        updateStatus(`Type detected: ${puzzleType}. Extracting grid...`, output);

        const extractionResult = handler.extract(html, url);
        await showScrapedOverlay(tab.id, puzzleType, extractionResult);

        updateStatus(`Solving ${puzzleType} via API...`, output);
        const solution = await handler.solve(extractionResult);

        if (solution) {
            const solutionText = handler.getSolutionDisplay(puzzleType, extractionResult, solution);
            await showSolutionOverlay(tab.id, solutionText);

            if (puzzleType !== 'sudoku') {
                const orderedPath = handler.getOrderedPath(null, solution);
                const blackCells = handler.getBlackCells(solution) || [];
                const solutionMatrix = solution.matrix || (Array.isArray(solution) && Array.isArray(solution[0]) ? solution : null);
                const rows = (extractionResult.grid && extractionResult.grid.length) ||
                    (extractionResult.data && extractionResult.data.rows_number) ||
                    (solutionMatrix && solutionMatrix.length) || 0;
                await injectPlayLogic(tab.id, orderedPath, blackCells, rows);
            }
            updateStatus("Solution displayed!", output);
        } else {
            updateStatus("No solution found.", output);
        }
    } catch (e: any) {
        updateStatus('Error: ' + e.message, output);
        console.error(e);
    }
};

function updateStatus(message: string, output: HTMLDivElement) {
    output.textContent = message;
}

async function showScrapedOverlay(tabId: number, puzzleType: string, extractionResult: any) {
    let scrapedDisplay = `Grid Type: ${puzzleType}\n\n`;

    const format2D = (g: any[][]) => g.map(row => row.map(c =>
        c === null ? ' ' : (typeof c === 'object' ? JSON.stringify(c) : c.toString())
    ).join(' ')).join('\n');

    if (extractionResult.regions) {
        scrapedDisplay += "Clues:\n" + format2D(extractionResult.clues) + "\n\n";
        scrapedDisplay += "Regions:\n" + format2D(extractionResult.regions);
    } else if (extractionResult.data && extractionResult.data.black_cells) {
        scrapedDisplay += `Akari Grid (${extractionResult.data.rows_number}x${extractionResult.data.columns_number})\n`;
        scrapedDisplay += `Black Cells: ${extractionResult.data.black_cells.length}\n`;
        scrapedDisplay += `Constraints: ${Object.keys(extractionResult.data.number_constraints).length}`;
    } else if (extractionResult.grid) {
        scrapedDisplay += "Grid:\n" + format2D(extractionResult.grid);
    } else {
        scrapedDisplay += "Extraction delegated to backend (no local preview).";
    }

    await chrome.scripting.executeScript({
        target: { tabId },
        func: (text: string) => {
            const id = 'gridpuzzle-scraped-overlay';
            const existing = document.getElementById(id);
            if (existing) existing.remove();

            const div = document.createElement('div');
            div.id = id;
            div.style.position = 'fixed';
            div.style.top = '20px';
            div.style.left = '20px';
            div.style.backgroundColor = '#f0f0f0';
            div.style.border = '2px solid #555';
            div.style.padding = '15px';
            div.style.zIndex = '999998';
            div.style.fontFamily = 'monospace';
            div.style.fontSize = '12px';
            div.style.boxShadow = '0 4px 12px rgba(0,0,0,0.2)';
            div.style.maxHeight = '90vh';
            div.style.overflow = 'auto';

            const close = document.createElement('button');
            close.textContent = '×';
            close.style.cssText = 'position:absolute;top:2px;right:5px;border:none;background:none;font-size:16px;cursor:pointer;';
            close.onclick = () => div.remove();

            const pre = document.createElement('pre');
            pre.textContent = text;
            pre.style.margin = '10px 0 0 0';

            div.appendChild(close);
            div.appendChild(pre);
            document.body.appendChild(div);
        },
        args: [scrapedDisplay]
    });
}

async function showSolutionOverlay(tabId: number, solutionText: string) {
    await chrome.scripting.executeScript({
        target: { tabId },
        func: (text: string) => {
            const id = 'gridpuzzle-solution-overlay';
            const existing = document.getElementById(id);
            if (existing) existing.remove();
            const div = document.createElement('div');
            div.id = id;
            div.style.position = 'fixed';
            div.style.top = '20px';
            div.style.right = '20px';
            div.style.backgroundColor = 'white';
            div.style.border = '2px solid #333';
            div.style.padding = '15px';
            div.style.zIndex = '999999';
            div.style.whiteSpace = 'pre';
            div.style.fontFamily = 'monospace';

            const close = document.createElement('button');
            close.textContent = '×';
            close.onclick = () => div.remove();
            div.appendChild(close);

            const pre = document.createElement('pre');
            pre.textContent = text;
            div.appendChild(pre);

            document.body.appendChild(div);
        },
        args: [solutionText]
    });
}

async function injectPlayLogic(tabId: number, path: any[] | null, blacks: any[], rows: number) {
    if (!path && blacks.length === 0) return;
    await chrome.scripting.executeScript({
        target: { tabId },
        func: async (p: any[] | null, bl: any[], rws: number) => {
            const playLogic = async (path: any[] | null, blacks: any[]) => {
                const canvas = document.querySelector('canvas');
                if (!canvas) return;
                const rect = canvas.getBoundingClientRect();
                const cellH = rect.height / rws;
                const cellW = cellH;

                const sim = (cx: number, cy: number, type: string, buttons: number) => {
                    canvas.dispatchEvent(new MouseEvent(type, {
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        clientX: cx,
                        clientY: cy,
                        buttons: buttons
                    }));
                };
                for (const b of blacks) {
                    const x = rect.left + cellW / 2 + b.c * cellW;
                    const y = rect.top + cellH / 2 + b.r * cellH;
                    sim(x, y, 'mousedown', 1);
                    sim(x, y, 'mouseup', 0);
                    await new Promise(r => setTimeout(r, 100));
                }

                if (path && path.length > 1) {
                    const start = path[0];
                    sim(rect.left + cellW / 2 + start.c * cellW, rect.top + cellH / 2 + start.r * cellH, 'mousedown', 1);
                    for (let i = 0; i < path.length - 1; i++) {
                        const next = path[i + 1];
                        sim(rect.left + cellW / 2 + next.c * cellW, rect.top + cellH / 2 + next.r * cellH, 'mousemove', 1);
                        await new Promise(r => setTimeout(r, 60));
                    }
                    const end = path[path.length - 1];
                    sim(rect.left + cellW / 2 + end.c * cellW, rect.top + cellH / 2 + end.r * cellH, 'mouseup', 0);
                }
            };
            playLogic(p, bl);
        },
        args: [path, blacks, rows]
    });
}

document.getElementById('closeBtn')!.onclick = () => {
    document.getElementById('solutionContainer')!.style.display = 'none';
};