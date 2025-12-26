using System;
using System.Text;

namespace EverySecondTurnSolver
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Every Second Turn Solver (.NET Port)");
            Console.WriteLine("=====================================");

            // Sample Grid (from Python tests or common sense)
            // Example:
            // * . .
            // . . .
            // . . *
            // Just a dummy 3x3 for structure, real puzzle logic requires valid input.

            // Let's use a small solvable example if possible.
            //
            // * . *
            // . . .
            // * . *
            //
            char[,] gridData = new char[,] {
                { '*', '.', '*' },
                { '.', '.', '.' },
                { '*', '.', '*' }
            };

            Console.WriteLine("Input Grid:");
            PrintGrid(gridData);

            try
            {
                var solver = new EverySecondTurnSolver(gridData);
                var solution = solver.GetSolution();

                if (solution != null)
                {
                    Console.WriteLine("\nSolution Found:");
                    PrintSolution(solution);
                }
                else
                {
                    Console.WriteLine("\nNo solution found.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
                Console.WriteLine(ex.StackTrace);
            }
        }

        static void PrintGrid(char[,] grid)
        {
            int rows = grid.GetLength(0);
            int cols = grid.GetLength(1);
            for (int r = 0; r < rows; r++)
            {
                for (int c = 0; c < cols; c++)
                {
                    Console.Write(grid[r, c] + " ");
                }
                Console.WriteLine();
            }
        }

        static void PrintSolution(IslandGrid solution)
        {
            // Simple ASCII representation of bridges
            // Since we don't have a full UI, we'll just print connection counts or simplistic lines

            // We can try to draw box drawing characters based on bridges
            int rows = solution.Rows;
            int cols = solution.Cols;

            // 2D char buffer (expand to 2x size for visual links)

            for (int r = 0; r < rows; r++)
            {
                // Top half of cell row
                StringBuilder line1 = new StringBuilder();
                // Bottom half (connections down)
                StringBuilder line2 = new StringBuilder();

                for (int c = 0; c < cols; c++)
                {
                    var island = solution[r, c];

                    // Determine char for center
                    // We assume input grid was passed or we know positions.
                    // Since solution object doesn't have original chars, we just use 'O' or '+'

                    bool up = island.Bridges.ContainsKey(Direction.Up) && island.Bridges[Direction.Up] > 0;
                    bool down = island.Bridges.ContainsKey(Direction.Down) && island.Bridges[Direction.Down] > 0;
                    bool left = island.Bridges.ContainsKey(Direction.Left) && island.Bridges[Direction.Left] > 0;
                    bool right = island.Bridges.ContainsKey(Direction.Right) && island.Bridges[Direction.Right] > 0;

                    string center = "+";
                    if (up && down && !left && !right) center = "|";
                    else if (!up && !down && left && right) center = "-";
                    else if (up && right) center = "L"; // Simplified
                    else if (down && right) center = "F";
                    else if (down && left) center = "7";
                    else if (up && left) center = "J";

                    line1.Append(center);
                    if (right) line1.Append("-");
                    else line1.Append(" ");

                    if (down) line2.Append("| ");
                    else line2.Append("  ");
                }
                Console.WriteLine(line1.ToString());
                Console.WriteLine(line2.ToString());
            }
        }
    }
}
