import asyncio
import os
import sys
import time
from io import StringIO
from unittest.mock import AsyncMock, patch

import pytest

from GridProviders.PlaywrightGridProvider import PlaywrightGridProvider
from Run.PuzzleMainConsole import PuzzleMainConsole

class BaseIntegrationTest:
    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        yield
        time.sleep(2)

    def run_integration_test(self, url, patches=None):
        if patches is None:
            patches = []

        with patch("builtins.input", return_value=url), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            
            with self._apply_patches(patches):
                try:
                    asyncio.run(PuzzleMainConsole.main())
                except Exception:
                    import traceback
                    traceback.print_exc()
                    raise

            output = mock_stdout.getvalue()
            self.assert_common_output(output)
            return output

    @staticmethod
    def _apply_patches(patches):
        if not patches:
            from contextlib import nullcontext
            return nullcontext()
        
        from contextlib import ExitStack
        stack = ExitStack()
        for p in patches:
            stack.enter_context(p)
        return stack

    @staticmethod
    def assert_common_output(output):
        assert "Puzzle Solver" in output
        assert "Enter game url" in output
        assert "getting grid..." in output
        assert "Solving..." in output
        assert "Solution found in" in output
        assert "Game played successfully" in output
        assert "Browser context closed" in output
        assert "Playwright stopped" in output
