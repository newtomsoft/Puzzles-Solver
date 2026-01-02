import unittest
import json
import sys
import os

sys.path.append(os.getcwd())

from Api.app import app

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
        self.assertTrue(any("sudoku" in p for p in data["patterns"]))

    def test_solve_sudoku(self):
        grid_matrix = [
            [5, 3, -1, -1, 7, -1, -1, -1, -1],
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

        if response.status_code != 200:
            print(f"Response: {response.data}")

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "solved")
        self.assertEqual(len(data["solution"]), 9)
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

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn("Initial numbers must be different", data["error"])

if __name__ == '__main__':
    unittest.main()
