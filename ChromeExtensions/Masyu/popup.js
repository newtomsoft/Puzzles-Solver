
// Popup script for Masyu Z3 Solver
const statusDiv = document.getElementById('status');
const solveBtn = document.getElementById('solveBtn');

// Initialize Z3 worker or load script
// Since z3-built.js puts Z3 on window, we can load it dynamically or via script tag.
// For extension, better to load explicitly.

async function loadScript(url) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = url;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

async function initSolver() {
    statusDiv.textContent = "Loading Z3...";
    if (!window.Z3) {
        await loadScript('z3-built.js');
    }
    if (!window.solveMasyu) {
        await loadScript('solver.js');
    }
    statusDiv.textContent = "Z3 Ready.";
}

solveBtn.addEventListener('click', async () => {
    try {
        statusDiv.textContent = "Initializing...";
        await initSolver();

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

            // Call solver
            const solution = await window.solveMasyu(grid);

            if (!solution) {
                statusDiv.textContent = "No Solution Found";
                return;
            }

            statusDiv.textContent = "Applying...";
            chrome.tabs.sendMessage(tab.id, { action: "applySolution", solution: solution });
            statusDiv.textContent = "Done!";
        });

    } catch (err) {
        console.error(err);
        statusDiv.textContent = "Error: " + err.message;
    }
});
