using System;
using System.Collections.Generic;

namespace MasyuSolver;

public class MasyuSolver
{
    private readonly char[,] _grid;
    private readonly int _rows;
    private readonly int _cols;

    // 0: Unknown, 1: Line, -1: No Line
    private int[,] _hEdges;
    private int[,] _vEdges;

    public MasyuSolver(char[,] grid)
    {
        _grid = grid;
        _rows = grid.GetLength(0);
        _cols = grid.GetLength(1);
        _hEdges = new int[_rows, _cols - 1];
        _vEdges = new int[_rows - 1, _cols];
    }

    public bool Solve()
    {
        if (!Propagate()) return false;

        // Find unknown edge using MRV (Minimum Remaining Values) or Degree heuristic?
        // Simple heuristic: find first unknown
        int r = -1, c = -1;
        bool isH = false;

        for (int i = 0; i < _rows; i++)
        {
            for (int j = 0; j < _cols - 1; j++)
            {
                if (_hEdges[i, j] == 0)
                {
                    r = i; c = j; isH = true;
                    goto Found;
                }
            }
        }
        for (int i = 0; i < _rows - 1; i++)
        {
            for (int j = 0; j < _cols; j++)
            {
                if (_vEdges[i, j] == 0)
                {
                    r = i; c = j; isH = false;
                    goto Found;
                }
            }
        }

        Found:
        if (r == -1)
        {
            return VerifySolution();
        }

        // Save state
        var savedH = (int[,])_hEdges.Clone();
        var savedV = (int[,])_vEdges.Clone();

        // Try 1 (Line)
        if (SetEdge(isH, r, c, 1))
        {
            if (Solve()) return true;
        }

        // Restore
        _hEdges = savedH;
        _vEdges = savedV;
        savedH = (int[,])_hEdges.Clone(); // Clone again or just copy back?
        // Actually we restored _hEdges reference to the saved one, but let's be safe:
        // When we backtrack, we must ensure we don't pollute the saved state if we reuse variables.
        // The simple assignment _hEdges = savedH works because savedH was a clone.

        // Try -1 (No Line)
        if (SetEdge(isH, r, c, -1))
        {
            if (Solve()) return true;
        }

        // Restore for caller (though irrelevant at top level)
        _hEdges = savedH;
        _vEdges = savedV;

        return false;
    }

    private bool VerifySolution()
    {
        // 1. Check all local constraints (degrees, straight/turn)
        for(int r=0; r<_rows; r++) {
            for(int c=0; c<_cols; c++) {
                int d = GetDegree(r, c);
                char type = _grid[r,c];

                // Degree checks
                if (type == 'w' || type == 'b') {
                    if (d != 2) return false;
                } else {
                    if (d != 0 && d != 2) return false;
                }

                if (d == 0) continue;

                // Edges
                int u = (r > 0) ? _vEdges[r-1, c] : -1;
                int down = (r < _rows - 1) ? _vEdges[r, c] : -1;
                int l = (c > 0) ? _hEdges[r, c-1] : -1;
                int right = (c < _cols - 1) ? _hEdges[r, c] : -1;

                // Black Circle Logic
                if (type == 'b') {
                    // Must turn: (u & d) is forbidden, (l & r) is forbidden
                    if (u == 1 && down == 1) return false;
                    if (l == 1 && right == 1) return false;
                    // Must extend legs (already mostly propagated but verify)
                    // If U, then U of U
                    if (u == 1 && (r < 2 || _vEdges[r-2, c] != 1)) return false;
                    if (down == 1 && (r > _rows - 3 || _vEdges[r+1, c] != 1)) return false;
                    if (l == 1 && (c < 2 || _hEdges[r, c-2] != 1)) return false;
                    if (right == 1 && (c > _cols - 3 || _hEdges[r, c+1] != 1)) return false;
                }

                // White Circle Logic
                if (type == 'w') {
                    // Must go straight
                    if (!((u == 1 && down == 1) || (l == 1 && right == 1))) return false;

                    // Must turn at one side
                    bool turnPrev = false;
                    bool turnNext = false;

                    if (u == 1 && down == 1) { // Vertical
                        // Top neighbor (r-1, c)
                        // It turns if it is NOT straight vertical.
                        // Straight vertical at (r-1, c) would mean v[r-2, c] == 1.
                        // So Turn means v[r-2, c] != 1.
                        // But wait, neighbor MUST exist on path.
                        // Since u=1, neighbor IS on path.
                        // So we just check if it goes straight through.
                        bool straightTop = (r >= 2 && _vEdges[r-2, c] == 1);
                        bool straightBottom = (r <= _rows - 3 && _vEdges[r+1, c] == 1);

                        if (!straightTop) turnPrev = true;
                        if (!straightBottom) turnNext = true;
                    }
                    else if (l == 1 && right == 1) { // Horizontal
                        bool straightLeft = (c >= 2 && _hEdges[r, c-2] == 1);
                        bool straightRight = (c <= _cols - 3 && _hEdges[r, c+1] == 1);

                        if (!straightLeft) turnPrev = true;
                        if (!straightRight) turnNext = true;
                    }

                    if (!turnPrev && !turnNext) return false;
                }
            }
        }

        // 2. Check Single Loop Connectivity
        // Find start
        int startR = -1, startC = -1;
        int totalNodes = 0;
        for(int r=0; r<_rows; r++) {
            for(int c=0; c<_cols; c++) {
                if (GetDegree(r,c) > 0) {
                    if (startR == -1) { startR = r; startC = c; }
                    totalNodes++;
                }
            }
        }

        if (startR == -1) return false; // Empty

        var visited = new bool[_rows, _cols];
        var q = new Queue<(int, int)>();
        q.Enqueue((startR, startC));
        visited[startR, startC] = true;
        int visitedCount = 1;

        while(q.Count > 0) {
            var (cr, cc) = q.Dequeue();

            // Neighbors
            if (cr > 0 && _vEdges[cr-1, cc] == 1 && !visited[cr-1, cc]) {
                visited[cr-1, cc] = true; visitedCount++; q.Enqueue((cr-1, cc));
            }
            if (cr < _rows - 1 && _vEdges[cr, cc] == 1 && !visited[cr+1, cc]) {
                visited[cr+1, cc] = true; visitedCount++; q.Enqueue((cr+1, cc));
            }
            if (cc > 0 && _hEdges[cr, cc-1] == 1 && !visited[cr, cc-1]) {
                visited[cr, cc-1] = true; visitedCount++; q.Enqueue((cr, cc-1));
            }
            if (cc < _cols - 1 && _hEdges[cr, cc] == 1 && !visited[cr, cc+1]) {
                visited[cr, cc+1] = true; visitedCount++; q.Enqueue((cr, cc+1));
            }
        }

        return visitedCount == totalNodes;
    }

