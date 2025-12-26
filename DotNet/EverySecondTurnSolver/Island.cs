namespace EverySecondTurnSolver;

public class Island(Position position, int maxBridges)
{
    public Position Position { get; } = position;

    public int MaxBridges { get; } = maxBridges;

    public Dictionary<DirectionEnum, int> Bridges { get; } = new();

    public override string ToString()
    {
        Bridges.TryGetValue(DirectionEnum.Up, out var up);
        Bridges.TryGetValue(DirectionEnum.Down, out var down);
        Bridges.TryGetValue(DirectionEnum.Left, out var left);
        Bridges.TryGetValue(DirectionEnum.Right, out var right);

        if (up == 0 && down == 0 && left == 0 && right == 0) return " · ";

        var leftChar = left == 1 ? '─' : ' ';
        var rightChar = right == 1 ? '─' : ' ';

        var centerChar = (up, down, left, right) switch
        {
            (1, 1, 1, 1) => '┼',
            (0, 1, 1, 1) => '┬',
            (1, 0, 1, 1) => '┴',
            (1, 1, 0, 1) => '├',
            (1, 1, 1, 0) => '┤',
            (1, 0, 1, 0) => '┘',
            (1, 0, 0, 1) => '└',
            (0, 1, 1, 0) => '┐',
            (0, 1, 0, 1) => '┌',
            (1, 1, 0, 0) => '│',
            (0, 0, 1, 1) => '─',
            (1, 0, 0, 0) => '╵',
            (0, 1, 0, 0) => '╷',
            (0, 0, 1, 0) => '╴',
            (0, 0, 0, 1) => '╶',
            _ => 'X'
        };

        return $"{leftChar}{centerChar}{rightChar}";
    }
}