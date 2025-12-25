// inject.js
// This script runs in the page context (Main World)

console.log("Masyu Solver Injected Script Loaded");

// Capture the base URL from the currently executing script tag
// This works because this code runs immediately when the script is injected
const currentScriptSrc = document.currentScript ? document.currentScript.src : null;
const extensionBase = currentScriptSrc ? currentScriptSrc.substring(0, currentScriptSrc.lastIndexOf('/') + 1) : null;

// Create UI
function createUI() {
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
            btn.innerText = "Error";
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

async function runSolver() {
    await loadPyodideAndRun();

    if (!extensionBase) {
        throw new Error("Could not determine extension base URL");
    }

    const pythonUrl = extensionBase + "masyu_solver.py";
    console.log("Fetching solver from:", pythonUrl);

    const response = await fetch(pythonUrl);
    if (!response.ok) throw new Error("Failed to fetch masyu_solver.py");
    const pythonCode = await response.text();

    // Prepare Data
    if (!window.gpl) {
        alert("Could not find grid data (window.gpl). Ensure you are on a puzzle page.");
        return;
    }

    const pqq = window.gpl.pqq || window.gpl.pq;
    const size = window.gpl.Size || window.gpl.size;

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
            await simulateDrawing(segments);
        } else {
            alert("No solution found by the backtracking solver.");
        }
    } else {
        console.error("Python script finished but 'solution_segments' was not set.");
    }
}

async function simulateDrawing(segments) {
    // gridpuzzle.com usually uses a canvas with id 'grid' or inside a container
    // We can try to find the canvas by context if id fails, but 'grid' is standard for gpl.
    // Sometimes the canvas is unnamed but is the only canvas in '.game-area'.

    let canvas = document.getElementById('grid');
    if (!canvas) {
        canvas = document.querySelector('canvas');
    }

    if (!canvas) {
        console.error("Canvas element not found");
        return;
    }

    const size = window.gpl.Size || window.gpl.size;
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

    // Iterate and draw lines
    // To ensure lines are drawn correctly, we drag from center to center.
    for (const seg of segments) {
        const [r1, c1, r2, c2] = seg;

        const xStart = rect.left + (c1 + 0.5) * cellW;
        const yStart = rect.top + (r1 + 0.5) * cellH;
        const xEnd = rect.left + (c2 + 0.5) * cellW;
        const yEnd = rect.top + (r2 + 0.5) * cellH;

        dispatch("mousedown", xStart, yStart);
        // Small step for better simulation?
        dispatch("mousemove", (xStart+xEnd)/2, (yStart+yEnd)/2);
        dispatch("mousemove", xEnd, yEnd);
        dispatch("mouseup", xEnd, yEnd);

        await new Promise(r => setTimeout(r, 10)); // Short delay
    }
}

// Initialize
createUI();
