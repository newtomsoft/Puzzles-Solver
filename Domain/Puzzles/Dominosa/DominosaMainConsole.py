# from GridProviders.PuzzleDominosaGridProvider import PuzzleDominosaGridProvider
# from GridProviders.StringGridProvider import StringGridProvider
# from Puzzles.Dominosa.DominosaSolver import DominosaSolver
# 
# 
# class DominosaMainConsole:
#     @staticmethod
#     def main():
#         grid = DominosaMainConsole.get_grid()
#         DominosaMainConsole.run(grid, self.solver_engine)
# 
# 
#     @staticmethod
#     def get_grid():
#         print("Dominosa Game")
#         print("Enter url or grid")
#         console_input = input()
# 
#         url_patterns = {
#             r"https://fr.puzzle-dominosa.com/": PuzzleDominosaGridProvider,
#             r"https://www.puzzle-dominosa.com/": PuzzleDominosaGridProvider
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
#     def run(grid):
#         dominosa = DominosaSolver(grid)
#         solution = dominosa.get_solution()
#         if solution:
#             print(f"Solution found:")
#             print(solution)
#         else:
#             print(f"No solution found)")
# 
# 
# if __name__ == '__main__':
#     DominosaMainConsole.main()
