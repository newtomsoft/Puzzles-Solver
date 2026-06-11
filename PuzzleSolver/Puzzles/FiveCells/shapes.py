"""Shape data for FiveCells (5-cell regions / free pentominoes).

This module provides the canonical list of shapes used for both solving
and generation. The JSON file is the portable source of truth; this module
loads it so Python code gets properly typed tuples.

Consumers that only need the shapes (e.g. ambiguity finders, generators,
analysis scripts) should import from here instead of pulling in the full solver:

    from PuzzleSolver.Puzzles.FiveCells.shapes import REGION_SIZE, ALL_SHAPES
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_SHAPES_FILE = Path(__file__).with_name("shapes.json")

with open(_SHAPES_FILE, encoding="utf-8") as f:
    _data: dict[str, Any] = json.load(f)

REGION_SIZE: int = _data["REGION_SIZE"]
ALL_SHAPES: list[list[tuple[int, int]]] = [
    [tuple(cell) for cell in shape] for shape in _data["ALL_SHAPES"]
]
