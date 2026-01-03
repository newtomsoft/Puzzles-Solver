// inject.js
// This script runs in the page context (Main World)

console.log("Masyu Solver Injected Script Loaded");

// Capture the base URL from the currently executing script tag
const currentScriptSrc = document.currentScript ? document.currentScript.src : null;
const extensionBase = currentScriptSrc ? currentScriptSrc.substring(0, currentScriptSrc.lastIndexOf('/') + 1) : null;

// Create UI
function createUI() {
    if (document.getElementById("masyu-solve-btn")) return; // Prevent duplicate buttons

    const title = document.querySelector('h1') || document.body;
    const btn = document.createElement('button');
    btn.innerText = "Solve Masyu";
    btn.id = "masyu-solve-btn";
    btn.style.marginLeft = "20px";
    btn.style.padding = "5px 10px";
    btn.style.backgroundColor = "#4CAF50";
    btn.style.color = "white";
    btn.style.border = "none";
    btn.style.cursor = "pointer";
    btn.style.fontSize = "16px";
    btn.style.borderRadius = "4px";
    btn.style.verticalAlign = "middle";

    btn.onclick = async () => {
        btn.innerText = "Solving...";
        btn.disabled = true;
        btn.style.backgroundColor = "#888";
        try {
            await runSolver();
            btn.innerText = "Solved!";
            btn.style.backgroundColor = "#4CAF50";
        } catch (e) {
            console.error("Solver failed:", e);
            btn.innerText = "Error: " + e.message;
            btn.style.backgroundColor = "#f44336";
        }
        setTimeout(() => {
            btn.disabled = false;
            btn.innerText = "Solve Masyu";
            btn.style.backgroundColor = "#4CAF50";
        }, 3000);
    };

    // Insert after h1 if possible
    if (document.querySelector('h1')) {
        document.querySelector('h1').appendChild(btn);
    } else {
        document.body.prepend(btn);
    }
}

// Load Pyodide
async function loadPyodideAndRun() {
    if (!window.pyodide) {
        console.log("Loading Pyodide...");
        const script = document.createElement('script');
        script.src = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js";
        document.head.appendChild(script);

        await new Promise((resolve, reject) => {
            script.onload = resolve;
            script.onerror = reject;
        });
        window.pyodide = await loadPyodide();
        console.log("Pyodide loaded");
    }
}

// Helper to extract GPL data from scripts if window.gpl is missing
function extractGplFromScripts() {
    console.log("Attempting to extract GPL data from script tags...");
    const scripts = document.getElementsByTagName('script');
    let pqq = null;
    let size = null;

    // Regex patterns matching the Python provider
    const sizeRegex = /gpl\.([Ss]ize)\s*=\s*(\d+);/;
    const pqqRegex = /gpl\.pq{1,2}\s*=\s*"(.*?)";/;

    for (let script of scripts) {
        if (script.innerHTML) {
            const content = script.innerHTML;

            if (!size) {
                const sizeMatch = content.match(sizeRegex);
                if (sizeMatch) size = parseInt(sizeMatch[2]);
            }

            if (!pqq) {
                const pqqMatch = content.match(pqqRegex);
                if (pqqMatch) pqq = pqqMatch[1];
            }

            if (size && pqq) break;
        }
    }

    if (size && pqq) {
        return { Size: size, pqq: pqq };
    }
    return null;
}

async function runSolver() {
    await loadPyodideAndRun();

    if (!extensionBase) {
        throw new Error("Could not determine extension base URL");
    }

    const pythonUrl = extensionBase + "masyu_solver.py";

    const response = await fetch(pythonUrl);
    if (!response.ok) throw new Error("Failed to fetch masyu_solver.py");
    const pythonCode = await response.text();

    // Prepare Data
    let gplData = window.gpl;

    if (!gplData) {
        gplData = extractGplFromScripts();
    }

    if (!gplData) {
        throw new Error("Could not find grid data (window.gpl or script tags). Ensure you are on a puzzle page.");
    }

    const pqq = gplData.pqq || gplData.pq;
    const size = gplData.Size || gplData.size;

    if (!pqq || !size) {
         throw new Error(`Incomplete grid data found. Size: ${size}, PQQ found: ${!!pqq}`);
    }

    window.pyodide.globals.set("gpl_pqq", pqq);
    window.pyodide.globals.set("gpl_size", size);

    // Run Python
    console.log("Running Python Solver...");
    await window.pyodide.runPythonAsync(pythonCode);

    // Get result
    if (window.pyodide.globals.get("solution_segments")) {
        const segments = window.pyodide.globals.get("solution_segments").toJs();
        console.log("Solution segments found:", segments.length);

        if (segments && segments.length > 0) {
            await simulateDrawing(segments, size);
        } else {
            alert("No solution found by the backtracking solver.");
        }
    } else {
        console.error("Python script finished but 'solution_segments' was not set.");
    }
}

async function simulateDrawing(segments, size) {
    let canvas = document.getElementById('grid');
    if (!canvas) {
        canvas = document.querySelector('canvas');
    }

    if (!canvas) {
        console.error("Canvas element not found");
        return;
    }

    // If we didn't get size passed, try to extract from data
    if (!size) size = window.pyodide.globals.get("gpl_size");

    const rect = canvas.getBoundingClientRect();
    const cellW = rect.width / size;
    const cellH = rect.height / size;

    // Helper to dispatch events
    function dispatch(type, x, y) {
        const ev = new MouseEvent(type, {
            view: window,
            bubbles: true,
            cancelable: true,
            clientX: x,
            clientY: y,
            button: 0,
            buttons: 1
        });
        canvas.dispatchEvent(ev);
    }

    for (const seg of segments) {
        const [r1, c1, r2, c2] = seg;

        const xStart = rect.left + (c1 + 0.5) * cellW;
        const yStart = rect.top + (r1 + 0.5) * cellH;
        const xEnd = rect.left + (c2 + 0.5) * cellW;
        const yEnd = rect.top + (r2 + 0.5) * cellH;

        dispatch("mousedown", xStart, yStart);
        dispatch("mousemove", (xStart+xEnd)/2, (yStart+yEnd)/2);
        dispatch("mousemove", xEnd, yEnd);
        dispatch("mouseup", xEnd, yEnd);

        await new Promise(r => setTimeout(r, 10));
    }
}

// Initialize
createUI();
