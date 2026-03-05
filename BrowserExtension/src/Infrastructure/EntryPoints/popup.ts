import { PuzzleRegistry } from '../Base/puzzle-registry.js';
import { PuzzleHandler } from '../Base/puzzle-handler.js';

const registry = PuzzleRegistry.createDefault();

document.getElementById('solveBtn')!.onclick = async () => {
    const output = document.getElementById('output') as HTMLDivElement;
    const container = document.getElementById('solutionContainer') as HTMLDivElement;

    container.style.display = 'block';
    updateStatus('Analyzing page...', output);

    try {
        const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
        const tab = tabs[0];
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
            
            const solutionMatrix = solution.matrix || (Array.isArray(solution) && Array.isArray(solution[0]) ? solution : null);
            const rows = (extractionResult.grid && extractionResult.grid.length) ||
                (extractionResult.data && extractionResult.data.rows_number) ||
                (solutionMatrix && solutionMatrix.length) || 0;
            const cols = (extractionResult.grid && extractionResult.grid[0].length) ||
                (extractionResult.data && extractionResult.data.columns_number) ||
                (solutionMatrix && solutionMatrix[0].length) || 0;
            
            await showSolutionOnHTML(tab.id, solution, rows, cols);

            if (puzzleType !== 'sudoku') {
                const orderedPath = handler.getOrderedPath(null, solution);
                const blackCells = handler.getBlackCells(solution) || [];
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


async function showSolutionOnHTML(tabId: number, solution: any, rows: number, cols: number) {
    await chrome.scripting.executeScript({
        target: { tabId },
        func: (sol: any, rows: number, cols: number) => {
            const canvas = document.querySelector('canvas');
            if (!canvas) return;

            const id = 'gridpuzzle-solution-html-overlay';
            const existing = document.getElementById(id);
            if (existing) existing.remove();

            const rect = canvas.getBoundingClientRect();
            const container = document.createElement('div');
            container.id = id;
            container.style.position = 'absolute';
            container.style.top = (window.scrollY + rect.top) + 'px';
            container.style.left = (window.scrollX + rect.left) + 'px';
            container.style.width = rect.width + 'px';
            container.style.height = rect.height + 'px';
            container.style.zIndex = '999999';
            container.style.pointerEvents = 'none';
            container.style.overflow = 'hidden';

            const cellWidth = rect.width / cols;
            const cellHeight = rect.height / rows;
            const fontSize = Math.min(cellWidth, cellHeight) * 0.6;

            const matrix = sol.matrix || (Array.isArray(sol) && Array.isArray(sol[0]) ? sol : null);
            
            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    let value = '';
                    if (matrix) {
                        value = matrix[r][c]?.toString() || '';
                    } else if (sol.black && sol.black[r] && sol.black[r][c]) {
                        value = '●';
                    }

                    if (value && value !== '0' && value !== 'false') {
                        const cell = document.createElement('div');
                        cell.style.position = 'absolute';
                        cell.style.left = (c * cellWidth) + 'px';
                        cell.style.top = (r * cellHeight) + 'px';
                        cell.style.width = cellWidth + 'px';
                        cell.style.height = cellHeight + 'px';
                        cell.style.display = 'flex';
                        cell.style.alignItems = 'center';
                        cell.style.justifyContent = 'center';
                        cell.style.color = '#CCCCCC';
                        cell.style.fontSize = fontSize + 'px';
                        cell.style.fontWeight = 'bold';
                        cell.style.fontFamily = 'Arial';
                        cell.style.textShadow = '-1px -1px 0 #FFF, 1px -1px 0 #FFF, -1px 1px 0 #FFF, 1px 1px 0 #FFF';
                        cell.textContent = value;
                        container.appendChild(cell);
                    }
                }
            }

            if (sol.h && sol.v) {
                const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                svg.setAttribute('width', rect.width.toString());
                svg.setAttribute('height', rect.height.toString());
                svg.style.position = 'absolute';
                svg.style.top = '0';
                svg.style.left = '0';

                const strokeWidth = Math.min(cellWidth, cellHeight) * 0.15;

                for (let r = 0; r < rows; r++) {
                    for (let c = 0; c < cols; c++) {
                        const centerX = c * cellWidth + cellWidth / 2;
                        const centerY = r * cellHeight + cellHeight / 2;

                        if (sol.h[r] && sol.h[r][c]) {
                            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                            line.setAttribute('x1', centerX.toString());
                            line.setAttribute('y1', centerY.toString());
                            line.setAttribute('x2', (centerX + cellWidth).toString());
                            line.setAttribute('y2', centerY.toString());
                            line.setAttribute('stroke', '#CCCCCC');
                            line.setAttribute('stroke-width', strokeWidth.toString());
                            line.setAttribute('stroke-linecap', 'round');
                            svg.appendChild(line);
                        }
                        if (sol.v && sol.v[r] && sol.v[r][c]) {
                            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                            line.setAttribute('x1', centerX.toString());
                            line.setAttribute('y1', centerY.toString());
                            line.setAttribute('x2', centerX.toString());
                            line.setAttribute('y2', (centerY + cellHeight).toString());
                            line.setAttribute('stroke', '#CCCCCC');
                            line.setAttribute('stroke-width', strokeWidth.toString());
                            line.setAttribute('stroke-linecap', 'round');
                            svg.appendChild(line);
                        }
                    }
                }
                container.appendChild(svg);
            }

            document.body.appendChild(container);
        },
        args: [solution, rows, cols]
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

document.getElementById('closeBtn')!.onclick = async () => {
    document.getElementById('solutionContainer')!.style.display = 'none';
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    const tab = tabs[0];
    if (tab && tab.id) {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => {
                const id = 'gridpuzzle-solution-html-overlay';
                const existing = document.getElementById(id);
                if (existing) existing.remove();
            }
        });
    }
};