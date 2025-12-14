from copy import deepcopy

from Domain.Board.Grid import Grid
from Domain.Board.Position import Position
from Domain.Puzzles.GameSolver import GameSolver


class ChessRangerSolver(GameSolver):
    def __init__(self, grid: Grid):
        self.grid = grid
        self.initial_grid = grid

    def get_solution(self) -> list[tuple[Position, Position]]:
        pieces = self._get_pieces(self.grid)
        # We need N-1 moves to reach 1 piece
        target_moves = len(pieces) - 1
        if target_moves < 0:
            return []

        solution = self._solve(self.grid, [], target_moves)
        return solution if solution else []

    def get_other_solution(self) -> Grid:
        # Not applicable usually, as we want *a* solution
        return None

    def _get_pieces(self, grid: Grid) -> dict[Position, str]:
        pieces = {}
        for r in range(grid.rows_number):
            for c in range(grid.columns_number):
                val = grid[r][c]
                if val is not None:
                    pieces[Position(r, c)] = val
        return pieces

    def _solve(self, grid: Grid, moves: list[tuple[Position, Position]], target_moves: int):
        if len(moves) == target_moves:
            return moves

        pieces = self._get_pieces(grid)

        # Optimization: Sort pieces? No, just iterate.
        for pos, piece_type in pieces.items():
            valid_moves = self._get_valid_moves(grid, pos, piece_type)
            for target_pos in valid_moves:
                # Execute move
                captured_piece = grid[target_pos]
                new_grid_matrix = [row[:] for row in grid.matrix]
                new_grid_matrix[target_pos.r][target_pos.c] = piece_type
                new_grid_matrix[pos.r][pos.c] = None
                new_grid = Grid(new_grid_matrix)

                new_moves = moves + [(pos, target_pos)]

                result = self._solve(new_grid, new_moves, target_moves)
                if result:
                    return result

        return None

    def _get_valid_moves(self, grid: Grid, start: Position, piece_type: str) -> list[Position]:
        moves = []

        # Piece types: K, Q, R, B, N, P
        # Only capture moves allowed. Target must be occupied.

        directions = []
        is_single_step = False
        is_knight = False
        is_pawn = False

        pt = piece_type.upper()

        if pt == 'K': # King
            directions = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
            is_single_step = True
        elif pt == 'Q': # Queen
            directions = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
        elif pt == 'R': # Rook
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        elif pt == 'B': # Bishop
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif pt == 'N': # Knight
            is_knight = True
            jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        elif pt == 'P': # Pawn
            is_pawn = True
            # Assuming white pawns moving UP (-1 row) for diagonal capture
            # BUT Solitaire Chess usually has no orientation.
            # Usually pawns capture diagonally forward (up-left, up-right).
            # If the board has "black" pawns they might move down.
            # Let's assume standard "White" pawns moving UP unless specified.
            # Capture: (-1, -1), (-1, 1)
            captures = [(-1, -1), (-1, 1)]


        if is_knight:
            for dr, dc in jumps:
                r, c = start.r + dr, start.c + dc
                if 0 <= r < grid.rows_number and 0 <= c < grid.columns_number:
                    if grid[r][c] is not None: # Must be a capture
                        moves.append(Position(r, c))

        elif is_pawn:
            # TODO: verify pawn direction. For now assume Up.
            for dr, dc in captures:
                r, c = start.r + dr, start.c + dc
                if 0 <= r < grid.rows_number and 0 <= c < grid.columns_number:
                     if grid[r][c] is not None:
                        moves.append(Position(r, c))

        else: # Sliding pieces (and King)
            for dr, dc in directions:
                r, c = start.r + dr, start.c + dc
                while 0 <= r < grid.rows_number and 0 <= c < grid.columns_number:
                    if grid[r][c] is not None:
                        # Found a piece to capture
                        moves.append(Position(r, c))
                        break # Cannot jump over

                    if is_single_step:
                        break # King stops after 1 step

                    r += dr
                    c += dc

        return moves
