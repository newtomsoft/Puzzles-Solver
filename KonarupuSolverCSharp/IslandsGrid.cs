using System.Collections.Generic;
using System.Linq;

namespace KonarupuSolverCSharp
{
    public class IslandsGrid : Grid<Island>
    {
        public Dictionary<Position, Island> Islands { get; }

        public IslandsGrid(List<List<Island>> matrix) : base(matrix)
        {
            Islands = new Dictionary<Position, Island>();
            foreach (var kvp in this)
            {
                if (kvp.Value != null && kvp.Value.BridgesCount != 0)
                {
                    Islands[kvp.Key] = kvp.Value;
                }
            }

            if (Islands.Count == 0)
            {
                _matrix = new List<List<Island>>();
                return;
            }

            ComputePossibleBridges();
        }

        public static new IslandsGrid Empty()
        {
            return new IslandsGrid(new List<List<Island>>());
        }

        private void ComputePossibleBridges()
        {
            foreach (var island in Islands.Values)
            {
                var min_distances = new Dictionary<Direction, (double, Position)>();
                foreach (var other_island in Islands.Values)
                {
                    if (island.Equals(other_island)) continue;

                    var direction = island.Position.DirectionTo(other_island.Position);
                    if (direction == Direction.None) continue;

                    if (!Direction.Orthogonals().Contains(direction)) continue;

                    var distance = island.Position.DistanceTo(other_island.Position);

                    if (!min_distances.ContainsKey(direction) || distance < min_distances[direction].Item1)
                    {
                        min_distances[direction] = (distance, other_island.Position);
                    }
                }

                if (min_distances.TryGetValue(Direction.Right, out var valRight))
                {
                    island.DirectionPositionBridges[Direction.Right] = (valRight.Item2, 0);
                }
                if (min_distances.TryGetValue(Direction.Left, out var valLeft))
                {
                    island.DirectionPositionBridges[Direction.Left] = (valLeft.Item2, 0);
                }
                if (min_distances.TryGetValue(Direction.Up, out var valUp))
                {
                    island.DirectionPositionBridges[Direction.Up] = (valUp.Item2, 0);
                }
                if (min_distances.TryGetValue(Direction.Down, out var valDown))
                {
                    island.DirectionPositionBridges[Direction.Down] = (valDown.Item2, 0);
                }
            }
        }

        public List<HashSet<Position>> GetConnectedPositions(bool excludeWithoutBridge = false)
        {
            var concernedIslands = excludeWithoutBridge
                ? Islands.Values.Where(i => i.BridgesCount != 0).ToList()
                : Islands.Values.ToList();

            var connectedComponents = new List<HashSet<Position>>();
            var visited = new HashSet<Position>();

            foreach (var island in concernedIslands)
            {
                if (!visited.Contains(island.Position))
                {
                    var component = new HashSet<Position>();
                    DepthFirstSearchIslands(island.Position, component);
                    connectedComponents.Add(component);
                    visited.UnionWith(component);
                }
            }
            return connectedComponents;
        }

        private void DepthFirstSearchIslands(Position position, HashSet<Position> visited)
        {
            if (visited.Contains(position))
            {
                return;
            }
            visited.Add(position);

            if (Islands.TryGetValue(position, out var island))
            {
                foreach (var (p, bridges) in island.DirectionPositionBridges.Values)
                {
                    if (bridges > 0)
                    {
                        DepthFirstSearchIslands(p, visited);
                    }
                }
            }
        }
    }
}