# from GridProviders.HitoriConquestGridProvider import HitoriConquestGridProvider
# from GridProviders.StringGridProvider import StringGridProvider
# from Puzzles.Hitori.HitoriSolver import HitoriSolver
# from Utils.Board import Board
# from Utils.Position import Position
# 
# 
# class HitoriMainConsole:
#     @staticmethod
#     def main():
#         grid = HitoriMainConsole.get_grid()
#         HitoriMainConsole.run(grid, self.solver_engine)
# 
# 
#     @staticmethod
#     def get_grid():
#         print("Hitori Game")
#         print("Enter url or grid")
#         console_input = input()
# 
#         url_patterns = {
#             r"hitoriconquest": HitoriConquestGridProvider,
#         }
# 
#         for pattern, provider_class in url_patterns.items():
#             if pattern in console_input:
#                 provider = provider_class()
#                 return provider.get_grid(console_input)
# 
#         return StringGridProvider().get_grid(console_input)
# 
#     @staticmethod
#     def run(grid, self.solver_engine)
# :
#         hitori = HitoriSolver(grid, self.solver_engine)
# 
#         solution_grid = hitori.get_solution()
#         if solution_grid != Board.empty():
#             print(f"Solution found:")
#             for r in range(solution_grid.rows_number):
#                 for c in range(solution_grid.columns_number):
#                     if solution_grid.value(r, c) is False:
#                         solution_grid.set_value(Position(r, c), '■')
#             print(solution_grid.to_console_string())
#         else:
#             print(f"No solution found)")
# 
# 
# if __name__ == '__main__':
#     HitoriMainConsole.main()
