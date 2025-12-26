
// Popup script
const statusDiv = document.getElementById('status');
const solveBtn = document.getElementById('solveBtn');

let pyodide = null;

async function initPyodide() {
    if (pyodide) return;
    statusDiv.textContent = "Loading Python...";
    // Point to local resources
    pyodide = await loadPyodide({ indexURL: "./lib/" });
    // Load local python files
    const files = [
        'solver_logic.py',
        'solver.py'
    ];

    for (const file of files) {
        const response = await fetch(file);
        const text = await response.text();
        const filename = file.split('/').pop();
        pyodide.FS.writeFile(filename, text);
    }
    statusDiv.textContent = "Python Ready.";
}

solveBtn.addEventListener('click', async () => {
    try {
        statusDiv.textContent = "Initializing...";
        await initPyodide();

        statusDiv.textContent = "Scraping Grid...";
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        chrome.tabs.sendMessage(tab.id, { action: "getGrid" }, async (response) => {
            if (!response || !response.grid) {
                statusDiv.textContent = "Error: No grid found.";
                return;
            }

            statusDiv.textContent = "Solving...";
            const grid = response.grid;

            // Run Python Solver
            // Pass grid as list of lists
            pyodide.globals.set("grid_data", grid);

            const pythonCode = `
import solver
import js

solution = solver.solve_masyu(grid_data.to_py())
solution
            `;

            const solution = await pyodide.runPythonAsync(pythonCode);

            if (!solution) {
                statusDiv.textContent = "No solution found.";
                return;
            }

            const solObj = solution.toJs();
            // Map comes as Map, convert to obj
            const result = {
                h: solObj.get('h'),
                v: solObj.get('v')
            };

            statusDiv.textContent = "Applying...";
            chrome.tabs.sendMessage(tab.id, { action: "applySolution", solution: result });
            statusDiv.textContent = "Done!";
        });

    } catch (err) {
        console.error(err);
        statusDiv.textContent = "Error: " + err.message;
    }
});
