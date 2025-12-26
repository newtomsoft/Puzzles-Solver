using System.Text;

namespace EverySecondTurnSolver;

public class IslandGrid
{
    private readonly Island[,] _islands;
    public int Rows { get; }
    public int Cols { get; }

    public IslandGrid(int rows, int cols)
    {
        Rows = rows;
        Cols = cols;
        _islands = new Island[rows, cols];
        for (int r = 0; r < rows; r++)
        {
            for (int c = 0; c < cols; c++)
            {
                _islands[r, c] = new Island(new Position(r, c), 2);
            }
        }
    }

    public Island this[Position p] => _islands[p.R, p.C];
    public Island this[int r, int c] => _islands[r, c];

    public bool IsValidPosition(Position p)
    {
        return p.R >= 0 && p.R < Rows && p.C >= 0 && p.C < Cols;
    }

    public IEnumerable<Island> GetAllIslands()
    {
        foreach (var island in _islands)
        {
            yield return island;
        }
    }

    // Helper to find connected components (Union-Find or BFS)
    public List<List<Position>> GetConnectedComponents()
    {
        var visited = new HashSet<Position>();
        var components = new List<List<Position>>();

        foreach (var island in GetAllIslands())
        {
            // Only consider islands that actually have bridges
            if (island.Bridges.Count == 0) continue;
            if (visited.Contains(island.Position)) continue;

            var component = new List<Position>();
            var queue = new Queue<Position>();
            queue.Enqueue(island.Position);
            visited.Add(island.Position);

            while (queue.Count > 0)
            {
                var current = queue.Dequeue();
                component.Add(current);

                if (IsValidPosition(current))
                {
                    var currentIsland = this[current];
                    foreach (var kvp in currentIsland.Bridges)
                    {
                        // If bridge count > 0, there is a connection
                        if (kvp.Value > 0)
                        {
                            var neighborPos = current.After(kvp.Key);
                            if (IsValidPosition(neighborPos) && !visited.Contains(neighborPos))
                            {
                                visited.Add(neighborPos);
                                queue.Enqueue(neighborPos);
                            }
                        }
                    }
                }
            }

            components.Add(component);
        }

        return components;
    }

    public static IslandGrid Empty() => new IslandGrid(0, 0);

    public override string ToString()
    {
        if (Rows == 0) return "";
        var sb = new StringBuilder();
        for (var r = 0; r < Rows; r++)
        {
            for (var c = 0; c < Cols; c++)
            {
                sb.Append(_islands[r, c]);
            }

            if (r < Rows - 1) sb.Append('\n');
        }

        return sb.ToString();
    }
}