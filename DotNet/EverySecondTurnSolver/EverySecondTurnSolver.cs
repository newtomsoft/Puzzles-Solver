using System;
using System.Collections.Generic;
using System.Linq;
using Google.OrTools.Sat;

namespace EverySecondTurnSolver
{
    // --- Helper Classes (Ported from Domain/Board) ---

    public enum DirectionEnum
    {
        Up,
        Right,
        Down,
        Left
    }

    public struct Position : IEquatable<Position>
    {
        public int R { get; }
        public int C { get; }

        public Position(int r, int c)
        {
            R = r;
            C = c;
        }

        public Position After(DirectionEnum direction)
        {
            return direction switch
            {
                DirectionEnum.Up => new Position(R - 1, C),
                DirectionEnum.Right => new Position(R, C + 1),
                DirectionEnum.Down => new Position(R + 1, C),
                DirectionEnum.Left => new Position(R, C - 1),
                _ => throw new ArgumentOutOfRangeException(nameof(direction), direction, null)
            };
        }

        public override bool Equals(object? obj) => obj is Position position && Equals(position);
        public bool Equals(Position other) => R == other.R && C == other.C;
        public override int GetHashCode() => HashCode.Combine(R, C);
        public static bool operator ==(Position left, Position right) => left.Equals(right);
        public static bool operator !=(Position left, Position right) => !(left == right);
        public override string ToString() => $"({R}, {C})";
    }

    public static class Direction
    {
        public static DirectionEnum Up => DirectionEnum.Up;
        public static DirectionEnum Right => DirectionEnum.Right;
        public static DirectionEnum Down => DirectionEnum.Down;
        public static DirectionEnum Left => DirectionEnum.Left;

        public static IEnumerable<DirectionEnum> OrthogonalDirections()
        {
            yield return Up;
            yield return Right;
            yield return Down;
            yield return Left;
        }

        public static DirectionEnum Opposite(this DirectionEnum d)
        {
            return d switch
            {
                Up => Down,
                Right => Left,
                Down => Up,
                Left => Right,
                _ => throw new ArgumentOutOfRangeException(nameof(d), d, null)
            };
        }
    }

    public class Island
    {
        public Position Position { get; }
        public int MaxBridges { get; }
        // Mapping: Direction -> (NeighborPosition, BridgeCount)
        public Dictionary<DirectionEnum, int> Bridges { get; } = new();

