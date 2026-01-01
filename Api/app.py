from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Ensure we can import from root
sys.path.append(os.getcwd())

from Run.UrlPatternMatcher import UrlPatternMatcher
from Run.GameRegistry import GameRegistry
from Run.GameComponentFactory import GameComponentFactory
from Domain.Board.Grid import Grid

app = Flask(__name__)
CORS(app)

# Initialize registry to register all games
UrlPatternMatcher()

@app.route('/api/patterns', methods=['GET'])
def get_patterns():
    """Returns the list of registered URL patterns."""
    patterns = list(GameRegistry.get_all_patterns().keys())
    return jsonify({"patterns": patterns})

@app.route('/api/solve', methods=['POST'])
def solve_puzzle():
    data = request.json
    if not data or 'url' not in data or 'grid' not in data:
        return jsonify({"error": "Missing 'url' or 'grid' in request body"}), 400

    url = data['url']
    grid_matrix = data['grid']
    extra_data = data.get('extra_data', [])

    try:
        # 1. Identify Solver Class using the URL pattern
        try:
            components = GameRegistry.get_components_for_url(url)
            solver_class = components[0]
        except ValueError:
             return jsonify({"error": "Unknown URL pattern or puzzle type"}), 404

        # 2. Create Grid
        # The grid constructor expects a list of lists.
        # We assume the JSON input is already a valid matrix of primitives (int, str, bool, null).
        grid = Grid(grid_matrix)

        # 3. Instantiate Solver
        # Factory expects (grid, *extra_data) if it's a tuple, or just the grid.
        # extra_data allows passing additional info that some solvers might need.
        if extra_data:
            game_data = (grid, *extra_data)
        else:
            game_data = grid

        solver = GameComponentFactory.create_solver(solver_class, game_data)

        # 4. Solve
        solution = solver.get_solution()

        # 5. Return result
        if solution is None:
             return jsonify({"status": "no_solution"}), 200

        if solution.is_empty():
            # Some solvers return Grid.empty() for no solution
            return jsonify({"status": "no_solution"}), 200

        return jsonify({
            "status": "solved",
            "solution": solution.matrix
        })

    except Exception as e:
        # Log the error (optional) and return 500
        print(f"Error solving puzzle: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
