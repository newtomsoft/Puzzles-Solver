import os
import sys
from unittest.mock import AsyncMock, patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))  # Root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Run

from Run.tests.Base.BaseIntegrationTest import BaseIntegrationTest

TEST_CASES = [
    ("akari", "https://vuqq.com/akari/"),
    ("hitori", "https://vuqq.com/hitori/"),
    ("netwalk", "https://vuqq.com/netwalk/"),
    ("skyscrapers", "https://vuqq.com/skyscrapers/"),
    ("sudoku", "https://vuqq.com/sudoku/"),
    ("tents", "https://vuqq.com/tents-and-trees/"),
]


class TestVuqqIntegration(BaseIntegrationTest):
    @pytest.mark.parametrize("puzzle_name, url", TEST_CASES)
    def test_integration_headless(self, puzzle_name, url):
        patches = [
            patch("asyncio.sleep", new_callable=AsyncMock)
        ]
        self.run_integration_test(url, patches=patches)
