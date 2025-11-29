from Domain.Board.Grid import Grid
from Domain.Puzzles.Arofuro.ArofuroSolver import ArofuroSolver
from GridPlayers.PlaywrightPlayer import PlaywrightPlayer


class GridPuzzleArofuroPlayer(PlaywrightPlayer):
    game_name = "arofuro"

    def play(self, solution: Grid):
        page = self.browser.pages[0]
        video, rectangle = self._get_data_video_viewport(page)

        cells = page.query_selector_all("div.g_cell")
        
        arrow_map = {
            ArofuroSolver.up: 'arrow-up',
            ArofuroSolver.down: 'arrow-down',
            ArofuroSolver.left: 'arrow-left',
            ArofuroSolver.right: 'arrow-right',
        }

        for position, solution_value in [(position, solution_value) for position, solution_value in solution if solution_value in arrow_map]:
            index = position.r * solution.columns_number + position.c
            cells[index].click()
            arrow_src_part = arrow_map[solution_value]
            arrow_selector = f"img.ipt_btn[src*='{arrow_src_part}']"
            page.wait_for_selector(arrow_selector, state="visible", timeout=2000)
            page.click(arrow_selector)

        self.close()
        self._process_video(video, rectangle, 0)
