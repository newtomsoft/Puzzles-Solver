from Domain.Abstractions.i_view import IView
from Domain.Board.Grid import Grid

class TerminalView(IView):
    def show_grid(self, grid: Grid):
        if grid != Grid.empty():
            print("Solution found:")
            print(grid)
        else:
            print("No solution found")
