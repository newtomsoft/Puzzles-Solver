# import re
# 
# from GridProviders.EscapeSudokuProvider import EscapeSudokuGridProvider
# from GridProviders.PuzzleSudokuGridProvider import PuzzleSudokuGridProvider
# from GridProviders.StringGridProvider import StringGridProvider
# from SudokuSolver import SudokuSolver
# from Utils.Grid import Grid
# 
# 
# class SudokuMainConsole:
#     @staticmethod
#     def main():
#         grid = SudokuMainConsole.get_grid()
#         SudokuMainConsole.run(grid, self.solver_engine)
# 
# 
#     @staticmethod
#     def get_grid():
#         print("Sodoku Game")
#         print("Enter url or grid")
#         console_input = input()
# 
#         url_patterns = {
#             r"https://www.puzzle-sudoku.com/.*": PuzzleSudokuGridProvider,
#             r"https://fr.puzzle-sudoku.com/.*": PuzzleSudokuGridProvider,
#             r"https://escape-sudoku.com/.*": EscapeSudokuGridProvider,
#         }
# 
#         for pattern, provider_class in url_patterns.items():
#             if re.match(pattern, console_input):
#                 provider = provider_class()
#                 return provider.get_grid(console_input)
# 
#         return StringGridProvider().get_grid(console_input)
# 
#     @staticmethod
#     def run(grid, self.solver_engine)
# :
#         game_solver = SudokuSolver(grid, self.solver_engine)
# 
#         solution_grid = game_solver.get_solution()
#         if solution_grid:
#             print(f"Solution found:")
#             print(solution_grid.to_console_string())
#             SudokuMainConsole.generate_html(solution_grid)
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
#                     file.write(f"<td style='background-color: white; color: black;'>{SudokuMainConsole.int_to_base26(solution_grid.value(r, c)())}</td>")
#                 file.write("</tr>")
#             file.write("</table></body></html>")
# 
#     @staticmethod
#     def int_to_base26(n):
#         if n <= 9:
#             return n
#         result = []
#         while n > 0:
#             n -= 1
#             if n < 9:
#                 result.append(str(n + 1))
#             else:
#                 result.append(chr(n - 9 + ord('A')))
#             n //= 35
#         return ''.join(reversed(result))
# 
# 
# if __name__ == '__main__':
#     SudokuMainConsole.main()
