# Yakuzu

Yakuzu (Yakazu) on GridPuzzle.

Rules:
- Grid divided by black cells (#) into compartments (maximal runs of adjacent white cells horizontally and vertically).
- Fill white cells with positive integers.
- For each compartment of length L >= 2 (horz or vert), the cells must contain each of 1..L exactly once (permutation).
- Length-1 compartments impose no constraint themselves; the number is constrained by the crossing compartment (if any has L>=2).
- Some cells may be pre-filled.

Provider: GridPuzzleYakuzuGridProvider (uses TagProvider + Playwright, detects b_cell)
Solver: YakuzuSolver (uses CP-SAT with compartment group constraints)

Example tested:
_ 3 _ 2 _ | 4 # 2 # 2 | 5 # _ # 3 | _ 3 _ 5 _ | 3 # 1 # 5
Solution:
1 3 5 2 4 | 4 # 2 # 2 | 5 # 3 # 3 | 2 3 4 5 1 | 3 # 1 # 5
