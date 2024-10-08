from flask import Flask, request, jsonify
from flask_cors import CORS

from Grid import Grid
from TapaGame import TapaGame

app = Flask(__name__)
CORS(app, origins="https://www.puzzle-tapa.com")


@app.route('/solution', methods=['POST'])
def get_solution():
    data = request.json
    grid_data = data.get('matrix')
    if not grid_data:
        return jsonify({"error": "matrix data is required"}), 400

    grid = Grid(grid_data)
    game = TapaGame(grid)
    solution_grid, _ = game.get_solution()
    if not solution_grid:
        return jsonify({"message": "No solution found"}), 200

    return jsonify(solution_grid.matrix), 200


if __name__ == '__main__':
    app.run(debug=True)
