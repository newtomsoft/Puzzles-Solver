from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.append(os.getcwd())

from Run.UrlPatternMatcher import UrlPatternMatcher
from Run.GameRegistry import GameRegistry
from Run.GameComponentFactory import GameComponentFactory
from Domain.Board.Grid import Grid
from Domain.Board.Direction import Direction
from Domain.Board.Position import Position
from Domain.Board.IslandsGrid import IslandGrid

app = Flask(__name__)
CORS(app)

# Initialize registry to register all games
UrlPatternMatcher()

@app.route('/api/patterns', methods=['GET'])
def get_patterns():
    """Returns the list of registered URL patterns."""
    patterns = list(GameRegistry.get_all_patterns().keys())
    return jsonify({"patterns": patterns})



def serialize_island_grid(grid):
    rows = grid.rows_number
    cols = grid.columns_number
    h = [[False] * (cols - 1) for _ in range(rows)]
    v = [[False] * cols for _ in range(rows - 1)]
    black = [[False] * cols for _ in range(rows)]
    
    for r in range(rows):
        for c in range(cols):
            pos = Position(r, c)
            if pos in grid.islands:
                island = grid.islands[pos]
                if c < cols - 1:
                    h[r][c] = island.bridges_number(Direction.right()) > 0
                if r < rows - 1:
                    v[r][c] = island.bridges_number(Direction.down()) > 0
            
            val = grid[pos]
            if val == '■':
                black[r][c] = True
                
    return {
        "h": h,
        "v": v,
        "black": black,
        "matrix": [[str(grid[Position(r, c)]) for c in range(cols)] for r in range(rows)]
    }

def serialize_solution(solution):
    if isinstance(solution, IslandGrid):
        return serialize_island_grid(solution)
    
    if hasattr(solution, 'matrix'):
        matrix = solution.matrix
        if isinstance(matrix, list) and len(matrix) > 0 and isinstance(matrix[0], list):
             # Check if it's a matrix of objects that need string conversion
             return [[(str(cell) if not isinstance(cell, (int, float, bool, str, type(None))) else cell) for cell in row] for row in matrix]
        return matrix
    
    return str(solution)

@app.route('/api/solve', methods=['POST'])
def solve_puzzle():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    url = data['url']
    grid_matrix = data.get('grid')
    raw_data = data.get('data')
    extra_data = data.get('extra_data', [])

    if grid_matrix is None and raw_data is None:
        if 'html' in data:
            try:
                # Use the Python provider to extract grid from HTML
                components = GameRegistry.get_components_for_url(url)
                provider_class = components[1]
                provider = provider_class()
                game_data = provider.get_grid_from_html(data['html'], url)
            except (ValueError, NotImplementedError) as e:
                return jsonify({"error": f"Failed to extract grid from HTML: {str(e)}"}), 400
            except Exception as e:
                return jsonify({"error": f"Error during Python extraction: {str(e)}"}), 500
        else:
            return jsonify({"error": "Missing 'grid', 'data', or 'html' in request body"}), 400
    else:
        try:
            try:
                components = GameRegistry.get_components_for_url(url)
                solver_class = components[0]
            except ValueError:
                 return jsonify({"error": "Unknown URL pattern or puzzle type"}), 404

            if raw_data is not None and grid_matrix is None:
                game_data = raw_data
            else:
                grid = Grid(grid_matrix)
                if extra_data:
                    processed_extra_data = []
                    for item in extra_data:
                        if isinstance(item, list) and len(item) > 0 and isinstance(item[0], list):
                            processed_extra_data.append(Grid(item))
                        else:
                            processed_extra_data.append(item)
                    game_data = (grid, *processed_extra_data)
                else:
                    game_data = grid
        except Exception as e:
            return jsonify({"error": f"Error processing input data: {str(e)}"}), 400

    try:
        # At this point game_data should be populated either from HTML or Grid
        solver_class = GameRegistry.get_components_for_url(url)[0]
        solver = GameComponentFactory.create_solver(solver_class, game_data)
        solution = solver.get_solution()
        if solution is None:
             return jsonify({"status": "no_solution"}), 200

        if hasattr(solution, 'is_empty') and solution.is_empty():
            return jsonify({"status": "no_solution"}), 200

        return jsonify({
            "status": "solved",
            "solution": serialize_solution(solution)
        })

    except Exception as e:
        print(f"Error solving puzzle: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
