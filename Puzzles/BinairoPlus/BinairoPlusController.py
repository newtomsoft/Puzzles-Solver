from flask import Flask, request, jsonify
from flask_cors import CORS

from BinairoPlusGame import BinairoPlusGame
from Utils.Grid import Grid

app = Flask(__name__)
CORS(app, origins="https://www.puzzles-mobile.com")


@app.route('/binairo-plus/solution', methods=['POST'])
def get_solution():
    print("api called")
    data = request.json
    grid_data = data.get('matrix')
    comparison_operators_data = data.get('comparison_operators')
    if not grid_data:
        return jsonify({"error": "matrix data is required"}), 400
    if not comparison_operators_data:
        return jsonify({"error": "comparison_operators data is required"}), 400

    grid = Grid(grid_data)
    comparison_operators = comparison_operators_data
    game = BinairoPlusGame(grid, comparison_operators)
    solution_grid = game.get_solution()
    if not solution_grid:
        return jsonify({"message": "No solution found"}), 200

    return jsonify(solution_grid.matrix), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)
