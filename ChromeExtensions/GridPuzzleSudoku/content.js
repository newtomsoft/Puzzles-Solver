// Main entry point
function init() {
    // Attempt to find the title to inject the button
    const title = document.querySelector('h1') || document.querySelector('.page-header');
    if (title) {
        const btn = document.createElement('button');
        btn.innerText = "Solve";
        btn.className = "solver-btn";
        btn.onclick = runSolver;
        title.appendChild(btn);
    } else {
        console.warn("Could not find title element to attach Solver button");
        // Fallback: Fixed position button
        const btn = document.createElement('button');
        btn.innerText = "Solve Sudoku";
        btn.className = "solver-btn";
        btn.style.position = "fixed";
        btn.style.top = "10px";
        btn.style.right = "10px";
        btn.style.zIndex = "9999";
        btn.onclick = runSolver;
        document.body.appendChild(btn);
    }
}

async function runSolver() {
    const btn = document.querySelector('.solver-btn');
    if (btn) {
        btn.disabled = true;
        btn.innerText = "Solving...";
    }

    try {
        const grid = scrapeGrid();
        if (!grid) {
            alert("Could not detect Sudoku grid.");
            return;
        }

        const solution = solveSudoku(grid);
        if (solution) {
            await applySolution(solution);
        } else {
            alert("No solution found!");
        }
    } catch (e) {
        console.error(e);
        alert("Error solving puzzle: " + e.message);
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerText = "Solve";
        }
    }
}

// Scrape the grid from the DOM
function scrapeGrid() {
    const cells = document.querySelectorAll('div.g_cell');
    if (!cells || cells.length === 0) return null;

    const size = Math.sqrt(cells.length);
    if (!Number.isInteger(size)) {
        console.error("Grid size is not a perfect square");
        return null;
    }

    const grid = [];
    for (let i = 0; i < size; i++) {
        const row = [];
        for (let j = 0; j < size; j++) {
            const index = i * size + j;
            const cell = cells[index];
            const isReadOnly = cell.getAttribute('data-readonly') === '1';
            const valStr = cell.getAttribute('data-val');

            // Only trust read-only cells as clues
            if (isReadOnly && valStr) {
                row.push(parseInt(valStr, 10));
            } else {
                row.push(0); // Empty
            }
        }
        grid.push(row);
    }
    return grid;
}

// Backtracking Solver
function solveSudoku(board) {
    const size = board.length;

    // Find empty cell
    let row = -1;
    let col = -1;
    let isEmpty = false;
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            if (board[i][j] === 0) {
                row = i;
                col = j;
                isEmpty = true;
                break;
            }
        }
        if (isEmpty) break;
    }

    // No empty cell -> Solved
    if (!isEmpty) return board;

    // Try values 1 to size
    for (let num = 1; num <= size; num++) {
        if (isSafe(board, row, col, num)) {
            board[row][col] = num;
            if (solveSudoku(board)) {
                return board;
            }
            board[row][col] = 0; // Backtrack
        }
    }
    return null;
}

function isSafe(board, row, col, num) {
    const size = board.length;
    const boxSize = Math.sqrt(size);

    // Check Row
    for (let d = 0; d < size; d++) {
        if (board[row][d] === num) return false;
    }

    // Check Column
    for (let r = 0; r < size; r++) {
        if (board[r][col] === num) return false;
    }

    // Check Box
    const boxRowStart = row - row % boxSize;
    const boxColStart = col - col % boxSize;

    for (let r = boxRowStart; r < boxRowStart + boxSize; r++) {
        for (let d = boxColStart; d < boxColStart + boxSize; d++) {
            if (board[r][d] === num) return false;
        }
    }

    return true;
}

// Apply solution to the DOM
async function applySolution(solution) {
    const cells = document.querySelectorAll('div.g_cell');
    const size = solution.length;

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const index = i * size + j;
            const cell = cells[index];

            // Skip readonly cells
            if (cell.getAttribute('data-readonly') === '1') continue;

            const targetVal = solution[i][j];
            const currentVal = parseInt(cell.getAttribute('data-val') || '0', 10);

            if (targetVal !== currentVal) {
                // Interaction logic based on GridPuzzle behavior
                // Click to focus, then type number
                cell.click();
                await new Promise(r => setTimeout(r, 10)); // Small delay for focus

                // Simulate key press
                const keyEvent = new KeyboardEvent('keydown', {
                    key: targetVal.toString(),
                    code: 'Digit' + targetVal.toString(),
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                document.dispatchEvent(keyEvent);

                // Also trigger keyup/keypress just in case
                 const keyPressEvent = new KeyboardEvent('keypress', {
                    key: targetVal.toString(),
                    code: 'Digit' + targetVal.toString(),
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                document.dispatchEvent(keyPressEvent);

                await new Promise(r => setTimeout(r, 20)); // Delay between moves
            }
        }
    }
}

// Run init when DOM is ready
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
} else {
    init();
}
