# Putteria

## Règles du jeu

Règles et astuces du Putteria

Putteria Rules

1. Grid & Regions: The puzzle consists of a rectangular grid divided into outlined regions (polyominoes).

2. Placement: Place exactly one number inside each region.

3. Number Value: The number placed must equal the number of cells in that region (i.e., its size).

4. Row/Column Constraint: No number may repeat in the same row or column (standard Latin-style constraint, but per row/column, not per region).

5. Adjacency Rule: Two cells containing numbers (i.e., the placed digits) must not be orthogonally adjacent , even if they are in different regions.

6. Cross Cells: Cells marked with a cross (X) cannot contain a number. The number for that region must be placed in another cell of the same region.

Putteria puzzle

Putteria puzzle Solution:

### Putteria Solving Techniques & Strategies

#### 1. Region Size Analysis

- Start by labeling each region with its size (e.g., a 4-cell region must contain the number 4).

- This immediately tells you which numbers are competing in each row/column.

#### 2. Cross Elimination

- Any cell with a cross is removed as a candidate for holding the number for its region.

- If a region has only one cell without a cross, that cell must contain the number.

#### 3. Row/Column Deductions (Latin Square Logic)

- In each row/column, track which region sizes appear there.

- Since numbers cannot repeat in a row/column, if a region of size n is in a given row, no other region of size n in that same row can have its number placed in that row.

- Often leads to “only one possible spot in this row/column for number k ” deductions.

#### 4. Adjacency Blocking (Touch Restriction)

- This is often the most powerful constraint after the row/column logic.

- If you place a number in a cell, all four orthogonal neighbors (in adjacent regions) become banned from containing their own region’s number.

- Look for “forced adjacency” scenarios: if two large regions are adjacent, placing numbers might conflict early.

- Use this to eliminate candidate cells within a region: if all cells in a region are adjacent to already-placed numbers except one, that one must hold the number.

#### 5. “Big Number” Focus

- Large region sizes (e.g., 5, 6) are often easier to place because:

- They are unique in their row/column more often.

- Their placement blocks many adjacent cells.

- Start solving with the largest or most constrained regions.

#### 6. Forcing Chains via Adjacency

- Sometimes, placing a number in one candidate cell forces another region’s number into a specific cell, which then blocks other placements, leading to a row/column conflict.

- Use this for contradiction-based elimination: “If I put region A’s number here, region B’s number must go there, blocking all options for region C in this row → impossible.”

#### 7. Row/Column Counting

- In a row of length L , the sum of the numbers placed equals the sum of the sizes of regions that have their number in that row.

- This sometimes helps, but because numbers equal region sizes, the total sum in a row is just the sum of sizes of regions placed in that row—not a fixed total.

#### 8. Region-internal Cross Constraints

- If a region has multiple crosses, the number must go in one of the remaining cells, but it also must not be adjacent to other numbers.

- This can force the number to a cell that is “isolated” from neighboring regions’ possible number cells.

### Step-by-Step Solving Approach

1. List region sizes and note crosses.

2. Mark impossible cells within each region that are adjacent to crosses (if the cross is in a neighboring region and could force adjacency conflict later—but careful: crosses aren’t numbers, so they don’t trigger the adjacency rule; only placed numbers do).

3. Apply row/column uniqueness : for each row/column, list region sizes present; if a size appears only once in that row/column, the number for that region must be placed in that row/column.

4. Use adjacency proactively : when placing a number, immediately mark its orthogonal neighbors as “no number” in their respective regions.

5. Iterate between adjacency blocking and row/column deductions until the grid is filled.

### Common Pitfalls to Avoid

- Confusing region size with cell position : the number n goes in one cell of an n -cell region, not in every cell.

- Forgetting that crosses don’t block adjacency rule —only numbered cells do. Two crosses can be adjacent freely.

- Overlooking that the adjacency rule applies across region boundaries —it’s global, not per region.

By combining Latin square logic with adjacency constraints , Putteria becomes a satisfying blend of Sudoku-like deduction and region-based placement puzzles. Start with large regions and heavily crossed regions to gain initial footholds.
