using System;
using System.Collections.Generic;

namespace KonarupuSolverCSharp
{
    public class Position
    {
        public int R { get; set; }
        public int C { get; set; }

        public Position(int row, int column)
        {
            R = row;
            C = column;
        }

        public List<Position> Neighbors(string mode = "orthogonal")
        {
            if (mode == "orthogonal")
            {
                return new List<Position> { Up, Left, Down, Right };
            }
            if (mode == "diagonal")
            {
                return new List<Position> { Up, UpLeft, Left, DownLeft, Down, DownRight, Right, UpRight };
            }
            throw new ArgumentException($"Unknown mode {mode}");
        }

        public HashSet<Position> StraddledNeighbors()
        {
            int rFloor = (int)Math.Floor((double)R);
            int cFloor = (int)Math.Floor((double)C);
            int rCeil = (int)Math.Ceiling((double)R);
            int cCeil = (int)Math.Ceiling((double)C);
            return new HashSet<Position>
            {
                new Position(rFloor, cFloor),
                new Position(rFloor, cCeil),
                new Position(rCeil, cFloor),
                new Position(rCeil, cCeil)
            };
        }

        public Direction DirectionTo(Position other)
        {
            if (other == null || this.Equals(other))
            {
                return Direction.None;
            }
            if (R == other.R)
            {
                return C < other.C ? Direction.Right : Direction.Left;
            }
            if (C == other.C)
            {
                return R < other.R ? Direction.Down : Direction.Up;
            }
            return Direction.None;
        }

        public Direction DirectionFrom(Position other)
        {
            return other.DirectionTo(this);
        }

        public double DistanceTo(Position other)
        {
            if (R == other.R)
            {
                return Math.Abs(C - other.C);
            }
            if (C == other.C)
            {
                return Math.Abs(R - other.R);
            }
            return Math.Sqrt(Math.Pow(R - other.R, 2) + Math.Pow(C - other.C, 2));
        }

        public Position After(Direction direction, int count = 1)
        {
            if (direction == Direction.Down) return new Position(R + count, C);
            if (direction == Direction.Right) return new Position(R, C + count);
            if (direction == Direction.Up) return new Position(R - count, C);
            if (direction == Direction.Left) return new Position(R, C - count);
            return this;
        }

        public Position Before(Direction direction, int count = 1)
        {
            return After(direction.Opposite(), count);
        }

        public Position Left => new Position(R, C - 1);
        public Position Right => new Position(R, C + 1);
        public Position Up => new Position(R - 1, C);
        public Position Down => new Position(R + 1, C);
        public Position UpLeft => new Position(R - 1, C - 1);
        public Position UpRight => new Position(R - 1, C + 1);
        public Position DownLeft => new Position(R + 1, C - 1);
        public Position DownRight => new Position(R + 1, C + 1);

        public List<Position> AllPositionsBetween(Position position)
        {
            var positions = new List<Position>();
            if (R == position.R)
            {
                for (int c = Math.Min(C, position.C) + 1; c < Math.Max(C, position.C); c++)
                {
                    positions.Add(new Position(R, c));
                }
            }
            else if (C == position.C)
            {
                for (int r = Math.Min(R, position.R) + 1; r < Math.Max(R, position.R); r++)
                {
                    positions.Add(new Position(r, C));
                }
            }
            return positions;
        }

        public List<Position> AllPositionsAndBoundsBetween(Position position)
        {
            var positions = new List<Position>();
            if (R == position.R)
            {
                for (int c = Math.Min(C, position.C); c <= Math.Max(C, position.C); c++)
                {
                    positions.Add(new Position(R, c));
                }
            }
            else if (C == position.C)
            {
                for (int r = Math.Min(R, position.R); r <= Math.Max(R, position.R); r++)
                {
                    positions.Add(new Position(r, C));
                }
            }
            return positions;
        }

        public Position Symmetric(Position position, bool toInt = true)
        {
            if (toInt)
            {
                return new Position((int)(2 * position.R - this.R), (int)(2 * position.C - this.C));
            }
            return new Position(2 * position.R - this.R, 2 * position.C - this.C);
        }

        public bool IsOnRow()
        {
            return R == Math.Floor((double)R);
        }

        public bool IsOnColumn()
        {
            return C == Math.Floor((double)C);
        }

        public override bool Equals(object obj)
        {
            return obj is Position pos && R == pos.R && C == pos.C;
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(R, C);
        }

        public override string ToString()
        {
            return $"({R}, {C})";
        }

        public static Position operator +(Position a, Position b) => new Position(a.R + b.R, a.C + b.C);
        public static Position operator -(Position a, Position b) => new Position(a.R - b.R, a.C - b.C);
        public static Position operator *(Position a, int b) => new Position(a.R * b, a.C * b);
        public static Position operator /(Position a, int b) => new Position(a.R / b, a.C / b);
    }
}