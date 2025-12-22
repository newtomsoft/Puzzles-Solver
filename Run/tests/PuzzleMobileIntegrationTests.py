import asyncio
import os
import sys
import time
from io import StringIO
from unittest.mock import AsyncMock, patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))  # Root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Run

from GridPlayers.PuzzleMobiles.Base.PuzzlesMobilePlayer import PuzzlesMobilePlayer
from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Run.PuzzleMainConsole import PuzzleMainConsole

TEST_CASES = [
    ("akari", "https://fr.puzzle-light-up.com/"),
    ("aquarium", "https://fr.puzzle-aquarium.com/"),
    ("battleships", "https://fr.puzzle-battleships.com/"),
    ("binairo-plus", "https://fr.puzzle-binairo.com/binairo-plus-6x6-easy/"),
    ("binairo", "https://fr.puzzle-binairo.com/binairo-6x6-easy/"),
    ("dominosa", "https://fr.puzzle-dominosa.com//"),
    ("futoshiki", "https://fr.puzzle-futoshiki.com/futoshiki-4x4-easy/"),
    ("galaxies", "https://fr.puzzle-galaxies.com/"),
    ("hashi", "https://fr.puzzle-bridges.com/"),
    ("heyawake", "https://fr.puzzle-heyawake.com/"),
    ("hitori", "https://fr.puzzle-hitori.com/"),
    ("kakurasu", "https://fr.puzzle-kakurasu.com/"),
    ("kakuro", "https://fr.puzzle-kakuro.com/"),
    ("kurodoko", "https://fr.puzzle-kurodoko.com/"),
    ("lits", "https://fr.puzzle-lits.com/"),
    ("masyu", "https://fr.puzzle-masyu.com/"),
    ("minesweeper", "https://fr.puzzle-minesweeper.com/minesweeper-5x5-easy/"),
    ("minesweeper mosaic", "https://fr.puzzle-minesweeper.com/mosaic-5x5-easy/"),
    ("nonograms", "https://fr.puzzle-nonograms.com/"),
    ("norinori", "https://fr.puzzle-norinori.com/"),
    ("nurikabe", "https://fr.puzzle-nurikabe.com/"),
    ("pipes", "https://fr.puzzle-pipes.com/"),
    ("shakashaka", "https://fr.puzzle-shakashaka.com/"),
    ("shikaku", "https://fr.puzzle-shikaku.com/"),
    ("shingoki", "https://fr.puzzle-shingoki.com/"),
    ("skyscrapers", "https://fr.puzzle-skyscrapers.com/"),
    ("slant", "https://fr.puzzle-slant.com/"),
    ("slitherlink", "https://fr.puzzle-loop.com/"),
    ("star-battle", "https://fr.puzzle-star-battle.com/"),
    ("stitches", "https://fr.puzzle-stitches.com/"),
    ("sudoku", "https://fr.puzzle-sudoku.com/"),
    ("tapa", "https://fr.puzzle-tapa.com/"),
    ("tents", "https://fr.puzzle-tents.com/"),
    ("thermometers", "https://fr.puzzle-thermometers.com/"),
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
         patch.object(PuzzlesMobilePlayer, "submit_score", new_callable=AsyncMock), \
         patch.object(PlaywrightGridProvider, "_read_config", autospec=True) as mock_config:

        def side_effect_read_config(self_provider):
            self_provider.headless = os.getenv("CI", "false").lower() == "true"
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
