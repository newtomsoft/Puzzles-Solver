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
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    url = data['url']
    # Input can be 'grid' (list of lists) or 'data' (generic object)
    grid_matrix = data.get('grid')
    raw_data = data.get('data')
    extra_data = data.get('extra_data', [])

    if grid_matrix is None and raw_data is None:
        return jsonify({"error": "Missing 'grid' or 'data' in request body"}), 400

    try:
        # 1. Identify Solver Class using the URL pattern
        try:
            components = GameRegistry.get_components_for_url(url)
            solver_class = components[0]
        except ValueError:
             return jsonify({"error": "Unknown URL pattern or puzzle type"}), 404

        # 2. Prepare Game Data
        if raw_data is not None:
            # If raw data is provided, use it directly (e.g. dict for Akari)
            game_data = raw_data
        else:
            # Construct Grid
            grid = Grid(grid_matrix)
            if extra_data:
                # Handle nested Grids in extra_data
                processed_extra_data = []
                for item in extra_data:
                    # Heuristic: if item looks like a matrix, make it a Grid
                    if isinstance(item, list) and len(item) > 0 and isinstance(item[0], list):
                        processed_extra_data.append(Grid(item))
                    else:
                        processed_extra_data.append(item)
                game_data = (grid, *processed_extra_data)
            else:
                game_data = grid

        # 3. Instantiate Solver
        solver = GameComponentFactory.create_solver(solver_class, game_data)

        # 4. Solve
        solution = solver.get_solution()

        # 5. Return result
        if solution is None:
             return jsonify({"status": "no_solution"}), 200

        if hasattr(solution, 'is_empty') and solution.is_empty():
            return jsonify({"status": "no_solution"}), 200

        # Handle cases where solution might not be a Grid (though GameSolver says it should be)
        if hasattr(solution, 'matrix'):
            return jsonify({
                "status": "solved",
                "solution": solution.matrix
            })
        else:
            # Fallback for non-standard return types
            return jsonify({
                "status": "solved",
                "solution": str(solution)
            })

    except Exception as e:
        # Log the error (optional) and return 500
        print(f"Error solving puzzle: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
