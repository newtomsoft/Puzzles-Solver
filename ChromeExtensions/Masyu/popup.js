
// Popup script for Masyu WASM Solver
const statusDiv = document.getElementById('status');
const solveBtn = document.getElementById('solveBtn');

let dotnetExports = null;

async function initWasm() {
    if (dotnetExports) return;
    statusDiv.textContent = "Loading WASM...";

    try {
        // Import dotnet runtime
        const { dotnet } = await import('./dotnet.js');

        // Initialize runtime
        const { getAssemblyExports, getConfig } = await dotnet
            .withDiagnosticTracing(false)
            .create();

        // Get exports from our assembly
        const exports = await getAssemblyExports("MasyuSolver.dll");
        dotnetExports = exports.MasyuSolver.Program;

        statusDiv.textContent = "WASM Ready.";
    } catch (e) {
        console.error(e);
        statusDiv.textContent = "WASM Load Error: " + e.message;
        throw e;
    }
}

solveBtn.addEventListener('click', async () => {
    try {
        statusDiv.textContent = "Initializing...";
        await initWasm();

        statusDiv.textContent = "Scraping Grid...";
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        chrome.tabs.sendMessage(tab.id, { action: "getGrid" }, async (response) => {
            if (chrome.runtime.lastError) {
                statusDiv.textContent = "Error: " + chrome.runtime.lastError.message;
                return;
            }
            if (!response || !response.grid) {
                statusDiv.textContent = "Error: No grid found.";
                return;
            }

            statusDiv.textContent = "Solving...";
            const grid = response.grid;

            // Grid is string[][]
            // Pass to WASM
            // Note: JS string array maps to string[] in C# if marshaling works,
            // but simple marshaling might need adjustment.
            // With JSExport, string[] should be supported.

            // Flatten rows to strings for safety if needed, or pass array directly.
            // Let's pass array of strings.
            const gridRows = grid.map(row => row.join(''));

            const resultStr = dotnetExports.Solve(gridRows);

            if (!resultStr || resultStr.startsWith("ERROR") || resultStr === "NO_SOLUTION") {
                statusDiv.textContent = resultStr || "No Solution Found";
                return;
            }

            // Parse result: ROWS|COLS|H_STRING|V_STRING
            const parts = resultStr.split('|');
            const rows = parseInt(parts[0]);
            const cols = parseInt(parts[1]);
            const hStr = parts[2];
            const vStr = parts[3];

            const h = [];
            let idx = 0;
            for(let r=0; r<rows; r++) {
                const row = [];
                for(let c=0; c<cols-1; c++) {
                    row.push(parseInt(hStr[idx]));
                    idx++;
                }
                h.push(row);
            }

            const v = [];
            idx = 0;
            for(let r=0; r<rows-1; r++) {
                const row = [];
                for(let c=0; c<cols; c++) {
                    row.push(parseInt(vStr[idx]));
                    idx++;
                }
                v.push(row);
            }

            statusDiv.textContent = "Applying...";
            const solution = { h, v };

            chrome.tabs.sendMessage(tab.id, { action: "applySolution", solution: solution });
            statusDiv.textContent = "Done!";
        });

    } catch (err) {
        console.error(err);
        statusDiv.textContent = "Error: " + err.message;
    }
});
