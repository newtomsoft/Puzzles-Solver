# GridPuzzle Sudoku Solver Extension

This is a Chrome extension that solves "Evil Sudoku" (and other difficulties) on `gridpuzzle.com`.

## Installation

1.  Open Chrome and navigate to `chrome://extensions`.
2.  Enable "Developer mode" by toggling the switch in the top right corner.
3.  Click the "Load unpacked" button.
4.  Select the `ChromeExtensions/GridPuzzleSudoku` directory from this repository.

## Usage

1.  Go to [https://gridpuzzle.com/evil-sudoku](https://gridpuzzle.com/evil-sudoku) (or any Sudoku page on the site).
2.  You should see a green "Solve" button next to the puzzle title.
3.  Click "Solve".
4.  The extension will calculate the solution and fill in the grid automatically.

## How it works

-   **Scraping:** It reads the grid state from the DOM, identifying fixed clues (read-only cells).
-   **Solving:** It uses a backtracking algorithm (JavaScript) to find the solution.
-   **Interaction:** It simulates user clicks and keyboard input to fill in the missing numbers.