        public Island(Position position, int maxBridges)
        {
            Position = position;
            MaxBridges = maxBridges;
        }
    }

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
    }

    // --- The Solver ---

    public class EverySecondTurnSolver
    {
        private readonly char[,] _inputGrid;
        private readonly int _rows;
        private readonly int _cols;
        private IslandGrid _islandGrid;
        private CpModel _model;
        // Map: Position -> Direction -> BoolVar
        private Dictionary<Position, Dictionary<DirectionEnum, BoolVar>> _islandBridges;
        private IslandGrid? _previousSolution;

        private const char CircleChar = '*';
        private const char EmptyChar = '.';

        public EverySecondTurnSolver(char[,] grid)
        {
            _inputGrid = grid;
            _rows = grid.GetLength(0);
            _cols = grid.GetLength(1);
            _islandGrid = new IslandGrid(_rows, _cols);
            _model = new CpModel();
            _islandBridges = new Dictionary<Position, Dictionary<DirectionEnum, BoolVar>>();
        }

        private void InitSolver()
        {
            _islandBridges.Clear();
            foreach (var island in _islandGrid.GetAllIslands())
            {
                var pos = island.Position;
                _islandBridges[pos] = new Dictionary<DirectionEnum, BoolVar>();
                foreach (var dir in Direction.OrthogonalDirections())
                {
                    _islandBridges[pos][dir] = _model.NewBoolVar($"{pos}_{dir}");
                }
            }
            AddConstraints();
        }

        public IslandGrid? GetSolution()
        {
            // If model is empty/fresh, init it
            if (_islandBridges.Count == 0)
            {
                InitSolver();
            }

            return EnsureAllIslandsConnected();
        }

        private IslandGrid? EnsureAllIslandsConnected()
        {
            var solver = new CpSolver();

            while (true)
            {
                var status = solver.Solve(_model);
                if (status != CpSolverStatus.Optimal && status != CpSolverStatus.Feasible)
                {
                    return null;
                }

                // Apply solution to _islandGrid to check connectivity
                foreach (var island in _islandGrid.GetAllIslands())
                {
                    island.Bridges.Clear(); // Reset
                    var pos = island.Position;
                    foreach (var dir in Direction.OrthogonalDirections())
                    {
                        var neighborPos = pos.After(dir);
                        if (!_islandGrid.IsValidPosition(neighborPos)) continue;

                        // Bridges are booleans here (0 or 1)
                        if (solver.Value(_islandBridges[pos][dir]) == 1)
                        {
                            island.Bridges[dir] = 1;
                        }
                    }
                }

                var components = _islandGrid.GetConnectedComponents();

                // If 0 components, it means empty grid solution (valid if grid is empty, but usually puzzle implies something)
                // If 1 component, we are done.
                if (components.Count <= 1)
                {
                    _previousSolution = _islandGrid; // Copy not strictly needed if we return current object, but logic matches python
                    return _islandGrid;
                }

                // Subtour elimination
                // For each component, add a constraint that at least one edge must be different
                // "not_loop_constraints" in python logic:
                // For a connected component, gather all active edges. Add constraint: OR(Not(edge)) for all edges in component.
                // This forces the solver to break this specific disconnected loop.

                foreach (var component in components)
                {
                    var activeEdges = new List<ILiteral>();
                    foreach (var pos in component)
                    {
                        var island = _islandGrid[pos];
                        foreach (var kvp in island.Bridges)
                        {
                            if (kvp.Value > 0)
                            {
                                // Add the BoolVar corresponding to this active edge
                                activeEdges.Add(_islandBridges[pos][kvp.Key]);
                            }
                        }
                    }
                    // At least one of these edges must NOT be present in the next solution
                    // to break this specific isolated component configuration.
                    // model.AddBoolOr([c.Not() ...])
                    _model.AddBoolOr(activeEdges.Select(x => x.Not()));
                }

                // Continue loop to solve again
            }
        }

        private void AddConstraints()
        {
            AddInitialConstraints();
            AddOppositeBridgesConstraints();
            AddLinksConstraints();
            AddTurnAtEveryCircleConstraints();
        }

        private void AddInitialConstraints()
        {
            foreach (var kvp in _islandBridges)
            {
                var bridges = kvp.Value.Values;
                // Sum of bridges leaving a cell == 2
                _model.Add(LinearExpr.Sum(bridges) == 2);
            }
        }

        private void AddOppositeBridgesConstraints()
        {
            foreach (var island in _islandGrid.GetAllIslands())
            {
                var pos = island.Position;
                foreach (var dir in Direction.OrthogonalDirections())
                {
                    var neighbor = pos.After(dir);
                    if (_islandGrid.IsValidPosition(neighbor))
                    {
                        // Bridge out to neighbor == Bridge in from neighbor
                        _model.Add(_islandBridges[pos][dir] == _islandBridges[neighbor][dir.Opposite()]);
                    }
                    else
                    {
                        // Boundary constraint
                        _model.Add(_islandBridges[pos][dir] == 0);
                    }
                }
            }
        }

        private void AddLinksConstraints()
        {
            for (int r = 0; r < _rows; r++)
            {
                for (int c = 0; c < _cols; c++)
                {
                    if (_inputGrid[r, c] == CircleChar)
                    {
                        var pos = new Position(r, c);
                        var linkConstraints = OneTurnBetweenLinkedCirclesConstraints(pos);
                        // Sum(linkConstraints) == 2
                        _model.Add(LinearExpr.Sum(linkConstraints) == 2);
                    }
                }
            }
        }

        private List<BoolVar> OneTurnBetweenLinkedCirclesConstraints(Position circlePos)
        {
            var constraints = new List<BoolVar>();
            var otherCircles = new List<Position>();

            for (int r = 0; r < _rows; r++)
            {
                for (int c = 0; c < _cols; c++)
                {
                    if (_inputGrid[r, c] == CircleChar && (r != circlePos.R || c != circlePos.C))
                    {
                        otherCircles.Add(new Position(r, c));
                    }
                }
            }

            foreach (var otherCirclePos in otherCircles)
            {
                var horTurnPos = new Position(circlePos.R, otherCirclePos.C);
                var vertTurnPos = new Position(otherCirclePos.R, circlePos.C);

                var horDirection = otherCirclePos.C > circlePos.C ? Direction.Right : Direction.Left;
                var vertDirection = otherCirclePos.R > circlePos.R ? Direction.Down : Direction.Up;

                // Path 1: Horizontal then Vertical (Turn at horTurnPos)
                var horPathVars = ToOtherCircleConstraint(circlePos, otherCirclePos, horTurnPos, horDirection, vertDirection);

                // Path 2: Vertical then Horizontal (Turn at vertTurnPos)
                var vertPathVars = ToOtherCircleConstraint(circlePos, otherCirclePos, vertTurnPos, vertDirection, horDirection);

                var horPathOk = NewAnd(horPathVars);
                var vertPathOk = NewAnd(vertPathVars);

                var linkOk = _model.NewBoolVar($"link_{circlePos}_to_{otherCirclePos}");

                // linkOk <=> (horPathOk OR vertPathOk)
                _model.AddBoolOr(new[] { horPathOk, vertPathOk }).OnlyEnforceIf(linkOk);
                _model.AddImplication(horPathOk, linkOk);
                _model.AddImplication(vertPathOk, linkOk);

                constraints.Add(linkOk);
            }

            return constraints;
        }

        private List<ILiteral> ToOtherCircleConstraint(Position start, Position end, Position turnPos, DirectionEnum dir1, DirectionEnum dir2)
        {
            var constraints = new List<ILiteral>();

            // First leg: start -> turnPos using dir1
            // Must have bridge in dir1
            constraints.Add(_islandBridges[start][dir1]);

            var current = start.After(dir1);

            // Traverse straight until turnPos
            // Python logic: while grid[pos] == '.' and pos != turnPos
            while (_islandGrid.IsValidPosition(current) && _inputGrid[current.R, current.C] == EmptyChar && current != turnPos)
            {
                constraints.Add(_islandBridges[current][dir1]);
                current = current.After(dir1);
            }

            // Check if we hit a blocker or went out of bounds before turnPos
            if (!_islandGrid.IsValidPosition(current) || _inputGrid[current.R, current.C] != EmptyChar)
            {
                // Logic mismatch: Python checks `if _input_grid[current_position] != _`.
                // If we stopped because it wasn't empty, but we aren't at turnPos yet, this path is invalid.
                // Or if we are at turnPos but it's not empty (it should be empty for a turn, unless turnPos is the target circle? No, turnPos is intermediate).
                // Actually the turn happens at an empty cell.

                // If we are forced to stop before turnPos (because hit a circle or boundary), fail.
                // Or if we reached turnPos, proceed.

                // Python specific check:
                // if input_grid[current] != _: fail.

                // If we successfully reached turnPos, the loop condition (current != turnPos) ensures we exit.
                // So if we exit the loop, we are either at turnPos OR input is not empty.
                if (!_islandGrid.IsValidPosition(current) || (_inputGrid[current.R, current.C] != EmptyChar && current != turnPos))
                {
                     // Return Impossible
                     var b = _model.NewBoolVar("impossible_path");
                     _model.Add(b == 0);
                     return new List<ILiteral> { b };
                }
            }

            // Now we should be at turnPos.
            // Python: constraints.append(bridges[current][dir2])
            constraints.Add(_islandBridges[current][dir2]);
            current = current.After(dir2);

            // Second leg: turnPos -> end using dir2
            while (_islandGrid.IsValidPosition(current) && _inputGrid[current.R, current.C] == EmptyChar && current != end)
            {
                constraints.Add(_islandBridges[current][dir2]);
                current = current.After(dir2);
            }

            if (!_islandGrid.IsValidPosition(current) || current != end)
            {
                 var b = _model.NewBoolVar("impossible_path_2");
                 _model.Add(b == 0);
                 return new List<ILiteral> { b };
            }

            return constraints;
        }

        private BoolVar NewAnd(List<ILiteral> literals)
        {
            var b = _model.NewBoolVar("reified_and");
            if (literals.Count == 0)
            {
                _model.Add(b == 1);
                return b;
            }

            // b => all literals
            foreach (var lit in literals)
            {
                _model.AddImplication(b, lit);
            }

            // !b => at least one !literal  (equivalent to: AND(literals) => b)
            // Logic: if all literals are true, then b must be true.
            // Python: AddBoolOr([l.Not() for l in literals] + [b])
            var clause = literals.Select(l => l.Not()).ToList();
            clause.Add(b);
            _model.AddBoolOr(clause);

            return b;
        }

        private void AddTurnAtEveryCircleConstraints()
        {
            for (int r = 0; r < _rows; r++)
            {
                for (int c = 0; c < _cols; c++)
                {
                    if (_inputGrid[r, c] == CircleChar)
                    {
                        var pos = new Position(r, c);
                        var right = _islandBridges[pos][Direction.Right];
                        var up = _islandBridges[pos][Direction.Up];
                        var left = _islandBridges[pos][Direction.Left];
                        var down = _islandBridges[pos][Direction.Down];

                        // Must be one of the 4 corners: RU, LU, LD, RD
                        _model.AddBoolOr(new[] {
                            NewAnd(new List<ILiteral>{ right, up, left.Not(), down.Not() }),
                            NewAnd(new List<ILiteral>{ right, up.Not(), left.Not(), down }),
                            NewAnd(new List<ILiteral>{ right.Not(), up.Not(), left, down }),
                            NewAnd(new List<ILiteral>{ right.Not(), up, left, down.Not() })
                        });
                    }
                }
            }
        }
    }
}
