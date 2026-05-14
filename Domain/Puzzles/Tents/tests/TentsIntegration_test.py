import unittest
from unittest.mock import patch, AsyncMock

from Domain.Puzzles.Tents.TentsSolver import TentsSolver
from GridProviders.GridPuzzle.GridPuzzleTentsGridProvider import GridPuzzleTentsGridProvider


class TentsIntegrationTests(unittest.IsolatedAsyncioTestCase):
    @staticmethod
    def _get_html_content():
        return """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Tents Puzzle #3n04x - 5x5 Easy | GridPuzzle</title></head><body><div id="puzzle" class="pm_5"><div class="d-flex"><div style="width:30px;overflow:hidden"></div><div class="ft_txt flex-fill d-flex flex-row justify-content-around" style="height:30px;line-height:30px"><div class="flex-fill text-center" style="width:20%">2</div><div class="flex-fill text-center" style="width:20%">0</div><div class="flex-fill text-center" style="width:20%">1</div><div class="flex-fill text-center" style="width:20%">1</div><div class="flex-fill text-center" style="width:20%">2</div></div></div><div class="d-flex"><div style="width:30px;overflow:hidden" class="fl_txt d-flex flex-column justify-content-around"><div class="justify-content-around"><span>&nbsp;</span>1</div><div class="justify-content-around"><span>&nbsp;</span>1</div><div class="justify-content-around"><span>&nbsp;</span>1</div><div class="justify-content-around"><span>&nbsp;</span>1</div><div class="justify-content-around"><span>&nbsp;</span>2</div></div><div class="flex-fill"><div id="puzzle_main" class="pzm_f2_box ps5"><div class="g_cell tree" data-id="1" data-a="#" data-v="T" id="c_1"></div><div class="g_cell" data-id="2" data-a="." data-v="." id="c_2"></div><div class="g_cell tree" data-id="3" data-a="#" data-v="T" id="c_3"></div><div class="g_cell" data-id="4" data-a="*" data-v="." id="c_4"></div><div class="g_cell" data-id="5" data-a="." data-v="." id="c_5"></div><div class="g_cell" data-id="6" data-a="*" data-v="." id="c_6"></div><div class="g_cell" data-id="7" data-a="." data-v="." id="c_7"></div><div class="g_cell" data-id="8" data-a="." data-v="." id="c_8"></div><div class="g_cell" data-id="9" data-a="." data-v="." id="c_9"></div><div class="g_cell" data-id="10" data-a="." data-v="." id="c_10"></div><div class="g_cell" data-id="11" data-a="." data-v="." id="c_11"></div><div class="g_cell" data-id="12" data-a="." data-v="." id="c_12"></div><div class="g_cell" data-id="13" data-a="." data-v="." id="c_13"></div><div class="g_cell" data-id="14" data-a="." data-v="." id="c_14"></div><div class="g_cell" data-id="15" data-a="*" data-v="." id="c_15"></div><div class="g_cell tree" data-id="16" data-a="#" data-v="T" id="c_16"></div><div class="g_cell tree" data-id="17" data-a="#" data-v="T" id="c_17"></div><div class="g_cell" data-id="18" data-a="*" data-v="." id="c_18"></div><div class="g_cell" data-id="19" data-a="." data-v="." id="c_19"></div><div class="g_cell tree" data-id="20" data-a="#" data-v="T" id="c_20"></div><div class="g_cell" data-id="21" data-a="*" data-v="." id="c_21"></div><div class="g_cell" data-id="22" data-a="." data-v="." id="c_22"></div><div class="g_cell" data-id="23" data-a="." data-v="." id="c_23"></div><div class="g_cell tree" data-id="24" data-a="#" data-v="T" id="c_24"></div><div class="g_cell" data-id="25" data-a="*" data-v="." id="c_25"></div></div></div></div></div></body></html>"""

    async def test_provider_direct_scrap(self):
        provider = GridPuzzleTentsGridProvider()

        with patch.object(GridPuzzleTentsGridProvider, 'get_html', new_callable=AsyncMock) as mock_get_html, \
             patch('GridProviders.PlaywrightGridProvider.PlaywrightGridProvider.screen_size', return_value=(1920, 1080)):
            mock_get_html.return_value = self._get_html_content()
            grid, tents_numbers = await provider.scrap_grid(None, 'https://gridpuzzle.com/tents/3n04x')

        self.assertEqual(grid.rows_number, 5)
        self.assertEqual(grid.columns_number, 5)
        self.assertEqual(tents_numbers['column'], [2, 0, 1, 1, 2])
        self.assertEqual(tents_numbers['row'], [1, 1, 1, 1, 2])

        solver = TentsSolver(grid, tents_numbers)
        solution = solver.get_solution()

        self.assertFalse(solution.is_empty())

    async def test_provider_solver_full_pipeline(self):
        provider = GridPuzzleTentsGridProvider()

        with patch.object(GridPuzzleTentsGridProvider, 'get_html', new_callable=AsyncMock) as mock_get_html, \
             patch('GridProviders.PlaywrightGridProvider.PlaywrightGridProvider.screen_size', return_value=(1920, 1080)):
            mock_get_html.return_value = self._get_html_content()
            grid, tents_numbers = await provider.scrap_grid(None, 'https://gridpuzzle.com/tents/3n04x')

        solver = TentsSolver(grid, tents_numbers)
        solution = solver.get_solution()

        for position, value in solution:
            if value:
                for neighbor in solution.neighbors_positions(position, 'diagonal'):
                    self.assertFalse(solution[neighbor], f"Tents adjacent at {position} and {neighbor}")

        for row_index in range(5):
            tents = sum(1 for c in range(5) if solution[row_index, c] and grid[row_index, c] != TentsSolver.tree_value)
            self.assertEqual(tents, tents_numbers['row'][row_index], f"Row {row_index} tent count mismatch")

        for col_index in range(5):
            tents = sum(1 for r in range(5) if solution[r, col_index] and grid[r, col_index] != TentsSolver.tree_value)
            self.assertEqual(tents, tents_numbers['column'][col_index], f"Column {col_index} tent count mismatch")

        for position, value in grid:
            if value == TentsSolver.tree_value:
                adjacent_tents = sum(1 for n in grid.neighbors_positions(position) if solution[n])
                self.assertGreaterEqual(adjacent_tents, 1, f"Tree at {position} has no adjacent tent")


if __name__ == '__main__':
    unittest.main()
