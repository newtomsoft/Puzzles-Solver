using System;
using System.Collections.Generic;
using System.Linq;

namespace KonarupuSolverCSharp
{
    public class Island
    {
        public Position Position { get; }
        public int BridgesCount { get; set; }
        public Dictionary<Direction, (Position, int)> DirectionPositionBridges { get; set; }

        public Island(Position position, int bridges, Dictionary<Position, int> positionsBridges = null)
        {
            Position = position;
            BridgesCount = bridges;
            if (bridges < 0 || bridges > 8)
            {
                throw new ArgumentException("Bridges must be between 0 and 8");
            }
            DirectionPositionBridges = new Dictionary<Direction, (Position, int)>();
            if (positionsBridges != null)
            {
                foreach (var (p, b) in positionsBridges)
                {
                    SetBridgeToPosition(p, b);
                }
            }
        }

        public void SetBridgeToPosition(Position position, int number)
        {
            var direction = Position.DirectionTo(position);
            DirectionPositionBridges[direction] = (position, number);
        }

        public void SetBridgeToDirection(Direction direction, int number)
        {
            var toPosition = Position.After(direction);
            DirectionPositionBridges[direction] = (toPosition, number);
        }

        public void SetBridgesCountAccordingToDirectionsBridges()
        {
            BridgesCount = DirectionPositionBridges.Values.Sum(v => v.Item2);
        }

        public bool HasNoBridge()
        {
            return BridgesCount == 0;
        }

        public override bool Equals(object obj)
        {
            return obj is Island island &&
                   Position.Equals(island.Position) &&
                   BridgesCount == island.BridgesCount &&
                   DirectionPositionBridges.Count == island.DirectionPositionBridges.Count &&
                   !DirectionPositionBridges.Except(island.DirectionPositionBridges).Any();
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(Position, BridgesCount, DirectionPositionBridges);
        }

        public override string ToString()
        {
            if (HasNoBridge()) return " · ";
            if (BridgesNumber(Direction.Up) != 0 && BridgesNumber(Direction.Down) != 0 && BridgesNumber(Direction.Left) != 0 && BridgesNumber(Direction.Right) != 0) return "─┼─";
            if (BridgesNumber(Direction.Up) != 0 && BridgesNumber(Direction.Left) != 0 && BridgesNumber(Direction.Right) != 0) return "─┴─";
            if (BridgesNumber(Direction.Down) != 0 && BridgesNumber(Direction.Left) != 0 && BridgesNumber(Direction.Right) != 0) return "─┬─";
            if (BridgesNumber(Direction.Up) != 0 && BridgesNumber(Direction.Down) != 0 && BridgesNumber(Direction.Left) != 0) return "─┤ ";
            if (BridgesNumber(Direction.Up) != 0 && BridgesNumber(Direction.Down) != 0 && BridgesNumber(Direction.Right) != 0) return " ├─";
            if (BridgesNumber(Direction.Up) != 0 && BridgesNumber(Direction.Left) != 0) return "─┘ ";
            if (BridgesNumber(Direction.Up) != 0 && BridgesNumber(Direction.Right) != 0) return " └─";
            if (BridgesNumber(Direction.Down) != 0 && BridgesNumber(Direction.Left) != 0) return "─┐ ";
            if (BridgesNumber(Direction.Right) != 0 && BridgesNumber(Direction.Down) != 0) return " ┌─";
            if (BridgesNumber(Direction.Up) != 0 && BridgesNumber(Direction.Down) != 0) return " │ ";
            if (BridgesNumber(Direction.Down) != 0) return " ╷ ";
            if (BridgesNumber(Direction.Up) != 0) return " ╵ ";
            if (BridgesNumber(Direction.Right) != 0 && BridgesNumber(Direction.Left) != 0) return "───";
            if (BridgesNumber(Direction.Right) != 0) return " ╶─";
            if (BridgesNumber(Direction.Left) != 0) return "─╴ ";
            return " X ";
        }

        public int BridgesNumber(Direction direction)
        {
            return DirectionPositionBridges.TryGetValue(direction, out var value) ? value.Item2 : 0;
        }
    }
}