namespace EverySecondTurnSolver;

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