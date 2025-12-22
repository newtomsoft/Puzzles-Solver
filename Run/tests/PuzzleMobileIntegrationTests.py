import os
import sys
from unittest.mock import AsyncMock, patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))  # Root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Run

from Run.tests.Base.BaseIntegrationTest import BaseIntegrationTest

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

class TestPuzzleMobileIntegration(BaseIntegrationTest):
    @pytest.mark.parametrize("puzzle_name, url", TEST_CASES)
    def test_integration_headless(self, puzzle_name, url):
        patches = [
            patch("asyncio.sleep", new_callable=AsyncMock),
            patch("GridPlayers.Base.PlaywrightPlayer.PlaywrightPlayer._process_video")
        ]
        self.run_integration_test(url, patches=patches)
