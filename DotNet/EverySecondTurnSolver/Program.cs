using System;
using System.Text;

namespace EverySecondTurnSolver;

internal static class Program
{
    private static void Main(string[] args)
    {
        Console.WriteLine("Every Second Turn Solver (.NET Port)");
        Console.WriteLine("=====================================");

        const char x = '*';
        const char _ = '.';
        var gridData = new[,]
        {
            { _, _, _, _, _, x },
            { _, x, _, _, _, _ },
            { _, _, _, _, x, _ },
            { x, _, _, x, _, _ },
            { _, _, x, _, _, x },
            { x, _, _, _, _, _ },
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

    private static void PrintGrid(char[,] grid)
    {
        var rows = grid.GetLength(0);
        var cols = grid.GetLength(1);
        for (var r = 0; r < rows; r++)
        {
            for (var c = 0; c < cols; c++)
            {
                Console.Write(grid[r, c] + " ");
            }

            Console.WriteLine();
        }
    }

    private static void PrintSolution(IslandGrid solution)
    {
        var rows = solution.Rows;
        var cols = solution.Cols;

        for (var r = 0; r < rows; r++)
        {
            var line1 = new StringBuilder();
            var line2 = new StringBuilder();

            for (var c = 0; c < cols; c++)
            {
                var island = solution[r, c];

                var up = island.Bridges.ContainsKey(Direction.Up) && island.Bridges[Direction.Up] > 0;
                var down = island.Bridges.ContainsKey(Direction.Down) && island.Bridges[Direction.Down] > 0;
                var left = island.Bridges.ContainsKey(Direction.Left) && island.Bridges[Direction.Left] > 0;
                var right = island.Bridges.ContainsKey(Direction.Right) && island.Bridges[Direction.Right] > 0;

                var center = "+";
                switch (up)
                {
                    case true when down && !left && !right:
                        center = "|";
                        break;
                    case false when !down && left && right:
                        center = "-";
                        break;
                    case true when right:
                        center = "L"; // Simplified
                        break;
                    default:
                    {
                        switch (down)
                        {
                            case true when right:
                                center = "F";
                                break;
                            case true when left:
                                center = "7";
                                break;
                            default:
                            {
                                if (up && left) center = "J";
                                break;
                            }
                        }

                        break;
                    }
                }

                line1.Append(center);
                line1.Append(right ? "-" : " ");

                line2.Append(down ? "| " : "  ");
            }

            Console.WriteLine(line1.ToString());
            Console.WriteLine(line2.ToString());
        }
    }
}