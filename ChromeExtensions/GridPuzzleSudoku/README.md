# GridPuzzle Sudoku Solver Extension

This is a Chrome extension that solves "Evil Sudoku" (and other difficulties) on `gridpuzzle.com`.
It leverages the powerful OR-Tools based Python solver present in this repository by communicating with a local server.

## Installation

1.  Open Chrome and navigate to `chrome://extensions`.
2.  Enable "Developer mode" by toggling the switch in the top right corner.
3.  Click the "Load unpacked" button.
4.  Select the `ChromeExtensions/GridPuzzleSudoku` directory from this repository.

## Running the Solver Server

Because this extension uses the robust Python solver from the codebase, you must run a local server:

1.  Open a terminal in the root directory of this repository.
2.  Install dependencies (if not already installed):
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the server:
    ```bash
    python Run/ExtensionServer.py
    ```
    The server will start on `http://127.0.0.1:5000`.

## Usage

1.  Ensure the Python server is running.
2.  Go to [https://gridpuzzle.com/evil-sudoku](https://gridpuzzle.com/evil-sudoku) (or any Sudoku page on the site).
3.  You should see a green "Solve (Python)" button next to the puzzle title.
4.  Click "Solve (Python)".
5.  The extension will send the grid to your local Python server, receive the solution, and fill in the grid automatically.

## Troubleshooting

-   **"Could not connect to Python server"**: Make sure you have started the server using `python Run/ExtensionServer.py` and it is printing "Starting Sudoku Solver Server...".
-   **Mixed Content Errors**: Chrome generally allows `https` pages to fetch from `http://127.0.0.1`, but if you encounter issues, ensure you are not using a VPN or proxy that might interfere with localhost loopback.
