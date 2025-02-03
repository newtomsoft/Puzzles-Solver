# import time
# 
# from GridPlayers.PuzzleBinairoPlusGridPlayer import PuzzleBinairoGridPlayer
# 
# from GridProviders.PuzzleBinairoPlusGridProvider import PuzzleBinairoPlusGridProvider
# from GridProviders.StringGridProvider import StringGridProvider
# from Puzzles.BinairoPlus.BinairoPlusSolver import BinairoPlusSolver
# from Utils.Grid import Grid
# 
# 
# class BinairoPlusMainConsole:
#     def __init__(self):
#         self.console_input = None
# 
#     def main(self):
#         data_game, browser = self.get_grid()
#         grid = data_game[0]
#         comparison_operators = data_game[1]
#         solution = self.run(grid, comparison_operators)
#         self.play(solution, browser)
# 
#     def get_grid(self):
#         print("BinairoPlus Game")
#         print("Enter url or grid")
#         self.console_input = input()
# 
#         url_patterns = {
#             "https://www.puzzle-binairo.com": PuzzleBinairoPlusGridProvider,
#             "https://fr.puzzle-binairo.com": PuzzleBinairoPlusGridProvider,
#         }
# 
#         for pattern, provider_class in url_patterns.items():
#             if pattern in self.console_input:
#                 provider = provider_class()
#                 return provider.get_grid(self.console_input)
# 
#         return StringGridProvider().get_grid(self.console_input)
# 
#     @staticmethod
#     def run(grid, comparison_operators):
#         game_solver = BinairoPlusSolver(grid, comparison_operators)
#         start_time = time.time()
#         solution_grid = game_solver.get_solution()
#         end_time = time.time()
#         execution_time = end_time - start_time
#         if solution_grid != Grid.empty():
#             print(f"Solution found in {execution_time:.2f} seconds")
#             print(solution_grid.to_console_string())
#             # BinairoMainConsole.generate_html(solution_grid)
#             return solution_grid
#         else:
#             print(f"No solution found")
# 
#     @staticmethod
#     def generate_html(solution_grid: Grid):
#         with open("solution.html", "w") as file:
#             file.write("<html><head><style>table {border-collapse: collapse;} td {border: 1px solid black; width: 20px; height: 20px; text-align: center;}</style></head><body><table>")
#             for r in range(solution_grid.rows_number):
#                 file.write("<tr>")
#                 for c in range(solution_grid.columns_number):
#                     file.write(f"<td style='background-color: white; color: black;'>{BinairoPlusMainConsole.int_to_base26(solution_grid.value(r, c).as_long())}</td>")
#                 file.write("</tr>")
#             file.write("</table></body></html>")
# 
#     def play(self, solution, browser):
#         url_patterns = {
#             "https://www.puzzle-binairo.com": PuzzleBinairoGridPlayer,
#             "https://fr.puzzle-binairo.com": PuzzleBinairoGridPlayer,
#         }
# 
#         for pattern, player_class in url_patterns.items():
#             if pattern in self.console_input:
#                 player = player_class()
#                 player.play(solution, browser)
#                 return
# 
#         raise ValueError("No player found")
# 
# 
# if __name__ == '__main__':
#     BinairoPlusMainConsole().main()
