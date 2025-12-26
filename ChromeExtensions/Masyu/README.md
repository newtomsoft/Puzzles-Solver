# Masyu Solver Extension

This Chrome Extension solves Masyu puzzles on `https://gridpuzzle.com/masyu`.

## Installation

1. Open Chrome and go to `chrome://extensions/`.
2. Enable "Developer mode" in the top right.
3. Click "Load unpacked".
4. Select the `ChromeExtensions/Masyu` folder.

## Usage

1. Navigate to a Masyu puzzle on `https://gridpuzzle.com/masyu`.
2. Open the extension popup (click the puzzle piece icon).
3. Click "Solve".
4. The extension will scrape the grid, solve it using Python (via Pyodide), and interact with the page to fill the solution.

## Architecture

- **Manifest V3**
- **Popup**: Loads Pyodide (WASM) to run Python code.
- **Content Script**: Scrapes grid data and clicks the canvas to apply moves.
- **Solver**: Pure Python logic (Constraint Propagation + Backtracking).
