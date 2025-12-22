import os
import sys
import time

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))  # Root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Run

from Run.tests.Base.BaseIntegrationTest import BaseIntegrationTest

TEST_CASES = [
    ("Hidoku", "https://gridgames.app/hidoku/?d=Easy")
]


class TestGridGamesIntegration(BaseIntegrationTest):
    @pytest.mark.parametrize("puzzle_name, url", TEST_CASES)
    def test_integration_headless(self, puzzle_name, url):
        self.run_integration_test(url)
