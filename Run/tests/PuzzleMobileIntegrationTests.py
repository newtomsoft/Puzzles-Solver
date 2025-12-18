import asyncio
import os
import sys
from io import StringIO
from unittest.mock import AsyncMock, patch

import pytest

# Add paths for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))  # Root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Run

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Run.PuzzleMainConsole import PuzzleMainConsole

TEST_CASES = [
    ("akari", "https://fr.puzzle-light-up.com/", "GridPlayers.PuzzleMobiles.PuzzleAkariPlayer.asyncio.sleep"),
    ("aquarium", "https://fr.puzzle-aquarium.com/", "GridPlayers.PuzzleMobiles.PuzzleAquariumPlayer.asyncio.sleep"),
    ("battleships", "https://fr.puzzle-battleships.com/", "GridPlayers.PuzzleMobiles.PuzzleBimaruPlayer.asyncio.sleep"),
    ("binairo-plus", "https://fr.puzzle-binairo.com/binairo-plus-6x6-easy/", "GridPlayers.PuzzleMobiles.PuzzleBinairoPlayer.asyncio.sleep"),
    ("binairo", "https://fr.puzzle-binairo.com/binairo-6x6-easy/", "GridPlayers.PuzzleMobiles.PuzzleBinairoPlayer.asyncio.sleep"),
    ("dominosa", "https://fr.puzzle-dominosa.com//", "GridPlayers.PuzzleMobiles.PuzzleDominosaPlayer.asyncio.sleep"),
    ("futoshiki", "https://fr.puzzle-futoshiki.com/futoshiki-4x4-easy/", "GridPlayers.PuzzleMobiles.PuzzleFutoshikiPlayer.asyncio.sleep"),
    ("galaxies", "https://fr.puzzle-galaxies.com/", "GridPlayers.PuzzleMobiles.PuzzleGalaxiesPlayer.asyncio.sleep"),
    ("hashi", "https://fr.puzzle-bridges.com/", "GridPlayers.PuzzleMobiles.PuzzleHashiPlayer.asyncio.sleep"),
    ("heyawake", "https://fr.puzzle-heyawake.com/", "GridPlayers.PuzzleMobiles.PuzzleHeyawakePlayer.asyncio.sleep"),
    ("hitori", "https://fr.puzzle-hitori.com/", "GridPlayers.PuzzleMobiles.PuzzleHitoriPlayer.asyncio.sleep"),
    ("kakurasu", "https://fr.puzzle-kakurasu.com/", "GridPlayers.PuzzleMobiles.PuzzleKakurasuPlayer.asyncio.sleep"),
    ("kakuro", "https://fr.puzzle-kakuro.com/", "GridPlayers.PuzzleMobiles.PuzzleKakuroPlayer.asyncio.sleep"),
    ("kurodoko", "https://fr.puzzle-kurodoko.com/", "GridPlayers.PuzzleMobiles.PuzzleKurodokoPlayer.asyncio.sleep"),
    ("lits", "https://fr.puzzle-lits.com/", "GridPlayers.PuzzleMobiles.PuzzleLitsPlayer.asyncio.sleep"),
    ("masyu", "https://fr.puzzle-masyu.com/", "GridPlayers.PuzzleMobiles.PuzzleMasyuPlayer.asyncio.sleep"),
    ("minesweeper", "https://fr.puzzle-minesweeper.com/minesweeper-5x5-easy/", "GridPlayers.PuzzleMobiles.PuzzleMinesweeperPlayer.asyncio.sleep"),
    ("mosaic", "https://fr.puzzle-minesweeper.com/mosaic-5x5-easy/", "GridPlayers.PuzzleMobiles.PuzzleMinesweeperMosaicPlayer.asyncio.sleep"),
    ("nonograms", "https://fr.puzzle-nonograms.com/", "GridPlayers.PuzzleMobiles.PuzzleNonogramsPlayer.asyncio.sleep"),
    ("norinori", "https://fr.puzzle-norinori.com/", "GridPlayers.PuzzleMobiles.PuzzleNorinoriPlayer.asyncio.sleep"),
    ("nurikabe", "https://fr.puzzle-nurikabe.com/", "GridPlayers.PuzzleMobiles.PuzzleNurikabePlayer.asyncio.sleep"),
    ("pipes", "https://fr.puzzle-pipes.com/", "GridPlayers.PuzzleMobiles.PuzzlePipesPlayer.asyncio.sleep"),
    ("shakashaka", "https://fr.puzzle-shakashaka.com/", "GridPlayers.PuzzleMobiles.PuzzleShakashakaPlayer.asyncio.sleep"),
    ("shikaku", "https://fr.puzzle-shikaku.com/", "GridPlayers.PuzzleMobiles.PuzzleShikakuPlayer.asyncio.sleep"),
    ("shingoki", "https://fr.puzzle-shingoki.com/", "GridPlayers.PuzzleMobiles.PuzzleShingokiPlayer.asyncio.sleep"),
    ("skyscrapers", "https://fr.puzzle-skyscrapers.com/", "GridPlayers.PuzzleMobiles.PuzzleSkyscrapersPlayer.asyncio.sleep"),
    ("slant", "https://fr.puzzle-slant.com/", "GridPlayers.PuzzleMobiles.PuzzleSlantPlayer.asyncio.sleep"),
    ("slitherlink", "https://fr.puzzle-loop.com/", "GridPlayers.PuzzleMobiles.PuzzleSlitherlinkPlayer.asyncio.sleep"),
    ("star-battle", "https://fr.puzzle-star-battle.com/", "GridPlayers.PuzzleMobiles.PuzzleStarBattlePlayer.asyncio.sleep"),
    ("stitches", "https://fr.puzzle-stitches.com/", "GridPlayers.PuzzleMobiles.PuzzleStitchesPlayer.asyncio.sleep"),
    ("sudoku", "https://fr.puzzle-sudoku.com/", "GridPlayers.PuzzleMobiles.PuzzleSudokuPlayer.asyncio.sleep"),
    ("tapa", "https://fr.puzzle-tapa.com/", "GridPlayers.PuzzleMobiles.PuzzleTapaPlayer.asyncio.sleep"),
    ("tents", "https://fr.puzzle-tents.com/", "GridPlayers.PuzzleMobiles.PuzzleTentsPlayer.asyncio.sleep"),
    ("thermometers", "https://fr.puzzle-thermometers.com/", "GridPlayers.PuzzleMobiles.PuzzleThermometersPlayer.asyncio.sleep"),
]

@pytest.mark.parametrize("puzzle_name, url, sleep_path", TEST_CASES)
def test_integration_headless(puzzle_name, url, sleep_path):
    with patch("builtins.input", return_value=url), \
         patch("sys.stdout", new_callable=StringIO) as mock_stdout, \
         patch(sleep_path, new_callable=AsyncMock), \
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
