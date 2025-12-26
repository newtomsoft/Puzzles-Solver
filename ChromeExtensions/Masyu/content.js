
// Masyu Content Script
// Extracts grid data and interacts with the page

console.log("Masyu Solver Content Script Loaded");

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getGrid") {
        const gridData = scrapeGrid();
        sendResponse({ grid: gridData });
    } else if (request.action === "applySolution") {
        applySolution(request.solution);
        sendResponse({ success: true });
    }
    return true;
});

function scrapeGrid() {
    // GridPuzzle stores data in a script tag with variables like gpl.pq
    // Since we can't access page variables directly from content script context easily without injection,
    // we will parse the script tags in the DOM.

    const scripts = document.getElementsByTagName('script');
    let pq = null;
    let size = null;

    for (let script of scripts) {
        const text = script.innerText;
        if (text.includes('gpl.pq')) {
            const pqMatch = text.match(/gpl\.pq{1,2}\s*=\s*"(.*?)";/);
            const sizeMatch = text.match(/gpl\.[Ss]ize\s*=\s*(\d+);/);

            if (pqMatch && sizeMatch) {
                pq = pqMatch[1];
                size = parseInt(sizeMatch[1]);
                break;
            }
        }
    }

    if (!pq || !size) {
        console.error("Could not find grid data");
        return null;
    }

    // Decode if needed (basic check if it looks like base64, though Python provider handles it)
    // For simplicity, let's assume it matches the Python logic.
    // However, JS environment might need explicit decoding if it is base64.
    // The Python provider checks 'gpl' prefix or valid base64.
    // Let's just send the raw string and size to Python side?
    // Wait, we are running Python in WASM here. We can replicate the logic in JS or Python.
    // Let's replicate the basic parsing in JS to send a Matrix.

    let decodedPq = pq;
    if (pq.startsWith('gpl')) {
        decodedPq = atob(pq.substring(3));
    }

    // Split into matrix
    const matrix = [];
    let idx = 0;
    // The data string format: each char is a cell.
    // | might be a separator

    const cleanStr = decodedPq.split('|').join('');

    for (let r = 0; r < size; r++) {
        const row = [];
        for (let c = 0; c < size; c++) {
            const char = cleanStr[idx];
            // Convert to domain format: 'w', 'b', ' '
            let val = ' ';
            if (char === 'W') val = 'w';
            else if (char === 'B') val = 'b';
            row.push(val);
            idx++;
        }
        matrix.push(row);
    }

    return matrix;
}

function applySolution(solution) {
    // solution contains h_edges and v_edges (1 or 0)
    // h_edges[r][c] is edge between (r,c) and (r,c+1)
    // v_edges[r][c] is edge between (r,c) and (r+1,c)

    // GridPuzzle interaction: Click on edges or draw lines.
    // Usually clicking the border between cells toggles line/x/empty.
    // We need to find the clickable elements.

    // Reverse engineering the DOM:
    // Cells are likely divs. Edges might be handled by canvas or specific divs.
    // GridPuzzle usually uses Canvas.

    // If it uses Canvas, we can't click DOM elements easily.
    // However, they often have a "keyboard" mode or "click" handler on the canvas.
    // Simulating clicks on coordinates.

    // Let's check if there are clickable elements for edges.
    // Usually hidden divs or we have to calculate coordinates on the canvas.

    const canvas = document.getElementById('canvas_1'); // Common ID
    if (!canvas) {
        console.error("Canvas not found");
        return;
    }

    const rect = canvas.getBoundingClientRect();
    const size = solution.h.length; // rows
    // Approximate cell size
    const cellWidth = rect.width / size;
    const cellHeight = rect.height / size;

    // We need to simulate clicks.
    // Vertical edges: between (r,c) and (r,c+1) ?? No, that's horizontal edge.
    // h_edges[r][c] -> right of (r,c). Center: (c+1)*width, (r+0.5)*height

    const actions = [];

    // Horizontal edges (Right of r,c)
    for (let r = 0; r < size; r++) {
        for (let c = 0; c < size - 1; c++) {
            if (solution.h[r][c] === 1) {
                 // Click the boundary between (r,c) and (r,c+1)
                 const x = (c + 1) * cellWidth;
                 const y = (r + 0.5) * cellHeight;
                 actions.push({x, y});
            }
        }
    }

    // Vertical edges (Bottom of r,c)
    for (let r = 0; r < size - 1; r++) {
        for (let c = 0; c < size; c++) {
            if (solution.v[r][c] === 1) {
                // Click boundary between (r,c) and (r+1,c)
                const x = (c + 0.5) * cellWidth;
                const y = (r + 1) * cellHeight;
                actions.push({x, y});
            }
        }
    }

    processActions(actions, canvas, rect);
}

function processActions(actions, canvas, rect) {
    if (actions.length === 0) return;

    const action = actions.shift();
    const clientX = rect.left + action.x;
    const clientY = rect.top + action.y;

    const eventOpts = {
        bubbles: true,
        cancelable: true,
        view: window,
        clientX: clientX,
        clientY: clientY
    };

    // MouseDown -> MouseUp usually triggers it
    canvas.dispatchEvent(new MouseEvent('mousedown', eventOpts));
    canvas.dispatchEvent(new MouseEvent('mouseup', eventOpts));
    canvas.dispatchEvent(new MouseEvent('click', eventOpts));

    setTimeout(() => processActions(actions, canvas, rect), 10);
}