    private int GetDegree(int r, int c)
    {
        int d = 0;
        if (r > 0 && _vEdges[r-1, c] == 1) d++;
        if (r < _rows - 1 && _vEdges[r, c] == 1) d++;
        if (c > 0 && _hEdges[r, c-1] == 1) d++;
        if (c < _cols - 1 && _hEdges[r, c] == 1) d++;
        return d;
    }

    private bool Propagate()
    {
        bool changed = true;
        while (changed)
        {
            changed = false;
            for (int r = 0; r < _rows; r++)
            {
                for (int c = 0; c < _cols; c++)
                {
                    if (!ApplyNodeConstraints(r, c, ref changed)) return false;
                }
            }
        }
        return true;
    }

    private bool ApplyNodeConstraints(int r, int c, ref bool changed)
    {
        char type = _grid[r, c];

        int u = (r > 0) ? _vEdges[r - 1, c] : -1;
        int d = (r < _rows - 1) ? _vEdges[r, c] : -1;
        int l = (c > 0) ? _hEdges[r, c - 1] : -1;
        int ri = (c < _cols - 1) ? _hEdges[r, c] : -1;

        var neighbors = new[] { u, d, l, ri };
        int lines = 0;
        int nolines = 0;
        int unknown = 0;
        foreach (var n in neighbors)
        {
            if (n == 1) lines++;
            else if (n == -1) nolines++;
            else unknown++;
        }

        // Degree Constraints
        if (lines > 2) return false;

        bool mustBe2 = (type == 'w' || type == 'b');
        if (mustBe2)
        {
            if (lines == 2 && unknown > 0)
            {
                if (!SetNeighbors(r, c, -1, ref changed)) return false;
            }
            else if (lines + unknown < 2) return false;
            else if (lines + unknown == 2 && unknown > 0)
            {
                if (!SetNeighbors(r, c, 1, ref changed)) return false;
            }
        }
        else
        {
            if (lines == 2 && unknown > 0)
            {
                 if (!SetNeighbors(r, c, -1, ref changed)) return false;
            }
            if (lines == 1 && unknown == 0) return false; // Dead end
            if (lines == 1 && unknown == 1)
            {
                if (!SetNeighbors(r, c, 1, ref changed)) return false;
            }
        }

        if (type == 'b') return ApplyBlackConstraints(r, c, u, d, l, ri, ref changed);
        if (type == 'w') return ApplyWhiteConstraints(r, c, u, d, l, ri, ref changed);

        return true;
    }

    private bool ApplyBlackConstraints(int r, int c, int u, int d, int l, int ri, ref bool changed)
    {
        // Must turn
        if (u == 1 && d == 1) return false;
        if (l == 1 && ri == 1) return false;

        // If one used, opposite blocked
        if (u == 1 && d == 0) { if (!SetV(r, c, -1)) return false; changed = true; }
        if (d == 1 && u == 0) { if (!SetV(r - 1, c, -1)) return false; changed = true; }
        if (l == 1 && ri == 0) { if (!SetH(r, c, -1)) return false; changed = true; }
        if (ri == 1 && l == 0) { if (!SetH(r, c - 1, -1)) return false; changed = true; }

        // Legs extension
        if (u == 1) { if (!SetV(r - 2, c, 1)) return false; changed = true; }
        if (d == 1) { if (!SetV(r + 1, c, 1)) return false; changed = true; }
        if (l == 1) { if (!SetH(r, c - 2, 1)) return false; changed = true; }
        if (ri == 1) { if (!SetH(r, c + 1, 1)) return false; changed = true; }

        return true;
    }

