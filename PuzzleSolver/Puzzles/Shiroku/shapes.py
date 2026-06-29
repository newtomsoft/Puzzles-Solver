import json
from pathlib import Path

_SHAPES_FILE = Path(__file__).with_name("shapes.json")

with open(_SHAPES_FILE, encoding="utf-8") as f:
    _data: dict = json.load(f)

REGION_SIZE: list[int] = [int(s) for s in _data["REGION_SIZE"]]
ALL_SHAPES: list[list[tuple[int, int]]] = [[(int(cell[0]), int(cell[1])) for cell in shape] for shape in _data["ALL_SHAPES"]]
