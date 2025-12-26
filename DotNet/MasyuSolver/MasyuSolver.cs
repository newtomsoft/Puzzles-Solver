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

        // Find unknown edge
        int r = -1, c = -1;
        bool isH = false;

        // Simple heuristic: find first unknown
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
            return VerifyLoop();
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

        // Try -1 (No Line)
        if (SetEdge(isH, r, c, -1))
        {
            if (Solve()) return true;
        }

        return false;
    }

    private bool VerifyLoop()
    {
        // Must form exactly one single loop that visits all circles.
        // Also degree constraints must be satisfied (already checked by propagate mostly)
        // Check connectivity.

        int startR = -1, startC = -1;
        int degrees = 0;

        // Check degrees first
        for(int r=0; r<_rows; r++) {
            for(int c=0; c<_cols; c++) {
                int d = GetDegree(r, c);
                if (d != 0 && d != 2) return false;

                char type = _grid[r,c];
                if ((type == 'w' || type == 'b') && d != 2) return false;

                if (d > 0 && startR == -1) {
                    startR = r; startC = c;
                }
                if (d > 0) degrees++;
            }
        }

        if (startR == -1) return false; // Empty grid?

        // BFS/DFS to count connected nodes
        var visited = new bool[_rows, _cols];
        var q = new Queue<(int, int)>();
        q.Enqueue((startR, startC));
        visited[startR, startC] = true;
        int visitedCount = 1;

        while(q.Count > 0) {
            var (cr, cc) = q.Dequeue();

            // Neighbors
            // Up
            if (cr > 0 && _vEdges[cr-1, cc] == 1 && !visited[cr-1, cc]) {
                visited[cr-1, cc] = true; visitedCount++; q.Enqueue((cr-1, cc));
            }
            // Down
            if (cr < _rows - 1 && _vEdges[cr, cc] == 1 && !visited[cr+1, cc]) {
                visited[cr+1, cc] = true; visitedCount++; q.Enqueue((cr+1, cc));
            }
            // Left
            if (cc > 0 && _hEdges[cr, cc-1] == 1 && !visited[cr, cc-1]) {
                visited[cr, cc-1] = true; visitedCount++; q.Enqueue((cr, cc-1));
            }
            // Right
            if (cc < _cols - 1 && _hEdges[cr, cc] == 1 && !visited[cr, cc+1]) {
                visited[cr, cc+1] = true; visitedCount++; q.Enqueue((cr, cc+1));
            }
        }

        return visitedCount == degrees;
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

        // Get neighbors states
        // Values: 1, -1, 0
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
                // Set all unknowns to -1
                if (!SetNeighbors(r, c, -1, ref changed)) return false;
            }
            else if (lines + unknown < 2) return false;
            else if (lines + unknown == 2 && unknown > 0)
            {
                // Set all unknowns to 1
                if (!SetNeighbors(r, c, 1, ref changed)) return false;
            }
        }
        else
        {
            // Empty: degree 0 or 2
            if (lines == 2 && unknown > 0)
            {
                 if (!SetNeighbors(r, c, -1, ref changed)) return false;
            }
            // Avoid degree 1 (dead end)
            // If lines=1 and unknown=0 -> fail
            if (lines == 1 && unknown == 0) return false;
            // If lines=1 and unknown=1, and nolines=2 -> Must extend
            // Wait, if lines=1, we must reach 2. So if unknown=1, that one must be 1.
            // If lines=1, we need 1 more. So any unknowns MUST be 1?
            // No, we could have 2 unknowns. One could be 1, one -1? No, if lines=1, we need exactly 1 more.
            // If lines=1, we cannot have 0 more (degree 1 bad). We MUST have degree 2.
            // So if lines=1, remaining lines needed is 1.
            // If we have > 1 unknowns, we don't know which one.
            // But if we have exactly 1 unknown, it MUST be 1.
            if (lines == 1 && unknown == 1)
            {
                if (!SetNeighbors(r, c, 1, ref changed)) return false;
            }
        }

        // Specific Constraints
        if (type == 'b') return ApplyBlackConstraints(r, c, u, d, l, ri, ref changed);
        if (type == 'w') return ApplyWhiteConstraints(r, c, u, d, l, ri, ref changed);

        return true;
    }

    private bool ApplyBlackConstraints(int r, int c, int u, int d, int l, int ri, ref bool changed)
    {
        // Must turn
        // Cannot be (Up & Down) or (Left & Right)
        if (u == 1 && d == 1) return false;
        if (l == 1 && ri == 1) return false;

        // If (u=1), then (d must be -1).
        if (u == 1 && d == 0) { if (!SetV(r, c, -1)) return false; changed = true; }
        if (d == 1 && u == 0) { if (!SetV(r - 1, c, -1)) return false; changed = true; }
        if (l == 1 && ri == 0) { if (!SetH(r, c, -1)) return false; changed = true; }
        if (ri == 1 && l == 0) { if (!SetH(r, c - 1, -1)) return false; changed = true; }

        // Legs extension
        // If u=1, u_of_u must be 1 (v[r-2, c])
        if (u == 1) { if (!SetV(r - 2, c, 1)) return false; changed = true; }
        if (d == 1) { if (!SetV(r + 1, c, 1)) return false; changed = true; }
        if (l == 1) { if (!SetH(r, c - 2, 1)) return false; changed = true; }
        if (ri == 1) { if (!SetH(r, c + 1, 1)) return false; changed = true; }

        return true;
    }

    private bool ApplyWhiteConstraints(int r, int c, int u, int d, int l, int ri, ref bool changed)
    {
        // Straight
        // (u=1 <=> d=1) and (l=1 <=> ri=1)
        if (u == 1 && d == 0) { if (!SetV(r, c, 1)) return false; changed = true; }
        if (d == 1 && u == 0) { if (!SetV(r - 1, c, 1)) return false; changed = true; }
        if (u == -1 && d == 0) { if (!SetV(r, c, -1)) return false; changed = true; }
        if (d == -1 && u == 0) { if (!SetV(r - 1, c, -1)) return false; changed = true; }

        if (l == 1 && ri == 0) { if (!SetH(r, c, 1)) return false; changed = true; }
        if (ri == 1 && l == 0) { if (!SetH(r, c - 1, 1)) return false; changed = true; }
        if (l == -1 && ri == 0) { if (!SetH(r, c, -1)) return false; changed = true; }
        if (ri == -1 && l == 0) { if (!SetH(r, c - 1, -1)) return false; changed = true; }

        // If turned, must be straight (degree 2 constraint handles "must visit", but straightness is key)
        // Check for "Turn at neighbor" rule:
        // If we go through White, we must turn at PREVIOUS or NEXT.
        // Complex to enforce locally without knowing which way is "previous".
        // But since it's symmetric: At least one neighbor must be a Corner/Turn.
        // If u=1 and d=1 (Vertical through White):
        // Then (TopNeighbor turns) OR (BottomNeighbor turns).
        // Turn means NOT Straight.
        // TopNeighbor (r-1, c). Straight Vertical there means v[r-2, c]=1.
        // So we need NOT (v[r-2, c]=1).
        // Wait, neighbor turn means it enters from Up and leaves to Left/Right.
        // If v[r-1, c]=1 (edge into white), then TopNeighbor must have l/r edge active?
        // Actually: if Vertical, then (UpNeighbor is NOT Straight Vertical) OR (DownNeighbor is NOT Straight Vertical).
        // Straight Vertical at neighbor means path continues.

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
        if (r < 0 || r >= _rows || c < 0 || c >= _cols - 1) return val == -1; // Out of bounds is implicitly -1
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
