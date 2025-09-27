using System;
using System.Collections.Generic;
using System.Linq;

namespace KonarupuSolverCSharp
{
    public sealed class Direction
    {
        private static readonly Dictionary<int, Direction> Instance = new Dictionary<int, Direction>();

        public static readonly Direction None = new Direction(0);
        public static readonly Direction Down = new Direction(1);
        public static readonly Direction Right = new Direction(2);
        public static readonly Direction Up = new Direction(3);
        public static readonly Direction Left = new Direction(4);

        private readonly int _value;

        private Direction(int value)
        {
            _value = value;
            Instance[value] = this;
        }

        public static IEnumerable<Direction> Orthogonals()
        {
            return new[] { Up, Left, Down, Right };
        }

        public Direction Opposite()
        {
            if (this == Down) return Up;
            if (this == Up) return Down;
            if (this == Right) return Left;
            if (this == Left) return Right;
            return None;
        }

        public override string ToString()
        {
            if (_value == Down._value) return "⊓";
            if (_value == Right._value) return "⊏";
            if (_value == Up._value) return "⊔";
            if (_value == Left._value) return "⊐";
            return "x";
        }
    }
}