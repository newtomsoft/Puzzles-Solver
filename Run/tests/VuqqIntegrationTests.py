import os
import sys
import time
from unittest.mock import AsyncMock, patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))  # Root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Run

from Run.tests.Base.BaseIntegrationTest import BaseIntegrationTest

TEST_CASES = [
    # ("skyscrapers", "https://vuqq.com/skyscrapers/"),
    # ("akari", "https://vuqq.com/akari/"),
    # ("netwalk", "https://vuqq.com/netwalk/"),
    # ("sudoku", "https://vuqq.com/sudoku/"),
    # ("hitori", "https://vuqq.com/hitori/"),
    ("tents", "https://vuqq.com/tents-and-trees/"),
]


class TestVuqqIntegration(BaseIntegrationTest):
    @pytest.mark.parametrize("puzzle_name, url", TEST_CASES)
    def test_integration_headless(self, puzzle_name, url):
        patches = [
            patch("asyncio.sleep", new_callable=AsyncMock)
        ]
        self.run_integration_test(url, patches=patches)
