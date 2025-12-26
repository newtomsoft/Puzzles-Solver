using System;
using System.Runtime.InteropServices.JavaScript;

namespace MasyuSolver;

public partial class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Masyu Solver WASM Loaded");
    }

    [JSExport]
    public static string Solve(string[] gridStrings)
    {
        try
        {
            var rows = gridStrings.Length;
            var cols = gridStrings[0].Length;
            var grid = new char[rows, cols];

            for (int r = 0; r < rows; r++)
            {
                for (int c = 0; c < cols; c++)
                {
                    grid[r, c] = gridStrings[r][c];
                }
            }

            var solver = new MasyuSolver(grid);
            bool success = solver.Solve();

            if (!success) return "NO_SOLUTION";

            var hEdges = solver.GetHEdges();
            var vEdges = solver.GetVEdges();

            var sbH = new System.Text.StringBuilder();
            var sbV = new System.Text.StringBuilder();

            for (int r = 0; r < rows; r++)
            {
                for (int c = 0; c < cols - 1; c++)
                {
                    sbH.Append(hEdges[r, c] == 1 ? "1" : "0");
                }
            }

            for (int r = 0; r < rows - 1; r++)
            {
                for (int c = 0; c < cols; c++)
                {
                    sbV.Append(vEdges[r, c] == 1 ? "1" : "0");
                }
            }

            return $"{rows}|{cols}|{sbH}|{sbV}";
        }
        catch (Exception ex)
        {
            return $"ERROR: {ex.Message}";
        }
    }
}