    private bool ApplyWhiteConstraints(int r, int c, int u, int d, int l, int ri, ref bool changed)
    {
        // Straight
        if (u == 1 && d == 0) { if (!SetV(r, c, 1)) return false; changed = true; }
        if (d == 1 && u == 0) { if (!SetV(r - 1, c, 1)) return false; changed = true; }
        if (u == -1 && d == 0) { if (!SetV(r, c, -1)) return false; changed = true; }
        if (d == -1 && u == 0) { if (!SetV(r - 1, c, -1)) return false; changed = true; }

        if (l == 1 && ri == 0) { if (!SetH(r, c, 1)) return false; changed = true; }
        if (ri == 1 && l == 0) { if (!SetH(r, c - 1, 1)) return false; changed = true; }
        if (l == -1 && ri == 0) { if (!SetH(r, c, -1)) return false; changed = true; }
        if (ri == -1 && l == 0) { if (!SetH(r, c - 1, -1)) return false; changed = true; }

        // Turn at neighbors check
        // If straight, check neighbors
        bool isVert = (u == 1 && d == 1);
        bool isHorz = (l == 1 && ri == 1);

        if (isVert)
        {
            // Vertical passage: neighbors at (r-1, c) and (r+1, c) must NOT both go straight vertical.
            // Straight Vertical at (r-1, c) => v[r-2, c] == 1.
            // Straight Vertical at (r+1, c) => v[r+1, c] == 1.
            // We need: (v[r-2, c] != 1) OR (v[r+1, c] != 1).
            // Logic: if v[r-2, c] == 1, then v[r+1, c] MUST be -1 (cannot be 1).

            int topLeg = (r >= 2) ? _vEdges[r-2, c] : -1; // -1 if OOB (no edge)
            int botLeg = (r <= _rows - 3) ? _vEdges[r+1, c] : -1;

            if (topLeg == 1) {
                if (botLeg == 1) return false; // Both straight!
                if (botLeg == 0) { if (!SetV(r + 1, c, -1)) return false; changed = true; }
            }
            if (botLeg == 1) {
                if (topLeg == 1) return false;
                if (topLeg == 0) { if (!SetV(r - 2, c, -1)) return false; changed = true; }
            }
        }

        if (isHorz)
        {
            // Horizontal passage: (r, c-1) and (r, c+1)
            // Left Straight: h[r, c-2] == 1
            // Right Straight: h[r, c+1] == 1
            int leftLeg = (c >= 2) ? _hEdges[r, c-2] : -1;
            int rightLeg = (c <= _cols - 3) ? _hEdges[r, c+1] : -1;

            if (leftLeg == 1) {
                if (rightLeg == 1) return false;
                if (rightLeg == 0) { if (!SetH(r, c + 1, -1)) return false; changed = true; }
            }
            if (rightLeg == 1) {
                if (leftLeg == 1) return false;
                if (leftLeg == 0) { if (!SetH(r, c - 2, -1)) return false; changed = true; }
            }
        }

        return true;
    }

    private bool SetNeighbors(int r, int c, int val, ref bool changed)
    {
        if (r > 0 && _vEdges[r-1, c] == 0) { if (!SetV(r-1, c, val)) return false; changed = true; }
        if (r < _rows - 1 && _vEdges[r, c] == 0) { if (!SetV(r, c, val)) return false; changed = true; }
        if (c > 0 && _hEdges[r, c-1] == 0) { if (!SetH(r, c-1, val)) return false; changed = true; }
        if (c < _cols - 1 && _hEdges[r, c] == 0) { if (!SetH(r, c, val)) return false; changed = true; }
        return true;
    }

    private bool SetEdge(bool isH, int r, int c, int val)
    {
        if (isH) return SetH(r, c, val);
        return SetV(r, c, val);
    }

    private bool SetH(int r, int c, int val)
    {
        if (r < 0 || r >= _rows || c < 0 || c >= _cols - 1) return val == -1;
        if (_hEdges[r, c] != 0 && _hEdges[r, c] != val) return false;
        _hEdges[r, c] = val;
        return true;
    }

    private bool SetV(int r, int c, int val)
    {
        if (r < 0 || r >= _rows - 1 || c < 0 || c >= _cols) return val == -1;
        if (_vEdges[r, c] != 0 && _vEdges[r, c] != val) return false;
        _vEdges[r, c] = val;
        return true;
    }

    public int[,] GetHEdges() => _hEdges;
    public int[,] GetVEdges() => _vEdges;
}
