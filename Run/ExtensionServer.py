from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Ensure the root directory is in python path
sys.path.append(os.getcwd())

from Domain.Board.Grid import Grid
from Domain.Puzzles.Sudoku.Sudoku.SudokuSolver import SudokuSolver

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/solve/sudoku', methods=['POST'])
def solve_sudoku():
    try:
        data = request.json
        if not data or 'grid' not in data:
            return jsonify({'error': 'Missing grid data'}), 400

        matrix = data['grid']
        # Convert 0 to SudokuSolver.empty (which is -1)
        # Note: SudokuSolver.empty is -1.
        # But wait, SudokuBaseSolver says empty = -1.
        # The scraper sends 0 for empty.

        # GridPuzzleSudokuGridProvider uses SudokuSolver.empty (-1) for empty cells.
        # The content.js currently sends 0 for empty cells.
        # I need to handle this conversion.

        # Let's inspect the scraped matrix. It is numbers.
        # 0 usually means empty in standard sudoku representations, but this project uses -1.

        processed_matrix = []
        for row in matrix:
            new_row = []
            for val in row:
                if val == 0:
                    new_row.append(SudokuSolver.empty)
                else:
                    new_row.append(val)
            processed_matrix.append(new_row)

        grid = Grid(processed_matrix)
        solver = SudokuSolver(grid)
        solution = solver.get_solution()

        if solution.is_empty():
            return jsonify({'success': False, 'message': 'No solution found'}), 200

        # Convert back to list of lists
        solution_matrix = solution.matrix
        return jsonify({'success': True, 'solution': solution_matrix}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Sudoku Solver Server on port 5000...")
    app.run(port=5000, debug=True)
