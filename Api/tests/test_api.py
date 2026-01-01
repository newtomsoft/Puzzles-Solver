import unittest
import json
import sys
import os

# Ensure we can import from root
sys.path.append(os.getcwd())

from Api.app import app
from Domain.Board.Grid import Grid

class TestApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_patterns(self):
        response = self.app.get('/api/patterns')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("patterns", data)
        self.assertTrue(len(data["patterns"]) > 0)
        # Check for a known pattern (e.g., Sudoku)
        self.assertTrue(any("sudoku" in p for p in data["patterns"]))

    def test_solve_sudoku(self):
        # Solvable 9x9 Sudoku grid (0 represents empty)
        # Taking a simple example.
        grid_matrix = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        # This is a standard valid Sudoku puzzle.
        # "0" should be treated as empty.
        # However, SudokuSolver uses `SudokuBaseSolver.empty = -1`.
        # I need to verify if the Grid constructor or Solver handles 0 as empty.
        # The input JSON usually comes from scraping or manual entry.
        # If the standard `SudokuSolver` expects -1 for empty, I should provide -1.
        # Let's check SudokuBaseSolver.py again. `empty = -1`.

        # Transform 0s to -1s for the test payload if the API doesn't do it.
        # The API currently just passes the grid as is.
        # So I should send -1 for empty cells.

        corrected_grid_matrix = [[-1 if x == 0 else x for x in row] for row in grid_matrix]

        payload = {
            "url": "https://www.puzzle-sudoku.com/", # Matches Sudoku regex
            "grid": corrected_grid_matrix
        }

        response = self.app.post('/api/solve',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        if response.status_code != 200:
            print(f"Response: {response.data}")

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "solved")
        self.assertEqual(len(data["solution"]), 9)
        # Spot check solution
        self.assertEqual(data["solution"][0][2], 4) # (0,2) should be 4

    def test_solve_invalid_url(self):
        payload = {
            "url": "https://invalid-url.com",
            "grid": [[0]]
        }
        response = self.app.post('/api/solve',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_solve_no_solution(self):
        # A grid with conflict: two 5s in the first row.
        grid_matrix = [
            [5, 5, -1, -1, 7, -1, -1, -1, -1],
            [6, -1, -1, 1, 9, 5, -1, -1, -1],
            [-1, 9, 8, -1, -1, -1, -1, 6, -1],
            [8, -1, -1, -1, 6, -1, -1, -1, 3],
            [4, -1, -1, 8, -1, 3, -1, -1, 1],
            [7, -1, -1, -1, 2, -1, -1, -1, 6],
            [-1, 6, -1, -1, -1, -1, 2, 8, -1],
            [-1, -1, -1, 4, 1, 9, -1, -1, 5],
            [-1, -1, -1, -1, 8, -1, -1, 7, 9]
        ]

        payload = {
            "url": "https://www.puzzle-sudoku.com/",
            "grid": grid_matrix
        }

        response = self.app.post('/api/solve',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        # SudokuSolver explicitly checks:
        # if not self._are_initial_numbers_different_in_row_and_column():
        #    raise ValueError("Initial numbers must be different in rows and columns")

        # So this will raise a ValueError, which the API catches and returns 500.
        # Ideally, validation errors should be 400 or something, but 500 with message is what the code does currently.

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn("Initial numbers must be different", data["error"])

if __name__ == '__main__':
    unittest.main()
