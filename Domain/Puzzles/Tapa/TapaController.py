from flask import Flask, request, jsonify
from flask_cors import CORS

from Domain.Board.Grid import Grid
from SolverEngineAdapters.Z3SolverEngine import Z3SolverEngine
from TapaSolver import TapaSolver

app = Flask(__name__)
CORS(app, origins="https://www.puzzle-tapa.com")


def get_solver_engine():
    return Z3SolverEngine()


@app.route('/solution', methods=['POST'])
def get_solution():
    data = request.json
    grid_data = data.get('matrix')
    if not grid_data:
        return jsonify({"error": "matrix data is required"}), 400

    grid = Grid(grid_data)
    game_solver = TapaSolver(grid, get_solver_engine())

    solution_grid = game_solver.get_solution()
    if not solution_grid:
        return jsonify({"message": "No solution found"}), 200

    return jsonify(solution_grid.matrix), 200


if __name__ == '__main__':
    app.run(debug=True)
