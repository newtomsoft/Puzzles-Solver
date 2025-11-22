from Factories.puzzle_factory import PuzzleFactory
from Views.terminal_view import TerminalView
from Run.UrlPatternMatcher import UrlPatternMatcher

class Application:
    def __init__(self, puzzle_factory: PuzzleFactory, view: TerminalView, url_matcher: UrlPatternMatcher):
        self._puzzle_factory = puzzle_factory
        self._view = view
        self._url_matcher = url_matcher

    def run(self):
        print("Puzzle Solver")
        print("Enter game url")
        url = input()

        solver_class, grid_provider_class, _ = self._url_matcher.get_components_for_url(url)

        grid_provider = grid_provider_class()
        grid_data, _ = grid_provider.get_grid(url)

        solver = self._puzzle_factory.create_solver(solver_class, grid_data)
        solution = solver.solve()

        self._view.show_grid(solution)

if __name__ == "__main__":
    puzzle_factory = PuzzleFactory()
    terminal_view = TerminalView()
    url_matcher = UrlPatternMatcher()

    app = Application(puzzle_factory, terminal_view, url_matcher)
    app.run()
