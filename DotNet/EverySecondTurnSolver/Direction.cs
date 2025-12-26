namespace EverySecondTurnSolver;

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
            DirectionEnum.Up => Down,
            DirectionEnum.Right => Left,
            DirectionEnum.Down => Up,
            DirectionEnum.Left => Right,
            _ => throw new ArgumentOutOfRangeException(nameof(d), d, null)
        };
    }
}