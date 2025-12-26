namespace EverySecondTurnSolver;

public readonly struct Position : IEquatable<Position>
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