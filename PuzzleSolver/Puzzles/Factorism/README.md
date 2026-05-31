# Factorism

## Règles du jeu

Règles et astuces du Factorism

Iva Sallay's Factorism , also known as "Find the Factors," is a fantastic and elegant logic puzzle. Here's a breakdown and a comprehensive guide to solving techniques.

### The Puzzle's Core Concept

You have an N x N grid.

Numbers 1 through N are placed once each in the top row header and once each in the left column header (outside the grid itself).

The numbers inside the grid cells are the product of their corresponding outside row and column numbers.

Your goal: Deduce the unique arrangement of the numbers 1-N in the top and left headers.

Key Insight: You are not given the headers. You must use the prime factorization of the grid numbers and the logic of the 1-N list constraint to reconstruct them.

Factorism Puzzle

Factorism Puzzle Solution:

### Step-by-Step Solving Strategy & Techniques

#### 1. Prime Factorization is Your Foundation

Every number in the grid must be broken down into its prime factors (e.g., 12 = 2² × 3). This is the absolute first step.

A cell's value = (Row Header) × (Column Header).

Therefore, the union of the prime factors of the Row Header and Column Header equals the prime factors of the cell.

#### 2. Identify "Singletons" and Forced Assignments

Look for cells where the prime factorization contains a prime number that appears nowhere else in its row or column .

Why? That prime must belong to the header for that row or that column. Often, you can deduce which one based on other constraints.

Example: If in a row, the number 7 appears in only one cell (as a factor of 14 or 7 itself), then the prime 7 must be in either that row's header or that column's header. If the column already has another number requiring a factor of 7, it forces the row header to be 7.

#### 3. Use the 1-N List Constraint (The Golden Rule)

This is the most powerful logical tool.

Each number from 1 to N is used exactly once in the row headers and once in the column headers.

Therefore, if you deduce that a row header must be 6 , you can immediately eliminate 6 as a possibility for all other row headers and for all column headers (and vice-versa).

This creates a constantly narrowing "pool" of available numbers.

#### 4. Look for the Largest/Smallest Numbers

The Largest Number in the Grid: Often appears where the largest row header and largest column header intersect. This can give you a starting point for pairing the high numbers.

The Number 1: This is a very subtle but powerful clue. If a row header is 1, then every cell in that row will simply be a copy of the column header . Conversely, if a column header is 1, every cell in that column will be a copy of the row header. A row or column that looks like a simple permutation of other headers is a strong candidate for having a header of 1.

#### 5. Process of Elimination within Rows/Columns

Within a single row:

All cells share the same row header factor .

Therefore, the greatest common divisor (GCD) of all numbers in that row is a strong candidate for (or a factor of) the row header.

Similarly, the GCD of a column hints at the column header.

#### 6. "Cross-Referencing" or "Intersection" Logic

This is the core deductive step. You often work in pairs:

> "If this row header were X, then that column header would have to be Y. But if that column header is Y, then in this other row it would create Z, which is impossible because... Therefore, the row header cannot be X."

### General Tips for Solvers

Start Small: Begin with the smallest grid (usually 5x5 or 6x6) to get a feel for the logic.

Pencil Marks: Like Sudoku, use pencil marks (tiny numbers) in cell corners to note possible header pairs or prime factors.

Think in Factors, Not Just Products: Train your brain to see a 12 as "a 3 and two 2's" that need to be allocated to two headers.

Patience with Cross-Referencing: The puzzle often reaches a point where you must make a "what-if" assumption for one header and follow the chain of consequences until you hit a contradiction or a solution.

### Why It's a Brilliant Puzzle

Factorism beautifully combines:

1. Elementary Number Theory (Prime Factorization).

2. Constraint Satisfaction Logic (like Sudoku or KenKen).

3. Deductive Reasoning through elimination and intersection.
