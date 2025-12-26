using Google.OrTools.Sat;

namespace EverySecondTurnSolver;

public class EverySecondTurnSolver
{
    private readonly char[,] _inputGrid;
    private readonly int _rows;
    private readonly int _cols;
    private readonly IslandGrid _islandGrid;
    private readonly CpModel _model;
    private readonly Dictionary<Position, Dictionary<DirectionEnum, BoolVar>> _islandBridges;
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
        if (_islandBridges.Count == 0) InitSolver();

        return EnsureAllIslandsConnected();
    }

    private IslandGrid? EnsureAllIslandsConnected()
    {
        var solver = new CpSolver();

        while (true)
        {
            var status = solver.Solve(_model);
            if (status != CpSolverStatus.Optimal && status != CpSolverStatus.Feasible)
                return null;

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

            if (components.Count <= 1)
            {
                _previousSolution = _islandGrid;
                return _islandGrid;
            }

            foreach (var component in components)
            {
                var activeEdges = new List<ILiteral>();
                foreach (var pos in component)
                {
                    var island = _islandGrid[pos];
                    foreach (var kvp in island.Bridges)
                    {
                        if (kvp.Value > 0) activeEdges.Add(_islandBridges[pos][kvp.Key]);
                    }
                }
                _model.AddBoolOr(activeEdges.Select(x => x.Not()));
            }
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
                    _model.Add(_islandBridges[pos][dir] == _islandBridges[neighbor][dir.Opposite()]);
                else
                    _model.Add(_islandBridges[pos][dir] == 0);
            }
        }
    }

    private void AddLinksConstraints()
    {
        for (var r = 0; r < _rows; r++)
        {
            for (var c = 0; c < _cols; c++)
            {
                if (_inputGrid[r, c] != CircleChar) continue;
                var pos = new Position(r, c);
                var linkConstraints = OneTurnBetweenLinkedCirclesConstraints(pos);
                _model.Add(LinearExpr.Sum(linkConstraints) == 2);
            }
        }
    }

    private List<BoolVar> OneTurnBetweenLinkedCirclesConstraints(Position circlePos)
    {
        var constraints = new List<BoolVar>();
        var otherCircles = new List<Position>();

        for (var r = 0; r < _rows; r++)
        {
            for (var c = 0; c < _cols; c++)
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

            var horPathVars = ToOtherCircleConstraint(circlePos, otherCirclePos, horTurnPos, horDirection, vertDirection);
            var vertPathVars = ToOtherCircleConstraint(circlePos, otherCirclePos, vertTurnPos, vertDirection, horDirection);

            var horPathOk = NewAnd(horPathVars);
            var vertPathOk = NewAnd(vertPathVars);

            var linkOk = _model.NewBoolVar($"link_{circlePos}_to_{otherCirclePos}");

            _model.AddBoolOr([horPathOk, vertPathOk]).OnlyEnforceIf(linkOk);
            _model.AddImplication(horPathOk, linkOk);
            _model.AddImplication(vertPathOk, linkOk);

            constraints.Add(linkOk);
        }

        return constraints;
    }

    private List<ILiteral> ToOtherCircleConstraint(Position start, Position end, Position turnPos, DirectionEnum dir1, DirectionEnum dir2)
    {
        var constraints = new List<ILiteral>();

        constraints.Add(_islandBridges[start][dir1]);
        var current = start.After(dir1);
        while (_islandGrid.IsValidPosition(current) && _inputGrid[current.R, current.C] == EmptyChar && current != turnPos)
        {
            constraints.Add(_islandBridges[current][dir1]);
            current = current.After(dir1);
        }

        // Check if we hit a blocker or went out of bounds before turnPos
        if (!_islandGrid.IsValidPosition(current) || _inputGrid[current.R, current.C] != EmptyChar)
        {
            if (!_islandGrid.IsValidPosition(current) || (_inputGrid[current.R, current.C] != EmptyChar && current != turnPos))
            {
                // Return Impossible
                var b = _model.NewBoolVar("impossible_path");
                _model.Add(b == 0);
                return [b];
            }
        }

        constraints.Add(_islandBridges[current][dir2]);
        current = current.After(dir2);

        while (_islandGrid.IsValidPosition(current) && _inputGrid[current.R, current.C] == EmptyChar && current != end)
        {
            constraints.Add(_islandBridges[current][dir2]);
            current = current.After(dir2);
        }

        if (_islandGrid.IsValidPosition(current) && current == end) return constraints;
        {
            var b = _model.NewBoolVar("impossible_path_2");
            _model.Add(b == 0);
            return [b];
        }

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

        var clause = literals.Select(l => l.Not()).ToList();
        clause.Add(b);
        _model.AddBoolOr(clause);

        return b;
    }

    private void AddTurnAtEveryCircleConstraints()
    {
        for (var r = 0; r < _rows; r++)
        {
            for (var c = 0; c < _cols; c++)
            {
                if (_inputGrid[r, c] != CircleChar) continue;

                var pos = new Position(r, c);
                var right = _islandBridges[pos][Direction.Right];
                var up = _islandBridges[pos][Direction.Up];
                var left = _islandBridges[pos][Direction.Left];
                var down = _islandBridges[pos][Direction.Down];

                _model.AddBoolOr([
                    NewAnd([right, up, left.Not(), down.Not()]),
                    NewAnd([right, up.Not(), left.Not(), down]),
                    NewAnd([right.Not(), up.Not(), left, down]),
                    NewAnd([right.Not(), up, left, down.Not()])
                ]);
            }
        }
    }
}