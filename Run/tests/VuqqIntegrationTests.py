import asyncio
import os
import sys
import time
from io import StringIO
from unittest.mock import AsyncMock, patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))  # Root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Run

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Run.PuzzleMainConsole import PuzzleMainConsole

TEST_CASES = [
    # ("skyscrapers", "https://vuqq.com/skyscrapers/"),
    # ("akari", "https://vuqq.com/akari/"),
    # ("netwalk", "https://vuqq.com/netwalk/"),
    # ("sudoku", "https://vuqq.com/sudoku/"),
    # ("hitori", "https://vuqq.com/hitori/"),
    ("tents", "https://vuqq.com/tents-and-trees/"),
]


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    time.sleep(2)


@pytest.mark.parametrize("puzzle_name, url", TEST_CASES)
def test_integration_headless(puzzle_name, url):
    with patch("builtins.input", return_value=url), \
         patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
         patch("asyncio.sleep", new_callable=AsyncMock), \
         patch.object(PlaywrightGridProvider, "_read_config", autospec=True) as mock_config:

        def side_effect_read_config(self_provider):
            self_provider.headless = True
            self_provider.record_video = False

        mock_config.side_effect = side_effect_read_config

        try:
            asyncio.run(PuzzleMainConsole.main())
        except Exception:
            import traceback
            traceback.print_exc()
            raise

        output = mock_stdout.getvalue()

        assert "Puzzle Solver" in output
        assert "Enter game url" in output
        assert "getting grid..." in output
        assert "Solving..." in output
        assert "Solution found in" in output
        assert "Game played successfully" in output
        assert "Browser context closed" in output
        assert "Playwright stopped" in output
