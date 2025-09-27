using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace KonarupuSolverCSharp
{
    public class Grid<T> : IEnumerable<KeyValuePair<Position, T>>
    {
        protected List<List<T>> _matrix;

        public Grid(List<List<T>> matrix)
        {
            _matrix = matrix;
        }

        public int RowsNumber => _matrix.Any() && _matrix[0].Any() ? _matrix.Count : 0;
        public int ColumnsNumber => _matrix.Any() && _matrix[0].Any() ? _matrix[0].Count : 0;

        public bool Contains(Position position)
        {
            return 0 <= position.R && position.R < RowsNumber && 0 <= position.C && position.C < ColumnsNumber;
        }

        public List<Position> NeighborsPositions(Position position, string mode = "orthogonal")
        {
            return position.Neighbors(mode).Where(Contains).ToList();
        }

        public T this[Position key]
        {
            get => _matrix[key.R][key.C];
            set => _matrix[key.R][key.C] = value;
        }

        public T this[int r, int c]
        {
            get => _matrix[r][c];
            set => _matrix[r][c] = value;
        }

        public static Grid<T> Empty()
        {
            return new Grid<T>(new List<List<T>>());
        }

        public bool IsEmpty()
        {
            return RowsNumber == 0;
        }

        public List<Position> EdgeUpPositions()
        {
            return Enumerable.Range(0, ColumnsNumber).Select(c => new Position(0, c)).ToList();
        }

        public List<Position> EdgeDownPositions()
        {
            return Enumerable.Range(0, ColumnsNumber).Select(c => new Position(RowsNumber - 1, c)).ToList();
        }

        public List<Position> EdgeLeftPositions()
        {
            return Enumerable.Range(0, RowsNumber).Select(r => new Position(r, 0)).ToList();
        }

        public List<Position> EdgeRightPositions()
        {
            return Enumerable.Range(0, RowsNumber).Select(r => new Position(r, ColumnsNumber - 1)).ToList();
        }

        private void DepthFirstSearch(Position position, T value, HashSet<Position> visited)
        {
            if (!Contains(position) || !EqualityComparer<T>.Default.Equals(this[position], value) || visited.Contains(position))
            {
                return;
            }
            visited.Add(position);

            foreach (var neighborPosition in NeighborsPositions(position, "orthogonal"))
            {
                DepthFirstSearch(neighborPosition, value, visited);
            }
        }

        public List<HashSet<Position>> GetConnectedPositions(T valueToSearch)
        {
            var connectedComponents = new List<HashSet<Position>>();
            var visited = new HashSet<Position>();

            foreach (var kvp in this)
            {
                if (EqualityComparer<T>.Default.Equals(kvp.Value, valueToSearch) && !visited.Contains(kvp.Key))
                {
                    var component = new HashSet<Position>();
                    DepthFirstSearch(kvp.Key, valueToSearch, component);
                    connectedComponents.Add(component);
                    visited.UnionWith(component);
                }
            }
            return connectedComponents;
        }

        public IEnumerator<KeyValuePair<Position, T>> GetEnumerator()
        {
            for (int r = 0; r < RowsNumber; r++)
            {
                for (int c = 0; c < ColumnsNumber; c++)
                {
                    yield return new KeyValuePair<Position, T>(new Position(r, c), _matrix[r][c]);
                }
            }
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }

        public override string ToString()
        {
            if (IsEmpty())
            {
                return "Grid.empty()";
            }

            var sb = new StringBuilder();
            for (int r = 0; r < RowsNumber; r++)
            {
                for (int c = 0; c < ColumnsNumber; c++)
                {
                    sb.Append(this[r, c]);
                }
                if (r < RowsNumber - 1)
                    sb.AppendLine();
            }
            return sb.ToString();
        }
    }
}