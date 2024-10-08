from Grid import Grid
from GridProviders.HitoriConquestGridProvider import HitoriConquestGridProvider
from GridProviders.StringGridProvider import StringGridProvider
from Puzzles.Hitori.HitoriGame import HitoriGame


class HitoriMainConsole:
    @staticmethod
    def main():
        grid = HitoriMainConsole.get_grid()
        HitoriMainConsole.run(grid)

    @staticmethod
    def get_grid():
        print("Hitori Game")
        print("Enter url or grid")
        console_input = input()

        url_patterns = {
            r"hitoriconquest": HitoriConquestGridProvider,
        }

        for pattern, provider_class in url_patterns.items():
            if pattern in console_input:
                provider = provider_class()
                return provider.get_grid(console_input)

        return StringGridProvider().get_grid(console_input)

    @staticmethod
    def run(grid):
        hitori = HitoriGame(grid)
        solution_grid, attempts = hitori.get_solution()
        if solution_grid != Grid.empty():
            print(f"Solution found after {attempts} attempts :")
            for r in range(solution_grid.rows_number):
                for c in range(solution_grid.columns_number):
                    if solution_grid.value(r, c) is False:
                        solution_grid.set_value(r, c, '■')
            print(solution_grid.to_console_string())
        else:
            print(f"No solution found ({attempts} attempts)")


if __name__ == '__main__':
    HitoriMainConsole.main()
